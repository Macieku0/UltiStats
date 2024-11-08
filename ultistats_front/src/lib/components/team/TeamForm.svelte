<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let team = null;

    let name = team?.name || "";
    let city = team?.city || "";
    let division = team?.division || "";
    let description = team?.description || "";

    function handleSubmit() {
        const teamData = {
            name,
            city,
            division,
            description,
            ...(team?.id ? { id: team.id } : {}),
        };

        dispatch("submit", teamData);
        resetForm();
    }

    function resetForm() {
        name = "";
        city = "";
        division = "";
        description = "";
    }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
        <label for="name" class="block text-sm font-medium">Team Name</label>
        <input
            type="text"
            id="name"
            bind:value={name}
            class="input mt-1 block w-full"
            required
        />
    </div>

    <div>
        <label for="city" class="block text-sm font-medium">City</label>
        <input
            type="text"
            id="city"
            bind:value={city}
            class="input mt-1 block w-full"
        />
    </div>

    <div>
        <label for="division" class="block text-sm font-medium">Division</label>
        <input
            type="text"
            id="division"
            bind:value={division}
            class="input mt-1 block w-full"
        />
    </div>

    <div>
        <label for="description" class="block text-sm font-medium"
            >Description</label
        >
        <textarea
            id="description"
            bind:value={description}
            rows="3"
            class="input mt-1 block w-full"
        ></textarea>
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
            {team ? "Update Team" : "Create Team"}
        </button>
    </div>
</form>
