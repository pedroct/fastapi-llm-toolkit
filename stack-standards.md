# Padrões de Stack & Playbook de Scaffolding

*Documento de referência reutilizável — use ao criar o esqueleto de novos projetos.*
Versão 1.0 · Junho de 2026

> Dois padrões de stack espelhados (backend Python / frontend TypeScript) num **monorepo** entregue via **Docker Compose**. O toolchain de qualidade é o mesmo em filosofia nos dois lados, com ferramentas equivalentes.

---

## 1. Os dois padrões em uma olhada

| Camada | Linguagem | Framework | Gerenciador | Banco |
|---|---|---|---|---|
| **Backend** | Python (≥3.12) | FastAPI | **uv** | PostgreSQL |
| **Frontend** | TypeScript | React / Next.js + Tailwind + shadcn/ui | **pnpm** (npm bloqueado) | — |

- **Repositório:** monorepo único. Isolamento de runtime vem do **Docker** (contêineres separados), não da separação de repos.
- **Contrato FE↔BE:** fonte única = schemas do FastAPI → **OpenAPI** → types TS gerados para o frontend.

---

## 2. Estrutura do monorepo

```
<projeto>/
├── pyproject.toml          # uv workspace (raiz): ferramentas Python repo-wide
├── uv.lock
├── package.json            # pnpm (raiz): ferramentas JS repo-wide
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── biome.json              # lint + format JS/TS
├── tsconfig.json           # base TypeScript (strict)
├── .gitignore
├── docker-compose.yml
├── apps/
│   ├── api/                # backend Python (FastAPI) — pyproject.toml próprio
│   └── web/                # frontend (Next.js)
└── packages/
    ├── contract/           # OpenAPI + types TS gerados (a costura FE↔BE)
    └── ui/                 # design system compartilhado
```

**Regra de localização das ferramentas:**
- **Repo-wide** (agem no repo inteiro, uma instância serve os dois lados): `pre-commit`, `commitizen`, `pysonar`/SonarScanner → na **raiz**.
- **Backend-scoped** (operam em código Python): `ruff`, `mypy`, `bandit`, `pip-audit`, `sqlfluff`, `pytest` → em **`apps/api`**.
- **Frontend-scoped/JS** (`biome`, `typescript`, `vitest`): raiz ou `apps/web` conforme o alcance.

---

## 3. Toolchain do BACKEND (Python)

| Ferramenta | Versão base | Função | Comando |
|---|---|---|---|
| **uv** | 0.11.x | Gerenciador de pacotes/ambientes/workspace | `uv` |
| **ruff** | 0.15.14 | Linter + formatter (substitui black, isort, flake8) | `ruff check` / `ruff format` |
| **mypy** | 2.1.0 | Type checking estático — **modo strict** | `mypy` |
| **pylint** | 3.3.0 | Análise profunda (CI); ruff PL cobre ~60% no loop de commit | `pylint` |
| **pre-commit** | 4.6.0 | Hooks automáticos antes de cada commit | `pre-commit run` |
| **semgrep** | 1.165.x | SAST multi-linguagem (Python + JS) — repo-wide, roda no pre-push | `semgrep` |
| **bandit** | 1.9.4 | SAST Python complementar (CI); ruff S cobre o essencial no pre-commit | `bandit` |
| **pip-audit** | 2.10.0 | Auditoria de CVEs nas dependências | `pip-audit` |
| **sqlfluff** | 4.2.1 | Lint de SQL / migrations Alembic (omitir se não houver SQL) | `sqlfluff lint` |
| **pytest** | 9.0.3 | Runner de testes | `pytest` |
| **pytest-asyncio** | 0.24.0 | Suporte a testes async (`asyncio_mode = "auto"`) | — plugin |
| **pytest-cov** | 5.0.0 | Cobertura de código integrada ao pytest | — plugin |
| **commitizen** | 4.16.2 | Commits guiados (Conventional Commits) | `cz commit` |
| **pysonar** | 1.6.x¹ | SonarScanner CLI para SonarQube | `pysonar` |

¹ *A 1.5.0 pode conflitar com `requires-python`; a 1.6.x resolve. Verifique a última estável no momento do scaffold.*

> **Nota:** versões são a **linha de base** validada. Ao iniciar um projeto novo, confirme a última estável de cada uma e **pine no Docker/lock** para reprodutibilidade.

---

## 4. Toolchain do FRONTEND (TypeScript) e equivalência FE↔BE

| Backend (Python) | Frontend equivalente | Versão base | Observação |
|---|---|---|---|
| uv | **pnpm** | 11.x | gerenciador de pacotes/workspaces; **npm bloqueado** |
| ruff (lint+format) | **Biome** | 2.4.x | tudo-em-um (lint+format), filosofia do ruff |
| mypy (strict) | **TypeScript** (`tsc`) | 6.x | `strict: true` no `tsconfig` |
| pytest | **Vitest** (+ Testing Library) | 4.x | `@testing-library/react` quando houver React |
| pip-audit | **pnpm audit** | nativo | sem instalar |
| bandit (SAST) | **semgrep**² | 1.165.x | multi-linguagem (cobre Python *e* JS) — repo-wide; **listado no §3** |
| pre-commit | **pre-commit** (mesmo) | — | roda hooks JS também — uma instância no repo |
| commitizen | **commitizen** (mesmo `cz`) | — | uma instância serve o repo inteiro |
| pysonar / SonarScanner | **mesmo scanner** | — | um projeto SonarQube multi-linguagem |
| sqlfluff (SQL) | — | — | sem equivalente no front (SQL é do backend) |

² *Recomendado para SAST de JS, pois Biome não tem plugin de segurança. Como é multi-linguagem, pode até substituir o bandit e unificar o SAST do repo.*

---

## 5. Convenções

- **pnpm, nunca npm.** Imposto por `preinstall: "npx -y only-allow pnpm"` no `package.json`.
- **Type checking estrito** dos dois lados: mypy `strict` e tsc `strict`.
- **Versões pinadas** no lock + Dockerfile (reprodutibilidade FE/BE/CI iguais).
- **Conventional Commits** via `cz commit`, uma única configuração no repo.
- **Quality gates** orquestrados por um único `.pre-commit-config.yaml` na raiz.
- **Contrato gerado, nunca escrito à mão:** FastAPI → OpenAPI → types TS.

---

## 6. Passo a passo de scaffolding (copiar e rodar)

```bash
# 0. Repositório
git init && git branch -M main

# 1. Raiz: uv workspace (Python) + arquivos base (ver §7 para o conteúdo)
#    crie pyproject.toml, apps/api/pyproject.toml, package.json,
#    pnpm-workspace.yaml, biome.json, tsconfig.json, .gitignore

# 2. Ferramentas Python repo-wide (raiz) — inclui semgrep (SAST unificado Python+JS)
uv add --dev "pre-commit==4.6.0" "commitizen==4.16.2" "pysonar" "semgrep"

# 3. Ferramentas Python do backend (apps/api)
uv add --directory apps/api --dev \
  "ruff==0.15.14" "mypy==2.1.0" "bandit==1.9.4" \
  "pip-audit==2.10.0" "sqlfluff==4.2.1" "pytest==9.0.3"

# 4. Ferramentas JS (raiz, via pnpm)
pnpm add -w -D @biomejs/biome typescript vitest jsdom @testing-library/jest-dom
#    (@testing-library/react + @vitejs/plugin-react quando apps/web tiver React)

# 5. Verificação
uv run --directory apps/api ruff check .
uv run cz version
pnpm exec biome check .

# 6. (pendente, fase de quality-gates) .pre-commit-config.yaml + config SonarQube + semgrep
```

> **Dica de versões:** para sempre pegar a última estável, troque `pkg==X` por `pkg` e deixe o resolver pinar; depois trave o resultado no lock.

---

## 7. Templates de configuração

### `pyproject.toml` (raiz — uv workspace virtual)
```toml
[project]
name = "<projeto>"
version = "0.0.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = false

[tool.uv.workspace]
members = ["apps/api"]

[dependency-groups]
dev = ["pre-commit==4.6.0", "commitizen==4.16.2", "pysonar>=1.6.0"]

[tool.commitizen]
name = "cz_conventional_commits"
version = "0.0.0"
tag_format = "v$version"
update_changelog_on_bump = true
```

### `apps/api/pyproject.toml` (backend)
```toml
[project]
name = "<projeto>-api"
version = "0.0.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = false

[dependency-groups]
dev = [
    "ruff>=0.15.14", "mypy>=2.1.0", "bandit>=1.9.4",
    "pip-audit>=2.10.0", "sqlfluff>=4.2.1", "pytest>=9.0.3",
    "pytest-asyncio>=0.24.0", "pytest-cov>=5.0.0",
]

# ---------------------------------------------------------------------------
# Ruff — linter + formatter (substitui black, isort e flake8)
# ---------------------------------------------------------------------------

[tool.ruff]
line-length    = 88
target-version = "py312"
src            = ["app", "tests"]
exclude        = [".venv", "__pycache__", "alembic/versions"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "UP",   # pyupgrade (Python 3.12+)
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "C4",   # flake8-comprehensions
    "N",    # pep8-naming
    "PL",   # pylint (~60% das regras via ruff, muito mais rápido)
    "RUF",  # ruff-specific
    "S",    # flake8-bandit
    "ANN",  # annotations
]
ignore = [
    "E501",     # line-too-long — ruff format já trata
    "ANN101",   # self sem anotação — desnecessário
    "ANN102",   # cls sem anotação — desnecessário
    "ANN401",   # Any permitido quando necessário
    "PLR0913",  # too-many-arguments — endpoints FastAPI com Depends
    "PLR2004",  # magic-value-comparison — aceitável em status codes HTTP
    "S101",     # assert — necessário em testes pytest
]

[tool.ruff.lint.per-file-ignores]
"tests/**"    = ["ANN", "S", "PLR"]
"alembic/**"  = ["ANN", "N999"]

[tool.ruff.lint.isort]
known-first-party      = ["app"]
force-sort-within-sections = true

[tool.ruff.lint.pylint]
max-args = 8

[tool.ruff.format]
quote-style               = "double"
indent-style              = "space"
line-ending               = "lf"
skip-magic-trailing-comma = false

# ---------------------------------------------------------------------------
# Pylint — análise profunda (CI); ruff PL cobre ~60% no loop de commit
# ---------------------------------------------------------------------------

[tool.pylint.main]
jobs         = 0
py-version   = "3.12"
recursive    = true
ignore-paths = [".venv", "__pycache__", "alembic"]

[tool.pylint."messages control"]
disable = [
    # Cobertos pelo ruff
    "C0301", "C0303", "C0304", "C0411", "C0412", "C0413",
    "W0611", "W0614", "W0401", "W0622", "W0621", "W0702", "W0703",
    "E0401",
    # Ruído geral
    "R0903", "R0801", "C0114", "C0115", "C0116",
]

[tool.pylint.design]
max-args       = 8
max-attributes = 10
max-branches   = 12
max-returns    = 6
max-statements = 50

[tool.pylint.format]
max-line-length = 88

# ---------------------------------------------------------------------------
# Mypy
# ---------------------------------------------------------------------------

[tool.mypy]
python_version         = "3.12"
strict                 = true
warn_return_any        = true
warn_unused_configs    = true
warn_unused_ignores    = true
warn_redundant_casts   = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module                = "tests.*"
disallow_untyped_defs = false

# ---------------------------------------------------------------------------
# Pytest + Coverage
# ---------------------------------------------------------------------------

[tool.pytest.ini_options]
asyncio_mode     = "auto"
testpaths        = ["tests"]
python_files     = ["test_*.py"]
python_classes   = ["Test*"]
python_functions = ["test_*"]
addopts          = "--cov --cov-report=term-missing"
markers          = ["integration: requer serviços externos reais"]

[tool.coverage.run]
relative_files = true
source         = ["app"]
branch         = true

[tool.coverage.report]
skip_empty = true

# ---------------------------------------------------------------------------
# Bandit — CI; ruff S cobre o essencial no pre-commit
# ---------------------------------------------------------------------------

[tool.bandit]
targets      = ["app"]
exclude_dirs = [".venv", "tests", "alembic"]
skips = [
    "B101",  # assert — coberto por ruff S101; necessário em testes
    "B104",  # bind-all-interfaces — falso positivo em config local
]

# ---------------------------------------------------------------------------
# SQLFluff
# ---------------------------------------------------------------------------

[tool.sqlfluff.core]
dialect         = "postgres"
templater       = "jinja"
max_line_length = 88
exclude_rules   = ["LT05"]

[tool.sqlfluff.indentation]
indent_unit    = "space"
tab_space_size = 4
```

### `package.json` (raiz)
```json
{
  "name": "<projeto>",
  "version": "0.0.0",
  "private": true,
  "packageManager": "pnpm@11.5.2",
  "engines": { "node": ">=22", "pnpm": ">=11" },
  "scripts": {
    "preinstall": "npx -y only-allow pnpm",
    "format": "biome format --write .",
    "lint": "biome check .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run"
  }
}
```

### `pnpm-workspace.yaml`
```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### `biome.json`
```json
{
  "$schema": "https://biomejs.dev/schemas/2.4.16/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "files": { "ignoreUnknown": true },
  "formatter": { "enabled": true, "indentStyle": "space", "indentWidth": 2, "lineWidth": 100 },
  "linter": { "enabled": true, "rules": { "recommended": true } },
  "javascript": { "formatter": { "quoteStyle": "double" } },
  "assist": { "actions": { "source": { "organizeImports": "on" } } }
}
```

### `tsconfig.json` (base strict)
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "noEmit": true,
    "jsx": "preserve"
  },
  "exclude": ["node_modules", "dist", ".next"]
}
```

### `.gitignore` (essencial)
```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
.mypy_cache/
.ruff_cache/
.pytest_cache/
# Node / pnpm
node_modules/
.pnpm-store/
dist/
.next/
coverage/
# Env / segredos
.env
.env.*
!.env.example
# SonarQube
.scannerwork/
```

### `.pre-commit-config.yaml`
Hooks locais reaproveitam o uv+pnpm (uma fonte de versão). Instale com `uv run pre-commit install --install-hooks`.
```yaml
minimum_pre_commit_version: "4.0.0"
default_install_hook_types: [pre-commit, commit-msg, pre-push]
default_stages: [pre-commit]   # só semgrep roda no pre-push

# Vendados, assets aprovados e lockfiles ficam fora dos gates (evita falsos positivos)
exclude: |
  (?x)^(
      _bmad/.*
    | base/.*
    | uv\.lock
    | pnpm-lock\.yaml
  )$

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-merge-conflict
      - id: mixed-line-ending
      - id: check-added-large-files
        args: ["--maxkb=1024"]
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff (lint + autofix)
        entry: uv run ruff check --fix --force-exclude
        language: system
        types_or: [python, pyi]
      - id: ruff-format
        name: ruff (format)
        entry: uv run ruff format --force-exclude
        language: system
        types_or: [python, pyi]
      - id: mypy
        name: mypy (strict)
        entry: uv run mypy --config-file apps/api/pyproject.toml apps/api
        language: system
        types_or: [python, pyi]
        pass_filenames: false
        files: ^apps/api/.*\.py$
      - id: bandit
        name: bandit (SAST Python)
        entry: uv run bandit -c apps/api/pyproject.toml -q
        language: system
        types: [python]
        files: ^apps/api/.*\.py$
      - id: sqlfluff
        name: sqlfluff (lint SQL)
        entry: uv run sqlfluff lint
        language: system
        types: [sql]
      - id: biome
        name: biome (lint + format)
        entry: pnpm exec biome check --write --no-errors-on-unmatched
        language: system
        types_or: [javascript, jsx, ts, tsx, json]
      - id: semgrep
        name: semgrep (SAST Python + JS)
        entry: uv run semgrep --error --skip-unknown-extensions --config p/security-audit --config p/secrets
        language: system
        pass_filenames: false
        stages: [pre-push]
      # SonarQube no pre-commit: dispara só em mudança de código (não docs/config).
      # Requer SONAR_TOKEN no .env + servidor acessível (offline → commit falha).
      # Alternativa mais leve: mover para stages: [pre-push].
      - id: sonar
        name: SonarQube (pysonar)
        entry: bash scripts/sonar-scan.sh
        language: system
        pass_filenames: false
        files: \.(py|pyi|ts|tsx|js|jsx|sql)$
      - id: commitizen-check
        name: commitizen (Conventional Commits)
        entry: uv run cz check --commit-msg-file
        language: system
        stages: [commit-msg]
```

### `.semgrepignore`
```gitignore
node_modules/
.venv/
.next/
dist/
coverage/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.scannerwork/
```

---

## 8. Pendências a fechar na fase de CI

- Configuração do SonarQube (`sonar-project.properties`) e do scanner.
- Pipeline CI executando: lint → typecheck → SAST → audit → testes.

**Rulesets semgrep recomendados:** `p/python`, `p/javascript`, `p/typescript`, `p/security-audit`, `p/secrets`, `p/owasp-top-ten`.
Ex.: `uv run semgrep --config p/security-audit --config p/secrets .`

*Fim do playbook. Mantenha as versões e este documento sincronizados quando atualizar o padrão.*
