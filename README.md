# UltiStats

Application for Ultimate Frisbee statistics gathering.

## Coding stack

Backend - Python 3.12.7 (FastAPI, Pydantic, SQLAlchemy, SQLite)
Frontend - HTML, CSS, JavaScript (Svelte)

## UI

Well designed user interface is crucial part of application due to high dynamics of the game.
It is very important to have easy to use and intuitive interface to gather data as fast as possible.
It is also important to have a good overview (with high readability) of the match statistics.
Actions should be easy to perform and the user should be guided through the process of gathering data - using drag and drop, big buttons, etc.

### Views

1. Start page view - Landing page with basic information about the application and links to other views:

- Team manager
- Create Game view
- Start Game view
- Match statistics
- Player statistics

2. Team manager view - Team creation and players management view
3. Create Game view - Page where user can setup new game - choose teams
4. Start Game view - Page where user can choose which game to start and add details about the point - players involved and which team starts on offence - it will lead to another view "Point"
5. Point view - This page starts with form to fill about the players involved in the point and the pull info. After submitting the form view will be changed. It will show the point in progress with the player that holds the disc after the pull and rest of the players from the team. In this view user can add details about the point - one by one - throw, catch, turnover, call, etc. After the point is finished user can submit the point and go back to the "Point view" for next point view.
6. Match statistics view - View with statistics about the match - course of the each point, summary of the points, turnovers, calls, etc.
7. Player statistics view - View with statistics about the player - number of points played, turnovers, catches, throws, for each match and in total.
