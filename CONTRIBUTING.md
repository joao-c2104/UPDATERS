# 🤝 Guia de Contribuição - UPDATERS

Obrigado por considerar contribuir com o projeto UPDATERS! Este documento fornece um guia completo sobre como configurar, executar e contribuir para o projeto.

---

## 📋 Índice

- [Bem-vindo](#-bem-vindo)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração do Ambiente de Desenvolvimento](#-configuração-do-ambiente-de-desenvolvimento)
- [Como Abrir o Projeto](#-como-abrir-o-projeto)
- [Como Rodar o Projeto](#-como-rodar-o-projeto)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Contribuir](#-como-contribuir)
- [Padrões de Código](#-padrões-de-código)
- [Executando Testes](#-executando-testes)
- [Criando Pull Requests](#-criando-pull-requests)
- [Solução de Problemas](#-solução-de-problemas)
- [Contato](#-contato)

---

## 🎉 Bem-vindo

Somos a **UPDATERS**, um coletivo de designers e desenvolvedores da **CESAR School**. Este projeto é uma plataforma de notícias desenvolvida para modernizar a experiência digital do **Jornal do Commercio**.

Sua contribuição é muito bem-vinda! Este guia foi criado para facilitar sua participação no projeto.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### Obrigatórios:
- **Python 3.10 ou superior** - [Download aqui](https://www.python.org/downloads/)
- **Git** - [Download aqui](https://git-scm.com/downloads)
- **pip** (geralmente vem com Python)

### Opcionais (mas recomendados):
- **Node.js 16+** e **npm** - Para executar testes E2E com Cypress
- **PostgreSQL** - Apenas se quiser testar com banco de dados de produção
- **Editor de código** - Recomendamos VS Code, PyCharm ou qualquer editor de sua preferência

### Verificando as instalações:

```bash
# Verificar Python
python --version
# ou
python3 --version

# Verificar pip
pip --version

# Verificar Git
git --version

# Verificar Node.js (opcional)
node --version
npm --version
```

---

## 🔧 Configuração do Ambiente de Desenvolvimento

### 1️⃣ Clonar o Repositório

Se você ainda não clonou o repositório:

```bash
git clone https://github.com/joao-c2104/UPDATERS.git
cd UPDATERS
```

### 2️⃣ Configurar o Ambiente Python

#### Windows (PowerShell) - Método Automatizado

O projeto possui um script de setup automatizado para Windows:

```powershell
# Execute o script de setup (na raiz do projeto)
.\setup.ps1
```

O script irá:
- Criar o ambiente virtual
- Instalar todas as dependências
- Configurar variáveis de ambiente
- Executar migrações
- Carregar dados iniciais
- Coletar arquivos estáticos

#### Windows (PowerShell) - Método Manual

```powershell
# Navegar para a pasta main
cd main

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Se houver erro de política de execução, execute primeiro:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows (CMD)

```cmd
cd main
python -m venv venv
venv\Scripts\activate.bat
```

#### Linux/Mac

```bash
cd main
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependências Python

Com o ambiente virtual ativado:

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

**Principais dependências instaladas:**
- Django 5.2.7
- Pillow 12.0.0 (processamento de imagens)
- python-decouple 3.8 (variáveis de ambiente)
- django-allauth 65.13.1 (autenticação social)
- whitenoise 6.11.0 (arquivos estáticos)
- gunicorn 23.0.0 (servidor de produção)
- psycopg2-binary 2.9.11 (adaptador PostgreSQL)

### 4️⃣ Configurar Variáveis de Ambiente

Crie um arquivo `.env` na pasta `main/`:

```bash
cd main
copy .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
```

**Gerar uma SECRET_KEY:**

**Opção 1 - Usando Python:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Opção 2 - Gerador online:**
Acesse: https://djecrety.ir/

### 5️⃣ Configurar Banco de Dados

```bash
# Executar migrações
python manage.py migrate

# Carregar dados iniciais (categorias)
python manage.py loaddata feed/fixtures/categories.json
```

### 6️⃣ Criar Superusuário (Admin)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar uma conta de administrador.

### 7️⃣ Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 8️⃣ Instalar Dependências do Cypress (Opcional)

Se você quiser executar os testes E2E:

```bash
# Na raiz do projeto (não na pasta main)
npm install
```

---

## 🚀 Como Abrir o Projeto

### No VS Code

1. Abra o VS Code
2. File → Open Folder
3. Selecione a pasta `UPDATERS`
4. Abra um terminal integrado (Ctrl + `)
5. Navegue para a pasta `main` e ative o ambiente virtual

### No PyCharm

1. File → Open
2. Selecione a pasta `UPDATERS`
3. Configure o interpretador Python:
   - File → Settings → Project → Python Interpreter
   - Selecione o ambiente virtual em `main/venv`

### Em qualquer editor

1. Abra o editor de sua preferência
2. Abra a pasta `UPDATERS`
3. Certifique-se de ativar o ambiente virtual antes de trabalhar

---

## ▶️ Como Rodar o Projeto

### Rodar o Servidor de Desenvolvimento

Com o ambiente virtual ativado e na pasta `main/`:

```bash
python manage.py runserver
```

O servidor estará disponível em:
- **Aplicação**: http://127.0.0.1:8000/
- **Painel Admin**: http://127.0.0.1:8000/admin/

### Rodar em uma porta específica

```bash
python manage.py runserver 8080
```

### Verificar se tudo está funcionando

1. Acesse http://127.0.0.1:8000/
2. Você deve ver a página inicial do projeto
3. Acesse http://127.0.0.1:8000/admin/
4. Faça login com o superusuário criado
5. Verifique se consegue criar e visualizar artigos

---

## 📁 Estrutura do Projeto

```
UPDATERS/
├── main/                          # Projeto Django (raiz)
│   ├── core/                      # Configurações principais
│   │   ├── settings.py           # Configurações do Django
│   │   ├── urls.py               # Roteamento principal
│   │   ├── wsgi.py               # Configuração WSGI
│   │   └── asgi.py               # Configuração ASGI
│   ├── feed/                      # App de notícias
│   │   ├── models.py             # Modelos (Article, Category, etc.)
│   │   ├── views.py              # Views e lógica de negócio
│   │   ├── urls.py               # URLs do app feed
│   │   ├── templates/            # Templates HTML
│   │   ├── static/               # CSS, JS, imagens
│   │   ├── fixtures/             # Dados iniciais
│   │   └── migrations/           # Migrações do banco
│   ├── login/                     # App de autenticação
│   │   ├── models.py             # Modelos de usuário
│   │   ├── views.py              # Views de login/registro
│   │   ├── forms.py              # Formulários
│   │   └── templates/            # Templates de autenticação
│   ├── media/                     # Arquivos enviados pelos usuários
│   ├── staticfiles/               # Arquivos estáticos coletados
│   ├── db.sqlite3                 # Banco de dados SQLite (dev)
│   ├── manage.py                  # Script de gerenciamento Django
│   ├── requirements.txt           # Dependências Python
│   ├── Procfile                   # Configuração para deploy
│   └── .env                       # Variáveis de ambiente (não versionado)
├── cypress/                        # Testes E2E
│   ├── e2e/                       # Testes end-to-end
│   ├── fixtures/                  # Dados de teste
│   └── support/                   # Comandos e configurações
├── imagens/                        # Imagens do projeto
├── links/                          # Documentação adicional
├── package.json                    # Dependências Node.js
├── cypress.config.js              # Configuração do Cypress
├── setup.ps1                       # Script de setup para Windows
├── README.md                       # Documentação principal
└── CONTRIBUTING.md                 # Este arquivo
```

---

## 🤝 Como Contribuir

### Workflow de Contribuição

1. **Fork o repositório** (se você não tem acesso direto)
2. **Crie uma branch** para sua feature/correção
3. **Faça suas alterações**
4. **Teste suas alterações**
5. **Commit suas mudanças**
6. **Push para sua branch**
7. **Abra um Pull Request**

### Criando uma Branch

```bash
# Atualizar a branch main
git checkout main
git pull origin main

# Criar nova branch
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
```

**Convenção de nomes de branches:**
- `feature/` - Para novas funcionalidades
- `fix/` - Para correções de bugs
- `docs/` - Para documentação
- `refactor/` - Para refatoração
- `test/` - Para adicionar testes

### Fazendo Commits

Siga estas diretrizes para commits:

**Formato:**
```
tipo: descrição curta (máx 50 caracteres)

Descrição mais detalhada (opcional, máx 72 caracteres por linha)
```

**Tipos de commit:**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças na documentação
- `style:` - Formatação, ponto e vírgula faltando, etc.
- `refactor:` - Refatoração de código
- `test:` - Adicionar ou corrigir testes
- `chore:` - Tarefas de manutenção

**Exemplos:**
```bash
git commit -m "feat: adiciona sistema de favoritos para artigos"

git commit -m "fix: corrige erro ao salvar imagem do artigo"

git commit -m "docs: atualiza guia de instalação no README"
```

---

## 📝 Padrões de Código

### Python (Django)

- Siga o **PEP 8** (guia de estilo Python)
- Use **4 espaços** para indentação (não tabs)
- Limite de **79 caracteres** por linha (quando possível)
- Use **snake_case** para nomes de variáveis e funções
- Use **PascalCase** para nomes de classes
- Adicione **docstrings** para funções e classes complexas

**Exemplo:**
```python
def get_article_by_id(article_id):
    """
    Retorna um artigo pelo ID.
    
    Args:
        article_id (int): ID do artigo
        
    Returns:
        Article: Objeto do artigo ou None se não encontrado
    """
    try:
        return Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return None
```

### HTML/CSS

- Use **indentação consistente** (2 ou 4 espaços)
- Use **semântica HTML5** adequada
- Mantenha CSS organizado e comentado quando necessário
- Use **classes descritivas** e significativas

### JavaScript (se houver)

- Use **camelCase** para variáveis e funções
- Use **const** e **let** (evite `var`)
- Adicione comentários quando necessário

---

## 🧪 Executando Testes

### Testes Django (Unitários)

```bash
# Executar todos os testes
python manage.py test

# Executar testes de um app específico
python manage.py test feed
python manage.py test login

# Executar um teste específico
python manage.py test feed.tests.TestArticleModel
```

### Testes E2E com Cypress

**Instalar dependências (se ainda não fez):**
```bash
npm install
```

**Abrir interface interativa do Cypress:**
```bash
npx cypress open
```

**Executar testes em modo headless:**
```bash
npm run cy:run
```

**Executar um teste específico:**
```bash
npx cypress run --spec "cypress/e2e/UPDATERS.cy.js"
```

### Verificar o Código

```bash
# Verificar configurações do Django
python manage.py check

# Verificar migrações pendentes
python manage.py showmigrations

# Verificar se há problemas de sintaxe
python -m py_compile main/**/*.py
```

---

## 🔄 Criando Pull Requests

### Antes de Abrir um PR

- [ ] Código segue os padrões do projeto
- [ ] Testes passam localmente
- [ ] Documentação atualizada (se necessário)
- [ ] Commits seguem o padrão estabelecido
- [ ] Branch está atualizada com `main`

### Processo de PR

1. **Atualize sua branch:**
```bash
git checkout main
git pull origin main
git checkout sua-branch
git merge main
```

2. **Resolva conflitos** (se houver)

3. **Teste novamente** após o merge

4. **Push suas alterações:**
```bash
git push origin sua-branch
```

5. **Abra o Pull Request no GitHub:**
   - Vá para o repositório no GitHub
   - Clique em "New Pull Request"
   - Selecione sua branch
   - Preencha o template do PR com:
     - Descrição do que foi feito
     - Como testar
     - Screenshots (se aplicável)
     - Issues relacionadas

### Template de PR

```markdown
## Descrição
Breve descrição das mudanças realizadas.

## Tipo de mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Refatoração
- [ ] Documentação
- [ ] Outro

## Como testar
Passos para testar as mudanças:
1. Passo 1
2. Passo 2
3. Passo 3

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Não há erros de lint
```

---

## 🔧 Solução de Problemas

### Problema: "No module named 'decouple'"

**Solução:**
```bash
# Certifique-se de que o ambiente virtual está ativado
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Instale as dependências novamente
pip install -r requirements.txt
```

### Problema: "SECRET_KEY not found"

**Solução:**
1. Certifique-se de que o arquivo `.env` existe em `main/`
2. Verifique se contém a linha `SECRET_KEY=...`
3. Gere uma nova chave se necessário:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Problema: "No such table: feed_category"

**Solução:**
```bash
# Execute as migrações
python manage.py migrate

# Carregue os dados iniciais
python manage.py loaddata feed/fixtures/categories.json
```

### Problema: Imagens não aparecem

**Solução:**
```bash
# Colete os arquivos estáticos
python manage.py collectstatic --noinput

# Certifique-se de que DEBUG=True no .env
# Verifique se a pasta media/ existe e tem permissões corretas
```

### Problema: Erro ao instalar Pillow no Windows

**Solução:**
```bash
# Tente atualizar o pip primeiro
pip install --upgrade pip

# Instale o Pillow
pip install pillow

# Se ainda falhar, instale Visual C++ Build Tools
# ou use uma wheel pré-compilada
```

### Problema: Erro de política de execução no PowerShell

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: Porta 8000 já está em uso

**Solução:**
```bash
# Use outra porta
python manage.py runserver 8080

# Ou encontre e encerre o processo usando a porta 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: Migrações conflitantes

**Solução:**
```bash
# Verifique o status das migrações
python manage.py showmigrations

# Se necessário, faça um reset (CUIDADO: apaga dados)
# Apenas em desenvolvimento!
python manage.py migrate feed zero
python manage.py migrate login zero
python manage.py migrate
python manage.py loaddata feed/fixtures/categories.json
```

---

## 📞 Contato

### Equipe UPDATERS

- **Product Owner**: Breno Santiago
- **Scrum Master**: Walter Maia
- **Desenvolvedores**: Filipe Correia, João Carlos, João P. Carvalho, João P. Pessôa, Mateus Dornellas
- **Designers**: Antonio Manoel, Artur Prazeres, Gabriel Ribeiro, João Henrique, Thiago Carvalho

### Recursos Adicionais

- **Documentação Django**: https://docs.djangoproject.com/en/5.2/
- **Documentação Cypress**: https://docs.cypress.io/
- **PEP 8 (Style Guide)**: https://pep8.org/
- **Git Flow**: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

### Reportar Problemas

Se encontrar um bug ou tiver uma sugestão:
1. Verifique se já existe uma issue aberta
2. Se não existir, abra uma nova issue no GitHub
3. Use o template de issue apropriado
4. Forneça o máximo de detalhes possível

---

## ✅ Checklist de Setup Completo

Antes de começar a contribuir, certifique-se de que:

- [ ] Python 3.10+ instalado
- [ ] Git instalado e configurado
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências Python instaladas
- [ ] Arquivo `.env` criado e configurado
- [ ] Migrações executadas
- [ ] Dados iniciais carregados
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] Servidor rodando sem erros
- [ ] Acesso ao admin funcionando
- [ ] Testes passando (se aplicável)

---

## 🎯 Próximos Passos

Agora que você tem tudo configurado:

1. **Explore o código** - Entenda a estrutura do projeto
2. **Leia as issues** - Veja o que precisa ser feito
3. **Escolha uma tarefa** - Comece com algo pequeno se for sua primeira contribuição
4. **Peça ajuda** - Não hesite em perguntar à equipe
5. **Divirta-se!** - Contribuir para projetos open source é uma experiência incrível

---

**Obrigado por contribuir com o UPDATERS! 🚀**

*Última atualização: Janeiro 2025*

