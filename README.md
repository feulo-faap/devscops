# devscops

Repositório de apoio às demonstrações práticas do curso **Fundamentos de
Segurança e DevSecOps** (FAAP — graduação em Ciência de Dados |
Inteligência Artificial). Reúne os scripts usados nas aulas gravadas e a
aplicação vulnerável usada como laboratório central do curso.

## Estrutura por aula

| Aula | Tema | Onde está o material |
|---|---|---|
| 1 | Fundamentos de Segurança da Informação e Tríade CIA | — (só slides) |
| 2 | Comunicação Cliente-Servidor e Protocolo HTTP | — (só slides) |
| 3 | Gestão de Identidades, Autenticação e Autorização (IAM/MFA/SSO/RBAC) | `devsecops-lab/` (rotas de auth e papéis de acesso) |
| 4 | Representação Binária, Encoding e Base da Criptografia | `aulas/aula-04-encoding/` |
| 5 | Criptografia Aplicada (simétrica, assimétrica, hashing) | `aulas/aula-05-criptografia/` |
| 6 | Vulnerabilidades em Aplicações Web (OWASP Top 10) | `devsecops-lab/` |
| 7 | Segurança em Machine Learning e Proteção de Dados/Modelos | `aulas/aula-07-seguranca-ml/` |
| 8 | Fundamentos de DevOps e Pipelines de CI/CD | `.github/workflows/` |
| 9 | Fundamentos de DevSecOps e Shift-Left Security | `.github/workflows/` + `devsecops-lab/` |

## `devsecops-lab/`

Aplicação Flask **propositalmente vulnerável**, usada como artefato único
nas Aulas 3, 5, 6, 7 e 9. Cada vulnerabilidade está sinalizada no código
com o comentário `# VULNERABILIDADE`.

| Rota / arquivo | Vulnerabilidade |
|---|---|
| `/autenticar` | SQL Injection + senha em texto puro |
| `config.py` | Segredo hardcoded (`123456`) |
| `/perfil/<id>`, `/buscar` | SQL Injection |
| `/mensagem` | Cross-Site Scripting (XSS) |
| `/admin` | Broken Access Control |
| `/hash` | Hash fraco (MD5) |
| `/ping` | Command Injection |
| `/calculadora` | `eval()` inseguro |
| `/arquivo` | Path Traversal |
| `/enviar` | Upload de arquivo sem validação |

Ver `devsecops-lab/README.md` para instruções de instalação e execução
local.

## `.github/workflows/`

Pipeline de CI/CD usado como base das Aulas 8 (montagem do pipeline) e 9
(inserção de segurança — shift-left):

| Workflow | Tipo | O que faz |
|---|---|---|
| `python.yaml` | Build/testes | Instala dependências e valida a aplicação |
| `bandit.yaml` | SAST | Analisa o código Python em busca de padrões inseguros |
| `semgrep.yml` | SAST | Regras de segurança configuráveis |
| `codeQL.yaml` | SAST | Análise semântica de código (GitHub CodeQL) |
| `pip-audit.yml` | SCA | Verifica vulnerabilidades conhecidas nas dependências |
| `zap.yaml` | DAST | Sobe a aplicação e ataca via OWASP ZAP |

## `aulas/`

Scripts avulsos de demonstração ao vivo, organizados por aula (ver tabela
acima). Cada subpasta tem seu próprio README com a lista de scripts, o
que cada um demonstra e a ordem sugerida de execução.

## Observações

- Os nomes de alguns scripts mantêm grafias já citadas nos roteiros de
  gravação (ex.: `enconding.py`, `crytography.py`) para não quebrar as
  referências existentes. Se os roteiros forem atualizados, os arquivos
  podem ser renomeados junto.
- Recomendação futura (ainda não aplicada): restringir os workflows de
  CI com `paths: devsecops-lab/**`, para que mudanças em `aulas/` não
  disparem o pipeline do laboratório.
