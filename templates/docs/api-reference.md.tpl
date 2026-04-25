# Referência de API - {{project-name}}

> [!TIP]
> Documentação dos contratos de entrada e saída de cada módulo.

---

## 👤 Identity Module
Gestão de acesso e autenticação.

### POST /auth/login
- **Input**: `{ email, password }`
- **Output**: `Result<Session, AuthError>`

---

## 🖼️ Profile Module
Gestão de dados do usuário.

### GET /profile/:id
- **Output**: `Result<Profile, NotFoundError>`

---

## 🔔 Notifications Module
Envio de mensagens (apenas via EventBus).

### Event: UserCreated
- **Payload**: `{ userId, email, name }`
- **Ação**: Dispara e-mail de boas-vindas.

---

## 📝 Audit Module
Trilha de auditoria (apenas via EventBus).

### Event: * (Qualquer Evento)
- **Ação**: Registra metadados do evento para compliance.

---

**Última Atualização:** {{date}}
