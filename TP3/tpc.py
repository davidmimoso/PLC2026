import re

texto = open("query.txt", encoding="utf-8").read()
er = re.compile(r'(?P<COMENT>\#.*)|(?P<LIMIT>\bLIMIT\b)|(?P<VAR>\?[a-zA-Z0-9]+)|(?P<NUM>\d+)|(?P<STR>".*?")|(?P<LANG>@\w{2})|(?P<DELIM>[{}.])|(?P<ID>\w+:\w+|\w+)|(?P<SKIP>\s+)|(?P<ERRO>.)')

for m in er.finditer(texto):
    for tipo, valor in m.groupdict().items():
        if valor is not None and tipo not in ("SKIP", "COMENT"):
            print(tipo, valor)