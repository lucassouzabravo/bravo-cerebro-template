---
name: salve
description: >
  Guarda o que acabou de ser feito no lugar certo do cérebro e envia ao GitHub. Depois,
  separa o que é conhecimento da Bravo, mostra a lista em linguagem normal com o motivo
  de cada item, e — só com a confirmação da pessoa — envia ao inbox da alçada dela.
  Bloqueia sozinho material que dispara os três gatilhos.
  Triggers: "/salve", "salva isso", "guarda isso", "registra aí".
disable-model-invocation: true
---

# /salve

> Duas fases. A **A** guarda no seu cérebro e sempre acontece. A **B** propõe o que vale para o cérebro coletivo da Bravo e **nunca acontece sem você confirmar**.

`disable-model-invocation` porque envia para o GitHub. Ação externa só roda quando você pede.

---

# FASE A — o seu cérebro

## A1. O que vale guardar

Varrer a conversa procurando o que vai continuar útil depois que ela fechar: decisão tomada, pendência que nasceu ou fechou, mudança de estado de projeto, coisa nova sobre uma pessoa, conhecimento da Bravo que foi explicado.

**O que não guardar:** pergunta solta, teste, conversa que não mudou nada. Cérebro poluído fica tão inútil quanto cérebro vazio.

## A2. Para onde vai cada coisa

O `MAPA.md` é a fonte. Se ele e esta tabela divergirem, **o MAPA vence**.

| O que é | Vai para |
|---|---|
| Decisão | `memory/context/decisoes/{AAAA-MM}.md` (acrescenta no fim) |
| Pendência | `memory/context/pendencias.md` (acrescenta no fim) |
| Estado de projeto | `memory/projects/{nome}.md` |
| Pessoa | `memory/context/people/{nome}.md` |
| Conhecimento da Bravo | `memory/context/bravo/{assunto}.md` |
| Contexto de um tema | `memory/context/{tema}/` |
| Entregável produzido | `content/drafts/{nome}/` |
| Nota do dia | `memory/{AAAA-MM-DD}.md` |
| **Em dúvida** | **perguntar** |

Classificar sozinho quando é óbvio; perguntar quando não casa limpo. Pasta nova só com parcimônia — e quando nascer, ela nasce com `MAPA.md` (incluindo o campo **Sensibilidade**), e a linha dela entra no `MAPA.md` da raiz.

## A3. Escrever

Criar a pasta antes de escrever — pasta vazia não vem do git:

```bash
mkdir -p "$(dirname {arquivo})"
```

Atualizar o `memory/hot.md` se o foco mudou, **incluindo o título com a data de hoje**.

## A4. Enviar

```bash
CEREBRO="$(git rev-parse --show-toplevel)"
cd "$CEREBRO"

# caminhos explícitos, só o que este /salve escreveu.
# NUNCA `git add .` nem `git add -A`.
git add "memory/context/decisoes/$(date +%Y-%m).md" "memory/context/pendencias.md"

git commit -m "salve: {o que foi guardado, em uma linha}"
git pull --rebase
git push
```

> ⚠️ **Por que caminho explícito.** Um `.env`, uma senha colada num arquivo de texto, um print com token — qualquer arquivo solto na pasta entraria junto e ficaria **permanente** no histórico do GitHub. Apagar depois não resolve: o histórico guarda.

Se o `pull --rebase` reclamar de mudança não commitada, é trabalho de outra sessão: `git stash push -u`, rebase, push, `git stash pop`. Nunca commitar o que não é seu.

Se der conflito, ver `referencias/conflito.md`.

---

# FASE B — o cérebro da Bravo

Só roda se `~/bravo/inbox` existir. Se não existir, dizer em uma linha que o acesso ainda não saiu e encerrar na Fase A — sem transformar isso em erro.

## B1. Bloquear antes de classificar

**Primeiro os gatilhos, sempre.** Antes de pensar em camada, antes de montar lista.

| # | Gatilho | Exemplos |
|---|---|---|
| 1 | Dinheiro com nome de gente | salário, comissão, bônus individual, quanto alguém ganhou |
| 2 | Avaliação de pessoa específica | feedback, desempenho, conflito, contratação, desligamento |
| 3 | Peso jurídico ou contratual sensível | acordo de sócios, NDA, litígio, processo, advocacia |

**Não é gatilho:** contrato operacional comum — hospedagem, SaaS, gateway, fornecedor padrão. Isso é conhecimento da operação e pode ir.

**Número de área não é gatilho 1.** "A equipe bateu 87% da meta" pode ir. "O Marcelo ganhou R$ 4.200 de comissão" não pode. A diferença é o nome próprio ligado ao valor.

O que dispara gatilho **sai da lista antes de a lista existir**. Não vira pergunta, não vira opção, não aparece na confirmação. Aparece só no bloco "ficou de fora", com o motivo.

## B2. Classificar o que sobrou

Só entra o que é **conhecimento da empresa** — coisa que outra pessoa da Bravo precisaria saber para trabalhar. Não entra rascunho, anotação pessoal, opinião, nem estado de projeto seu.

O filtro é uma pergunta: **isso responde a alguma destas?** Ler as camadas de `.cerebro.yml`:

| Camada | A pergunta que ela responde |
|---|---|
| Inventário | o que existe aqui |
| Tarefas | o que se faz, passo a passo |
| Papéis | quem faz e o que pode decidir |
| Domínio | o que esse termo quer dizer |
| Julgamento | como uma decisão real foi tomada |
| Passagens | quem entrega o quê para quem |

Se não responde a nenhuma, não sobe. Na dúvida entre duas camadas, escolher e seguir — a classificação é **sugestão**, quem decide o destino final é a auditoria do lado da Bravo.

> ⚠️ A numeração das camadas tem um buraco de propósito. **Nunca oferecer camada 6** — ela está em revisão no cérebro coletivo. Ler sempre de `.cerebro.yml`, nunca de memória.

Ser generoso aqui é o certo: é melhor subir uma coisa a mais, que a auditoria descarta, do que perder conhecimento que só existia naquela conversa.

## B3. O report — o formato importa tanto quanto o conteúdo

Esta é a tela que a pessoa vai ver todos os dias. **Ela decide se o hábito pega ou morre.**

Regras do report:

- **tabela, nunca texto corrido.** Sem parágrafo, sem "conforme identificado", sem voz de sistema;
- **linguagem normal.** Nunca dizer "camada 4-dominio" e parar aí — dizer o nome e o que ela quer dizer;
- **o porquê é obrigatório**, e é específico daquele item. "É relevante" não é motivo;
- **cabe numa tela.** Se passar de 6 itens, agrupar e dizer quantos;
- **o que ficou de fora aparece**, com o motivo. É esse bloco que ensina a pessoa a separar sozinha;
- **uma confirmação só**, no fim.

Modelo:

```
Separei 3 coisas de hoje que fazem sentido pro cérebro da Bravo:

| O que é | Onde encaixa | Por que vale subir |
|---|---|---|
| Como você monta o relatório de gap semanal | Tarefas — o que se faz, passo a passo | Você descreveu o processo inteiro e ele não está escrito em lugar nenhum |
| O que significa "monto alto" | Domínio — o que um termo quer dizer | Apareceu 4x hoje e ninguém de fora entenderia |
| Quem aprova desconto acima de 30% | Papéis — quem decide o quê | Define uma alçada que hoje só existe na cabeça de quem já trabalha aqui |

Ficou de fora:
· A conversa sobre a entrega do Marcelo — é avaliação de pessoa, não sai daqui.
· Seus rascunhos de e-mail — pessoais, ficam só no seu cérebro.

Sobe tudo? [Enter = sim] · tirar algum? me diz qual
```

**Se ela tirar um item, tirar sem perguntar por quê.** Não insistir, não argumentar, não perguntar de novo no próximo `/salve`.

**Se ela não responder nada, não sobe.** Silêncio não é confirmação.

## B4. Copiar e fichar

Para cada item confirmado:

```bash
INBOX=~/bravo/inbox
SLUG={slug do .cerebro.yml}
STAMP=$(date +%Y-%m-%d-%H%M)
DEST="$INBOX/$SLUG/${STAMP}-{assunto}.md"
cp "{arquivo original}" "$DEST"
```

O arquivo de conteúdo vai **limpo**, sem cabeçalho de metadados. Toda a ficha técnica mora no arquivo-par, para o conteúdo poder ser promovido intacto depois:

```yaml
# arquivo: $DEST.meta.yaml
autor: {slug}
data: {ISO com fuso}
fonte: salve
tipo: nota
maturidade: cru
camada_sugerida: {id da camada}
destino_sugerido:
gatilhos_triados:
  dinheiro_pessoa: nao
  avaliacao_pessoa: nao
  juridico_sensivel: nao
relacionado:
  - pessoal:{caminho no cérebro dela}
tags: [salve]
```

**Só `.md`.** Anexo, imagem, planilha e PDF não vão — vira uma linha de referência dentro do markdown. Binário no histórico do git incha o repositório de todo mundo da alçada, para sempre.

## B5. Enviar

```bash
cd "$INBOX"
git checkout staging 2>/dev/null || git checkout -b staging
git pull --rebase origin staging

# só a própria pasta. NUNCA `git add .` nem `-A`.
git add "$SLUG/"
git commit -m "salve: $SLUG ({N} capturas)"
git push origin staging
```

Confirmar no destino, e mostrar a saída:

```bash
git ls-tree --name-only origin/staging "$SLUG/" | tail -5
```

O `push` responder sem erro prova que a chamada foi aceita, não que o conteúdo chegou. Quem prova é a leitura do remoto.

Voltar para o cérebro pessoal ao terminar.

---

## Fechamento

```
✓ Guardado no seu cérebro
    {N} arquivos · {commit}

✓ Enviado pro inbox da {alçada}
    {M} capturas · {commit}
    {K} ficaram só aqui
```

Se a Fase B não rodou, dizer por quê em uma linha — sem transformar em alarme.

---

## Quando algo não funciona

| Sintoma | Causa | O que fazer |
|---|---|---|
| Pede usuário e senha no push | Credencial do git não configurada | `gh auth setup-git` |
| `non-fast-forward` | Outra máquina, ou colega da alçada, enviou antes | `git pull --rebase` e repetir. **Nunca `--force`** |
| Conflito no rebase | Os dois lados escreveram no mesmo arquivo | Ver `referencias/conflito.md` |
| `Permission denied` no inbox | Acesso da alçada não liberado | Anotar pendência (dono: Lucas) e encerrar na Fase A |
| Nada foi classificado como Bravo | Normal em dia de trabalho interno | Dizer numa linha e não insistir |
| A pessoa pediu para não subir nada hoje | Prerrogativa dela | Encerrar na Fase A sem perguntar de novo |
| Um item que ela tirou ontem reaparece | Defeito — não repropor o que foi recusado | Registrar a recusa e não oferecer de novo |

## O que esta skill não faz

Não varre a conversa atrás de coisa para perguntar "quer guardar isso?" o tempo todo. Não sobe nada sozinha. Não lê nem edita o cérebro coletivo da Bravo — daqui só se envia, e só para a sua pasta dentro do inbox da sua alçada.
