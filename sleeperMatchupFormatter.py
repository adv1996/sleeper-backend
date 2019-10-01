import requests
import json

def portLeagueSettings(league_setting, output):
  league_settings = {}
  settings = ["total_rosters", "status", "season_type", "season", "roster_positions", "name", "league_id", "avatar"]
  with open(league_setting) as json_file:
    data = json.load(json_file)
    for setting in settings:
      league_settings[setting] = data[setting]
  json_file.close()
  output["settings"] = league_settings

def portPlayerSettings(output, statsFile, matchupsFile):
  matchups = {}
  playerSettings = ["roster_id", "players", "points"]
  roster_positions = output["settings"]["roster_positions"]
  # filter out the bench positions
  filteredPositions = list(filter(lambda pos: ("BN" != pos), roster_positions))
  positions = []
  count = 0
  for pos in range (0, len(filteredPositions)):
    if filteredPositions[pos] in filteredPositions[pos + 1::]:
      count += 1
    else:
      count = 0
    print(filteredPositions[pos], count)
    positions.append(filteredPositions[pos] + "-" + str(count))
  stats = {}
  with open(statsFile) as stat_file:
    stats = json.load(stat_file)
  stat_file.close()

  with open(matchupsFile) as json_file:
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

def portLeagueRosters(league_user, league_roster, output):
  league_rosters = {}
  rosterSettings = ["owner_id"]
  users = {}
  with open(league_user) as users_file:
    users = json.load(users_file)
  users_file.close()
  with open(league_roster) as json_file:
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