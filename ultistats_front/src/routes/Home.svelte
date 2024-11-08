<script>
  import { Link } from "svelte-routing";
</script>

<div class="py-12">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center">
      <h1 class="text-4xl font-bold sm:text-5xl md:text-6xl">
        Welcome to UltiStats
      </h1>
      <p
        class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl"
      >
        Track your Ultimate Frisbee statistics with ease. Manage teams, record
        games, and analyze performance.
      </p>
      <div class="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
        <div class="rounded-md">
          <Link to="/create-game" class="btn btn-primary inline-block">
            Create New Game
          </Link>
        </div>
        <div class="mt-3 rounded-md sm:mt-0 sm:ml-3">
          <Link to="/team-manager" class="btn btn-secondary inline-block">
            Manage Teams
          </Link>
        </div>
      </div>
    </div>
  </div>
</div>
