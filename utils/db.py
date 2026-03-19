
import sqlite3
import os
import pandas as pd
import config as cfg


os.makedirs(cfg.DATA_DB_DIR, exist_ok=True)
caminho_banco = os.path.join(cfg.DATA_DB_DIR, "db_automacao_ECOM.db")

conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ordens_para_encerrar (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               Ordens TEXT NOT NULL UNIQUE               
)""")

conexao.commit()