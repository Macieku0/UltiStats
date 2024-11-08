<script>
    import { gameStore } from "../lib/stores/gameStore";
    export let id; // This will come from the route parameters

    let players = [
        { id: 1, name: "Player 1" },
        { id: 2, name: "Player 2" },
        { id: 3, name: "Player 3" },
        { id: 4, name: "Player 4" },
    ];

    let discHolder = null;
    let throwSequence = [];

    function onDragStart(event) {
        event.dataTransfer.setData(
            "text/plain",
            discHolder ? discHolder : "disc",
        );
    }

    function onDragOver(event) {
        event.preventDefault();
    }

    function onDrop(event, player) {
        event.preventDefault();
        const data = event.dataTransfer.getData("text/plain");
        if (data === "disc" || data === String(discHolder)) {
            discHolder = player.id;
            throwSequence.push({
                from: data === "disc" ? "Start" : data,
                to: player.id,
            });
            // Optionally reset draggable area if needed
        }
    }

    function handleAction(action) {
        if (action === "turnover") {
            discHolder = null;
            throwSequence.push({ action: "Turnover" });
        } else if (action === "timeout") {
            throwSequence.push({ action: "Timeout" });
        }
        // Handle other actions as needed
    }
</script>

<div class="container mx-auto px-4">
    <h1 class="text-3xl font-bold mb-6">Point Details</h1>
    <div class="card">
        <p>Point tracking interface coming soon...</p>
        <p>Point ID: {id}</p>
        <div class="players">
            {#each players as player}
                <div
                    class="player-circle"
                    on:dragover={onDragOver}
                    on:drop={(event) => onDrop(event, player)}
                >
                    {player.name}
                </div>
            {/each}
        </div>
        <div class="disc-area">
            {#if discHolder === null}
                <div
                    class="disc-circle"
                    draggable="true"
                    on:dragstart={onDragStart}
                >
                    Disc
                </div>
            {:else}
                <div
                    class="disc-circle"
                    draggable="true"
                    on:dragstart={onDragStart}
                >
                    {#if discHolder !== "Start"}{players.find(
                            (p) => p.id === discHolder,
                        ).name}{/if}
                </div>
            {/if}
        </div>
        <div class="actions">
            <button on:click={() => handleAction("turnover")}>Turnover</button>
            <button on:click={() => handleAction("timeout")}>Timeout</button>
            <!-- Add more action buttons as needed -->
        </div>
        <div class="throw-sequence mt-4">
            <h2 class="text-xl font-semibold">Throw Sequence</h2>
            <ul>
                {#each throwSequence as step, index}
                    <li>{index + 1}. {step.from} → {step.to || step.action}</li>
                {/each}
            </ul>
        </div>
    </div>
</div>

<style>
    /* ...existing styles... */
    .players {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .player-circle {
        width: 60px;
        height: 60px;
        background-color: #e0e0e0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #ccc;
        cursor: pointer;
    }
    .disc-area {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .disc-circle {
        width: 60px;
        height: 60px;
        background-color: #ffd700;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: grab;
    }
    .actions {
        display: flex;
        justify-content: space-around;
    }
    .actions button {
        padding: 10px 20px;
        margin: 5px;
    }
    .throw-sequence {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 5px;
    }
    .throw-sequence ul {
        list-style-type: decimal;
        padding-left: 20px;
    }
</style>
