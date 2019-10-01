import sleeperFetches
import sleeperMatchupFormatter
import sys
import os
import time

# python3 sleeper_service.py {league_id} {year} {week}
def service():
  start = time.time()
  arguments = len(sys.argv) - 1
  if arguments == 3:
    print("league_id - ", sys.argv[1])
    print("year - ", sys.argv[2])
    print("week - ", sys.argv[3])

    # TODO check validity of arguments passed
    league_id = sys.argv[1]
    year = sys.argv[2]
    week = sys.argv[3]

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
    if not os.path.exists(usersFile):
      sleeperFetches.getLeagueUsers(league_id)
    if not os.path.exists(rostersFile):
      sleeperFetches.getLeagueRosters(league_id)
    if not os.path.exists(settingsFile):
      sleeperFetches.getLeagueSettings(league_id)
    if not os.path.exists(matchupsFile):
      sleeperFetches.getLeagueMatchupsStats(week, league_id)
  else:
    print("Missing Arguments")
  end = time.time()
  print(end - start)
  # takes 3.5 minutes to pull all the base data for a new league.

def saveStats(year, week):
  stats_directory = "stats"
  if not os.path.isdir(stats_directory):
    os.mkdir(stats_directory)
  filename = "stats/" + str(year) + "w" + str(week) + ".json"
  if not os.path.exists(filename):
    sleeperFetches.fetchAllPlayers(year, week)

def generateOutput():
  start = time.time()
  arguments = len(sys.argv) - 1
  if arguments == 3:
    # TODO check validity of arguments passed
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

service()
generateOutput()
