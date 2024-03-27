import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from sklearn.model_selection import train_test_split, GridSearchCV

data = pd.read_csv('data/Players_Avg_Data.csv')
features = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
            'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
            'STL', 'BLK', 'TOV', 'PF']
X = data[features]
y = data['PTS']

lebron_info = players.find_players_by_full_name('LeBron James')[0]
lebron_id = lebron_info['id']

gamelog_lebron = playergamelog.PlayerGameLog(player_id=lebron_id, season='2023')
df_lebron_games = gamelog_lebron.get_data_frames()[0]

X_lebron = df_lebron_games[features].head(10)  
best_params = {'colsample_bytree': 0.3, 'learning_rate': 0.01, 'max_depth': 5, 'alpha': 10, 'n_estimators': 100}
xg_reg = xgb.XGBRegressor(**best_params, objective='reg:squarederror')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xg_reg.fit(X_train, y_train)

y_pred_lebron = xg_reg.predict(X_lebron)

print("勒布朗·詹姆斯的预测得分：", y_pred_lebron)
