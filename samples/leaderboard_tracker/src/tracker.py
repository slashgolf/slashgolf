"""
Sample application using the Slash Golf PGA Tour Data API. The application tracks players' leaderboard movements for
the current week's tournament.

Please check https://slashgolf.dev/docs for more detailed information on the various API endpoints
"""

from datetime import datetime
import requests
import time
import traceback

import leaderboard_tracker.config as cfg

API_BASE_URL = "https://live-golf-data.p.rapidapi.com"

API_DEFAULT_HEADERS = {
    "x-rapidapi-host": "live-golf-data.p.rapidapi.com",
    "x-rapidapi-key": cfg.RAPID_API_KEY,
}


# Player object represents a golfer that we want to track in the LeaderboardTracker. The first_name and last_name
# fielda are case-sensitive. You can look up player names either via the /players endpoint or looking at the `players`
# field on /tournament endpoint response
class Player:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def first_name(self):
        return self.first_name()

    def last_name(self):
        return self.last_name()


# LeaderboardTracker accepts a list of Player objects that the user wants to track. It then checks that these players
# are trackable by ensuring the player is in the tournament field and is not cut, disqualified, or withdrawn. Then,
# the /leaderboard endpoint is called every LEADERBOARD_UPDATE_INTERVAL_MINUTES, and any player leaderboard movements
# are printed to the console
class LeaderboardTracker:
    def __init__(self, players):
        """
        :param players: list of Player objects
        """
        if not isinstance(players, list):
            raise Exception("Exception: must provide list of Player objects to constructor")

        if len(players) == 0:
            print("No players provided to constructor so will track the top {} players from leaderboard".format(
                cfg.DEFAULT_LEADERGBOARD_SIZE
            ))

        self.players = players

    def get_tournament_from_schedule(self):
        """
        Determine the current week's tournament based off of the /schedule endpoint
        :return: string `tournId` (e.g. "004") that identifies a given tournament
        """
        url = "{}/schedule".format(API_BASE_URL)
        query_string = {
            "year": cfg.SEASON_YEAR,
        }

        resp = requests.get(url=url, headers=API_DEFAULT_HEADERS, params=query_string)
        if resp.status_code != 200:
            raise Exception("Exception: failed to query the schedule endpoint ({}): {}".format(resp.status_code, resp.content))

        current_week_num = datetime.now().isocalendar()[1]
        for tournament in resp.json()['schedule']:
            if int(tournament['date']['weekNumber']) == current_week_num:
                print("Found this week's tournament: {}".format(tournament))
                return tournament['tournId']

        raise Exception("Exception: could not find tournament id for week number {}".format(current_week_num))

    def get_tournament_info(self, tourn_id):
        """
        Fetch a given tournament's metadata based on the provided `tournId`. The /tournament endpoint has information
        such as the entry list, courses played, and prize purse.
        :param tourn_id: string `tournId` used to identify a given tournament
        :return: Dictionary response from /tournament endpoint
        """
        url = "{}/tournament".format(API_BASE_URL)
        query_string = {
            "tournId": tourn_id,
            "year": cfg.SEASON_YEAR,
        }

        resp = requests.get(url=url, headers=API_DEFAULT_HEADERS, params=query_string)
        if resp.status_code != 200:
            raise Exception("Exception: failed to query the tournament endpoint ({}): {}".format(resp.status_code, resp.content))

        return resp.json()

    def validate_players_in_entry_list(self, players, entry_list):
        """
        Given a list of Player objects and the tournament's entry list, ensure that the players are trackable for this
        tournament
        :param players: list of Player objects
        :param entry_list: list of players in an entry list with fields {"firstName", "lastName"}
        :return: Dictionary of trackable players with their initial scores set to None
        """
        tracked_player_dict = {}

        # Generate a hash of the entry list based on the tuple (first_name, last_name) for faster lookups
        # Skip any player whose status != "active", meaning they were cut, wd, or dq
        entry_list_dict = {}
        for official_player in entry_list:
            if official_player['status'] == "active":
                name_key = (official_player['firstName'], official_player['lastName'])
                entry_list_dict[name_key] = None

        # Validate that the desired players are all active and in the tournament
        for desired_player in players:
            desired_player_key = (desired_player.first_name, desired_player.last_name)
            if desired_player_key in entry_list_dict:
                tracked_player_dict[desired_player_key] = None
                print("Tracking player {} for this tournament".format(desired_player_key))
            else:
                print("Player {} is not trackable for this tournament".format(desired_player_key))

        return tracked_player_dict

    def get_top_n_of_entry_list(self, entry_list, num_of_entry_list):
        """
        Given a tournament entry list
        :param entry_list: list of players in an entry list with fields {"firstName", "lastName"}
        :param num_of_entry_list: int number of players from the top of the entry list to track
        :return: Dictionary of trackable players with their initial scores set to None
        """
        tracked_player_dict = {}

        for official_player in entry_list:
            if official_player['status'] == "active":
                name_key = (official_player['firstName'], official_player['lastName'])
                tracked_player_dict[name_key] = None

            # Once we have our desired number of tracked players, return
            if len(tracked_player_dict) == num_of_entry_list:
                return tracked_player_dict

        return tracked_player_dict

    def sleep(self):
        time.sleep(60 * cfg.LEADERBOARD_UPDATE_INTERVAL_MINUTES)

    def Run(self):
        """
        While the roundStatus is "In Progress", query for leaderboard updates every interval
        :return:
        """
        # Get necessary metadata for this week's tournament
        tourn_id = self.get_tournament_from_schedule()
        tourn_info = self.get_tournament_info(tourn_id)

        # Check that provided players are active (not cut, dq, etc.) and trackable for this event
        player_id_to_leaderboard_position = self.validate_players_in_entry_list(self.players, tourn_info['players'])
        if len(player_id_to_leaderboard_position) == 0:
            print("None of the provided players {} are trackable", self.players)
            player_id_to_leaderboard_position = self.get_top_n_of_entry_list(tourn_info['players'], cfg.DEFAULT_LEADERGBOARD_SIZE)
            if len(player_id_to_leaderboard_position) == 0:
                raise Exception("Exception: no players found in entry list")

        # Parameters for querying the /leaderboard endpoint
        url = "{}/leaderboard".format(API_BASE_URL)
        query_string = {
            "tournId": tourn_id,
            "year": cfg.SEASON_YEAR,
        }

        while True:
            print("{} Querying for leaderboard update".format(datetime.now()))

            # Fetch the most up-to-date leaderboard from the Live Golf Data API
            resp = requests.get(url=url, headers=API_DEFAULT_HEADERS, params=query_string)
            if resp.status_code != 200:
                # Don't throw Exception here, instead sleep another interval and try again
                print("Failed to query the leaderboard endpoint ({}): {}".format(resp.status_code, resp.content))
                self.sleep()
                continue

            # If round hasn't started yet, return
            if resp.json()['roundStatus'] == "Groupings Official":
                raise Exception("Exception: round has not yet started")

            # Parse leaderboard for player updates
            for row in resp.json()['leaderboardRows']:
                player_name_key = (row['firstName'], row['lastName'])
                if player_name_key in player_id_to_leaderboard_position:
                    new_position = row['position']
                    print("Found player {} in leaderboard position {}".format(player_name_key, new_position))

                    # Check if leaderboard position is different than last
                    prev_position = player_id_to_leaderboard_position[player_name_key]
                    if prev_position is not None and prev_position != new_position:
                        # Right now, we just print to console when there's an update to a player's leaderboard position.
                        # However, you could make this whatever you want! E.g. Send a push notification or update the UI
                        print("\N{bell} {} {} has moved from position {} to position {}".format(
                            row['firstName'],
                            row['lastName'],
                            prev_position,
                            new_position,
                        ))

                    # Update position in memory
                    player_id_to_leaderboard_position[player_name_key] = new_position

            # return if the round has ended
            if resp.json()['roundStatus'] == "Official":
                print("Round has completed")
                return

            # Wait for the next interval
            self.sleep()


if __name__ == "__main__":
    print("Running Leaderboard Tracker")

    # List of Player objects that we want to track. Players' official name can be queried from the /players endpoint
    players = [
        # Player("Will", "Zalatoris"),
        # Player("Luke", "List"),
        # Player("Collin", "Morikawa"),
        # Player("Hideki", "Matsuyama"),
    ]

    try:
        # Instantiate the tracker with list of players and run it
        lt = LeaderboardTracker(players)

        lt.Run()
    except Exception as e:
        print("Exception: {}".format(e))
        traceback.print_exc()
