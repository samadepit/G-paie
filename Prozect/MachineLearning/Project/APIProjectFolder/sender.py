import sqlite3
import pandas as pd

<<<<<<< HEAD
df = pd.read_csv('Prozect/MachineLearning/Project/APIProjectFolder/produits_fcfa_expiration(2).csv')
=======
df = pd.read_csv('./produits_fcfa_expiration(2).csv')
>>>>>>> cad91402d12568c602dff85174b15f648bd70fa5

Connection = sqlite3.connect('db.sqlite3')

df.to_sql('Prediction_task', Connection, if_exists='replace')
Connection.close()