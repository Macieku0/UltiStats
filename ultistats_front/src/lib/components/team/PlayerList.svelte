<script lang="ts">
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let players = [];
    export let selectedTeam = null;
</script>

<div class="space-y-4">
    <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold">
            {#if selectedTeam}
                Players in {selectedTeam.name}
            {:else}
                Select a team to view players
            {/if}
        </h3>
        <button class="btn btn-primary" on:click={() => dispatch("addPlayer")}>
            Add Player
        </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {#each players as player (player.id)}
            <div class="p-4 border rounded-lg cursor-pointer">
                <div class="flex justify-between items-center">
                    <div>
                        <h4 class="font-medium">
                            {player.number} - {player.name}
                        </h4>
                        <p class="text-sm text-gray-500">
                            {player.position || "No position"}
                        </p>
                    </div>
                    <button
                        class="text-ultimate-blue hover:text-blue-700"
                        on:click|stopPropagation={() =>
                            dispatch("editPlayer", player)}
                    >
                        Edit
                    </button>
                </div>
            </div>
        {/each}

        {#if players.length === 0}
            <div class="col-span-2 text-center py-8 text-gray-500">
                No players added yet.
            </div>
        {/if}
    </div>
</div>
