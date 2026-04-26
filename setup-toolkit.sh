#!/bin/bash

# Setup Script para o Toolkit-29 (Mac/Linux)
# Local: Dinâmico

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENGINE_PATH="$BASE_DIR/factory/29-engine.js"

echo "🚀 Iniciando setup do Toolkit-29..."
echo "📍 Caminho detectado: $BASE_DIR"

# 1. VERIFICAÇÃO DE PRÉ-REQUISITOS (NODE.JS)
if ! command -v node >/dev/null 2>&1; then
    echo ""
    echo "❌ ERRO: Node.js não encontrado!"
    echo "--------------------------------------------------"
    echo "O Toolkit-29 exige o Node.js para funcionar."
    echo ""
    echo "Como instalar:"
    echo "👉 Linux (Ubuntu/Debian): sudo apt update && sudo apt install nodejs"
    echo "👉 Mac (Homebrew): brew install node"
    echo "👉 Ou baixe em: https://nodejs.org/"
    echo "--------------------------------------------------"
    exit 1
fi

# Dar permissão de execução ao motor
chmod +x "$ENGINE_PATH"

# Detectar shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    # Fallback para .zshrc ou .bashrc se não detectado
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
fi

echo "🐚 Shell detectado: $SHELL_RC"

# Função para adicionar ou atualizar alias
update_alias() {
    local name=$1
    local command=$2
    if ! grep -q "alias $name=" "$SHELL_RC" 2>/dev/null; then
        echo "alias $name='$command'" >> "$SHELL_RC"
        echo "✅ Alias '$name' adicionado."
    else
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s|alias $name=.*|alias $name='$command'|g" "$SHELL_RC"
        else
            sed -i "s|alias $name=.*|alias $name='$command'|g" "$SHELL_RC"
        fi
        echo "🟡 Alias '$name' atualizado."
    fi
}

update_alias "29-init" "node $ENGINE_PATH"
update_alias "29-toolkit" "cd $BASE_DIR/29-toolkit"

echo ""
echo "✅ Setup concluído com sucesso!"
echo "--------------------------------------------------"
echo "💡 IMPORTANTE: Para usar os comandos '29-init' de qualquer"
echo "lugar no futuro, você precisará rodar:"
echo "source $SHELL_RC"
echo "ou simplesmente abrir um novo terminal."
echo "--------------------------------------------------"
echo ""

read -p "🚀 Deseja iniciar seu primeiro projeto agora? (s/n): " confirm
if [[ $confirm == [sS] || $confirm == [sS][iI] ]]; then
    node "$ENGINE_PATH"
else
    echo "Até logo! Quando estiver pronto, use o comando '29-init'."
fi

