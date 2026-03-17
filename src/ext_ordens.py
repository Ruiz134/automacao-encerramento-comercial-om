import pandas as pd
import psutil

def fechar_excel_instancia():

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and 'EXCEL' in proc.info['name'].upper():
            try:
                proc.terminate()
            except:
                pass

def _status_text(session) -> str:
    try:
        return session.findById("wnd[0]/sbar").Text.strip()
    except Exception:
        return ""

def extract_ordens(session, tcode: str,  variante = "SAP_RUIZ_IW38", output = str, filename = "relat_ordens")-> pd.Dataframe:
    
    
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
