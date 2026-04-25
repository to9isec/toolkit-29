/**
 * FusionONE Local Quality Gate - Reporter
 * v2.40.0
 * 
 * Este script formata os resultados da esteira local e gerencia o histórico de logs.
 */

const fs = require('fs');
const path = require('path');

const REPORTS_DIR = path.join(__dirname, '../reports');
const MAX_HISTORY = 5;

// Mapeamento de Fases
const PHASE_LABELS = {
    'SECURITY': 'Security Audit (npm audit)',
    'LINT': 'Code Consistency (eslint)',
    'TYPES': 'Type Integrity (tsc)',
    'TESTS': 'Logic Verification (vitest)',
    'BUILD': 'Production Assembly (build)',
    'E2E': 'Functional Defense (playwright)'
};

async function generateReport() {
    const args = process.argv.slice(2);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const version = '2.40.0';
    
    let overallSuccess = true;
    let reportContent = `\n🚀 FUSIONONE LOCAL QUALITY GATE - v${version}\n`;
    reportContent += `📅 Execução: ${new Date().toLocaleString()}\n`;
    reportContent += `-----------------------------------------------------------\n`;
    reportContent += `| Status | Check                      | Result             |\n`;
    reportContent += `| :---   | :---                       | :---               |\n`;

    for (const arg of args) {
        const [phase, code] = arg.split(':');
        const success = code === '0';
        const label = PHASE_LABELS[phase] || phase;
        const icon = success ? '✅' : '❌';
        const resultText = success ? 'PASS' : 'FAIL';
        
        if (!success) overallSuccess = false;
        
        reportContent += `|   ${icon}   | ${label.padEnd(26)} | ${resultText.padEnd(18)} |\n`;
    }

    reportContent += `-----------------------------------------------------------\n`;
    reportContent += `RESULT: ${overallSuccess ? '✨ APPROVED' : '🚨 REJECTED'}\n`;
    reportContent += `-----------------------------------------------------------\n`;

    // 1. Exibir no Terminal
    console.log(reportContent);

    // 2. Salvar Log Consolidado
    const logFile = path.join(REPORTS_DIR, `quality_gate_${timestamp}.log`);
    fs.writeFileSync(logFile, reportContent);

    // 3. Gerenciar Histórico (Manter 5)
    await rotateLogs();

    // 4. Se falhou, sair com código 1 para o bash saber
    process.exit(overallSuccess ? 0 : 1);
}

async function rotateLogs() {
    try {
        const files = fs.readdirSync(REPORTS_DIR)
            .filter(f => f.startsWith('quality_gate_') && f.endsWith('.log'))
            .map(f => ({
                name: f,
                time: fs.statSync(path.join(REPORTS_DIR, f)).mtime.getTime()
            }))
            .sort((a, b) => b.time - a.time); // Mais novos primeiro

        if (files.length > MAX_HISTORY) {
            const toDelete = files.slice(MAX_HISTORY);
            toDelete.forEach(f => {
                fs.unlinkSync(path.join(REPORTS_DIR, f.name));
                // console.log(`🗑️ Log antigo removido: ${f.name}`);
            });
        }
    } catch (err) {
        console.error('Erro ao rotacionar logs:', err);
    }
}

generateReport().catch(err => {
    console.error('Falha fatal no Reporter:', err);
    process.exit(1);
});
