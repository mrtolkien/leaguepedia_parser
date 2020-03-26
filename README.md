# leaguepedia_parser
A parser for the Leaguepedia website, focused on accessing esports data.

Possible future functionality includes direct querying for games from team names, fuzzy matching for tournament names, 
and so on and so forth.

# Install
`pip install leaguepedia_parser`

# Usage
```python
import leaguepedia_parser

lp = leaguepedia_parser.LeaguepediaParser()

# Gets you available regions
lp.get_tournament_regions()

# Gets you tournaments in the region, by default only returns primary tournaments
tournaments = lp.get_tournaments('Korea', year=2020)

# Gets you all games for a tournament. Get the name from get_tournaments()
games = lp.get_games(tournaments[0]['name'])

# Gets picks and bans for a game. Get the game object from get_games()
lp.get_picks_bans(games[0])
```