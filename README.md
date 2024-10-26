# UltiStats
Application for Ultimate Frisbee statistics gathering.

## Coding stack
Python 3.12.7

## UI
Well designed user interface is crucial part of application due to high dynamics of the game. 
It is very important to have easy to use and intuitive interface to gather data as fast as possible. 
Idea is to have a multiplatform application with web interface and mobile application. 
I am planning to use Python Flet framework to build whole application MVP.


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


Project structure
``` 
├── README.md
├── requirements.txt
├── main.py
├── config/
│   ├── __init__.py
│   └── settings.py          # Application configuration, DB settings, etc.
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── team.py         # Team model
│   │   ├── player.py       # Player model
│   │   ├── match.py        # Match model
│   │   ├── point.py        # Point model
│   │   └── stats.py        # Statistics models
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py   # Database connection handling
│       └── domain_repositories.py   # Data access layer
│   │   └── repository.py   # Data access layer
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py         # Main UI application class
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── theme.py   # Theme-related components
│   │   │   ├── player_circle.py  # Player circle component
│   │   │   └── common.py  # Shared UI components
│   │   └── views/
│   │       ├── __init__.py
│   │       ├── base_view.py      # Base view class
│   │       ├── start_page.py     # Start/landing page
│   │       ├── team_manager.py   # Team creation/management
│   │       ├── game_view.py      # Active game view
│   │       ├── match_stats.py    # Match statistics view
│   |       ├── point_view.py     # Point view
│   │       └── player_stats.py   # Player statistics view
│   └── utils/
│       ├── __init__.py
│       ├── validators.py   # Input validation functions
│       └── statistics.py   # Statistics calculation helpers
└── tests/
    ├── __init__.py
    ├── test_models/
    ├── test_ui/
    └── test_utils/
```