import requests
import json

def portTeamSnapshot(league_id, year):
  url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/1501330?view=mTeam"
  response = requests.get(url, cookies = {
      "swid": "{9B5EAD9D-4AAC-459D-9EAD-9D4AAC759DC4}",
      "espn_s2": "AECVyzlDo1bnXrYnpt%2B1w2MQU3YHiKl4jKN%2BTkoSqnA%2FNNbIvoV3zM%2FXQybF53nWMuD%2BIuKSlBdkrqcN5JPFgU0HuMnRecHJaDNBnLFRfv13aTVcQvmT0UfaxP%2BOyOmKrteoxu1%2FctKOuppBCpZa%2BnQC9Ze54aDQICRCNLYXws3BFPF1G%2BbT6lrf7%2BRSic%2FweK8cKcobHGXBPynLHeqc%2BY7W9lj3mKnDz0fPsmMNtwzmGFsS1s6D6yoTYQDV01uhHefrPyakIbELUn9sY%2FOPdwHRJf6QC2gBUAYwX9Dhg9LO3A%3D%3D"
  })
  saveJson("espn_data_team.json", response.json())

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()

def generateSnapshotOutput():
  espn_team = "espn_data_team.json"
  output = {}
  players = []
  with open(espn_team) as espn_team:
    data = json.load(espn_team)
    teams = data["teams"]
    for team in teams:
      playerData = {}
      playerData["owner_id"] = team["primaryOwner"]
      playerData["avatar"] = team["logo"]
      playerData["wins"] = team["record"]["overall"]["wins"]
      playerData["fpts_against"] = team["record"]["overall"]["pointsAgainst"]
      playerData["fpts"] = team["record"]["overall"]["pointsFor"]
      players.append(playerData)
  espn_team.close()
  output["players"] = players
  saveJson("espn_output.json", output)

generateSnapshotOutput()