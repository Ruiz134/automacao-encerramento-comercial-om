#%%
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
BASE_BDOC = Path(r'C:\Users\FL4K\PETROBRAS\G&E TERM UTE-CBT - 4. BANCO_AUTOMATIZADO')

DATA_DIR = BASE_DIR / 'data'
DATA_DIR_SQL = DATA_DIR / 'db'
DATA_RAW_DIR = DATA_DIR / 'raw'
DATA_INTERIM_DIR = DATA_DIR / 'interim'
DATA_PROCESSED_DIR = DATA_DIR / 'processed'

INPUT_RELATORIO_NOTAS_DIR = DATA_RAW_DIR / 'input_nota'
INPUT_SPOOL_DIR = DATA_RAW_DIR / 'input_spool'
OUTPUT_LOG_NOTAS_DIR = DATA_RAW_DIR / 'output_log_nota'
OUTPUT_LOG_ORDENS_DIR = DATA_RAW_DIR / 'output_log_ordem'

CONSOLIDADO_LOG_NOTAS_DIR = DATA_INTERIM_DIR / 'log_notas'
CONSOLIDADO_LOG_ORDENS_DIR = DATA_INTERIM_DIR / 'log_ordens'

print(BASE_DIR)

#%%


