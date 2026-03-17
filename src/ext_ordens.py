import pandas as pd
from pathlib import Path
import time
   
def transformação_excel(filename, input_output):

    BASE = Path(input_output) / filename

    time.sleep(2)

    df = pd.read_excel(BASE, skiprows=1)
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')
    df = df.reset_index(drop=True)
    df.columns = df.columns.str.strip()
    df['Ordem'] = pd.to_numeric(df['Ordem'], errors='coerce')

    df['Ordem'] = df['Ordem'].astype(int)

    df.to_excel(BASE, index=False)

    print(f"Transformação concluída: {filename}")

def extract_ordens(session, tcode: str,  variante = "SAP_RUIZ_IW38", output = str, filename = "relat_ordens"):
    
    
    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/tbar[0]/okcd").text = f"/n{tcode}"
    session.findById("wnd[0]").sendVKey (0)


    session.findById("wnd[0]/tbar[1]/btn[17]").press()
    session.findById("wnd[1]/usr/txtV-LOW").text = variante
    session.findById("wnd[1]/usr/txtV-LOW").caretPosition = 13
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]/tbar[1]/btn[8]").press()

    session.findById("wnd[0]/mbar/menu[0]/menu[10]/menu[2]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()

    session.findById("wnd[1]/usr/ctxtDY_PATH").text = output
    session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = filename

    session.findById("wnd[1]/usr/ctxtDY_FILE_ENCODING").setFocus()
    session.findById("wnd[1]/usr/ctxtDY_FILE_ENCODING").caretPosition = (0)
    session.findById("wnd[1]/tbar[0]/btn[0]").press()

    print(f"Extração concluída: {filename}")

    transformação_excel(filename, output)

