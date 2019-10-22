import requests
import json

def portTeamSnapshot():
  url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/1501330?view=mTeam"
  response = requests.get(url, cookies = {
      "swid": "{9B5EAD9D-4AAC-459D-9EAD-9D4AAC759DC4}",
      "espn_s2": "AECVyzlDo1bnXrYnpt%2B1w2MQU3YHiKl4jKN%2BTkoSqnA%2FNNbIvoV3zM%2FXQybF53nWMuD%2BIuKSlBdkrqcN5JPFgU0HuMnRecHJaDNBnLFRfv13aTVcQvmT0UfaxP%2BOyOmKrteoxu1%2FctKOuppBCpZa%2BnQC9Ze54aDQICRCNLYXws3BFPF1G%2BbT6lrf7%2BRSic%2FweK8cKcobHGXBPynLHeqc%2BY7W9lj3mKnDz0fPsmMNtwzmGFsS1s6D6yoTYQDV01uhHefrPyakIbELUn9sY%2FOPdwHRJf6QC2gBUAYwX9Dhg9LO3A%3D%3D"
  })
  saveJson("espn_data_team.json", response.json())

def portTeamMatchup():
  url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/1501330?view=mMatchup"
  response = requests.get(url, cookies = {
      "swid": "{9B5EAD9D-4AAC-459D-9EAD-9D4AAC759DC4}",
      "espn_s2": "AECVyzlDo1bnXrYnpt%2B1w2MQU3YHiKl4jKN%2BTkoSqnA%2FNNbIvoV3zM%2FXQybF53nWMuD%2BIuKSlBdkrqcN5JPFgU0HuMnRecHJaDNBnLFRfv13aTVcQvmT0UfaxP%2BOyOmKrteoxu1%2FctKOuppBCpZa%2BnQC9Ze54aDQICRCNLYXws3BFPF1G%2BbT6lrf7%2BRSic%2FweK8cKcobHGXBPynLHeqc%2BY7W9lj3mKnDz0fPsmMNtwzmGFsS1s6D6yoTYQDV01uhHefrPyakIbELUn9sY%2FOPdwHRJf6QC2gBUAYwX9Dhg9LO3A%3D%3D"
  })
  saveJson("espn_data_matchup.json", response.json())

def saveJson(filename, data):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile)
  outfile.close()

def generateWeeklyScoresOutput():
  matchup_file = "espn_data_matchup.json"
  data = {}
  with open(matchup_file) as matchups:
    data = json.load(matchups)
  matchups.close()
  output = {}
  outcomes = []
  for game in data["schedule"]:
    if game["winner"] != "UNDECIDED":
      team1_id = game["away"]["teamId"]
      team2_id = game["home"]["teamId"]
      team1_score = game["away"]["totalPoints"]
      team2_score = game["home"]["totalPoints"]
      week = game["matchupPeriodId"]
      team1_outcome = "loss"
      team2_outcome = "loss"
      team_margin = 0
      if team1_score > team2_score:
        team1_outcome = "win"
        team_margin = round(team1_score - team2_score, 2)
      else:
        team2_outcome = "loss"
        team_margin = round(team2_score - team1_score, 2)
      outcomes.append({
        "roster_id": team1_id,
        "points": team1_score,
        "week": week,
        "outcome": team1_outcome,
        "margin": team_margin
      })
      outcomes.append({
        "roster_id": team2_id,
        "points": team2_score,
        "week": week,
        "outcome": team2_outcome,
        "margin": team_margin
      })
  output["games"] = outcomes
  output["platform"] = "espn"
  saveJson("espn_weekly_scores.json", output)
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

portTeamSnapshot()
generateSnapshotOutput()
portTeamMatchup()
generateWeeklyScoresOutput()