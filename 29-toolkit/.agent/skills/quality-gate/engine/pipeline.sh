#!/bin/bash

# FusionONE Local Quality Gate - Engine
# v2.40.0

# Cores para o Terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Definir PATH explicitamente para ambiente Antigravity/macOS
export PATH=$PATH:/usr/local/bin:/opt/homebrew/bin

echo -e "${BLUE}🚀 Iniciando FusionONE Local Quality Gate...${NC}"
echo -e "${BLUE}-----------------------------------------------------------${NC}"

# Função para rodar comando e salvar resultado
run_step() {
    local name=$1
    local cmd=$2
    local output_file=".agent/skills/quality-gate/reports/step_${name}.raw"
    
    echo -ne "${YELLOW}⏳ Rodando $name...${NC}"
    
    # Executa o comando e captura output e exit code
    eval "$cmd" > "$output_file" 2>&1
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo -e "\r${GREEN}✅ $name Finalizado com Sucesso!${NC}"
        return 0
    else
        echo -e "\r${RED}❌ $name Falhou! (Verificando impacto global...)${NC}"
        return 1
    fi
}

# Criar pasta de reports se não existir (sanity check)
mkdir -p .agent/skills/quality-gate/reports

# --- ESTEIRA DE QUALIDADE ---
results=""

# 1. Security Audit
run_step "SECURITY" "npm audit --audit-level=high"
results="$results SECURITY:$?"

# 2. Consistency (Lint)
run_step "LINT" "npm run lint -- --max-warnings 0"
results="$results LINT:$?"

# 3. Integrity (Types)
run_step "TYPES" "npx tsc --noEmit"
results="$results TYPES:$?"

# 4. Logic (Tests)
run_step "TESTS" "npm run test:coverage"
results="$results TESTS:$?"

# 5. Build Proof
run_step "BUILD" "npm run build"
results="$results BUILD:$?"

# 6. E2E Defense
run_step "E2E_INSTALL" "npx playwright install --with-deps chromium"
results="$results E2E_INSTALL:$?"

run_step "E2E" "npx playwright test --reporter=line"
results="$results E2E:$?"

# 7. Documentation Sync (Lei 101)
run_step "DOC_SYNC" "npm run doc-sync"
results="$results DOC_SYNC:$?"

echo -e "${BLUE}-----------------------------------------------------------${NC}"
echo -e "${BLUE}📊 Gerando Relatório de Especialista...${NC}"

# Chama o Reporter para formatar o resultado final e gerenciar histórico
# Passamos os resultados como argumentos: SECURITY:0 LINT:1 ...
node .agent/skills/quality-gate/bin/reporter.cjs $results

exit_code=$?

echo -e "${BLUE}-----------------------------------------------------------${NC}"
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✨ Quality Gate PASS v2.40.0${NC}"
else
    echo -e "${RED}🚨 Quality Gate REJECTED v2.40.0${NC}"
fi

exit $exit_code
