# UltiStats

## General structure
JSON - Match
-----------
{
  "teams":{
    "team_1_name":{
      "players":{
        "number":"name",
      }
    },
    ...
  },
  "points":{
    "point_number":{
      "point_winner":"team_name",
      "catcher":"player_number",
      "thrower":"player_number",
      "actions":{
        "action_number":{
          "action_type":"type",
          "initial_team":"team_name",
          "initial_holder":"player_number",
          "destination":"player_number" # If action type == "drop" or similar than destination player is from other team
          "destination_team":"team_name"
        }  
      }
    }
  }
}
