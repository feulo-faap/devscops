# Aula 4 — Representação Binária, Encoding e Base da Criptografia

Scripts de apoio à demonstração ao vivo (Vídeo 3). Mostram que encoding
(binário, hexadecimal, Base64) é apenas **representação** de dados — é
público e reversível por qualquer pessoa, diferente de criptografia
(precisa de chave) e de hashing (não é reversível).

| Script | O que mostra |
|---|---|
| `enconding.py` | Texto → bytes UTF-8 → binário → Base64, e volta. Base do exemplo dado em aula. *(nome do arquivo mantido como está no roteiro de gravação; o correto seria "encoding.py")* |
| `representacao_e_encoding.py` | Mesma ideia, com mais exemplos (acentuação, emoji multibyte) e a demonstração central: "esconder" uma senha em Base64 não protege nada — qualquer um decodifica sem chave. |

Executar:

```bash
python enconding.py
python representacao_e_encoding.py
```

Sem dependências externas (usa apenas a biblioteca padrão do Python).
