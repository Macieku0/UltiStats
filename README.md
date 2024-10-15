# UltiStats
Application for Ultimate Frisbee statistics gathering.

## Coding stack
Python 3.12.7

## UI
Well designed user interface is crucial part of application due to high dynamics of the game. 
It is very important to have easy to use and intuitive interface to gather data as fast as possible. 
Idea is to have a multiplatform application with web interface and mobile application. 
I am planning to use Python with Flet for interface design.


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
          "action_type":"action_enum:throw,pull,pull_lift,pull_catch,turnover,call",
          "action_details":{
            "throw_details":{
              "throw_type":"throw_enum/optinal",
              "caught":"true/false",
              },
            "pull_details":{
              "in_bounds":"true/false",
              },
            "pull_lift_details":{
              "bricked":"true/false",
              },
            "pull_catch_details":{
              "caught":"true/false",
              },
            "turnover_details":{
              "turnover_type":"turnover_enum",
              },
            "call_details":{
              "call_type":"call_enum",
              "calling_player":"player_number",
              "call_result":"call_result_enum",
              },
          },
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
