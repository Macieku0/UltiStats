<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let player = null;
    export let teamId = null;

    let name = player?.name || "";
    let number = player?.number || "";
    let position = player?.position || "";
    let gender = player?.gender || "";
    let email = player?.email || "";

    const positions = ["Handler", "Cutter", "Hybrid"];

    function handleSubmit() {
        const playerData = {
            name,
            number,
            position,
            gender,
            email,
            teamId,
            ...(player?.id ? { id: player.id } : {}),
        };

        dispatch("submit", playerData);
        resetForm();
    }

    function resetForm() {
        name = "";
        number = "";
        position = "";
        email = "";
    }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
        <label for="name" class="block text-sm font-medium">Player Name</label>
        <input
            type="text"
            id="name"
            bind:value={name}
            class="input mt-1 block w-full"
            required
        />
    </div>

    <div>
        <label for="number" class="block text-sm font-medium"
            >Jersey Number</label
        >
        <input
            type="number"
            id="number"
            bind:value={number}
            class="input mt-1 block w-full"
            min="0"
            max="99"
        />
    </div>

    <div>
        <label for="position" class="block text-sm font-medium">Position</label>
        <select
            id="position"
            bind:value={position}
            class="input mt-1 block w-full"
        >
            <option value="">Select a position...</option>
            {#each positions as pos}
                <option value={pos}>{pos}</option>
            {/each}
        </select>
    </div>

    <div>
        <label for="email" class="block text-sm font-medium">Email</label>
        <input
            type="email"
            id="email"
            bind:value={email}
            class="input mt-1 block w-full"
        />
    </div>

    <div class="flex justify-end space-x-3">
        <button
            type="button"
            class="btn btn-secondary"
            on:click={() => dispatch("cancel")}
        >
            Cancel
        </button>
        <button type="submit" class="btn btn-primary">
            {player ? "Update Player" : "Add Player"}
        </button>
    </div>
</form>
