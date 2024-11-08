<script>
    import { theme } from "../stores/theme";
    import { Moon, Sun } from "lucide-svelte";

    function toggleTheme() {
        theme.update((current) => {
            const newTheme = current === "light" ? "dark" : "light";
            return newTheme;
        });
    }
</script>

<button
    on:click={toggleTheme}
    class="p-2 rounded-lg text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors duration-200"
    aria-label="Toggle theme"
>
    {#if $theme === "light"}
        <Moon size={20} />
    {:else}
        <Sun size={20} />
    {/if}
</button>
