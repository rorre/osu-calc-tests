import diff_calc
import requests
import pp_calc
import sys
import b_info
import configparser
import profile_map_calc
from beatmap import Beatmap


def return_values(user, key):

    url = 'https://osu.ppy.sh/api/get_user_best?k={}&u={}&limit=100'.format(key, user)
    js = requests.get(url).json()

    pp_info = []

    number = 0

    for i in js:
        beatmap_id = int(i['beatmap_id'])
        combo = int(i['maxcombo'])
        c100 = int(i['count100'])
        c50 = int(i['count50'])
        miss = int(i['countmiss'])
        mods = int(i['enabled_mods'])
        old_pp = float(i['pp'])

        #try:
        pp_info.append(profile_map_calc.return_values(c100, c50, miss, combo, beatmap_id, mods) + (old_pp,))
        #except Exception as e:
        #    print(e)
        #    pp_info.append(("Error processing this beatmap.",0,0))

    return pp_info