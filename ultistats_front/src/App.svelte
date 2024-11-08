<script>
  import { Router, Link, Route } from "svelte-routing";
  import MainLayout from "./lib/components/layout/MainLayout.svelte";
  import Home from "./routes/Home.svelte";
  import TeamManager from "./routes/TeamManager.svelte";
  import CreateGame from "./routes/CreateGame.svelte";
  import StartGame from "./routes/StartGame.svelte";
  import Point from "./routes/Point.svelte";
  import MatchStats from "./routes/MatchStats.svelte";
  import PlayerStats from "./routes/PlayerStats.svelte";
  import "./app.css";
  
  export let url = "";
</script>

<Router {url}>
  <MainLayout>
    <Route path="/" component={Home} />
    <Route path="/team-manager" component={TeamManager} />
    <Route path="/create-game" component={CreateGame} />
    <Route path="/start-game" component={StartGame} />
    <Route path="/point/:id" component={Point} />
    <Route path="/match-stats" component={MatchStats} />
    <Route path="/player-stats" component={PlayerStats} />
  </MainLayout>
</Router>