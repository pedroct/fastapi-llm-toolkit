#!/usr/bin/env bash
set -euo pipefail

# Carrega o .env sem poluir o ambiente global
if [ -f .env ]; then
    set -a; source .env; set +a
fi

: "${SONAR_TOKEN:?Variável SONAR_TOKEN não encontrada no .env}"

uv run pysonar \
  --sonar-host-url=https://sonar.pedroct.com.br \
  --sonar-token="${SONAR_TOKEN}" \
  --sonar-project-key=pedroct_fastapi-llm-toolkit_10e0579f-1e73-48bb-b0f8-abad7d5faa76
