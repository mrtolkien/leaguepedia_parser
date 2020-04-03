from typing import List
import datetime
import sys

try:
    from river_mwclient.esports_client import EsportsClient
except ModuleNotFoundError:
    import mwclient

river_mwclient_loaded = True if 'river_mwclient' in sys.modules else False


class LeaguepediaParser(EsportsClient if river_mwclient_loaded else object):
    """
    Simple esports-oriented parser for the Leaguepedia API

    Full documentation: https://lol.gamepedia.com/Help:API_Documentation
    """

    def __init__(self,
                 get_full_results: bool = False,
                 **kwarg):
        # If this is True the parser will automatically issue multiple queries if the answer is over 500 rows.
        self.get_full_results = get_full_results

        # This class is made to interact only with the LoL wiki
        if river_mwclient_loaded:
            super().__init__('lol', **kwarg)
            self.query = self.cargo_client.query
        else:
            self.client = mwclient.Site('lol.gamepedia.com', path='/', **kwarg)
            self.query = lambda **kwargs: [row['title'] for row in
                                           self.client.api('cargoquery', **kwargs)['cargoquery']]

        # leaguepedia_game_id is the field called ScoreboardID_Wiki in ScoreboardGame
        # picks_bans_cache[tournament_name][leaguepedia_game_id] = {pick_bans}
        self.picks_bans_cache = {}

        # players_cache[player_link] = {player, updated_at}
        self.players_cache = {}

    def _cargoquery(self, **kwargs) -> list:
        if 'limit' in kwargs:
            limit = kwargs.pop('limit')
        else:
            limit = self.client.api_limit

        result = self.query(**kwargs, limit=limit)

        # Kinda wish Python had a do while loop, would like to cleanup the code duplication here.
        while self.get_full_results and result and result.__len__() % limit == 0:
            result += self.query(**kwargs, limit=limit, offset=result.__len__())

        return result

    def get_tournament_regions(self) -> List[str]:
        """
        Returns a list of all region names that appear in the Tournaments table.

        Issues one query.

        :return:    The list of all region names
        """
        regions_dicts_list = self._cargoquery(tables='Tournaments',
                                              fields='Region',
                                              group_by='Region')

        return [row['Region'] for row in regions_dicts_list]

    def get_tournaments(self,
                        region: str = None,
                        year: int = None,
                        tournament_level: str = 'Primary',
                        is_playoffs: bool = None,
                        **kwargs) -> List[dict]:
        """
        Returns a list of tournament dictionaries.
        Notable keys include 'name', 'region', 'league', 'date_start', and 'date_end'.

        Issues one query per 500 rows.

        :param region
                    Recommended to get it from get_tournament_regions().
        :param year
                    Year to filter on. Defaults to None.
        :param tournament_level
                    Can be Primary, Secondary, Major, Secondary, Showmatch. Defaults to Primary.
        :param is_playoffs
                    Can be used to filter between playoffs and regular season tournaments.
        :return:
                    A list of tournaments dictionaries.
        """
        # We need to cast is_playoffs as an integer for the cargoquery
        if is_playoffs is not None:
            is_playoffs = 1 if is_playoffs else 0

        # This generated the WHERE part of the cargoquery
        where_string = ''.join([" AND Tournaments.{}='{}'".format(field_name, value) for field_name, value in
                                [('Region', region),
                                 ('Year', year),
                                 ('TournamentLevel', tournament_level),
                                 ('IsPlayoffs', is_playoffs)] if value is not None])[5:]  # Cutting the leading AND

        return self._cargoquery(tables='Tournaments',
                                fields='Name = name, '
                                       'DateStart = date_start, '
                                       'Date = date_end, '
                                       'Region = region, '
                                       'League = league, '
                                       'Rulebook = rulebook, '
                                       'TournamentLevel = tournament_level, '
                                       'IsQualifier = is_qualifier, '
                                       'IsPlayoffs = is_playoffs, '
                                       'IsOfficial = is_official, '
                                       'OverviewPage = overview_page',
                                order_by="Tournaments.Date",
                                where=where_string,
                                **kwargs)

    def get_games(self, tournament_name=None, get_players=False, **kwargs) -> List[dict]:
        """
        Returns the list of games played in a tournament.
        Notable keys include 'leaguepedia_game_id', 'winner', 'date_time_utc', 'match_history_url', 'vod_url'.

        :param tournament_name
                    Name of the tournament, which can be gotten from get_tournaments().
        :param get_players
                    Also attaches a dictionary with player objects to every game.
        :return:
                    A list of game dictionaries.
        """
        games = self._cargoquery(tables='ScoreboardGame',
                                 fields='Tournament = tournament, '
                                        'Team1 = team1, '
                                        'Team2 = team2, '
                                        'Winner = winner, '
                                        'DateTime_UTC = date_time_utc, '
                                        'DST = dst, '
                                        'Team1Score = team1_match_score, '
                                        'Team2Score = team2_match_score, '
                                        'Team1Bans = team1_bans, '
                                        'Team2Bans = team2_bans, '
                                        'Team1Picks = team1_picks, '
                                        'Team2Picks = team2_picks, '
                                        'Team1Names = team1_names, '
                                        'Team2Names = team2_names, '
                                        'Team1Links = team1_links, '
                                        'Team2Links = team2_links, '
                                        'Team1Dragons = team1_dragons, '
                                        'Team2Dragons = team2_dragons, '
                                        'Team1Barons = team1_barons, '
                                        'Team2Barons = team2_barons, '
                                        'Team1Towers = team1_towers, '
                                        'Team2Towers = team2_towers, '
                                        'Team1Gold = team1_gold, '
                                        'Team2Gold = team2_gold, '
                                        'Team1Kills = team1_kills, '
                                        'Team2Kills = team2_kills, '
                                        'Team1RiftHeralds = team1_rift_heralds, '
                                        'Team2RiftHeralds = team2_rift_heralds, '
                                        'Team1Inhibitors = team1_inhibitors, '
                                        'Team2Inhibitors = team2_inhibitors, '
                                        'Patch = patch, '
                                        'MatchHistory = match_history_url, '
                                        'VOD = vod_url, '
                                        'Gamename = game_in_match, '
                                        'OverviewPage = overview_page, '
                                        'ScoreboardID_Wiki = leaguepedia_game_id, ',
                                 where="ScoreboardGame.Tournament='{}'".format(tournament_name),
                                 order_by="ScoreboardGame.DateTime_UTC",
                                 **kwargs)

        if get_players:
            for game in games:
                game['players'] = self.get_players(game['team1_links'].split(',') + game['team2_links'].split(','))

        return games

    def get_picks_bans(self, game, **kwargs) -> dict:
        """
        Returns the picks and bans for a game.

        Only issues a query if picks and bans for the tournament have not been loaded yet.

        :param game
                    Game dictionary, coming from get_games()
        :return:
                    The picks and bans dictionary, matched on ScoreboardGame/ScoreboardID_Wiki and PicksAndBansS7/GameID_Wiki
        """
        overview_page = game['overview_page']
        if overview_page not in self.picks_bans_cache:
            self._load_tournament_picks_bans(overview_page, **kwargs)

        try:
            return self.picks_bans_cache[overview_page][game['leaguepedia_game_id']]
        except KeyError:
            return self._get_picks_bans_through_champions(game)

    def get_team_logo(self, team_name: str, retry=True) -> str:
        """
        Returns the URL with the team’s logo.

        :param team_name
                    Team name, usually gotten from the game dictionary.
        :param retry
                    If True, the function will try to use get_long_team_name if the name isn’t understood.
        :return:
                    URL pointing to the team’s logo
        """
        result = self.client.api(action='query',
                                 format='json',
                                 prop='imageinfo',
                                 titles=u'File:{}logo square.png'.format(team_name),
                                 iiprop='url')

        try:
            url = None
            pages = result.get('query').get('pages')
            for k, v in pages.items():
                url = v.get('imageinfo')[0].get('url')
        except (TypeError, AttributeError):
            # This happens when the team name was not properly understood.
            if river_mwclient_loaded and retry:
                return self.get_team_logo(self.get_long_team_name(team_name), False)
            else:
                raise Exception('Logo not found for the given team name')
        return url

    def get_long_team_name(self, team_abbreviation: str) -> str:
        """
        Returns the long team name for the given team abbreviation, using Leaguepedia’s search pages.

        Only issues a query the first time it is called, then stores the data in its cache.

        :param team_abbreviation:
                    A team name abbreviation, like IG or RNG
        :return:
                    The long team name, like "Invictus Gaming", "Royal Never Give Up", ...
        """
        if not river_mwclient_loaded:
            raise Exception('This features requires river_mwclient')
        return self.cache.get('Team', team_abbreviation, 'long')

    def get_player(self, player_link, **kwargs) -> dict:
        """
        Returns the Player object from a player link. Returns None if the player doesn't have a page.

        :param player_link: a player link , coming from ScoreboardGame.TeamXLinks or ScoreboardPlayer.Link for example
        :return: the player object representing its current information (including current player name)
        """
        try:
            return self._cargoquery(tables='Players, PlayerRedirects',
                                    join_on="Players._pageName = PlayerRedirects.OverviewPage",
                                    fields="Players.ID = game_name, "
                                           "Players.Image = image,"
                                           "Players.NameFull = real_name, "
                                           "Players.Birthdate  = birthday, "
                                           "Players.Team = team, "
                                           "Players.Role = role, "
                                           "Players.SoloqueueIds = account_names, "
                                           "Players.Stream = stream, "
                                           "Players.Twitter = twitter, "
                                           "Players._pageName = page_name",
                                    where="PlayerRedirects.AllName = '{}'".format(player_link),
                                    **kwargs)[0]
        except IndexError:
            return {}

    def get_players(self, player_links, **kwargs) -> dict:
        """
        Returns the Player object from a list of player links.

        :param player_links: a list of player links, coming from ScoreboardGame.TeamXLinks most likely
        :return: a dict of player objects representing their current information with their link as the key
        """
        results_dict = {}
        for link in player_links:
            if link in self.players_cache and \
                    self.players_cache[link]['updated_at'] > datetime.datetime.now() - datetime.timedelta(hours=1):
                results_dict[link] = self.players_cache[link]

        missing_links = [link for link in player_links if link not in results_dict]
        if not missing_links:
            return results_dict

        new_players = {link: self.get_player(link) for link in missing_links}

        # TODO Find a way to make a single query while using the proper links
        # new_players = {p['link']: p for p in self._cargoquery(tables='Players, PlayerRedirects',
        #                                                       join_on="Players._pageName = PlayerRedirects.OverviewPage",
        #                                                       fields="PlayerRedirects.AllName = link, "
        #                                                              "Players.ID = game_name, "
        #                                                              "Players.Image = image,"
        #                                                              "Players.NameFull = real_name, "
        #                                                              "Players.Birthdate  = birthday, "
        #                                                              "Players.Team = team, "
        #                                                              "Players.Role = role, "
        #                                                              "Players.SoloqueueIds = account_names, "
        #                                                              "Players.Stream = stream, "
        #                                                              "Players.Twitter = twitter, "
        #                                                              "Players._pageName = page_name",
        #                                                       where="PlayerRedirects.AllName = '" +
        #                                                             "' OR PlayerRedirects.AllName = '".join(
        #                                                                 missing_links) +
        #                                                             "'",
        #                                                       **kwargs)}

        for p in new_players:
            # Necessary to handle None objects from get_player.
            new_players[p]['updated_at'] = datetime.datetime.now()
            results_dict[p] = new_players[p]

        self.players_cache.update(new_players)

        return results_dict

    def _load_tournament_picks_bans(self, overview_page, **kwargs):
        self.picks_bans_cache[overview_page] = \
            {pb['leaguepedia_game_id']: pb for pb in
             self._cargoquery(tables='PicksAndBansS7',
                              fields='Team1Role1 = team1_role1, '
                                     'Team1Role2 = team1_role2, '
                                     'Team1Role3 = team1_role3, '
                                     'Team1Role4 = team1_role4, '
                                     'Team1Role5 = team1_role5, '
                                     'Team2Role1 = team2_role1, '
                                     'Team2Role2 = team2_role2, '
                                     'Team2Role3 = team2_role3, '
                                     'Team2Role4 = team2_role4, '
                                     'Team2Role5 = team2_role5, '
                                     'Team1Ban1 = team1_ban1, '
                                     'Team1Ban2 = team1_ban2, '
                                     'Team1Ban3 = team1_ban3, '
                                     'Team1Ban4 = team1_ban4, '
                                     'Team1Ban5 = team1_ban5, '
                                     'Team1Pick1 = team1_pick1, '
                                     'Team1Pick2 = team1_pick2, '
                                     'Team1Pick3 = team1_pick3, '
                                     'Team1Pick4 = team1_pick4, '
                                     'Team1Pick5 = team1_pick5, '
                                     'Team2Ban1 = team2_ban1, '
                                     'Team2Ban2 = team2_ban2, '
                                     'Team2Ban3 = team2_ban3, '
                                     'Team2Ban4 = team2_ban4, '
                                     'Team2Ban5 = team2_ban5, '
                                     'Team2Pick1 = team2_pick1, '
                                     'Team2Pick2 = team2_pick2, '
                                     'Team2Pick3 = team2_pick3, '
                                     'Team2Pick4 = team2_pick4, '
                                     'Team2Pick5 = team2_pick5, '
                                     'Team1 = team1, '
                                     'Team2 = team2, '
                                     'Winner = winner, '
                                     'Team1Score = team1_score, '
                                     'Team2Score = team2_score, '
                                     'OverviewPage = overview_page, '
                                     'Phase = phase, '
                                     'UniqueLine = unique_line, '
                                     'Tab = tab, '
                                     'N_Page = n__page, '
                                     'N_TabInPage = n__tab_in_page, '
                                     'N_MatchInPage = n__match_in_page, '
                                     'N_GameInPage = n__game_in_page, '
                                     'N_GameInMatch = n__game_in_match, '
                                     'N_MatchInTab = n__match_in_tab, '
                                     'N_GameInTab = n__game_in_tab, '
                                     'GameID_Wiki = leaguepedia_game_id',
                              where='OverviewPage="{}"'.format(overview_page),
                              **kwargs)}

    def _get_picks_bans_through_champions(self, game):
        game_pb_list = [sorted(
            ['None' if (x == '' or 'Loss' in x) else x
             for x in game['team{}_{}'.format(team_id, pick_or_ban)].split(',')])
            for team_id in [1, 2]
            for pick_or_ban in ['picks', 'bans']]

        # We simply look at all picks and bans and see if there was one with the same 20 champions and team names
        matched_pb = []
        for possible_pb in self.picks_bans_cache[game['overview_page']].values():
            if not game['team1'] == possible_pb['team1'] and game['team2'] == possible_pb['team2']:
                continue
            possible_pb_list = [(sorted([
                possible_pb.get('team{}_{}{}'.format(team_id, pick_or_ban, player_id))
                for player_id in range(1, 6)]))
                for team_id in [1, 2]
                for pick_or_ban in ['pick', 'ban']]
            if possible_pb_list == game_pb_list:
                matched_pb.append(possible_pb)

        # Raising an IndexError if no picks and bans were found
        if matched_pb.__len__() == 1:
            return matched_pb[0]
        else:
            raise Exception('Picks and bans could not be found for game {}'.format(game['leaguepedia_game_id']))

##
