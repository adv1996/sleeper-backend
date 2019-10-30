import requests
import json
from pydash import py_
import pandas
import sys

def portLeagueSettings(league_setting, output):
  league_settings = {}
  settings = ["total_rosters", "status", "season_type", "season", "roster_positions", "name", "league_id", "avatar"]
  with open(league_setting) as json_file:
    data = json.load(json_file)
    for setting in settings:
      league_settings[setting] = data[setting]
  json_file.close()
  league_settings["starters"] = getStarters(league_settings["roster_positions"])
  output["settings"] = league_settings

def getStarters(roster_positions):
  filteredPositions = list(filter(lambda pos: ("BN" != pos), roster_positions))
  positions = []
  count = 0
  for pos in range (0, len(filteredPositions)):
    if filteredPositions[pos] in filteredPositions[pos + 1::]:
      count += 1
    else:
      count = 0
    positions.append(filteredPositions[pos] + "-" + str(count))
  return positions
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
        if starter not in stats:
          scores = 0
        elif starter.isalpha():
          if "pts_std" in stats[starter]:
            scores = stats[starter]["pts_std"]
          else:
            scores = 0
        elif "pts_half_ppr" in stats[starter]:
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
  rosterSettings = ["owner_id", "roster_id"]
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
            output["players"][str(player["roster_id"])]["display_name"] = user["display_name"]
  json_file.close()

def portLeagueSnapshot(league_user, league_roster, output):
  league_rosters = {}
  rosterSettings = ["owner_id", "roster_id"]
  snapshotSettings = ["wins", "fpts_against", "fpts"]
  users = {}
  with open(league_user) as users_file:
    users = json.load(users_file)
  users_file.close()
  players = []
  with open(league_roster) as roster_file:
    data = json.load(roster_file)
    for player in data:
      playerData = {}
      for setting in rosterSettings:
        playerData[setting] = player[setting]
        for user in users:
          if user["user_id"] == player[setting]:
            playerData["avatar"] = user["avatar"]
      for setting in snapshotSettings:
        playerData[setting] = player["settings"][setting]
      players.append(playerData)
  roster_file.close()
  output["players"] = players

def generateWeeklyScore(week, weekly_file):
  data = {}
  matchups = {}
  with open(weekly_file) as week_file:
    data = json.load(week_file)
  week_file.close()
  # combine matchups into one
  for player in data:
    if player["matchup_id"] not in matchups:
      matchups[player["matchup_id"]] = [player]
    else:
      matchups[player["matchup_id"]].append(player)
  
  weeks = []
  for matchup_id in matchups:
    game1margin = 0
    game2margin = 0
    game1points = round(matchups[matchup_id][0]["points"], 2)
    game2points = round(matchups[matchup_id][1]["points"], 2)
    if game1points > game2points:
      game1margin = game1points - game2points
      game2margin = game1points - game2points
    else:
      game1margin = game2points - game1points
      game2margin = game2points - game1points
    game1 = {
      "roster_id": matchups[matchup_id][0]["roster_id"],
      "points": game1points,
      "week": int(week),
      "outcome": "win" if game1points > game2points else "loss",
      "margin": round(game1margin, 2)
    }
    game2 = {
      "roster_id": matchups[matchup_id][1]["roster_id"],
      "points": game2points,
      "week": int(week),
      "outcome": "win" if game2points > game1points else "loss",
      "margin": round(game2margin, 2)
    }
    weeks.append(game1)
    weeks.append(game2)
  return weeks

def generateDraft(filename, roster_file, rosterNames):
  data = {}
  with open(filename) as draft_file:
    data = json.load(draft_file)
  draft_file.close()

  rNames = {}
  with open(rosterNames) as s_file:
    rNames = json.load(s_file)
  s_file.close()

  rosters = {}
  with open(roster_file) as r_file:
    rosters = json.load(r_file)
  r_file.close()
  mappedRosters = list(
    map(lambda x: {
      "roster_id": x["roster_id"],
      "players": x["players"]
    }, rosters)
  )
  groupedRosters = py_.group_by(mappedRosters, "roster_id")
  # print(groupedRosters)
  mappedData = list(
    map(lambda x: {
      "roster_id": x["roster_id"],
      "player_id": x["player_id"],
    }, data)
  )

  groupedData = py_.group_by(mappedData, "roster_id")
  groupedOutput = {}
  names = []
  drafted = []
  acquired = []
  percentage = []
  for key, value in groupedData.items():
    players = []
    for player in value:
      players.append(player["player_id"])
    rosterPlayers = groupedRosters[key][0]["players"]
    # print(len(rosterPlayers))
    groupedOutput[key] = players
    output = {}
    output["drafted"] = py_.intersection(players, rosterPlayers)
    output["acquired"] = py_.difference(rosterPlayers, players)
    # print(rNames["players"][str(key)]["display_name"] + ","  + str(len(output["drafted"])) + "," + str(len(output["acquired"])))
    # table = pandas.DataFrame({"names": rNames["players"][str(key)]["display_name"]})
    # print(table)
    names.append(rNames["players"][str(key)]["display_name"])
    drafted.append(len(output["drafted"]))
    acquired.append(len(output["acquired"]))
    percentage.append(round(len(output["drafted"]) / 15, 2))
    groupedOutput[key] = output

  table = pandas.DataFrame({"names": names, "drafted": drafted, "acquired": acquired, "Percentage": percentage})
  output = {}
  output["draft"] = groupedOutput

  league_id = "458672130456809472"
  draft_file = "leagues/" + league_id + "/draftSorted.json"
  # saveJson(draft_file, output)

def playerPyramids(week):
  league_id = sys.argv[1]
  weekData = {}
  for x in range(1, week + 1):
    output_file = "leagues/" + league_id + "/week" + str(x) + "_output.json"
    data = {}
    with open(output_file) as outfile:
      data = json.load(outfile)
    outfile.close()
    for player in data["players"].keys():
      points = data["players"][player]["points"]
      if player in weekData:
        weekData[player]["scores"].append(data["players"][player]["scores"])
      else:
        weekData[player] = {
          "scores": [data["players"][player]["scores"]],
          "avatar": data["players"][player]["avatar"],
          "display_name": data["players"][player]["display_name"],
          "owner_id": data["players"][player]["owner_id"]
        }
  return weekData

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()
  print('Completed Web Scraping ' + str(len(data)) + ' Items')