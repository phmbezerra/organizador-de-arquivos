from pathlib import Path
from shutil import move
from datetime import datetime

EXTENSOES = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Documentos": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Planilhas": [".csv", ".xls", ".xlsx"],
    "Compactados": [".zip", ".rar", ".7z"],
    "Codigos": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    "Audios": [".mp3", ".wav", ".ogg"],
    "Videos": [".mp4", ".mkv", ".avi"],
}


def identificar_categoria(extensao: str) -> str:
    for categoria, lista_extensoes in EXTENSOES.items():
        if extensao.lower() in lista_extensoes:
            return categoria
    return "Outros"


def organizar_pasta(caminho_pasta: str) -> None:
    pasta = Path(caminho_pasta)

    if not pasta.exists() or not pasta.is_dir():
        print("Pasta inválida. Verifique o caminho informado.")
        return

    movimentados = []

    for arquivo in pasta.iterdir():
        if arquivo.is_file():
            categoria = identificar_categoria(arquivo.suffix)
            destino = pasta / categoria
            destino.mkdir(exist_ok=True)

            novo_caminho = destino / arquivo.name

            contador = 1
            while novo_caminho.exists():
                novo_nome = f"{arquivo.stem}_{contador}{arquivo.suffix}"
                novo_caminho = destino / novo_nome
                contador += 1

            move(str(arquivo), str(novo_caminho))
            movimentados.append((arquivo.name, categoria, novo_caminho.name))

    gerar_relatorio(pasta, movimentados)
    print("Organização concluída com sucesso.")



def gerar_relatorio(pasta: Path, movimentados: list[tuple[str, str, str]]) -> None:
    relatorio = pasta / "relatorio_organizacao.txt"
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with relatorio.open("w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE ORGANIZAÇÃO DE ARQUIVOS\n")
        arquivo.write(f"Data: {agora}\n")
        arquivo.write("=" * 45 + "\n\n")

        if not movimentados:
            arquivo.write("Nenhum arquivo foi movido.\n")
            return

        for nome_original, categoria, nome_final in movimentados:
            arquivo.write(
                f"Arquivo: {nome_original} | Categoria: {categoria} | Destino: {nome_final}\n"
            )

        arquivo.write(f"\nTotal de arquivos organizados: {len(movimentados)}\n")


if __name__ == "__main__":
    caminho = input("Digite o caminho da pasta que deseja organizar: ").strip()
    organizar_pasta(caminho)
