import sys
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict, Literal, overload

# Leaguepedia name
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


class LeaguepediaTournament(TypedDict):
    name: str

    start: str  # Expressed as YYYY-MM-DD
    end: str  # Expressed as YYYY-MM-DD

    region: str
    league: str
    leagueShort: str

    rulebook: str  # Rulebook URL

    tournamentLevel: str

    isQualifier: bool
    isPlayoffs: bool
    isOfficial: bool

    overviewPage: str


def transmute_tournament(tournament: dict) -> LeaguepediaTournament:
    return LeaguepediaTournament(
        name=tournament["Name"],
        start=tournament["DateStart"],
        end=tournament["Date"],
        region=tournament["Region"],
        league=tournament["League"],
        leagueShort=tournament["League Short"],
        rulebook=tournament["Rulebook"],
        tournamentLevel=tournament["TournamentLevel"],
        isQualifier=bool(tournament["IsQualifier"]),
        isPlayoffs=bool(tournament["IsPlayoffs"]),
        isOfficial=bool(tournament["IsOfficial"]),
        overviewPage=tournament["OverviewPage"],
    )
