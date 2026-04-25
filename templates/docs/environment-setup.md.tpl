# Setup de Ambiente - {{project-name}}

> [!TIP]
> Guia passo-a-passo para configurar o ambiente de desenvolvimento local.

---

## 🛠️ Requisitos
- Node.js (v18+)
- NPM / PNPM
- Git
- Docker (opcional, para banco local)

---

## 🚀 Passo a Passo

1.  **Clone o repositório** (se já tiver um):
    ```bash
    git clone ...
    ```
2.  **Instale as dependências**:
    ```bash
    npm install
    ```
3.  **Configure as variáveis de ambiente**:
    ```bash
    cp .env.example .env
    ```
    Preencha os valores no `.env`.
4.  **Inicie o banco de dados** (se necessário):
    ```bash
    # Exemplo Supabase local
    npx supabase start
    ```
5.  **Execute o projeto**:
    ```bash
    npm run dev
    ```

---

## 🔑 Variáveis de Ambiente (.env)

| Variável | Descrição | Valor Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão com o banco | `postgresql://...` |
| `API_KEY` | Chave de acesso à API externa | `sb_publishable_...` |

---

**Última Atualização:** {{date}}
