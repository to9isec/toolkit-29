const fs = require('fs');
const path = require('path');
const os = require('os');

// Nota: Esta biblioteca deve ser instalada via 'npm install'
let AdmZip;
try {
  AdmZip = require('adm-zip');
} catch (e) {
  console.error('\n❌ ERRO: Biblioteca "adm-zip" não encontrada.');
  console.log('👉 Por favor, rode: npm install\n');
  process.exit(1);
}

async function startIngestor() {
  console.log('\n📥 [Design Ingestor] Iniciando motor de processamento...');

  const inboxDir = path.join(process.cwd(), 'factory', 'inbox', 'design');
  
  console.log(`📂 Procurando em: ${inboxDir}`);

  // Garantir que a pasta existe
  if (!fs.existsSync(inboxDir)) {
    fs.mkdirSync(inboxDir, { recursive: true });
  }

  // Busca insensível a maiúsculas (.zip ou .ZIP)
  const files = fs.readdirSync(inboxDir).filter(f => f.toLowerCase().endsWith('.zip'));

  if (files.length === 0) {
    console.log('🟡 Nenhuns arquivos .zip encontrados em factory/inbox/design/');
    console.log('💡 Dica: Coloque seu layout.zip lá e rode este comando novamente.\n');
    return;
  }

  // Pegar o arquivo mais recente
  const targetZip = files[0];
  const zipPath = path.join(inboxDir, targetZip);
  const extractDir = path.join(process.cwd(), 'factory', 'temp_design');

  console.log(`📦 Processando: ${targetZip}`);

  try {
    const zip = new AdmZip(zipPath);
    
    if (fs.existsSync(extractDir)) {
      fs.rmSync(extractDir, { recursive: true, force: true });
    }
    fs.mkdirSync(extractDir, { recursive: true });

    zip.extractAllTo(extractDir, true);
    console.log('✅ Extração concluída com sucesso.');

    // Análise de Tecnologia
    analyzeTech(extractDir);

  } catch (error) {
    console.error('❌ Falha ao processar o ZIP:', error.message);
  }
}

function analyzeTech(dir) {
  const pkgPath = path.join(dir, 'package.json');
  console.log('\n🔍 Analisando a estrutura do seu código...');

  if (fs.existsSync(pkgPath)) {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    
    console.log(`📍 Projeto Identificado: ${pkg.name || 'Layout de Design'}`);
    
    if (deps.next) {
      console.log('🚀 Tecnologia: Next.js (Excelente escolha para performance!).');
    } else if (deps.react) {
      console.log('⚛️  Tecnologia: React detectado.');
    } else if (deps.vue) {
      console.log('🖖 Tecnologia: Vue detectado.');
    } else {
      console.log('📄 Tecnologia: HTML/JS Puro ou Framework desconhecido.');
    }

    console.log('\n⚖️  [Protocolo 29] Status: Tudo pronto para a "Blindagem" de arquitetura.');
    console.log('👉 Próximo Passo: O Agente 29 começará a organizar o código em Módulos (Silos).');
  } else {
    console.log('⚠️  Aviso: Não encontrei um arquivo package.json. Vou tratar o design como um site estático.');
  }
  
  console.log('\n✨ O processamento inicial terminou! Seu código está pronto na pasta temporária.\n');
}

startIngestor();
