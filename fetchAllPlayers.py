import requests
import json

league_id = "458672130456809472"
def fetchAllPlayers(week):
  sleeper_url = "https://api.sleeper.app/v1/stats/nfl/regular/2019/" + str(week)
  response = requests.get(sleeper_url)
  filename = "2019w" + str(week) + ".json"
  saveJson(filename, response.json())

def fetchMatchupsStats(week):
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/matchups/" + str(week)
  response = requests.get(sleeper_url)
  filename = "atl_2019_week" + str(week) + "_matchups.json"
  saveJson(filename, response.json())

def fetchLeagueSettings():
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id
  response = requests.get(sleeper_url)
  saveJson("league_settings.json", response.json())

def getAllUsers():
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/users"
  response = requests.get(sleeper_url)
  saveJson("league_users.json", response.json())

def getAllRosters():
  sleeper_url = "https://api.sleeper.app/v1/league/" + league_id + "/rosters"
  response = requests.get(sleeper_url)
  saveJson("league_rosters.json", response.json())

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)

fetchAllPlayers(3)
fetchMatchupsStats(3)