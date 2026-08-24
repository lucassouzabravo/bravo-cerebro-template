---
name: iniciar-repo
description: >
  Cria o repositório pessoal a partir do template (pelo navegador, sem instalar nada),
  coloca a pasta no layout ~/bravo/, clona o inbox da alçada ao lado, e preenche o
  .cerebro.yml com os endereços. Chamada pelo /iniciar no passo 3.
  Triggers: "/iniciar-repo", "cria meu repositório".
disable-model-invocation: true
---

# iniciar-repo

> Passo 3 do `/iniciar`.

## Como o repositório é criado, e por que assim

**Pelo navegador, com o botão "Use this template" do GitHub.** A pessoa clica, escolhe o nome, marca como privado, e pronto.

Existe um programa (`gh`) que faria isso por comando, mas ele é **mais um software para instalar e aprovar em máquina corporativa** — e não resolve nada que o navegador não resolva em 30 segundos. O que a gente precisa de verdade do terminal é clonar e enviar, e isso o git comum faz sozinho.

---

## O layout

Tudo em `~/bravo/`, lado a lado:

```
~/bravo/
├── pessoal/   ← o cérebro dela
└── inbox/     ← o inbox da alçada
```

Motivo prático: o Claude Code lê o `CLAUDE.md` da pasta em que foi aberto e das pastas **acima**, mas não desce em subpastas. Abrindo em `~/bravo/`, os dois ficam alcançáveis.

---

## Passo 1 — Detectar

```bash
echo "--- layout ---"; ls -d ~/bravo/pessoal ~/bravo/inbox 2>/dev/null || echo "AUSENTE"
echo "--- onde estou ---"; git rev-parse --show-toplevel 2>/dev/null || echo "FORA DE REPO"
echo "--- remote ---"; git remote -v 2>/dev/null | head -2
```

Se `~/bravo/pessoal` já existe com remote próprio, o repositório já foi criado. Confirmar e pular para o Passo 4.

---

## Passo 2 — Criar o repositório pessoal

Perguntar o nome primeiro:

> "Como você quer chamar o seu repositório? Sugiro `cerebro-{primeiro-nome}`. Ele vai ser **privado** — só você enxerga."

Depois, dar as instruções **uma por vez**, e esperar ela dizer que terminou:

> "Abre este link: **github.com/lucassouzabravo/bravo-cerebro-template**
>
> 1. Clica no botão verde **Use this template** → **Create a new repository**
> 2. Em *Repository name*, põe `{nome escolhido}`
> 3. Marca **Private** ⚠️ isso não é opcional — o cérebro guarda contexto do seu trabalho
> 4. Clica em **Create repository**
> 5. Me manda o endereço que aparecer na barra do navegador"

> ⚠️ **Se o botão "Use this template" não aparecer**, é falta de acesso ao template — ele é privado. Não é erro dela. Anotar pendência e avisar: *"o Lucas precisa te liberar leitura no template. Vou seguir com o resto e a gente fecha isso quando o acesso sair."*

Com o endereço em mãos, clonar:

```bash
mkdir -p ~/bravo
[ -e ~/bravo/pessoal ] && echo "JA EXISTE — parar e perguntar" \
  || git clone "https://github.com/{usuario}/{nome}.git" ~/bravo/pessoal
```

> Este é o momento em que a **janela do navegador pode abrir** pedindo para entrar no GitHub. É o Credential Manager conectando a conta, e acontece uma vez só. Avise antes, para ela não se assustar.

Conferir, e mostrar:

```bash
git -C ~/bravo/pessoal remote -v
git -C ~/bravo/pessoal log --oneline -1
ls ~/bravo/pessoal
```

---

## Passo 3 — Clonar o inbox da alçada

Ler a alçada no `.cerebro.yml` (bloco `alcadas`) e clonar o repositório correspondente:

```bash
git clone "https://github.com/lucassouzabravo/bravo-inbox-{alcada}.git" ~/bravo/inbox
```

**Se der erro de permissão**, é o caso esperado quando o acesso ainda não saiu. Não é falha da configuração:

> "O acesso ao inbox da {alçada} ainda não foi liberado pra sua conta. Isso é normal — quem libera é o Lucas (AI Operation). Vou seguir com o resto e deixar anotado; quando o acesso sair, a gente fecha em 1 minuto."

Anotar em `memory/context/pendencias.md` com dono (Lucas) e condição de fechamento, e **seguir**. O cérebro pessoal funciona 100% sem isso; só a Fase B do `/salve` fica esperando.

Se funcionou, garantir a branch de trabalho:

```bash
git -C ~/bravo/inbox checkout staging 2>/dev/null || git -C ~/bravo/inbox checkout -b staging
```

---

## Passo 4 — Preencher o `.cerebro.yml`

Editar `~/bravo/pessoal/.cerebro.yml`, blocos `pessoal` e `alcada`, com os valores reais. O `slug` é o primeiro nome em minúsculas, sem acento.

**Mostrar o arquivo depois de escrever** e provar que não sobrou marcador:

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
| O botão "Use this template" não aparece | Sem acesso de leitura no template | Pendência com dono Lucas. Seguir o resto |
| `Repository not found` ao clonar | Nome errado, ou repo criado em outra conta | Conferir o endereço que ela mandou |
| `HTTP 403` ao clonar o inbox | Acesso da alçada não liberado | Anotar pendência e seguir — não é erro de configuração |
| `~/bravo/pessoal` já existe com conteúdo | Configuração anterior, ou outra coisa | **Parar e perguntar.** Nunca sobrescrever |
| A janela de login não abre e o terminal pede senha | Credential Manager desligado | Voltar ao `iniciar-ambiente`, passo 2.1 |
| Repositório criado público por engano | `Private` não foi marcado | Corrigir na hora: Settings → General → Danger Zone → Change visibility |
