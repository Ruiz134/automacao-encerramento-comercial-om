from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import src.ext_ordens as extracao
import utils.config as cfg
from api import (
    DEFAULT_API_HOST,
    DEFAULT_API_PORT,
    DEFAULT_EXTERNAL_HOST,
    start_api_background,
)
from src.processamento_ordens import processar_ordens_excel
from utils.abrir_sap import SapAutomation
from utils.db import get_db_path

DEFAULT_SAP_CONNECTION = "02 PEP - SAP S/4HANA Produção (SAP SCRIPT)"
DEFAULT_VARIANT = "SAP_RUIZ_IW38"
DEFAULT_EXTRACAO_TCODE = "IW38"
DEFAULT_ENCERRAMENTO_TCODE = "IW32"


@dataclass(slots=True)
class PipelineConfig:
    excel_path: str | None = None
    conexao_sap: str = DEFAULT_SAP_CONNECTION
    variante: str = DEFAULT_VARIANT
    extracao_tcode: str = DEFAULT_EXTRACAO_TCODE
    encerramento_tcode: str = DEFAULT_ENCERRAMENTO_TCODE
    skip_extract: bool = False
    skip_process: bool = False
    api_host: str = DEFAULT_API_HOST
    api_port: int = DEFAULT_API_PORT
    external_host: str = DEFAULT_EXTERNAL_HOST
    start_api: bool = True



def resolve_excel_path(excel_path: str | None) -> Path:
    if not excel_path:
        return (cfg.DATA_INPUT_DIR / extracao.DEFAULT_EXCEL_NAME).resolve()

    caminho = Path(excel_path)
    if caminho.is_absolute():
        return caminho

    return (cfg.BASE_DIR / caminho).resolve()



def conectar_sessao_sap(nome_conexao: str):
    sap = SapAutomation(nome_conexao)
    sessao = sap.conectar()

    if not sessao:
        raise RuntimeError("Nao foi possivel estabelecer conexao com o SAP.")

    return sessao



def garantir_api_background(config: PipelineConfig) -> None:
    if not config.start_api:
        return

    start_api_background(
        host=config.api_host,
        port=config.api_port,
        db_path=get_db_path(),
        external_host=config.external_host,
    )



def run_pipeline(config: PipelineConfig) -> dict[str, int] | None:
    excel_path = resolve_excel_path(config.excel_path)
    excel_path.parent.mkdir(parents=True, exist_ok=True)

    if config.skip_extract and config.skip_process:
        print("Nada a executar no SAP. Garantindo apenas a disponibilidade da API.")
        garantir_api_background(config)
        return None

    sessao = conectar_sessao_sap(config.conexao_sap)

    if not config.skip_extract:
        caminho_extraido = extracao.extract_ordens(
            session=sessao,
            tcode=config.extracao_tcode,
            variante=config.variante,
            output=str(excel_path.parent),
            filename=excel_path.name,
        )
        print(f"Excel de entrada atualizado em: {caminho_extraido}")

    resumo = None
    if not config.skip_process:
        resumo = processar_ordens_excel(
            session=sessao,
            tcode=config.encerramento_tcode,
            excel_path=excel_path,
        )

    garantir_api_background(config)
    print("[PIPELINE] Rodada concluida. API mantida ativa em background para consumo externo.")
    return resumo
