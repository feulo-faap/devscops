# Aula 3 — Gestão de Identidades, Autenticação e Autorização

Scripts de apoio à demonstração ao vivo (Vídeo 3). Mostram, na prática,
como a secret key hardcoded e fraca do `devsecops-lab/config.py`
(`SECRET_KEY = "123456"`) permite forjar uma sessão inteira da aplicação
— o mesmo mecanismo que a ferramenta `flask-unsign` explora ao vivo,
contra um cookie real, no roteiro de gravação.

| Arquivo | O que é |
|---|---|
| `forjar_sessao.py` | Recria isoladamente o esquema de assinatura de cookies do Flask (sem precisar do servidor rodando) e mostra os 5 passos: cookie legítimo → payload legível sem chave → tentativa de adulteração sem a chave certa falha → cookie forjado com a chave conhecida → servidor aceita o cookie forjado. |
| `wordlist.txt` | Lista curta de chaves fracas comuns, usada ao vivo com `flask-unsign --unsign --wordlist wordlist.txt` para "descobrir" a secret key do cookie real capturado no navegador. |

Executar:

```bash
python forjar_sessao.py
```

Requer Flask instalado (já é dependência do `devsecops-lab` — rode a
partir de um ambiente com `pip install -r ../../devsecops-lab/requirements.txt`).

Para a demonstração ao vivo com um cookie real, instale também:

```bash
pip install flask-unsign
```
