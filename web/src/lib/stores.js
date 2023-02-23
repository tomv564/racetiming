import { writable } from 'svelte/store'

export const events = writable([]);

export const raceStarted = writable(false);