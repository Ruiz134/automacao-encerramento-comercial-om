import pythoncom
import win32com.client


class SapGuiError(RuntimeError):
    pass


def conectar_sap():
    """
    Conecta na primeira sessão SAP aberta.

    Requisitos:
    - SAP Logon aberto
    - Sessão SAP logada (ex: SAP Easy Access)
    - SAP GUI Scripting habilitado
    """

    pythoncom.CoInitialize()

    # SAP GUI disponível?
    try:
        sap_gui = win32com.client.GetObject("SAPGUI")
    except Exception as e:
        raise SapGuiError(
            "SAP GUI não encontrado. Abra o SAP Logon e faça login no ambiente."
        ) from e

    # Scripting habilitado?
    try:
        app = sap_gui.GetScriptingEngine
    except Exception as e:
        raise SapGuiError(
            "SAP GUI Scripting não está habilitado."
        ) from e

    # Existe conexão aberta?
    if app.Connections.Count == 0:
        raise SapGuiError(
            "Nenhuma conexão SAP ativa. Entre no ambiente e tente novamente."
        )

    conn = app.Children(0)

    # Existe sessão ativa?
    if conn.Sessions.Count == 0:
        raise SapGuiError(
            "Conectado ao SAP, mas sem sessão aberta."
        )

    session = conn.Children(0)

    # Sessão responde?
    try:
        _ = session.Info.Transaction
    except Exception:
        raise SapGuiError(
            "Sessão SAP não está acessível. Feche e abra o SAP novamente."
        )

    return session