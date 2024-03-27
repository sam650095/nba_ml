import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
import time
def get_team_player_data(team_id, min_games=20):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
    all_players_stats = []
    for _, row in roster.iterrows():
        player_id = row['PLAYER_ID']
        seasons = [str(year) + '-' + str(year+1)[-2:] for year in range(2016, 2021)]
        player_stats = []
        
        for season in seasons:
            gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
            if len(gamelog) >= min_games:
               avg_stats = gamelog.mean(numeric_only=True)
               print(avg_stats)
               avg_stats['GP'] = len(gamelog)  
            #    print(avg_stats)
            #    avg_stats['position'] = gamelog['POSITION'].iloc[0]
            #    avg_stats['PER'] = calculate_per(avg_stats)
            #    avg_stats['USG'] = calculate_usg(avg_stats)
            #    avg_stats['TS'] = calculate_ts(avg_stats)
               player_stats.append(avg_stats)
            time.sleep(0.6)  
            print(player_stats)

        if player_stats:
            player_avg_stats = pd.concat(player_stats, axis=1).mean(axis=1)
            player_avg_stats['TEAM_ID'] = team_id 
            all_players_stats.append(player_avg_stats) 
    # print(all_players_stats)
    if all_players_stats:
        return pd.concat(all_players_stats, axis=1).transpose()
    else:
        return pd.DataFrame()
def calculate_per(player_stats):
    per = (
        (player_stats['PTS'] + player_stats['TRB'] + player_stats['AST'] + player_stats['STL'] + player_stats['BLK'])
        - (player_stats['FGA'] - player_stats['FGM']) - (player_stats['FTA'] - player_stats['FTM']) - player_stats['TOV']
    ) / player_stats['MP']
    return per
def calculate_usg(player_stats):
    usg = (player_stats['FGA'] + 0.44 * player_stats['FTA'] + player_stats['TOV']) / (player_stats['MP'] / 5)
    return usg

def calculate_ts(player_stats):
    ts = player_stats['PTS']/ (2 * (player_stats['FGA'] + 0.44 * player_stats['FTA']))
    return ts

nba_teams = teams.get_teams()
all_teams_stats = []
for team in nba_teams:
    team_id = team['id']
    team_stats = get_team_player_data(team_id)
    all_teams_stats.append(team_stats)
    break  # 如果想處理所有球隊，需要移除此行

complete_data = pd.concat(all_teams_stats, ignore_index=True)

columns_to_drop = ['PLUS_MINUS', 'VIDEO_AVAILABLE']
complete_data = complete_data.drop(columns=columns_to_drop, errors='ignore')

complete_data = complete_data.dropna(how='all', subset=complete_data.columns.difference(['Team', 'TEAM_ID']))

complete_data.to_csv('./data/Players_Avg_Data.csv', index=False)

print(complete_data)
