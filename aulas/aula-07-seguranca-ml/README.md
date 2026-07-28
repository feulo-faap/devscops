# Aula 7 — Segurança em Machine Learning e Proteção de Dados/Modelos

| Script | O que mostra |
|---|---|
| `1_ataque_adversarial.py` | Ataque adversarial por evasão (FGSM) contra um classificador de dígitos (regressão logística). Uma perturbação quase imperceptível na entrada muda a predição do modelo. |
| `2_anonimizacao_dataset.py` | Pseudonimização, generalização e ruído numérico (privacidade diferencial simplificada) aplicados a um dataset de alunos antes de treinar um modelo. Também ilustra o risco de reidentificação por correlação (k-anonimidade insuficiente). |

```bash
pip install scikit-learn numpy
python 1_ataque_adversarial.py
python 2_anonimizacao_dataset.py
```
