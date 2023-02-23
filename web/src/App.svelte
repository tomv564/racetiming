<script>
  import Starter from './lib/Starter.svelte'
  import Log from './lib/Log.svelte'
  import { events, raceStarted } from './lib/stores.js'

  const handleStart = () => {
    fetch('/start')
    // todo: await andcheck result.
    raceStarted.set(true);
  }

  const handleReset = () => {
    fetch('/reset')
    raceStarted.set(false);
  }

  const socket = new WebSocket('ws://' + location.host + '/updates');
  socket.addEventListener('message', ev => {
    let msg = JSON.parse(ev.data);

    $events.push(msg);
    events.set($events)

    // log(msg.type, 'blue');
  });
</script>

<main>
  <h1>Race Timing</h1>

  <Starter on:start={handleStart} on:reset={handleReset} raceStarted={$raceStarted}/>
  <Log />

</main>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: 100;
    line-height: 1.1;
    margin: 2rem auto;
    max-width: 14rem;
  }

  p {
    max-width: 14rem;
    margin: 1rem auto;
    line-height: 1.35;
  }

  @media (min-width: 480px) {
    h1 {
      max-width: none;
    }

    p {
      max-width: none;
    }
  }
</style>
