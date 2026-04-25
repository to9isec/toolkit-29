# Setup Script para o Toolkit-29 (Windows PowerShell)
# Local: Dinâmico

$BaseDir = Get-Location
$EnginePath = Join-Path $BaseDir "factory\29-engine.js"

Write-Host "🚀 Iniciando setup do Toolkit-29..." -ForegroundColor Cyan
Write-Host "📍 Caminho detectado: $BaseDir"

# Função para adicionar funções ao Profile
function Add-ToolkitFunction {
    param (
        [string]$Name,
        [string]$ScriptBlock
    )

    $ProfilePath = $PROFILE
    if (!(Test-Path $ProfilePath)) {
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
Add-ToolkitFunction -Name "29-init" -ScriptBlock "node `"$EnginePath`" `$args"
Add-ToolkitFunction -Name "29-toolkit" -ScriptBlock "Set-Location `"$BaseDir\29-toolkit`""

Write-Host "`n✅ Setup concluído!" -ForegroundColor Green
Write-Host "💡 Reinicie o PowerShell ou execute: . `$PROFILE" -ForegroundColor Cyan
