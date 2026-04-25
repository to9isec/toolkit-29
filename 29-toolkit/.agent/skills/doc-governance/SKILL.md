---
name: "doc-governance"
description: "Padrões de Governança de Documentação (Lei 101 / Doc-Lock) para garantir a integridade e versionamento automático de artefatos do projeto."
---

# Doc-Governance Skill (A Lei 101)

Esta skill orienta o agente sobre como aplicar as regras de **Governança de Documentação Automática (Doc-Lock)** em qualquer projeto. 

O princípio da Lei 101 é que a documentação (como `README.md` e `changelog.md`) nunca deve ficar dessincronizada com o `package.json`.

## O Princípio da Lei 101

Em projetos robustos (como o FusionONE), não dependemos da atualização manual de datas ou versões nos documentos principais. Ao invés disso, utilizamos um script (`doc_sync`) que é acoplado ao Quality Gate (CI/CD) para forçar a sincronização.

## Como implementar a Lei 101 em novos projetos

Se o usuário solicitar a configuração da "Lei 101" ou "Doc-Lock" em um projeto novo, você deve:

1.  **Criar o Script de Sincronização:**
    Crie um arquivo na raiz do projeto chamado `scripts/doc_sync.cjs`. Este script deve ler a propriedade `version` do `package.json` e a data atual, e injetar esses dados no topo do `README.md`.

2.  **Adicionar o Comando no package.json:**
    Adicione o script de sync ao `package.json`:
    ```json
    "scripts": {
      "doc-sync": "node scripts/doc_sync.cjs"
    }
    ```

3.  **Vincular ao Quality Gate:**
    O `doc-sync` deve ser executado automaticamente antes do fechamento de qualquer PR ou deploy em produção (geralmente como um dos passos do pipeline ou do pre-commit hook).

## Código de Referência do Doc-Sync (Node.js/CJS)

```javascript
const fs = require('fs');
const path = require('path');

// Ler o package.json
const packageJsonPath = path.join(process.cwd(), 'package.json');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
const currentVersion = packageJson.version;

// Gerar a data no formato DD/MM/YYYY
const today = new Date();
const formattedDate = `${String(today.getDate()).padStart(2, '0')}/${String(today.getMonth() + 1).padStart(2, '0')}/${today.getFullYear()}`;

// Arquivos alvo
const readmePath = path.join(process.cwd(), 'docs/README.md');

// Função de atualização (exemplo simples)
function updateDocs(filePath, version, date) {
    if (!fs.existsSync(filePath)) return;
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Substitui marcações padrão. Exemplo de Regex: /v\d+\.\d+\.\d+/g
    content = content.replace(/v\d+\.\d+\.\d+/g, `v${version}`);
    
    fs.writeFileSync(filePath, content);
    console.log(`✅ [Doc-Lock] ${path.basename(filePath)} atualizado para a versão ${version}`);
}

updateDocs(readmePath, currentVersion, formattedDate);
```

## Regras de Atuação do Agente

1. Ao criar um novo artefato de documentação para o projeto, certifique-se de referenciar a versão do projeto lendo-a do `package.json`.
2. Após implementar uma nova funcionalidade (Features ou Refactor), verifique se o script `doc-sync` rodou ou recomende que o usuário o rode para finalizar o desenvolvimento.
