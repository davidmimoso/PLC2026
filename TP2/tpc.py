import re

def lista(m):
    """Recebe o bloco inteiro de linhas '1. ...' e devolve o <ol> correspondente."""
    itens = re.findall(r"^\d+\.\s+(.*)$", m.group(0), flags=re.M)
    li = "\n".join(f"<li>{i}</li>" for i in itens)
    return f"<ol>\n{li}\n</ol>"
 


def converte(texto):
    texto = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"\*(.*?)\*", r"<i>\1</i>", texto)
    texto = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img src="\2" alt="\1"/>', texto)   
    texto = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', texto)         
    texto = re.sub(r"^#\s+(.*)$", r"<h1>\1</h1>", texto, flags=re.M)
    texto = re.sub(r"^##\s+(.*)$", r"<h2>\1</h2>", texto, flags=re.M)
    texto = re.sub(r"^###\s+(.*)$", r"<h3>\1</h3>", texto, flags=re.M)
    texto = re.sub(r"^\d+\.\s+.*(?:\n\d+\.\s+.*)*", lista, texto, flags=re.M) 
    return texto

markdown = """# Exemplo
Este é um **exemplo** de texto com *itálico*.
Como pode ser consultado em [página da UC](http://www.uc.pt)

1. Primeiro item
2. Segundo item
3. Terceiro item"""

print(converte(markdown))