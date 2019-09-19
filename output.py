import requests
import json

def portLeagueSettings(output):
  league_settings = {}
  settings = ["total_rosters", "status", "season_type", "season", "roster_positions", "name", "league_id", "avatar"]
  with open('league_settings.json') as json_file:
    data = json.load(json_file)
    for setting in settings:
      league_settings[setting] = data[setting]
  json_file.close()
  output["settings"] = league_settings

def portPlayerSettings(output):
  matchups = {}
  playerSettings = ["roster_id", "players", "points"]
  # need to get this from the league setting and remove bench positions
  positions = [
    "QB",
    "RB1",
    "RB2",
    "WR1",
    "WR2",
    "TE",
    "FLEX",
    "K",
    "DEF"
  ]
  stats = {}
  with open('2019w1.json') as stat_file:
    stats = json.load(stat_file)
  stat_file.close()

  with open('atl_2019_week1_stats.json') as json_file:
    data = json.load(json_file)
    for player in data:
      playerData = {}
      for setting in playerSettings:
        playerData[setting] = player[setting]
      playerData["scores"] = {}
      for starterIndex in range(0, len(player["starters"])):
        scores = 0
        starter = player["starters"][starterIndex]
        if "pts_half_ppr" in stats[starter]:
          scores = stats[starter]["pts_half_ppr"]
        else:
          scores = 0
        playerData["scores"][positions[starterIndex]] = scores
      matchups[str(player["roster_id"])] = playerData
      # matchups[str(player["roster_id"])]["scores"] = scores
  json_file.close()
  output["players"] = matchups

def portLeagueRosters(output):
  league_rosters = {}
  rosterSettings = ["owner_id"]
  users = {}
  with open('league_users.json') as users_file:
    users = json.load(users_file)
  users_file.close()
  with open('league_rosters.json') as json_file:
    data = json.load(json_file)
    playerData = {}
    for player in data:
      for setting in rosterSettings:
        output["players"][str(player["roster_id"])][setting] = player[setting]
        for user in users:
          if user["user_id"] == player[setting]:
            output["players"][str(player["roster_id"])]["avatar"] = user["avatar"]
  json_file.close()

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()
  print('Completed Web Scraping ' + str(len(data)) + ' Items')

output = {}
portLeagueSettings(output)
portPlayerSettings(output)
portLeagueRosters(output)
saveJson("output_week1.json", output)