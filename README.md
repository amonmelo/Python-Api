# User API – FastAPI + SQLite + JWT

API de gerenciamento de usuários com autenticação JWT, arquitetura organizada e testes automatizados.  
Projeto desenvolvido com foco em boas práticas de arquitetura e clean code.

---

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/user-api.git
cd user-api
```

### 2. Instale dependências
```bash
npm install
```

Durante a instalação, o projeto executa um **setup interativo** que cria o arquivo `.env` com as configurações mínimas:
- `JWT_SECRET`
- `JWT_EXP_MINUTES`

É possível escolher instalação **padrão** ou **customizada** (informar segredo ou gerar aleatório e definir tempo de expiração).

### 3. (Opcional) Criar usuário administrador inicial
```bash
npm run seed
```

Usuário criado:
- Email: `admin@example.com`
- Senha: `Admin123!`

---

## Execução

Inicie o servidor:
```bash
npm run dev
```

A documentação interativa estará disponível em:  
[http://localhost:9025/docs](http://localhost:9025/docs)

---

## Autenticação

1. Endpoint **POST /auth/login**  
   Corpo da requisição:
   ```json
   {
     "email": "admin@example.com",
     "password": "Admin123!"
   }
   ```
2. Copie o `access_token` retornado.  
3. No Swagger, clique em **Authorize** e informe:
   ```
   Bearer SEU_TOKEN_AQUI
   ```

---

## CRUD de Usuários

### Criar Usuário
**POST /users/**
```json
{
  "name": "João da Silva",
  "email": "joao@example.com",
  "password": "Senha123!"
}
```

### Listar Usuários (com paginação)
**GET /users/?skip=0&limit=10**

### Buscar Usuário por ID
**GET /users/{id}**

### Atualizar Usuário
**PUT /users/{id}**
```json
{
  "name": "João Atualizado",
  "is_active": false
}
```

### Deletar Usuário
**DELETE /users/{id}**

---

## Testes

Executar toda a suíte:
```bash
npm test
```

- Framework: **pytest + httpx**  
- Cobertura próxima de **100%**  
- Casos incluídos: autenticação, CRUD, paginação, tokens inválidos e expirados.

---

## Extras (Customização)

Durante o `npm install`, o projeto executa `scripts/setup.py`, que pode ser usado de duas formas:

- **Instalação padrão** → cria `.env` automático com segredo e expiração default.  
- **Instalação customizada** → permite escolher:
  - Segredo padrão, personalizado ou aleatório forte.  
  - Tempo de expiração do token JWT (em minutos).  

Benefícios:
- Configuração flexível e segura.  
- Tokens ajustáveis ao ambiente.  
- Compatibilidade cross-platform (Windows, Linux, Mac).

---

## Estrutura do Projeto

```
app/
 ├── domain/          # entidades de negócio
 ├── application/     # serviços e ports
 ├── infrastructure/  # banco, repositórios, segurança
 ├── interfaces/      # HTTP (routers + schemas)
 └── main.py          # composição da aplicação
scripts/
 ├── setup.py         # cria .env interativo
 └── seed_admin.py    # cria usuário admin inicial
tests/                # testes automatizados
data/                 # banco SQLite (ignorado no GitHub)
logs/                 # logs de execução
```

---

## Requisitos atendidos

- FastAPI + SQLite  
- Autenticação JWT (com expiração configurável)  
- CRUD completo de usuários com paginação  
- Testes unitários com cobertura  
- Documentação automática via Swagger  
- Setup rápido (`npm install`)  
- Customização extra no setup (JWT e expiração configuráveis)  
