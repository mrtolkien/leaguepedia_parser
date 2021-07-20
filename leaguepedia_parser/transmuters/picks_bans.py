from typing import List
from lol_dto.classes.game.lol_game import LolPickBan
import lol_id_tools as lit

from leaguepedia_parser.transmuters.field_names import picks_bans_fields


def transmute_picks_bans(input_dict) -> List[LolPickBan]:
    pb_list = []

    for field in picks_bans_fields:
        pb_list.append(
            LolPickBan(
                championId=lit.get_id(input_dict[field], object_type="champion"),
                isBan="Ban" in field,
                team="BLUE" if "Team1" in field else "RED",
            )
        )

    return pb_list
