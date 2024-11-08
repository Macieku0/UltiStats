/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{svelte,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'ultimate-blue': '#1e40af',
        'ultimate-green': '#15803d',
        'ultimate-red': '#dc2626',
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [],
}
