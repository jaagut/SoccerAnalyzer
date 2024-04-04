import json
import pandas as pd

from socceranalyzer import MatchAnalyzer, Match, HLKid, Logger, JupyterAdapter


# LOGFILE_PATH = "https://data.bit-bots.de/HLVS/2023/GAME_K-GD1-1_2023-03-17-07_itandroids_bitbots/public_logs/data_collection/referee_data_collection_COMPLETE_2023-03-17T11-12-33.feather"
LOGFILE_PATH = "/home/jan/mafiasi-cloud/UHH/BA/data/pre-analysis/HLVS/2022_23/K-GD2/K-GD2-1/referee_data_collection_COMPLETE_2023-04-01T16-03-28.feather"
META_DATA_PATH = "/home/jan/mafiasi-cloud/UHH/BA/data/pre-analysis/HLVS/2022_23/K-GD2/K-GD2-1/referee_data_collection_COMPLETE_2023-04-01T16-03-28.json"

dataframe = pd.read_feather(LOGFILE_PATH)
meta_data = json.load(open(META_DATA_PATH))

match_object = Match(dataframe, HLKid, meta_data)
field = match_object.field
match_analyzer = MatchAnalyzer(match_object)
jupyter = JupyterAdapter(match_analyzer)
