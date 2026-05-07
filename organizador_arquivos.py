from __future__ import annotations

import json
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from shutil import move
from tkinter import filedialog, messagebox, ttk
from typing import Iterable


EXTENSOES: dict[str, list[str]] = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"],
    "Documentos": [".pdf", ".docx", ".txt", ".pptx", ".doc"],
    "Planilhas": [".csv", ".xls", ".xlsx"],
    "Compactados": [".zip", ".rar", ".7z"],
    "Codigos": [".py", ".js", ".html", ".css", ".java", ".cpp", ".json"],
    "Audios": [".mp3", ".wav", ".ogg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
}

ARQUIVO_HISTORICO = ".historico_organizacao.json"


@dataclass
class MovimentoArquivo:
    nome_original: str
    nome_final: str
    categoria: str
    extensao: str
    origem: str
    destino: str
    horario: str


def identificar_categoria(extensao: str) -> str:
    extensao = extensao.lower()
    for categoria, lista_extensoes in EXTENSOES.items():
        if extensao in lista_extensoes:
            return categoria
    return "Outros"


def gerar_nome_disponivel(destino: Path) -> Path:
    if not destino.exists():
        return destino

    contador = 1
    while True:
        novo_nome = f"{destino.stem}_{contador}{destino.suffix}"
        novo_destino = destino.with_name(novo_nome)
        if not novo_destino.exists():
            return novo_destino
        contador += 1


def salvar_historico(pasta: Path, movimentos: list[MovimentoArquivo]) -> Path:
    historico_path = pasta / ARQUIVO_HISTORICO

    if historico_path.exists():
        try:
            historico_atual = json.loads(historico_path.read_text(encoding="utf-8"))
            if not isinstance(historico_atual, list):
                historico_atual = []
        except json.JSONDecodeError:
            historico_atual = []
    else:
        historico_atual = []

    registro = {
        "data_execucao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total_arquivos": len(movimentos),
        "movimentos": [mov.__dict__ for mov in movimentos],
    }

    historico_atual.append(registro)
    historico_path.write_text(
        json.dumps(historico_atual, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return historico_path


def gerar_relatorio_detalhado(
    pasta: Path,
    movimentos: list[MovimentoArquivo],
    categorias_filtradas: Iterable[str],
) -> Path:
    relatorio = pasta / "relatorio_organizacao.txt"
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    categorias_texto = ", ".join(categorias_filtradas) if categorias_filtradas else "Todas"

    resumo_por_categoria: dict[str, int] = {}
    for mov in movimentos:
        resumo_por_categoria[mov.categoria] = resumo_por_categoria.get(mov.categoria, 0) + 1

    with relatorio.open("w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DETALHADO DE ORGANIZAÇÃO DE ARQUIVOS\n")
        arquivo.write(f"Data da execução: {agora}\n")
        arquivo.write(f"Pasta analisada: {pasta}\n")
        arquivo.write(f"Categorias selecionadas: {categorias_texto}\n")
        arquivo.write("=" * 72 + "\n\n")

        if not movimentos:
            arquivo.write("Nenhum arquivo foi movido nesta execução.\n")
            return relatorio

        arquivo.write("RESUMO POR CATEGORIA\n")
        arquivo.write("-" * 72 + "\n")
        for categoria, total in sorted(resumo_por_categoria.items()):
            arquivo.write(f"{categoria}: {total} arquivo(s)\n")

        arquivo.write("\nDETALHAMENTO DOS ARQUIVOS MOVIDOS\n")
        arquivo.write("-" * 72 + "\n")
        for mov in movimentos:
            arquivo.write(f"Nome original : {mov.nome_original}\n")
            arquivo.write(f"Nome final    : {mov.nome_final}\n")
            arquivo.write(f"Categoria     : {mov.categoria}\n")
            arquivo.write(f"Extensão      : {mov.extensao or '[sem extensão]'}\n")
            arquivo.write(f"Origem        : {mov.origem}\n")
            arquivo.write(f"Destino       : {mov.destino}\n")
            arquivo.write(f"Horário       : {mov.horario}\n")
            arquivo.write("-" * 72 + "\n")

        arquivo.write(f"\nTotal de arquivos organizados: {len(movimentos)}\n")

    return relatorio


def organizar_pasta(
    caminho_pasta: str,
    categorias_permitidas: set[str] | None = None,
) -> tuple[list[MovimentoArquivo], Path, Path]:
    pasta = Path(caminho_pasta)

    if not pasta.exists() or not pasta.is_dir():
        raise FileNotFoundError("A pasta informada não existe ou não é válida.")

    movimentos: list[MovimentoArquivo] = []

    for arquivo in pasta.iterdir():
        if not arquivo.is_file():
            continue

        if arquivo.name in {"relatorio_organizacao.txt", ARQUIVO_HISTORICO}:
            continue

        categoria = identificar_categoria(arquivo.suffix)

        if categorias_permitidas and categoria not in categorias_permitidas:
            continue

        destino_dir = pasta / categoria
        destino_dir.mkdir(exist_ok=True)

        destino_final = gerar_nome_disponivel(destino_dir / arquivo.name)
        move(str(arquivo), str(destino_final))

        movimentos.append(
            MovimentoArquivo(
                nome_original=arquivo.name,
                nome_final=destino_final.name,
                categoria=categoria,
                extensao=arquivo.suffix.lower(),
                origem=str(arquivo),
                destino=str(destino_final),
                horario=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            )
        )

    relatorio = gerar_relatorio_detalhado(
        pasta=pasta,
        movimentos=movimentos,
        categorias_filtradas=categorias_permitidas or set(),
    )
    historico = salvar_historico(pasta, movimentos)

    return movimentos, relatorio, historico


def desfazer_ultima_organizacao(caminho_pasta: str) -> tuple[int, list[str]]:
    pasta = Path(caminho_pasta)
    historico_path = pasta / ARQUIVO_HISTORICO

    if not historico_path.exists():
        raise FileNotFoundError("Nenhum histórico encontrado para desfazer a organização.")

    try:
        historico = json.loads(historico_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("O histórico de organização está corrompido.") from exc

    if not historico:
        raise ValueError("Não há nenhuma execução registrada para desfazer.")

    ultima_execucao = historico[-1]
    movimentos = ultima_execucao.get("movimentos", [])

    restaurados = 0
    erros: list[str] = []

    for mov in reversed(movimentos):
        origem_atual = Path(mov["destino"])
        destino_original = Path(mov["origem"])

        try:
            if not origem_atual.exists():
                erros.append(f"Arquivo não encontrado para restauração: {origem_atual}")
                continue

            destino_original = gerar_nome_disponivel(destino_original)
            move(str(origem_atual), str(destino_original))
            restaurados += 1

            pasta_categoria = origem_atual.parent
            if pasta_categoria.is_dir() and not any(pasta_categoria.iterdir()):
                pasta_categoria.rmdir()

        except Exception as exc:
            erros.append(f"Erro ao restaurar {origem_atual.name}: {exc}")

    historico.pop()
    historico_path.write_text(
        json.dumps(historico, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return restaurados, erros


class OrganizadorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Organizador de Arquivos")
        self.root.geometry("860x700")
        self.root.minsize(760, 620)

        self.caminho_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Selecione uma pasta para começar.")

        self.categorias_vars: dict[str, tk.BooleanVar] = {
            categoria: tk.BooleanVar(value=True)
            for categoria in list(EXTENSOES.keys()) + ["Outros"]
        }

        self._criar_interface()

    def _criar_interface(self) -> None:
        frame_principal = ttk.Frame(self.root, padding=18)
        frame_principal.pack(fill="both", expand=True)

        titulo = ttk.Label(
            frame_principal,
            text="Organizador de Arquivos",
            font=("Segoe UI", 22, "bold"),
        )
        titulo.pack(anchor="w")

        subtitulo = ttk.Label(
            frame_principal,
            text=(
                "Organize arquivos por categoria, gere relatório detalhado e "
                "desfaça a última organização quando necessário."
            ),
            wraplength=760,
        )
        subtitulo.pack(anchor="w", pady=(6, 18))

        frame_pasta = ttk.LabelFrame(frame_principal, text="Pasta de trabalho", padding=14)
        frame_pasta.pack(fill="x", pady=(0, 14))

        ttk.Entry(frame_pasta, textvariable=self.caminho_var).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10),
        )

        ttk.Button(
            frame_pasta,
            text="Escolher pasta",
            command=self.escolher_pasta,
        ).pack(side="left")

        frame_filtros = ttk.LabelFrame(
            frame_principal,
            text="Categorias permitidas na organização",
            padding=14,
        )
        frame_filtros.pack(fill="x", pady=(0, 14))

        grid = ttk.Frame(frame_filtros)
        grid.pack(fill="x")

        categorias_lista = list(self.categorias_vars.items())
        for indice, (categoria, var) in enumerate(categorias_lista):
            check = ttk.Checkbutton(grid, text=categoria, variable=var)
            linha = indice // 3
            coluna = indice % 3
            check.grid(row=linha, column=coluna, sticky="w", padx=8, pady=6)

        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill="x", pady=(0, 14))

        ttk.Button(
            frame_botoes,
            text="Organizar arquivos",
            command=self.executar_organizacao,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            frame_botoes,
            text="Desfazer última organização",
            command=self.executar_desfazer,
        ).pack(side="left")

        ttk.Label(
            frame_principal,
            textvariable=self.status_var,
            foreground="#1f6f4a",
        ).pack(anchor="w", pady=(0, 10))

        frame_log = ttk.LabelFrame(frame_principal, text="Saída do sistema", padding=12)
        frame_log.pack(fill="both", expand=True)

        self.log = tk.Text(
            frame_log,
            wrap="word",
            height=20,
            font=("Consolas", 10),
        )
        self.log.pack(fill="both", expand=True)

        self._adicionar_log("Sistema iniciado com sucesso.\n")

    def _adicionar_log(self, texto: str) -> None:
        self.log.insert("end", texto + "\n")
        self.log.see("end")

    def escolher_pasta(self) -> None:
        pasta = filedialog.askdirectory(title="Selecione a pasta que deseja organizar")
        if pasta:
            self.caminho_var.set(pasta)
            self.status_var.set("Pasta selecionada com sucesso.")
            self._adicionar_log(f"Pasta selecionada: {pasta}")

    def categorias_selecionadas(self) -> set[str]:
        return {
            categoria
            for categoria, var in self.categorias_vars.items()
            if var.get()
        }

    def executar_organizacao(self) -> None:
        caminho = self.caminho_var.get().strip()
        if not caminho:
            messagebox.showwarning("Atenção", "Selecione uma pasta antes de organizar.")
            return

        categorias = self.categorias_selecionadas()
        if not categorias:
            messagebox.showwarning("Atenção", "Selecione pelo menos uma categoria.")
            return

        try:
            movimentos, relatorio, historico = organizar_pasta(caminho, categorias)
            self.status_var.set("Organização concluída com sucesso.")
            self._adicionar_log("=" * 72)
            self._adicionar_log("ORGANIZAÇÃO CONCLUÍDA")
            self._adicionar_log(f"Total de arquivos movidos: {len(movimentos)}")
            self._adicionar_log(f"Relatório gerado em: {relatorio}")
            self._adicionar_log(f"Histórico salvo em: {historico}")

            if movimentos:
                for mov in movimentos:
                    self._adicionar_log(
                        f"- {mov.nome_original} -> {mov.categoria}/{mov.nome_final}"
                    )
            else:
                self._adicionar_log("Nenhum arquivo foi movido nesta execução.")

            messagebox.showinfo(
                "Sucesso",
                f"Organização concluída.\nArquivos movidos: {len(movimentos)}",
            )

        except Exception as exc:
            self.status_var.set("Erro durante a organização.")
            self._adicionar_log(f"ERRO: {exc}")
            messagebox.showerror("Erro", str(exc))

    def executar_desfazer(self) -> None:
        caminho = self.caminho_var.get().strip()
        if not caminho:
            messagebox.showwarning("Atenção", "Selecione uma pasta antes de desfazer.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja desfazer a última organização realizada nesta pasta?",
        )
        if not confirmar:
            return

        try:
            restaurados, erros = desfazer_ultima_organizacao(caminho)
            self.status_var.set("Última organização desfeita com sucesso.")
            self._adicionar_log("=" * 72)
            self._adicionar_log("DESFAZER ORGANIZAÇÃO")
            self._adicionar_log(f"Arquivos restaurados: {restaurados}")

            if erros:
                self._adicionar_log("Ocorreram alguns problemas:")
                for erro in erros:
                    self._adicionar_log(f"- {erro}")

            messagebox.showinfo(
                "Concluído",
                f"Arquivos restaurados: {restaurados}",
            )

        except Exception as exc:
            self.status_var.set("Erro ao desfazer organização.")
            self._adicionar_log(f"ERRO AO DESFAZER: {exc}")
            messagebox.showerror("Erro", str(exc))


def main() -> None:
    root = tk.Tk()
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    app = OrganizadorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
