# UltiStats
Application for Ultimate Frisbee statistics gathering.

## UI
Well designed user interface is crucial part of application due to high dynamics of the game. It is 


## General structure
JSON - Match struct
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
          "action_details":{},
          "initial_team":"team_name",
          "initial_holder":"player_number",
          "destination":"player_number" # If action type == "drop" or similar than destination player is from other team
          "destination_team":"team_name"
        }  
      }
    }
  }
}
-----------
