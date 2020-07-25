[![Generic badge](https://img.shields.io/github/workflow/status/mrtolkien/leaguepedia_parser/Python%20application)](https://shields.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Leaguepedia Parser

A parser for Leaguepedia focused on accessing esports data, which largely keeps game data in the [community-defined LoL DTO format](https://github.com/mrtolkien/lol_dto).

It's very minimal at the moment and focused on my own usage of Leaguepedia’s data.
Pull requests to add features are more than welcome! (See ["Contributing"](https://github.com/mrtolkien/leaguepedia_parser#Contributing))

# Install

`pip install leaguepedia_parser`

# Demo

![Demo](leaguepedia_parser_demo.gif)

# Usage

Use the following code-blocks as examples if you want to get:

- leaguepedia_parser imported

  ```python
  import leaguepedia_parser as lpp
  # using "as lpp" not necessary, but makes code less verbose
  ```

- a _list_ of region names as _strings_:

  ```python
  regions = lpp.get_regions()
  ```

- a _list_ of tournament _dictionaries_ for a region:

  ```python
  tournaments = lpp.get_tournaments("Korea", year=2020)
  # default returns primary tournaments
  ```

* a _list_ of game _dictionaries_ for a tournament

  ```python
  games = lpp.get_games("LCK 2020 Spring")
  # name comes from lpp.get_tournaments()[x]['name']
  ```

- a _dictionary_ of picks/bans, gold, kills, and other details from a game (for details see dictionary appendix).

  ```python
  game = leaguepedia_parser.get_game_details(games[0])
  # game comes from lpp.get_games()[x]
  ```

- a _string_ of the URL to the team’s logo

  ```python
  logo_url = leaguepedia_parser.get_team_logo('T1')
  ```

More usage examples can be found in the [\_tests folder](https://github.com/mrtolkien/leaguepedia_parser/tree/master/leaguepedia_parser/_tests).

# Contributing

**To Do List:**

- Add more fields/functions from [Leaguepedia tables](https://lol.gamepedia.com/Special:CargoTables). These are commented as `#TODO` in transmuter/parser files
- Add functions to export or write data directly to SQL/SQLite3/CSV/R using pandas
- Potentially find a way to import information on plates taken, and to whom the gold was distributed

**General Philosopy:**

- We try to adhere to the [Google JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml?showone=Property_Name_Format#Property_Name_Format)
- We use [black](https://pypi.org/project/black/) formatting
- Ensure that all tests on the latest master branch are passing on yours
  - We only use pytest for testing in the repo, so if you'd like to add new tests please also use pytest ([examples in \_tests folder](https://github.com/mrtolkien/leaguepedia_parser/tree/master/leaguepedia_parser/_tests))

**Adding-to/modifying functions:**

- Information should be input as close as possible to the objects it refers to
  - Player-specific information is directly under player objects
  - Team-wide information is directly under team objects
- Field names are coherent and comply with modern LoL nomenclature
  - Every field that is an identifier ends with id
  - Fields like cs or monstersKilled use current game vocabulary (as of June 2020)
  - All durations from the game start are expressed in seconds

Thanks for your interest! :D
