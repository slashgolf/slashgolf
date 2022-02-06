# :golf: Leaderboard Tracker

## :book: Overview
This sample program tracks player leaderboard movements for the current week's golf tournament. On each poll of the
leaderboard, a player's new leaderboard position is compared with his old position. If a player changes positions since
the last poll, an alert is printed to the console.

This is a great starter program for learning how to use the Live Golf Data API provided on 
RapidAPI [here](https://rapidapi.com/slashgolf/api/live-golf-data/). You can learn more and find `openAPI` documentation
on the [Slash Golf Website](https://slashgolf.dev).

## :tada: Quickstart
1. Install the necessary modules using pip: `pip install -r requirements.txt`
2. Add your RapidAPI API key to `RAPID_API_KEY` in [config.py](config.py)
    1. Note that you will need to subscribe to the Live Golf Data API on RapidAPI to get an API Key [here](https://rapidapi.com/slashgolf/api/live-golf-data/pricing)
        1. There's a free tier :smiley: :hearts:
3. Run `tracker.py` using python (tested on Python 3.9.2), which will track the current top 10 players on the leaderboard as a default
    1. If you want to track specific players, add them to the tracker constructor following the example in the code
        ```python
        # List of Player objects that we want to track. Players' official name can be queried from the /players endpoint
        players = [
            Player("Will", "Zalatoris"),
            Player("Luke", "List"),
            Player("Collin", "Morikawa"),
            Player("Hideki", "Matsuyama"),
        ]
        ```
    2. If any of the provided players are not trackable (not playing this tournament, cut, etc.), they will be ignored
4. Feel free to open an issue, submit a PR, or fork for you own use!

## :computer: Happy coding! :computer:
