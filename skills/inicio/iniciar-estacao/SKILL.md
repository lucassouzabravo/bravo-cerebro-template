---
name: iniciar-estacao
description: >
  Abre a estação da pessoa dentro do inbox da alçada dela — cria a pasta com o slug,
  o README e o modelo de ficha técnica, e deixa as slash commands disponíveis no layout
  ~/bravo/. Chamada pelo /iniciar no passo 6. Depende do iniciar-repo e do iniciar-entrevista.
  Triggers: "/iniciar-estacao", "cria minha pasta no inbox".
disable-model-invocation: true
---

# iniciar-estacao

> Passo 6 do `/iniciar`. Escreve e envia no repositório da alçada — ação externa.

## Pré-condições

| O que | Como conferir | Se faltar |
|---|---|---|
| Inbox clonado | `test -d ~/bravo/inbox/.git` | Acesso ainda não liberado — anotar pendência e **parar aqui**, sem travar o resto |
| `.cerebro.yml` preenchido | `grep -c '{' ~/bravo/pessoal/.cerebro.yml` = 0 | Voltar ao `iniciar-repo` |
| Slug definido | campo `alcada.slug` | Voltar ao `iniciar-entrevista` |

---

## Passo 1 — Criar a estação

O slug é o primeiro nome em minúsculas, sem acento. Ele identifica a pessoa dentro do inbox.

```bash
INBOX=~/bravo/inbox
SLUG={slug}
mkdir -p "$INBOX/$SLUG"
```

Escrever `$INBOX/$SLUG/README.md`:

```markdown
# Estação de {Pessoa}

- **Alçada:** {alçada}
- **Área:** {área}
- **Aberta em:** {data}

O que chega aqui vem do `/salve` do cérebro pessoal de {Pessoa}, sempre com
confirmação dela. Cada captura tem um arquivo-par `.meta.yaml` com a ficha
técnica: quando entrou, de onde veio, e em qual camada parece encaixar.

Material que dispara os três gatilhos — dinheiro com nome de gente, avaliação
de pessoa específica, ou peso jurídico — **não passa por aqui**. Fica no
cérebro pessoal.
```

---

## Passo 2 — Enviar a estação

Trabalhar em `staging` e adicionar **só a própria pasta**:

```bash
cd "$INBOX"
git checkout staging 2>/dev/null || git checkout -b staging
git pull --rebase origin staging 2>/dev/null || true

# caminho explícito. NUNCA `git add .` nem `git add -A`.
git add "$SLUG/"
git commit -m "estacao: abre $SLUG"
git push origin staging
```

> ⚠️ **O `git add` com caminho explícito não é preciosismo.** O inbox é compartilhado com as outras pessoas da alçada. Um `git add .` levaria junto qualquer arquivo solto na pasta — inclusive material de colega que veio no `pull`, ou um arquivo com credencial que caiu ali por acidente. E o histórico do git guarda para sempre.

Confirmar no remoto, e **mostrar a saída**:

```bash
git ls-tree --name-only origin/staging "$SLUG/"
```

Se a pasta aparecer ali, chegou de verdade. Ler a resposta do `push` não prova nada — ela diz que a chamada foi aceita, não que o conteúdo está lá.

---

## Passo 3 — Deixar os comandos à mão

O Claude Code descobre skills a partir da pasta em que foi aberto. Como a pessoa vai abrir em `~/bravo/`, os comandos do cérebro pessoal precisam estar alcançáveis de lá:

```bash
mkdir -p ~/bravo/.claude
ln -sfn ~/bravo/pessoal/.claude/skills ~/bravo/.claude/skills
ls -l ~/bravo/.claude/skills
```

No Windows, se o link simbólico falhar por falta de permissão, não insistir: instruir a pessoa a abrir o Claude Code direto em `~/bravo/pessoal/` e registrar em `TOOLS.md` que o inbox fica alcançável pelo caminho absoluto. Funciona igual, só é menos elegante.

---

## Passo 4 — Confirmação

```
Estação aberta:

  ✓ Pasta       inbox/{slug}/
  ✓ No remoto   confirmado em origin/staging
  ✓ Comandos    /cerebro e /salve disponíveis em ~/bravo/

  A partir daqui, o /salve já sabe pra onde mandar as coisas da Bravo.
```

## Quando algo não funciona

| Sintoma | Causa | O que fazer |
|---|---|---|
| `Permission denied` no push | Acesso de escrita não liberado na alçada | Anotar pendência com dono Lucas. O cérebro pessoal segue funcionando |
| `non-fast-forward` | Outra pessoa da alçada enviou antes | `git pull --rebase origin staging` e repetir. **Nunca `--force`** |
| A pasta já existe no remoto | Estação de máquina anterior | Reaproveitar, não recriar. Confirmar com a pessoa que é ela mesma |
| Link simbólico falhou no Windows | Falta permissão de criar link | Abrir o Claude Code em `~/bravo/pessoal/` e registrar em `TOOLS.md` |
