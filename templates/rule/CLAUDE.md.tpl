# ⚖️ Protocolo 29: Leis de Governança

> [!IMPORTANT]
> Este documento define as leis absolutas para o projeto **{{project-name}}**. Nenhuma modificação de IA ou humana deve violar estas premissas sem aprovação explícita.

## 1. Integridade Documental
*   **Versionamento:** Todo documento técnico deve seguir o padrão de rastreabilidade do ecossistema.
*   **Sincronização:** Toda alteração estrutural no código deve ser refletida imediatamente na documentação correspondente.
*   **Qualidade Visual:** Utilize alertas [!IMPORTANT], [!NOTE] e [!WARNING] para destacar pontos críticos e decisões arquiteturais.

## 2. Arquitetura e Segurança
*   **Isolamento:** Módulos de negócio devem ser independentes e desacoplados (Siloed Architecture).
*   **Tipagem Forte:** O uso de tipos explícitos é obrigatório. Evite o uso de tipos genéricos ou indefinidos que ocultem a intenção do código.
*   **Proteção de Segredos:** Chaves de API, tokens e credenciais nunca devem ser persistidos no código fonte. Utilize variáveis de ambiente.

## 3. Protocolo de Colaboração com IA
*   **Contexto Prévio:** Antes de qualquer implementação, o agente deve revisar as regras contidas na pasta `/rule`.
*   **Preservação de Hardening:** Melhorias de segurança e refatorações de qualidade não devem ser revertidas em favor de implementações mais rápidas.

---
**Projeto:** {{project-name}} | **Versão:** 0.1.0 | **Protocolo 29**
