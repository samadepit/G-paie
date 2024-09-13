import sqlite3
import pandas as pd

df = pd.read_csv('data.csv')

Connection = sqlite3.connect('db.sqlite3')

df.to_sql('testing_projet', Connection, if_exists='replace')
Connection.close()
