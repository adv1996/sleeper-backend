import sleeperFetches
import sleeperMatchupFormatter
import sys
import os
import time
from pydash import py_

# python3 sleeper_service.py {league_id} {year} {week}
def service(week):
  start = time.time()
  arguments = len(sys.argv) - 1
  league_id = sys.argv[1] # 458672130456809472
  year = sys.argv[2]
  reset = bool(sys.argv[4])
  print(reset, reset == True)

  saveStats(year, week)
  # refactor the directory naming so that it's linked in the fetchAllPlayers file
  league_directory = "leagues/" + league_id
  if not os.path.isdir(league_directory):
    os.mkdir(league_directory)

  # save league settings, users, rosters
  usersFile = "leagues/" + league_id + "/users.json"
  rostersFile = "leagues/" + league_id + "/rosters.json"
  settingsFile = "leagues/" + league_id + "/settings.json"
  matchupsFile = "leagues/" + league_id + "/week" + str(week) + "_matchups.json"
  
  # push this logic onto the saveJson function
  # figure out why requests take a long time 
  if not os.path.exists(usersFile) or reset:
    sleeperFetches.getLeagueUsers(league_id)
  if not os.path.exists(rostersFile) or reset:
    sleeperFetches.getLeagueRosters(league_id)
  if not os.path.exists(settingsFile) or reset:
    sleeperFetches.getLeagueSettings(league_id)
  if not os.path.exists(matchupsFile) or reset:
    sleeperFetches.getLeagueMatchupsStats(week, league_id)
  end = time.time()
  print(end - start)

def saveStats(year, week):
  stats_directory = "stats"
  if not os.path.isdir(stats_directory):
    os.mkdir(stats_directory)
  filename = "stats/" + str(year) + "w" + str(week) + ".json"
  if not os.path.exists(filename):
    sleeperFetches.fetchAllPlayers(year, week)

def generateOutput(week):
  league_id = sys.argv[1]
  year = sys.argv[2]
  output = {}
  statsFile = "stats/" + year + "w" + week + ".json"
  matchupsFile = "leagues/" + league_id + "/week"  + week + "_matchups.json"
  league_users = "leagues/" + league_id + "/users.json"
  league_rosters = "leagues/" + league_id + "/rosters.json"
  league_settings = "leagues/" + league_id + "/settings.json"
  outputFile = 'leagues/' + league_id + "/week"  + week + "_output.json"
  sleeperMatchupFormatter.portLeagueSettings(league_settings, output)
  sleeperMatchupFormatter.portPlayerSettings(output, statsFile, matchupsFile, week)
  sleeperMatchupFormatter.portLeagueRosters(league_users, league_rosters, output)
  sleeperMatchupFormatter.saveJson(outputFile, output)

def generateTeamSnapshot():
  arguments = len(sys.argv) - 1
  print(arguments, sys.argv[1])
  if arguments >= 1:
    # TODO check validity of arguments passed
    league_id = sys.argv[1]
    output = {}
    league_users = "leagues/" + league_id + "/users.json"
    league_rosters = "leagues/" + league_id + "/rosters.json"
    outputFile = "leagues/" + league_id + "/snapshot_output.json"
    sleeperMatchupFormatter.portLeagueSnapshot(league_users, league_rosters, output)
    sleeperMatchupFormatter.saveJson(outputFile, output)
    return output

def generateWeeklyScores():
  arguments = len(sys.argv) - 1
  print("activated", arguments)
  print(sys.argv)
  if arguments == 4:
    # TODO check validity of arguments passed
    league_id = sys.argv[1]
    year = sys.argv[2]
    week = sys.argv[3]
    output = {}
    outputFile = "leagues/" + league_id + "/weeklyScores_output.json"
    output["games"] = []
    for x in range(int(week), 0, -1):
      week_file = "leagues/" + league_id + "/week" + str(x) + "_matchups.json"
      weeks = sleeperMatchupFormatter.generateWeeklyScore(str(x), week_file)
      print(weeks)
      output["games"].extend(weeks)
    sleeperMatchupFormatter.saveJson(outputFile, output)

def serviceMultipleWeeks():
  arguments = len(sys.argv) - 1
  if arguments == 4:
    print("week - ", sys.argv[3])
    week = int(sys.argv[3])
    for w in range(week, 0, -1):
      service(str(w))
      generateOutput(str(w))

# serviceMultipleWeeks()
# generateWeeklyScores()

def combineSnapshotPyramids():
  league_id = sys.argv[1]
  week = sys.argv[3]
  output = generateTeamSnapshot()
  players = py_.key_by(output["players"], 'roster_id')
  league_settings = "leagues/" + league_id + "/settings.json"
  sleeperMatchupFormatter.portLeagueSettings(league_settings, output)
  weekData = sleeperMatchupFormatter.playerPyramids(int(week))
  collated = "leagues/" + league_id + "/data.json"
  for k in weekData.keys():
    weekData[k]["wins"] = players[int(k)]["wins"] # these roster ids need to be the same type
  output["players"] = weekData
  sleeperMatchupFormatter.saveJson(collated, output)

combineSnapshotPyramids()