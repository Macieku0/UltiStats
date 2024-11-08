import { writable } from 'svelte/store';

const getInitialTheme = () => {
    if (typeof window !== 'undefined') {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        // Check system preference
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
            return 'dark';
        }
    }
    return 'light';
};

export const theme = writable(getInitialTheme());

// Apply theme changes when the store updates
theme.subscribe(value => {
    if (typeof window !== 'undefined') {
        localStorage.setItem('theme', value);
        if (value === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }
});