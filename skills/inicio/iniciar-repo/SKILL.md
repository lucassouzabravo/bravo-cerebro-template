---
name: iniciar-repo
description: >
  Cria o repositório pessoal da pessoa a partir do template, coloca a pasta no layout
  ~/bravo/, clona o inbox da alçada dela ao lado, e preenche o .cerebro.yml com os
  endereços. Chamada pelo /iniciar no passo 3. Depende do iniciar-ambiente.
  Triggers: "/iniciar-repo", "cria meu repositório".
disable-model-invocation: true
---

# iniciar-repo

> Passo 3 do `/iniciar`. Cria repositório no GitHub — ação externa, por isso `disable-model-invocation`.

## Pré-condição

`gh auth status` tem que responder autenticado. Se não responder, voltar para `iniciar-ambiente` — não tentar contornar.

## O layout

Tudo em `~/bravo/`, lado a lado. Motivo prático: o Claude Code lê o `CLAUDE.md` da pasta em que foi aberto e das pastas acima, **mas não desce em subpastas**. Abrindo em `~/bravo/`, os dois cérebros ficam alcançáveis.

```
~/bravo/
├── pessoal/   ← o cérebro dela
└── inbox/     ← o inbox da alçada
```

---

## Passo 1 — Detectar

```bash
echo "--- layout ---"; ls -d ~/bravo/pessoal ~/bravo/inbox 2>/dev/null || echo "AUSENTE"
echo "--- onde estou ---"; git rev-parse --show-toplevel 2>/dev/null || echo "FORA DE REPO"
echo "--- remote atual ---"; git remote -v 2>/dev/null | head -2
```

Se `~/bravo/pessoal` já existe e tem remote próprio, o repositório já foi criado. Confirmar com a pessoa e pular para o Passo 4.

---

## Passo 2 — Criar o repositório pessoal

Perguntar o nome. Sugerir um padrão e deixar mudar:

> "Como você quer chamar o seu repositório? Sugiro `cerebro-{primeiro-nome}`. Ele vai ser **privado** — só você enxerga."

Criar a partir deste template:

```bash
gh repo create {nome} --private --template lucassouzabravo/bravo-cerebro-template --clone
```

> ⚠️ **`--private` não é opcional.** Este cérebro vai guardar contexto de trabalho da pessoa. Se o comando falhar, corrigir e repetir — nunca cair para público como alternativa.

Mover para o layout, sem apagar nada que já esteja lá:

```bash
mkdir -p ~/bravo
[ -e ~/bravo/pessoal ] && echo "JA EXISTE — parar e perguntar" || mv {nome} ~/bravo/pessoal
```

Conferir e mostrar:

```bash
git -C ~/bravo/pessoal remote -v
git -C ~/bravo/pessoal log --oneline -1
```

---

## Passo 3 — Clonar o inbox da alçada

Ler a alçada do `.cerebro.yml` (bloco `alcadas`) e clonar o repositório correspondente:

```bash
gh repo clone {repo-da-alcada} ~/bravo/inbox
```

**Se der erro de permissão**, é o caso esperado quando o acesso ainda não saiu. Não é falha da configuração:

> "O acesso ao inbox da {alçada} ainda não foi liberado pra sua conta. Isso é normal — quem libera é o Lucas (AI Operation). Vou seguir com o resto e deixar isso anotado; quando o acesso sair, a gente fecha em 1 minuto."

Anotar em `memory/context/pendencias.md` com dono (Lucas) e condição de fechamento (o clone funcionar), e **seguir**. O cérebro pessoal funciona 100% sem isso; só a Fase B do `/salve` fica esperando.

Se funcionou, garantir a branch de trabalho:

```bash
git -C ~/bravo/inbox checkout staging 2>/dev/null || git -C ~/bravo/inbox checkout -b staging
```

O inbox trabalha em `staging`. A `main` dele só muda pela consolidação do lado da Bravo.

---

## Passo 4 — Preencher o `.cerebro.yml`

Editar `~/bravo/pessoal/.cerebro.yml`, bloco `pessoal` e bloco `alcada`, com os valores reais. O `slug` é o primeiro nome em minúsculas, sem acento — é o nome da pasta dela dentro do inbox.

**Mostrar o arquivo depois de escrever** e confirmar que não sobrou marcador entre chaves:

```bash
grep -n '{' ~/bravo/pessoal/.cerebro.yml || echo "OK — nenhum marcador pendente"
```

---

## Passo 5 — Confirmação

```
Repositórios prontos:

  ✓ Seu cérebro    ~/bravo/pessoal  →  {url}  (privado)
  ✓ Inbox {alçada} ~/bravo/inbox    →  {url}  (branch staging)

  A partir de agora, abra o Claude Code em ~/bravo/ — não dentro de
  uma das duas pastas. É de lá que eu enxergo os dois.
```

Se o inbox ficou pendente, trocar a segunda linha por `⏳ Inbox {alçada} — aguardando liberação de acesso (Lucas)`.

---

## Quando algo não funciona

| Sintoma | Causa | O que fazer |
|---|---|---|
| `could not create repository: Name already exists` | Já tem um repo com esse nome | Perguntar outro nome, ou confirmar se é o mesmo cérebro |
| `HTTP 404` ao clonar o inbox | Acesso não liberado | Anotar pendência e seguir — não é erro de configuração |
| `~/bravo/pessoal` já existe com conteúdo | Configuração anterior, ou pasta de outra coisa | **Parar e perguntar.** Nunca sobrescrever |
| Repo criado público por engano | `--private` faltou | `gh repo edit {repo} --visibility private --accept-visibility-change-consequences` na hora |
