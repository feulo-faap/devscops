# Aula 5 — Criptografia Aplicada

Progressão didática usada na demonstração ao vivo: da cifra mais simples
até o padrão usado hoje em dia, terminando em hashing (que não é
criptografia, mas é frequentemente confundido com ela).

| Ordem | Script | Conceito |
|---|---|---|
| 1 | `1_cifra_cesar.py` | Cifra de substituição por deslocamento. Chave pequena (25 possibilidades) → quebrada por força bruta em milissegundos. |
| 2 | `2_cifra_substituicao.py` | Alfabeto embaralhado. Espaço de chaves gigante (26! ≈ 4×10²⁶), mas ainda quebrável por análise de frequência de letras. |
| 3 | `3_enigma_simulado.py` | Cifra eletromecânica (rotores + refletor + plugboard). Introduz o conceito de chave composta e de estado que muda a cada letra. |
| 4 | `4_aes_exemplo.py` | AES-256-GCM: criptografia simétrica moderna, opera sobre bytes (não só letras) e já inclui autenticação de integridade. |
| 5 | `crytography.py` | Hashing de senha com bcrypt (salt + fator de custo). Contraponto final: hashing não é criptografia — não existe "decifrar" um hash. |

Executar em sequência (1 → 5) para reproduzir a progressão da aula.

```bash
pip install cryptography bcrypt
python 1_cifra_cesar.py
python 2_cifra_substituicao.py
python 3_enigma_simulado.py
python 4_aes_exemplo.py
python crytography.py
```
