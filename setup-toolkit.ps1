# Setup Script para o Toolkit-29 (Windows PowerShell)
# Local: Dinâmico e Robusto

# Garante que o caminho seja absoluto e correto
$BaseDir = $PSScriptRoot
if (!$BaseDir) { $BaseDir = Get-Location }
$EnginePath = Join-Path $BaseDir "factory\29-engine.js"

Write-Host "`n🚀 Iniciando setup do Toolkit-29..." -ForegroundColor Cyan
Write-Host "📍 Caminho detectado: $BaseDir"

# 0. INSTALAÇÃO DE DEPENDÊNCIAS
if (Test-Path "$BaseDir\package.json") {
    Write-Host "📦 Instalando motores internos..." -ForegroundColor Gray
    Push-Location $BaseDir
    npm install --silent
    Pop-Location
}

# 1. VERIFICAÇÃO DE PRÉ-REQUISITOS (NODE.JS)
if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "`n❌ ERRO: Node.js não encontrado!" -ForegroundColor Red
    Write-Host "--------------------------------------------------" -ForegroundColor Gray
    Write-Host "O Toolkit-29 exige o Node.js para funcionar."
    Write-Host ""
    Write-Host "Como instalar:"
    Write-Host "👉 PowerShell (Winget): winget install OpenJS.NodeJS"
    Write-Host "👉 Ou baixe em: https://nodejs.org/"
    Write-Host "--------------------------------------------------" -ForegroundColor Gray
    exit
}

# Função para adicionar funções ao Profile
function Add-ToolkitFunction {
    param (
        [string]$Name,
        [string]$ScriptBlock
    )

    $ProfilePath = $PROFILE
    if (!(Test-Path $ProfilePath)) {
        # Cria a pasta do perfil se não existir
        $ProfileDir = Split-Path $ProfilePath
        if (!(Test-Path $ProfileDir)) { New-Item -Path $ProfileDir -ItemType Directory -Force | Out-Null }
        New-Item -Path $ProfilePath -ItemType File -Force | Out-Null
    }

    $FunctionDefinition = @"

function $Name {
    $ScriptBlock
}
"@

    if (!(Select-String -Path $ProfilePath -Pattern "function $Name {" -SimpleMatch)) {
        Add-Content -Path $ProfilePath -Value $FunctionDefinition
        Write-Host "✅ Comando '$Name' adicionado ao seu Perfil do PowerShell." -ForegroundColor Green
    } else {
        Write-Host "🟡 Comando '$Name' já existe no seu Perfil." -ForegroundColor Yellow
    }
}

# Adicionando os comandos
# Usamos caminhos relativos à Home se possível para maior portabilidade
$DisplayEnginePath = $EnginePath
if ($EnginePath.StartsWith($HOME)) {
    $DisplayEnginePath = "~" + $EnginePath.Substring($HOME.Length)
}

$DisplayBaseDir = $BaseDir
if ($BaseDir.StartsWith($HOME)) {
    $DisplayBaseDir = "~" + $BaseDir.Substring($HOME.Length)
}

Add-ToolkitFunction -Name "29-init" -ScriptBlock "node `"$DisplayEnginePath`" `$args"
Add-ToolkitFunction -Name "29-toolkit" -ScriptBlock "Set-Location `"$DisplayBaseDir\29-toolkit`""
Add-ToolkitFunction -Name "29-import" -ScriptBlock "node `"$DisplayBaseDir\factory\29-ingestor.js`""

Write-Host "`n✅ Setup concluído com sucesso!" -ForegroundColor Green
Write-Host "--------------------------------------------------" -ForegroundColor Gray
Write-Host "💡 IMPORTANTE: Para usar os comandos '29-init' de qualquer"
Write-Host "lugar no futuro, você precisará reiniciar o PowerShell ou rodar:"
Write-Host ". `$PROFILE"
Write-Host ""
Write-Host "⚠️  Se receber erro de permissão (Script Execution Policy), rode:"
Write-Host "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
Write-Host "--------------------------------------------------" -ForegroundColor Gray
Write-Host ""

$Choice = Read-Host "🚀 Deseja iniciar seu primeiro projeto agora? (s/n)"
if ($Choice -eq "s" -or $Choice -eq "si") {
    node "$EnginePath"
} else {
    Write-Host "`nAté logo! Quando estiver pronto, use o comando '29-init'." -ForegroundColor Cyan
}
