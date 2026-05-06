#!/bin/sh

# Setup Script para o Toolkit-29 (Compatibilidade Universal: Sh, Dash, Bash, Zsh)
# Local: Dinâmico

# Pega o diretório do script de forma compatível
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
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

# Detectar shell de forma mais robusta
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_RC_DISPLAY="~/.zshrc"
else
    SHELL_RC="$HOME/.bashrc"
    SHELL_RC_DISPLAY="~/.bashrc"
fi

echo "🐚 Shell detectado: $SHELL_RC_DISPLAY"

# Função para adicionar ou atualizar alias (Compatível com POSIX)
update_alias() {
    name=$1
    cmd=$2
    
    # Tornar o comando genérico se estiver dentro da home
    case "$cmd" in
        "$HOME"*)
            cmd_display="~${cmd#$HOME}"
            ;;
        *)
            cmd_display="$cmd"
            ;;
    esac

    if ! grep -q "alias $name=" "$SHELL_RC" 2>/dev/null; then
        echo "alias $name='$cmd_display'" >> "$SHELL_RC"
        echo "✅ Alias '$name' adicionado."
    else
        # Detecta OS para o SED correto
        if [ "$(uname)" = "Darwin" ]; then
            sed -i '' "s|alias $name=.*|alias $name='$cmd_display'|g" "$SHELL_RC"
        else
            sed -i "s|alias $name=.*|alias $name='$cmd_display'|g" "$SHELL_RC"
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
echo "source $SHELL_RC_DISPLAY"
echo "ou simplesmente abrir um novo terminal."
echo "--------------------------------------------------"
echo ""

echo "🚀 Deseja iniciar seu primeiro projeto agora? (s/n): "
read confirm

case "$confirm" in
    [sS]|[sS][iI])
        node "$ENGINE_PATH"
        ;;
    *)
        echo "Até logo! Quando estiver pronto, use o comando '29-init'."
        ;;
esac
