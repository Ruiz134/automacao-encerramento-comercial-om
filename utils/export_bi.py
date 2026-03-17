import pandas as pd
import utils.config as cfg
import utils.db as db 


def exportar_para_sharepoint():
    conn = db.connect()

    pasta_bi = cfg.BASE_BDOC.resolve()
    pasta_bi.mkdir(parents=True, exist_ok=True)

    tabelas = [
        "relatorio_notas",
        "log_ordens_consolidado",
        "log_spool_consolidado",
        "extracoes"
    ]

    for tabela in tabelas:
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)

        caminho = pasta_bi / f"{tabela}.csv"
        df.to_csv(caminho, index=False, sep=";", encoding="utf-8-sig")

        print(f"[OK] Exportado: {caminho.name}")

    conn.close()