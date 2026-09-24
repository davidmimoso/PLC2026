#!/usr/bin/env python3
"""
Atualiza a secção "## Autor" em todos os README.md das pastas TP1..TP8
(ou nas pastas que indicares em TP_DIRS), substituindo pelo bloco fixo
definido em AUTOR_BLOCK.

Como usar:
1. Corre este script a partir da RAIZ do repositório clonado
   (a pasta que tem as subpastas TP1, TP2, ...).
2. Ajusta AUTOR_BLOCK e TP_DIRS abaixo, se precisares.
3. python3 atualizar_autor.py
   -> por omissão faz sempre um "dry run" (só mostra o que ia mudar).
4. Quando estiveres confiante, corre:
   python3 atualizar_autor.py --write
   -> aí sim grava as alterações nos ficheiros.
"""

import re
import sys
from pathlib import Path

# ---- AJUSTA AQUI ----
AUTOR_BLOCK = """## Autor
- Nome: David Mimoso
- Número: a111115
- Foto: <img src="foto.jpg" width="150">

"""

TP_DIRS = [f"TP{i}" for i in range(1, 9)]  # TP1 .. TP8
# ----------------------

# Apanha da linha "## Autor" até à próxima linha que comece por "## "
# (ou até ao fim do ficheiro, se não houver mais secções).
SECTION_RE = re.compile(
    r"^## Autor\s*\n(?:(?!^## ).*\n?)*",
    re.MULTILINE,
)


BOMS = {
    b"\xff\xfe": "utf-16-le",
    b"\xfe\xff": "utf-16-be",
    b"\xef\xbb\xbf": "utf-8",
}


def split_bom(raw: bytes):
    """Devolve (bom_bytes, encoding, texto_sem_bom)."""
    for bom, enc in BOMS.items():
        if raw.startswith(bom):
            return bom, enc, raw[len(bom):].decode(enc)
    return b"", "utf-8", raw.decode("utf-8")


def insert_after_title(text: str) -> str:
    """
    Insere o AUTOR_BLOCK logo a seguir à primeira linha (assumida como o
    título, ex: '# Nome do trabalho'). Se não houver título reconhecível,
    insere no topo do ficheiro.
    """
    lines = text.splitlines(keepends=True)
    if lines and lines[0].lstrip().startswith("# "):
        # salta o título e uma eventual linha em branco a seguir
        idx = 1
        if idx < len(lines) and lines[idx].strip() == "":
            idx += 1
        return "".join(lines[:idx]) + "\n" + AUTOR_BLOCK + "".join(lines[idx:])
    else:
        return AUTOR_BLOCK + "\n" + text


def process_file(path: Path, write: bool) -> str:
    raw = path.read_bytes()
    bom, encoding, text = split_bom(raw)

    has_autor = re.search(r"^## Autor\b", text, re.MULTILINE)

    if not has_autor:
        new_text = insert_after_title(text)
        action = "inserida (secção não existia)"
    else:
        new_text, n = SECTION_RE.subn(AUTOR_BLOCK, text, count=1)
        if n == 0:
            return f"[AVISO] não consegui isolar a secção Autor em {path} — verifica manualmente."
        action = "substituída"

    if new_text == text:
        return f"[OK] {path} já estava atualizado."

    if write:
        path.write_bytes(bom + new_text.encode(encoding))
        return f"[ESCRITO] {path} — secção {action} (codificação: {encoding})."
    else:
        return f"[DRY-RUN] {path} — secção seria {action} (usa --write para gravar)."


def main():
    write = "--write" in sys.argv
    root = Path(".").resolve()

    results = []
    for tp in TP_DIRS:
        readme = root / tp / "README.md"
        if not readme.exists():
            results.append(f"[AVISO] {readme} não existe — ignorado.")
            continue
        results.append(process_file(readme, write))

    print("\n".join(results))
    if not write:
        print("\n--- Nenhum ficheiro foi alterado (modo dry-run). ---")
        print("Confirma o output acima e corre com --write para gravar de facto.")


if __name__ == "__main__":
    main()
