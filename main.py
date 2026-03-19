import src.ext_ordens as exo
import ipykernel 
import openpyxl
import pandas
import psutil
import utils.config as cfg
from utils.abrir_sap import SapAutomation
from pathlib import Path

from utils.sap_session import conectar_sap

if __name__ == '__main__':

    # Abrir Sessão SAP
    sap = SapAutomation("02 PEP - SAP S/4HANA Produção (SAP SCRIPT)")
    sessao = sap.conectar()
    
    if sessao:

        #Extração Ordens para Encerrar
        
        exo.extract_ordens(
            session = conectar_sap(),
            tcode = "IW38",
            variante = "SAP_RUIZ_IW38",
            output= str(cfg.DATA_INPUT_DIR), 
            filename= "ordens_para_encerrar.xlsx"
        )

