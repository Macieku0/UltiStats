import { writable } from 'svelte/store';

function createGameStore() {
    const { subscribe, set, update } = writable({
        currentGame: null,
        currentPoint: null,
        teams: [],
        players: [],
        points: [],
        actions: []
    });

    return {
        subscribe,
        setCurrentGame: (game) => update(state => ({ ...state, currentGame: game })),
        setCurrentPoint: (point) => update(state => ({ ...state, currentPoint: point })),
        addTeam: (team) => update(state => ({ ...state, teams: [...state.teams, team] })),
        addPlayer: (player) => update(state => ({ ...state, players: [...state.players, player] })),
        addPoint: (point) => update(state => ({ ...state, points: [...state.points, point] })),
        addAction: (action) => update(state => ({ ...state, actions: [...state.actions, action] })),
        reset: () => set({
            currentGame: null,
            currentPoint: null,
            teams: [],
            players: [],
            points: [],
            actions: []
        })
    };
}

export const gameStore = createGameStore();