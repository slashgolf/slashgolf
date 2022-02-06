---
layout: page
permalink: /quickstart/
title: Quick Start
---
# Live Leaderboard Data

### Step 1: Fetch the Schedule
The schedule for a PGA Tour season is obtainable from the `/schedules` endpoint. Each entry in the `schedule` array
contains metadata about a given tournament. The most important field in this object is the `tournId` field, which 
is used to query almost every other endpoint.

### Step 2: Fetch the Leaderboard
The leaderboard for a specific tournament is obtainable from the `/leaderboards` endpoint. Each tournament has 1 
leaderboard entry for each round of a tournament for a given year. A leaderboard is queryable using `tournId` obtained 
from the `/schedules` endpoint along with the `year` for that `tournId`. Note that a tournament's `tournId` can change
for a different year. For example, The Masters was played "twice" in the 2021 season, so it has 2 `tournId`.

To fetch the leaderboard for a specific round, you can include the optional `roundId` parameter in the api call. If not 
included, the most up-to-date leaderboard for that tournament will be returned.

#### Github Tutorial
[Leaderboard Tracker Sample](https://github.com/slashgolf/slashgolf/tree/main/samples/leaderboard_tracker)

# Live Scorecard Data

### Step 1: Fetch the Schedule
See [schedule](live-leaderboard-data).

### Step 2: Fetch the Tournament Entry List
In order to query for live scorecard data, a `playerId` parameter must be included in the query along with the tournament's
`tournId` and `year`. Entry list, along with other pertinent metadata, such as location and course information, can
be fetched from the `/tournaments` endpoint. The entry list can be found under the `players` array in the endpoint's response.
A player's `status` can also be found in each entry of the array, which will have values `active`, `cut`, or `wd`.

Note that a tournament's entry list is finalized by the PGA Tour some time after 5 pm ET.

### Step 3: Fetch Player's Scorecard
The player's scorecard for a given year's tournament can be fetched from the `/scorecards` endpoint. The `tournId`, `year`, 
and `playerId` are all required parameters. To query only a single round for the given player, include the `roundId`
parameter. If no `roundId` is included, an array of all the player's scorecards will be returned.

#### Github Tutorial
Coming Soon!

# Tournament Results

### Step 1: Fetch the Schedule
See [schedule](live-leaderboard-data).

### Step 2: Fetch FedExCup Points
A tournament's FedExCup points can be fetched from the `/points` endpoint by providing the tournament's `tournId` and `year`
parameters. The `leaderboard` array has an object for each player on the leaderboard who earned FedExCup points from the event.
The points are populated usually a few hours after the tournament has ended. 

Note that non-PGA Tour players will not
be accounted for in this leaderboard.

### Step 3: Fetch Earnings
A tournament's earnings can be fetched from the `/earnings` endpoint by providing the tournament's `tournId` and `year`
parameters. The `leaderboard` array has an object for each player on the leaderboard who earned a paycheck from the event.
The earnings are populated usually a few hours after the tournament has ended.

#### Github Tutorial
Coming Soon!
