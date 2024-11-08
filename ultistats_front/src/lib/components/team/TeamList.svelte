<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let teams = [];

    function handleTeamClick(team) {
        dispatch("selectTeam", team);
    }
</script>

<div class="space-y-4">
    {#each teams as team (team.id)}
        <div
            class="p-4 border rounded-lg cursor-pointer"
            role="button"
            tabindex="0"
            on:click={() => handleTeamClick(team)}
            on:keydown={(e) => e.key === "Enter" && handleTeamClick(team)}
        >
            <div class="flex justify-between items-center">
                <div>
                    <h3 class="text-lg font-semibold">
                        {team.name}
                    </h3>
                    <p class="text-sm text-gray-500">
                        {team.numberOfPlayers || 0} players
                    </p>
                </div>
                <button
                    class="text-ultimate-blue hover:text-blue-700"
                    on:click|stopPropagation={() => dispatch("editTeam", team)}
                >
                    Edit
                </button>
            </div>
        </div>
    {/each}

    {#if teams.length === 0}
        <div class="text-center py-8 text-gray-500">
            No teams created yet. Create your first team!
        </div>
    {/if}
</div>
