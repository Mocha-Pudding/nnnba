import nba
from nba import *
import basketballCrawler as bc
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import json
from logger import *

def start(parallel=True, measure_type="Advanced"):
    pool = ThreadPool(4)
    
    def process_to_raw_data(bballref_players, player_stat_info):
        nba_player = NBA_player(player_stat_info[0], player_stat_info[1], player_stat_info[2])
        logger.debug(nba_player.name)
        nba_player = nba.manualFix(nba_player)
        if measure_type == "Advanced":
            nba_player.getPlayerAdvStats()
        elif measure_type == "Basic":
            nba_player.getPlayerStats()
        nba_player.setSalaries(bballref_players[nba_player.name].salaries)
        return nba_player.summarize()
    
    print ("Start")
    print ("nbastats = nba.getAllPlayers()")
    nbastats = nba.getAllPlayers()
    print ("bballref_players = bc.loadPlayerDictionary('crawled_data/players.json')")
    bballref_players = bc.loadPlayerDictionary('crawled_data/players.json')
    
    print ("process to raw data")
    raw_data = []
    if parallel:
        func = partial(process_to_raw_data, bballref_players)
        raw_data = pool.map(func, nbastats)
    else:
        for player_stat_info in nbastats:
            raw_data.append(process_to_raw_data(bballref_players, player_stat_info))
            
    with open("crawled_data/raw_data.json", "w") as outfile:
        json.dump(raw_data, outfile)

if __name__ == "__main__":
    start()
