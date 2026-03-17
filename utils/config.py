from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
BASE_BDOC = Path(r'C:\Users\FL4K\PETROBRAS\G&E TERM UTE-CBT - 4. BANCO_AUTOMATIZADO\automacao_encerramento_comercial_om')

DATA_DIR = BASE_DIR / 'dados' #pasta dados
DATA_DB_DIR = DATA_DIR / 'db'
DATA_INPUT_DIR = DATA_DIR / 'input'
DATA_PROCESS_DIR = DATA_DIR / 'process'

print(BASE_DIR)