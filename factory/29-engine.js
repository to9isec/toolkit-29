#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const os = require('os');
const { execSync } = require('child_process');

/**
 * Toolkit-29 - Framework de Auxílio Arquitetural
 * Versão: 1.3.0 (Zero-Friction + Auto-Copy)
 */

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const configPath = path.join(__dirname, 'config.json');

function checkEnvironment() {
  const issues = [];
  const nodeVersion = process.versions.node.split('.')[0];
  if (parseInt(nodeVersion) < 16) {
    issues.push(`- Node.js desatualizado (${process.version}). Recomenda-se v16+`);
  }
  try {
    execSync('git --version', { stdio: 'ignore' });
  } catch (e) {
    issues.push('- Git não encontrado (Opcional).');
  }
  if (issues.length > 0) {
    console.log('⚠️  Diagnóstico:');
    issues.forEach(issue => console.log(issue));
    console.log('--------------------------------------------------\n');
  }
}

async function ask(question, defaultValue = '') {
  const query = defaultValue ? `${question} (${defaultValue}): ` : `${question}: `;
  return new Promise((resolve) => {
    rl.question(query, (answer) => {
      resolve(answer.trim() || defaultValue);
    });
  });
}

function slugify(text) {
  return text.toString().toLowerCase().trim()
    .replace(/\s+/g, '-').replace(/[^\w-]+/g, '').replace(/--+/g, '-');
}

async function ensureConfig() {
  // Detecção Automática e Silenciosa do Toolkit (Sempre calculada em tempo de execução)
  const currentToolkitPath = path.resolve(__dirname, '../29-toolkit/.agent');

  if (fs.existsSync(configPath)) {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    
    // Auto-reparo: Se o caminho salvo não existir mais ou estiver diferente, atualiza
    if (!fs.existsSync(config.toolkitPath) || config.toolkitPath !== currentToolkitPath) {
      config.toolkitPath = currentToolkitPath;
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    }

    console.log(`\n📁 Diretório mestre de projetos: ${config.projectsDir}`);
    return config;
  }

  console.log('\n🚀 Bem-vindo ao Toolkit-29! Vamos configurar seu ambiente.\n');
  console.log('ℹ️  Esta configuração será feita apenas uma vez. Ela define onde todos');
  console.log('   os seus futuros projetos serão criados automaticamente.\n');

  const home = os.homedir();
  const docsName = fs.existsSync(path.join(home, 'Documentos')) ? 'Documentos' : 'Documents';
  const defaultProjectsDir = path.join(home, docsName, 'Projetos');
  const projectsDir = await ask('? Onde deseja salvar todos os seus projetos?', defaultProjectsDir);
  
  if (!fs.existsSync(projectsDir)) {
    fs.mkdirSync(projectsDir, { recursive: true });
  }
  
  // Detecção Automática e Silenciosa do Toolkit
  const toolkitPath = path.resolve(__dirname, '../29-toolkit/.agent');
  
  if (!fs.existsSync(toolkitPath)) {
    console.error(`\n❌ Erro Crítico: Pasta do toolkit não encontrada em: ${toolkitPath}`);
    console.log('Certifique-se de que a pasta 29-toolkit/.agent existe na raiz do toolkit.');
    process.exit(1);
  }

  const config = { 
    projectsDir, 
    toolkitPath, 
    setupDate: new Date().toISOString() 
  };

  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  console.log('\n✅ Configuração salva com sucesso!');
  console.log(`💡 Dica: Para mudar estas configurações futuramente, apague o arquivo:`);
  console.log(`   ${configPath}\n`);

  return config;
}


// Função de cópia robusta (sem dependências)
function copyFolderSync(from, to) {
  if (!fs.existsSync(from)) return;
  if (!fs.existsSync(to)) fs.mkdirSync(to, { recursive: true });
  fs.readdirSync(from).forEach(element => {
    if (fs.lstatSync(path.join(from, element)).isDirectory()) {
      copyFolderSync(path.join(from, element), path.join(to, element));
    } else {
      fs.copyFileSync(path.join(from, element), path.join(to, element));
    }
  });
}

function copyRecursive(src, dest, replacements) {
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach(child => {
      copyRecursive(path.join(src, child), path.join(dest, child), replacements);
    });
  } else {
    const isText = src.match(/\.(md|tpl|json|ts|js|sh|txt|yml|yaml|sql)$/);
    const finalDest = dest.replace('.tpl', '');
    if (isText) {
      let content = fs.readFileSync(src, 'utf8');
      Object.keys(replacements).forEach(key => {
        content = content.replace(new RegExp(`{{${key}}}`, 'g'), replacements[key]);
      });
      fs.writeFileSync(finalDest, content);
    } else {
      fs.copyFileSync(src, finalDest);
    }
  }
}

async function init() {
  checkEnvironment();
  const config = await ensureConfig();
  const templatesDir = path.join(__dirname, '../templates');

  console.log('\n🏗️  Toolkit-29 — Criando novo projeto...');
  console.log('⚠️  Aviso: Esta é uma ferramenta de auxílio arquitetural. O uso e a');
  console.log('   integridade do código gerado são de sua inteira responsabilidade.\n');
  const args = process.argv.slice(2);
  let name, description, stack;

  if (args.length >= 3) {
    name = slugify(args[0]);
    description = args[1];
    stack = args[2];
    console.log(`> Usando argumentos: Nome=${name}, Desc=${description}, Stack=${stack}`);
  } else {
    name = slugify(await ask('? Nome do projeto'));
    description = await ask('? Descrição', 'Novo projeto Toolkit-29');
    stack = await ask('? Stack', 'Next.js');
  }

  const projectDir = path.join(config.projectsDir, name);
  if (fs.existsSync(projectDir)) {
    console.error(`\n❌ Erro: ${projectDir} já existe.`);
    rl.close();
    process.exit(1);
  }

  const replacements = {
    'project-name': name,
    'project-description': description,
    'stack-choice': stack,
    'date': new Date().toISOString().split('T')[0],
    'year': new Date().getFullYear(),
  };

  // 1. Copiar Templates
  copyRecursive(templatesDir, projectDir, replacements);

  // 2. Copiar Toolkit (como solicitado pelo usuário)
  console.log('🧠 Copiando Toolkit 29...');
  const agentPath = path.join(projectDir, '.agent');
  if (fs.existsSync(agentPath)) fs.rmSync(agentPath, { recursive: true, force: true });
  copyFolderSync(config.toolkitPath, agentPath);
  console.log('✅ Toolkit copiado.');

  // 3. Git
  try { execSync('git init', { cwd: projectDir, stdio: 'ignore' }); } catch (e) {}

  console.log('\n--------------------------------------------------');
  console.log('✅ PROJETO CRIADO COM SUCESSO!');
  console.log(`📍 Local: ${projectDir}`);
  console.log('--------------------------------------------------\n');
  rl.close();
}

init().catch(err => { console.error('❌ Erro:', err); process.exit(1); });
