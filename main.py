from gpiozero import Button, LineSensor
import time
from flask import Flask, render_template
from flask_sock import Sock
import json

app = Flask(__name__, static_url_path='/static', static_folder='web/dist')
sock = Sock(app)

messages = []


def make_message(label, state):
	return {
		'type': label,
		'state': state
	}

@app.route("/")
def hello_world():
	return render_template("index.html")

@app.route("/start")
def start():
	if start_race():
		return "success"
	else:
		return "failed"

@app.route("/reset")
def reset():
	# pass
	stop_race()
	return "success"
	#todo

@sock.route('/updates')
def updates(ws):
	while True:
		if messages:
			message = messages.pop()
			if message is not None:
				ws.send(json.dumps(message))


#from gpiozero.pins.mock import MockFactory

#Device.pin_factory = MockFactory()
# GPIOZERO_PIN_FACTORY=mock python3 main.py

# single race

race_started = False
race_finished = False
start_time = 0
laps_remaining = 3
last_lap_time = 0

def lap_completed():
	global laps_remaining, last_lap_time
	laps_remaining -= 1
	current_time = time.time()
	lap_time = current_time - last_lap_time
	print("lap time: {}".format(lap_time))
	# messages.append("lap time: {}".format(lap_time))
	messages.append(make_message('LapCompleted', {}))
	if laps_remaining == 0:
		stop_race()
	else:
		last_lap_time = current_time
		print("laps remaining: {}".format(laps_remaining))
		# messages.append("laps remaining: {}".format(laps_remaining))


def stop_race():
	global race_started, race_finished, start_time, laps_remaining
	race_finished = True
	race_started = False
	laps_remaining = 3
	end_time = time.time()
	time_elapsed = end_time - start_time
	print("race finished: {}".format(time_elapsed))
	messages.append(make_message('RaceFinished', {}))


def beam_broken():
	global race_started
	print("beam broken")
	if race_started:
		lap_completed()

def beam_restored():
	print("beam restored")


def start_race():
	global race_started, race_finished, start_time, last_lap_time, messages
	if not race_started:
		start_time = time.time()
		last_lap_time = start_time
		race_started = True
		race_finished = False
		messages.append(make_message('RaceStarted', {}))
		print("race started")
		return True
	else:
		print("race already in progress")
		return False

print("setting up beam and trigger...")

sensor = LineSensor(5, pull_up=True)
sensor.when_line = beam_restored
sensor.when_no_line = beam_broken

button = Button(16)
button.when_pressed = start_race

print("ready.")

# pause()