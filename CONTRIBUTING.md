#  Contribuindo com o UPDATERS

Obrigado por querer ajudar no projeto!  
Aqui estão as instruções básicas para conseguir rodar tudo localmente e colaborar com a equipe.

---

##  Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/joao-c2104/UPDATERS.git
cd UPDATERS/main
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
```

Ativar:

- Windows: `.env\Scripts\Activate.ps1`
- Linux/Mac: `source venv/bin/activate`

Instalar dependências:

```bash
pip install -r requirements.txt
```

### 3. Criar o arquivo `.env`

Crie `main/.env` baseado no `.env.example`.

Gerar SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Migrar o banco e preparar o ambiente

```bash
python manage.py migrate
python manage.py loaddata feed/fixtures/categories.json
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 5. Rodar o servidor

```bash
python manage.py runserver
```

Acesse o app em: http://127.0.0.1:8000

---

## Como contribuir

### Branches

Use nomes simples, tipo:

- `feature/nome-da-feature`
- `fix/nome-do-bug`
- `docs/`
- `refactor/`

### Commits

Tente seguir o estilo:

- `feat: adiciona função X`
- `fix: corrige bug Y`
- `docs: atualiza documentação`

Nada muito formal, só que dê pra entender.

### Pull Requests

Antes de abrir:

1. Atualize sua branch com a `main`
2. Teste sua alteração
3. Escreva um resumo do que mudou

---

##  Testes

Rodar testes do Django:

```bash
python manage.py test
```

---

##  Problemas comuns

| Problema | Solução |
|----------|---------|
| Module not found | Ative a venv e instale dependências |
| SECRET_KEY not found | Verifique se o `.env` existe |
| No such table | Rode `python manage.py migrate` |
| Imagens não aparecem | `python manage.py collectstatic` |
| Porta 8000 ocupada | `python manage.py runserver 8080` |

---

## 👥 Time UPDATERS

Breno Santiago, Walter Maia, Filipe, João Carlos, João Carvalho,  
João Pessôa, Mateus, Antonio, Artur, Gabriel, João Henrique, Thiago
