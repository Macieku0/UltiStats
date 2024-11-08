<script lang="ts">
    import { onMount } from "svelte";
    import TeamList from "../lib/components/team/TeamList.svelte";
    import TeamForm from "../lib/components/team/TeamForm.svelte";
    import PlayerList from "../lib/components/team/PlayerList.svelte";
    import PlayerForm from "../lib/components/team/PlayerForm.svelte";
    import { gameStore } from "../lib/stores/gameStore";
    import { playerStore } from "../lib/stores/playerStore";

    let teams = [];
    let players = [];
    let selectedTeam = null;
    let showTeamForm = false;
    let showPlayerForm = false;
    let editingTeam = null;
    let editingPlayer = null;

    let searchQuery = "";
    let filteredTeams = teams;
    let filteredPlayers = [];

    // Simulated data - replace with actual API calls
    // TODO Replace with actual API calls
    onMount(() => {
        // Mock data for testing
        teams = [
            {
                id: 1,
                name: "Thunderbolts",
                city: "Seattle",
                description: "Community team",
                numberOfPlayers: 2,
            },
            {
                id: 2,
                name: "Windchasers",
                city: "Portland",
                description: "Club team",
                numberOfPlayers: 4,
            },
        ];

        players = [
            {
                id: 1,
                teamId: 1,
                name: "John Doe",
                number: "7",
                position: "Handler",
                email: "john@example.com",
            },
            {
                id: 2,
                teamId: 1,
                name: "Jane Smith",
                number: "13",
                position: "Cutter",
                email: "jane@example.com",
            },
            {
                id: 3,
                teamId: 2,
                name: "Alice Johnson",
                number: "21",
                position: "Handler",
                email: "",
            },
            {
                id: 4,
                teamId: 2,
                name: "Bob Brown",
                number: "42",
                position: "Cutter",
                email: "",
            },
            {
                id: 5,
                teamId: 2,
                name: "Charlie White",
                number: "99",
                position: "Cutter",
                email: "",
            },
            {
                id: 6,
                teamId: 2,
                name: "David Black",
                number: "23",
                position: "Handler",
                email: "",
            },
        ];
    });

    function handleTeamSubmit(event) {
        const teamData = event.detail;
        if (editingTeam) {
            // Update existing team
            teams = teams.map((t) => (t.id === editingTeam.id ? teamData : t));
        } else {
            // Add new team
            teams = [...teams, { ...teamData, id: Date.now() }];
        }
        closeTeamForm();
    }

    function handlePlayerSubmit(event) {
        const playerData = event.detail;
        if (editingPlayer) {
            // Update existing player
            players = players.map((p) =>
                p.id === editingPlayer.id ? playerData : p,
            );
        } else {
            // Add new player
            players = [...players, { ...playerData, id: Date.now() }];
        }
        closePlayerForm();
    }

    function handleTeamSelect(event) {
        selectedTeam = event.detail;
        filteredPlayers = players.filter((p) => p.teamId === selectedTeam.id);
    }

    function handleEditTeam(event) {
        editingTeam = event.detail;
        showTeamForm = true;
    }

    function handleEditPlayer(event) {
        editingPlayer = event.detail;
        showPlayerForm = true;
    }

    function closeTeamForm() {
        showTeamForm = false;
        editingTeam = null;
    }

    function closePlayerForm() {
        showPlayerForm = false;
        editingPlayer = null;
    }

    $: filteredPlayers = selectedTeam
        ? players.filter((p) => p.teamId === selectedTeam.id)
        : [];

    $: filteredTeams = teams.filter((team) =>
        team.name.toLowerCase().includes(searchQuery.toLowerCase()),
    );

    $: filteredPlayers = selectedTeam
        ? filteredPlayers.filter((p) =>
              p.name.toLowerCase().includes(searchQuery.toLowerCase()),
          )
        : filteredPlayers.filter((p) =>
              p.name.toLowerCase().includes(searchQuery.toLowerCase()),
          );
</script>

<div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold">Team Manager</h1>
    </div>

    <input
        type="text"
        class="w-full p-2 mb-4 border-2 border-gray-300 rounded-md"
        placeholder="Search..."
        on:input={(e) => (searchQuery = e.target.value)}
    />

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Teams Section -->
        <div class="space-y-6">
            <h2 class="text-xl font-semibold">Teams</h2>
            <button
                class="btn btn-primary"
                on:click={() => (showTeamForm = true)}
            >
                Create New Team
            </button>
            {#if showTeamForm}
                <div class="card">
                    <TeamForm
                        team={editingTeam}
                        on:submit={handleTeamSubmit}
                        on:cancel={closeTeamForm}
                    />
                </div>
            {:else}
                <TeamList
                    teams={filteredTeams}
                    on:selectTeam={handleTeamSelect}
                    on:editTeam={handleEditTeam}
                />
            {/if}
        </div>

        <!-- Players Section -->
        <div class="space-y-6">
            {#if showPlayerForm}
                <div class="card">
                    <PlayerForm
                        player={editingPlayer}
                        teamId={selectedTeam?.id}
                        on:submit={handlePlayerSubmit}
                        on:cancel={closePlayerForm}
                    />
                </div>
            {:else}
                <PlayerList
                    players={filteredPlayers}
                    {selectedTeam}
                    on:addPlayer={() => (showPlayerForm = true)}
                    on:editPlayer={handleEditPlayer}
                />
            {/if}
        </div>
    </div>
</div>
