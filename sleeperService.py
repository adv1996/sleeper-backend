import sleeperFetches
import sleeperMatchupFormatter
import sys
import os
import time

# python3 sleeper_service.py {league_id} {year} {week}
def service():
  start = time.time()
  arguments = len(sys.argv) - 1
  if arguments == 4:
    print("league_id - ", sys.argv[1])
    print("year - ", sys.argv[2])
    print("week - ", sys.argv[3])

    # TODO check validity of arguments passed
    league_id = sys.argv[1] # 458672130456809472
    year = sys.argv[2]
    week = sys.argv[3]
    reset = bool(sys.argv[4])
    print(reset, reset == True)

    saveStats(year, week, reset)
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
  else:
    print("Missing Arguments")
  end = time.time()
  print(end - start)

def saveStats(year, week, go):
  stats_directory = "stats"
  if not os.path.isdir(stats_directory):
    os.mkdir(stats_directory)
  filename = "stats/" + str(year) + "w" + str(week) + ".json"
  if not os.path.exists(filename) or go:
    sleeperFetches.fetchAllPlayers(year, week)

def generateOutput():
  start = time.time()
  arguments = len(sys.argv) - 1
  if arguments == 4:
    # TODO check validity of arguments passed
    print("entering the dragon")
    league_id = sys.argv[1]
    year = sys.argv[2]
    week = sys.argv[3]
    output = {}
    statsFile = "stats/" + year + "w" + week + ".json"
    matchupsFile = "leagues/" + league_id + "/week"  + week + "_matchups.json"
    league_users = "leagues/" + league_id + "/users.json"
    league_rosters = "leagues/" + league_id + "/rosters.json"
    league_settings = "leagues/" + league_id + "/settings.json"
    outputFile = 'leagues/' + league_id + "/week"  + week + "_output.json"
    sleeperMatchupFormatter.portLeagueSettings(league_settings, output)
    sleeperMatchupFormatter.portPlayerSettings(output, statsFile, matchupsFile)
    sleeperMatchupFormatter.portLeagueRosters(league_users, league_rosters, output)
    sleeperMatchupFormatter.saveJson(outputFile, output)
  end = time.time()
  print(end - start)

def generateTeamSnapshot():
  arguments = len(sys.argv) - 1
  if arguments == 4:
    # TODO check validity of arguments passed
    league_id = sys.argv[1]
    year = sys.argv[2]
    week = sys.argv[3]
    output = {}
    league_users = "leagues/" + league_id + "/users.json"
    league_rosters = "leagues/" + league_id + "/rosters.json"
    outputFile = "leagues/" + league_id + "/snapshot_output.json"
    sleeperMatchupFormatter.portLeagueSnapshot(league_users, league_rosters, output)
    sleeperMatchupFormatter.saveJson(outputFile, output)

def generateWeeklyScores():
  arguments = len(sys.argv) - 1
  print("activated", arguments)
  print(sys.argv)
  if arguments == 4:
    # TODO check validity of arguments passed
    print("activated")
    league_id = sys.argv[1]
    year = sys.argv[2]
    week = sys.argv[3]
    output = {}
    # week_file = "leagues/" + league_id + "/week" + week + "_matchups.json"
    outputFile = "leagues/" + league_id + "/weeklyScores_output.json"
    # call sleeper matchupFormatter
    output["games"] = []
    for x in range(int(week), 0, -1):
      week_file = "leagues/" + league_id + "/week" + str(x) + "_matchups.json"
      weeks = sleeperMatchupFormatter.generateWeeklyScore(str(x), week_file)
      print(weeks)
      output["games"].extend(weeks)
    sleeperMatchupFormatter.saveJson(outputFile, output)

# TODO create fun c that can pull multiple weeks
# service()
generateOutput()
# generateTeamSnapshot()
# generateWeeklyScores()

# sleeperFetches.getDraft("458672130456809472", "458672131274698752")
league_id = "458672130456809472"

draft_file = "leagues/" + league_id + "/draft.json"
league_rosters = "leagues/" + league_id + "/rosters.json"
roster_names = "leagues/" + league_id + "/week6_output.json"
# sleeperMatchupFormatter.generateDraft(draft_file, league_rosters, roster_names)
sleeperMatchupFormatter.playerPyramids(6)