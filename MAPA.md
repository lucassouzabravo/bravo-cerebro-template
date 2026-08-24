# MAPA.md

O índice do cérebro. Quando não souber onde uma coisa mora, a resposta está aqui.

## Arquitetura

```text
SOUL.md      quem eu sou, como penso, meu tom e meus limites
USER.md      quem é {PESSOA} e como trabalhamos
MEMORY.md    contexto durável essencial e onde retomar
MAPA.md      este arquivo — o índice
AGENTS.md    como eu opero, o que faço sozinho e onde eu paro
TOOLS.md     ferramentas, integrações e onde as credenciais moram (nunca o valor)
CREDITOS.md  licenças de terceiros

memory/      contexto e estado
content/     artefatos e entregáveis
skills/      procedimentos repetíveis
.claude/     descoberta de skills pelo Claude Code (gerado)
scripts/     utilitários do próprio cérebro
```

## Onde salvar cada coisa

| O que | Vai para |
|---|---|
| Nota do dia | `memory/AAAA-MM-DD.md` |
| Decisão tomada | `memory/context/decisoes/AAAA-MM.md` |
| Pendência (com dono e condição de fechamento) | `memory/context/pendencias.md` |
| Estado e próximo passo de um projeto | `memory/projects/{nome}.md` |
| Entregável, rascunho, arquivo produzido | `content/drafts/{nome}/` |
| Projeto ou conteúdo concluído | `content/archive/{nome}/` |
| Pessoa com quem trabalho | `memory/context/people/{nome}.md` |
| Contexto da Bravo | `memory/context/bravo/` |
| Contexto de um tema recorrente | `memory/context/{tema}/` |
| Procedimento que vou repetir | `skills/{categoria}/{nome}/SKILL.md` |
| Ferramenta, integração ou **onde** a credencial mora | `TOOLS.md` — só o nome da variável, nunca o valor |
| Segredo, token, senha, chave | **Fora do repositório.** Arquivo `.env` local, que o `.gitignore` bloqueia |

## O orçamento dos arquivos-raiz

`USER.md` e `MEMORY.md` são lidos em **toda** sessão. Por isso têm teto de tamanho:

| Arquivo | Teto | O que fazer com o que não cabe |
|---|---|---|
| `USER.md` | **1375 caracteres** | vai para `memory/context/people/{slug}.md` |
| `MEMORY.md` | **2200 caracteres** | vai para `memory/context/` |

Não é limitação técnica — é economia de atenção. Espaço gasto com detalhe que raramente importa é espaço que falta pro trabalho do dia. O `/cerebro` confere e avisa quando estourar.

## Regra dos mapas

Cada pasta importante tem o próprio `MAPA.md` local. O mapa da raiz aponta para as pastas; quem descreve o conteúdo é o mapa de dentro.

Isso existe porque um índice único e gigante cresce sem controle, duplica informação e desatualiza em silêncio. Mapa perto do conteúdo envelhece junto com ele.

**Pasta de tema nova nasce com `MAPA.md`** contendo: Objetivo · Quando usar · Quando NÃO usar · **Sensibilidade** · Mapa rápido.

O campo **Sensibilidade** diz se o conteúdo daquela pasta pode ir para o cérebro coletivo da Bravo, e é o que o `/salve` consulta antes de propor qualquer envio.

## Regra do índice único

Quando um mapa novo nasce cobrindo um território, o mapa antigo que cobria o mesmo território **vira ponteiro**, nunca cópia paralela. Dois índices do mesmo lugar divergem, e o dia em que divergirem ninguém vai saber qual está certo.
