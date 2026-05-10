# Mini Projeto Flask + PostgreSQL + JWT

Este projeto é uma API desenvolvida em **Flask**, utilizando **SQLAlchemy** para integração com banco de dados **PostgreSQL** hospedado no Render. A autenticação é feita com **JWT (JSON Web Token)**.

---

## Tecnologias utilizadas
- Python + Flask
- SQLAlchemy
- PostgreSQL (Render)
- JWT para autenticação
- Postman para testes

---

## Configuração
### Variáveis de ambiente necessárias:
- `DATABASE_URL` → URL de conexão com o banco PostgreSQL no Render.
- `JWT_SECRET_KEY` → chave secreta para geração dos tokens JWT.

---

## Endpoints da API

### 1. **Registro de usuário**
`POST https://mini-projeto-flask-f6k4.onrender.com/register`

Body:
```json
{
  "usuario": "admin",
  "senha": "123456",
  "role": "admin"
}

Resposta:
{
  "msg": "Usuário admin criado com sucesso!"
}
### 2. **Login** 
'POST https://mini-projeto-flask-f6k4.onrender.com/login'

Body:
'''json
{
  "usuario": "admin",
  "senha": "123456"
}
Resposta:
{
  "usuario": "admin",
  "senha": "123456"
}

### 3. **Criar Clientes**
'POST https://mini-projeto-flask-f6k4.onrender.com/clientes'

Headers:
Authorization: Bearer <token_jwt>
Body
'''json
{
  "nome": "Cliente Teste"
}
Resposta:
{
  "msg": "Cliente criado com sucesso!"
}
### 4. **Lista Clientes**
'GET https://mini-projeto-flask-f6k4.onrender.com/clientes'

Headers:
Authorization: Bearer <token_jwt>
Resposta:
'''json
[
  {
    "id": 1,
    "nome": "Cliente Teste"
  }
]

### 5. **Editar cliente**
'PUT https://mini-projeto-flask-f6k4.onrender.com/clientes/1'

Headers:
Authorization: Bearer <token_jwt>
Body:
'''json
{
  "nome": "Cliente Atualizado"
}
Resposta:
{
  "msg": "Cliente atualizado com sucesso!"
}

### 6. **Excluir Cliente**
'DELETE https://mini-projeto-flask-f6k4.onrender.com/clientes/1'

Headers:
Authorization: Bearer <token_jwt>
Resposta:
{
  "msg": "Cliente excluído com sucesso!"
}

### 7. **Estrutura do banco de dados**
Tabela users
    id((Integer, PK)
    usuario (String, único, obrigatório)
    senha (String, hash da senha)
    role (String, padrão "user")

Tabela clientes
    id (Integer, PK)
    nome (String, obrigatório)

### 8. **Evidências de testes**
Todos os endpoints foram validados via Postman:
Registro de usuário
Login com geração de token JWT
CRUD completo de clientes (criar, listar, editar, excluir)

### 9. **Deploy**
A API está disponível publicamente em:
https://mini-projeto-flask-f6k4.onrender.com

### 10. **Autor**
Projeto desenvolvido por Valdessandro Costa Moreira






