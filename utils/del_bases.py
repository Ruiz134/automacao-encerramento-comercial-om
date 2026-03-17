from pathlib import Path
import shutil

def limpar_bases(lista_diretorios):
    for caminho in lista_diretorios:
        target_dir = Path(caminho)

        if not target_dir.exists() or not target_dir.is_dir():
            print(f"[ABORTADO] '{caminho}' não encontrado ou não é pasta.")
            continue

        print(f"[DELETANDO] {target_dir} ...")

        # 1. Remove recursivamente todos os .xlsx
        for arquivo in target_dir.rglob("*.xlsx"):
            try:
                arquivo.unlink()
                print(f"\r\033[K[DELETANDO_ARQUIVOS] {arquivo.name}", end="", flush=True)

            except Exception as e:
            
                print(f"\r\033[K[ERRO] Erro ao deletar {arquivo.name}: {e}")


        for item in target_dir.iterdir():
            if item.is_dir():
                try:
                    shutil.rmtree(item)
                    print(f"\r\033[K[DELETANDO_SUBPASTAS] Subpasta removida: {item.name}", end="", flush=True)
                except Exception as e:
                    print(f"\r\033[K[ERRO] Erro ao remover pasta {item.name}: {e}")