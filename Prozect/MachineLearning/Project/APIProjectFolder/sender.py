import sqlite3
import pandas as pd

df = pd.read_csv('./produits_fcfa_expiration(2).csv')

Connection = sqlite3.connect('db.sqlite3')

df.to_sql('Prediction_task', Connection, if_exists='replace')
Connection.close()