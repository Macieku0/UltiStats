import { writable } from 'svelte/store';

function createPlayerStore() {
    const { subscribe, set, update } = writable({
        roster: [],
        activePoint: []
    });

    return {
        subscribe,
        addToRoster: (player) => update(state => ({
            ...state,
            roster: [...state.roster, player]
        })),
        setActivePoint: (players) => update(state => ({
            ...state,
            activePoint: players
        })),
        removeFromRoster: (playerId) => update(state => ({
            ...state,
            roster: state.roster.filter(p => p.id !== playerId)
        }))
    };
}

export const playerStore = createPlayerStore();