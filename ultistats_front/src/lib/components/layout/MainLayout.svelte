<script>
    import { Link } from "svelte-routing";
    import { onMount } from "svelte";
    import { theme } from "../../stores/theme";
    import ThemeToggle from "../../components/ThemeToggle.svelte";
    import "../../../app.css";
    let mobileMenuOpen = false;

    function toggleMobileMenu() {
        mobileMenuOpen = !mobileMenuOpen;
        const mobileMenu = document.querySelector(".mobile-menu");
        mobileMenu.classList.toggle("hidden");
    }

    function navigate() {
        mobileMenuOpen = false;
        const mobileMenu = document.querySelector(".mobile-menu");
        mobileMenu.classList.add("hidden");
    }
</script>

<div
    class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200"
>
    <nav class="bg-white dark:bg-gray-800 shadow-md">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between h-16">
                <div class="flex">
                    <div class="flex-shrink-0 flex items-center">
                        <Link
                            to="/"
                            class="text-2xl font-bold text-ultimate-blue dark:text-blue-400"
                            >UltiStats</Link
                        >
                    </div>
                    <div class="sm:hidden ml-6 flex space-x-8">
                        <button
                            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:text-gray-500 dark:hover:text-gray-400 dark:hover:bg-gray-800 transition-colors duration-200"
                            on:click={() => toggleMobileMenu()}
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-6 w-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M4 6h16M4 12h16M4 18h16"
                                />
                            </svg>
                        </button>
                    </div>
                    <!-- Mobile menu -->
                    <ul
                        class="mobile-menu absolute top-16 w-full bg-white dark:bg-gray-800 shadow-md p-4 flex flex-col items-center space-y-4 hidden"
                    >
                        <li>
                            <Link
                                to="/team-manager"
                                class="nav-link"
                                on:click={() => navigate()}>Team Manager</Link
                            >
                        </li>
                        <li>
                            <Link
                                to="/create-game"
                                class="nav-link"
                                on:click={() => navigate()}>Create Game</Link
                            >
                        </li>
                        <li>
                            <Link
                                to="/start-game"
                                class="nav-link"
                                on:click={() => navigate()}>Start Game</Link
                            >
                        </li>
                        <li>
                            <Link
                                to="/match-stats"
                                class="nav-link"
                                on:click={() => navigate()}>Match Stats</Link
                            >
                        </li>
                        <li>
                            <Link
                                to="/player-stats"
                                class="nav-link"
                                on:click={() => navigate()}>Player Stats</Link
                            >
                        </li>
                    </ul>
                    <div class="hidden sm:flex sm:ml-6 sm:space-x-8">
                        <!-- Desktop navigation -->
                        <Link to="/team-manager" class="nav-link"
                            >Team Manager</Link
                        >
                        <Link to="/create-game" class="nav-link"
                            >Create Game</Link
                        >
                        <Link to="/start-game" class="nav-link">Start Game</Link
                        >
                        <Link to="/match-stats" class="nav-link"
                            >Match Stats</Link
                        >
                        <Link to="/player-stats" class="nav-link"
                            >Player Stats</Link
                        >
                    </div>
                </div>
                <div class="flex items-center">
                    <ThemeToggle />
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <slot></slot>
    </main>
</div>

<style>
    :global(.nav-link) {
        @apply inline-flex items-center px-1 pt-1 text-sm font-medium 
               text-gray-500 hover:text-gray-900 
               dark:text-gray-400 dark:hover:text-white 
               transition-colors duration-200;
    }
</style>
