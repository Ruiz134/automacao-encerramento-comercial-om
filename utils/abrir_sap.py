import win32com.client
import subprocess
import time
import pythoncom

class SapAutomation:
    def __init__(self, nome_conexao='02 PEP - SAP S/4HANA Produção (SAP SCRIPT)'):
        self.nome_conexao = nome_conexao
        self.sap_gui_auto = None
        self.application = None
        self.connection = None
        self.session = None

    def conectar(self):
        """
        Tenta conectar em uma sessão existente ou abre o SAP do zero.
        """
        try:
            pythoncom.CoInitialize()
            
            # 1. Tenta capturar o Scripting Engine (SAPGUI deve estar aberto)
            try:
                self.sap_gui_auto = win32com.client.GetObject("SAPGUI")
                self.application = self.sap_gui_auto.GetScriptingEngine
            except Exception:
                print("SAP Logon não encontrado. Iniciando executável...")
                self._abrir_executavel_sap()
                self.sap_gui_auto = win32com.client.GetObject("SAPGUI")
                self.application = self.sap_gui_auto.GetScriptingEngine

            # 2. Verifica se já existe uma sessão aberta no ambiente correto
            if self.application.Connections.Count > 0:
                for conn in self.application.Connections:
                    for sess in conn.Sessions:
                        # Verifica se o nome do sistema ou descrição bate
                        if self.nome_conexao in conn.Description or self.nome_conexao in sess.Info.SystemName:
                            print(f"Sessão ativa encontrada em: {conn.Description}")
                            self.session = sess
                            return self.session

            # 3. Se não encontrou sessão aberta, abre uma nova conexão
            print(f"Abrindo nova conexão: {self.nome_conexao}")
            self.connection = self.application.OpenConnection(self.nome_conexao, True)
            time.sleep(3) # Tempo para o SAP autenticar e carregar a GUI
            
            self.session = self.connection.Children(0)
            
            # Limpa o campo de transação para garantir que estamos na tela inicial
            self.session.findById("wnd[0]/tbar[0]/okcd").text = "/n"
            self.session.findById("wnd[0]").sendVKey(0)
            
            return self.session

        except Exception as e:
            print(f"Erro crítico ao conectar ao SAP: {e}")
            return None

    def _abrir_executavel_sap(self):
        """Abre o saplogon.exe caso esteja fechado."""
        sap_path = r"C:\Program Files\SAP\FrontEnd\SAPGUI\saplogon.exe"
        subprocess.Popen(sap_path)
        time.sleep(6) # Aguarda o processo carregar completamente

    def executar_transacao(self, transacao):
        """Exemplo de método para usar a sessão"""
        if self.session:
            self.session.findById("wnd[0]/tbar[0]/okcd").text = f"/n{transacao}"
            self.session.findById("wnd[0]").sendVKey(0)
            print(f"Transação {transacao} iniciada.")

# --- EXEMPLO DE USO NO MAIN ---
if __name__ == "__main__":
    # Instancia a classe
    sap = SapAutomation(nome_conexao='02 PEP - SAP S/4HANA Produção (SAP SCRIPT)')
    
    # Conecta
    sessao = sap.conectar()
    
    if sessao:
        print("Sucesso! O script agora pode interagir com o SAP.")
        # Exemplo: Acessar a transação SE16N
        sap.executar_transacao("SE16N")
    else:
        print("Não foi possível estabelecer conexão.")