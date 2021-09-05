# Those are the field names of the cargo tables of leaguepedia

# Tournament
tournaments_fields = {
    "Name",
    "DateStart",
    "Date",
    "Region",
    "League",
    "Rulebook",
    "TournamentLevel",
    "IsQualifier",
    "IsPlayoffs",
    "IsOfficial",
    "OverviewPage",
}

# Game
game_fields = {
    "GameId",
    "MatchId",
    "Tournament",
    "Team1",
    "Team2",
    "Winner",
    "Gamelength_Number",
    "DateTime_UTC",
    "Team1Score",
    "Team2Score",
    "Team1Bans",
    "Team2Bans",
    "Team1Picks",
    "Team2Picks",
    "Team1Players",
    "Team2Players",
    "Team1Dragons",
    "Team2Dragons",
    "Team1Barons",
    "Team2Barons",
    "Team1Towers",
    "Team2Towers",
    "Team1RiftHeralds",
    "Team2RiftHeralds",
    "Team1Inhibitors",
    "Team2Inhibitors",
    "Patch",
    "MatchHistory",
    "VOD",
    "Gamename",
    "N_GameInMatch",
    "OverviewPage",
}


# Game Player
game_players_fields = {
    "ScoreboardPlayers.Name=gameName",
    "ScoreboardPlayers.Role_Number=gameRoleNumber",
    "ScoreboardPlayers.Champion",
    "ScoreboardPlayers.Side",
    "Players.Name=irlName",
    "Players.Country",
    "Players.Birthdate",
    "Players.ID=currentGameName",
    # "Players.Image",
    # "Players.Team=currentTeam",
    # "Players.Role=currentRole",
    # "Players.SoloqueueIds",
}


# Ordered in the draft order for pro play as of June 2020
picks_bans_fields = [
    "Team1Ban1",
    "Team2Ban1",
    "Team1Ban2",
    "Team2Ban2",
    "Team1Ban3",
    "Team2Ban3",
    "Team1Pick1",
    "Team2Pick1",
    "Team2Pick2",
    "Team1Pick2",
    "Team1Pick3",
    "Team2Pick3",
    "Team2Ban4",
    "Team1Ban4",
    "Team2Ban5",
    "Team1Ban5",
    "Team2Pick4",
    "Team1Pick4",
    "Team1Pick5",
    "Team2Pick5",
]
