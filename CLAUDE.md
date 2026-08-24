# CLAUDE.md

Este repositório é o cérebro de trabalho de **{PESSOA}**. Você opera a partir dele.

> **Primeira vez aqui?** Se `SOUL.md` ainda tiver `{AGENTE}` e outros marcadores entre chaves, o cérebro não foi iniciado. Rode `/iniciar` antes de qualquer outra coisa e conduza a pessoa por ele.

## Boot

Leia nesta ordem:

@SOUL.md
@USER.md
@MEMORY.md
@MAPA.md
@AGENTS.md

Depois abra `memory/hot.md`, a nota mais recente de `memory/`, `memory/context/pendencias.md` e as fichas de projeto que estiverem no foco quente.

Antes de usar integração, credencial, CLI ou ferramenta externa, leia `TOOLS.md`. Ele é catálogo sob demanda e **nunca** contém valores de segredo.

## Regras do runtime

- Skills canônicas vivem em `skills/{categoria}/{nome}/SKILL.md`. `.claude/skills/` é apenas a camada de descoberta do Claude Code, gerada por `scripts/sync_runtime_adapters.py` — nunca editar lá.
- `/iniciar` configura o cérebro na primeira vez. Roda uma vez só, mas é seguro repetir.
- `/cerebro` retoma o contexto no começo da sessão.
- `/salve` guarda o que foi feito e envia ao GitHub.
- Memória importante é salva proativamente, sem esperar o comando.
- Alteração local e reversível pode avançar sozinha. **Push, envio de mensagem, publicação e qualquer ação externa exigem pedido explícito da pessoa.**

## Os dois cérebros

| Cérebro | O que é | Quem escreve |
|---|---|---|
| **Este repositório** | O cérebro pessoal de {PESSOA}. Privado. | Só {PESSOA} |
| **Inbox da alçada `{ALCADA}`** | A porta de entrada do cérebro coletivo da Bravo | Quem é da mesma alçada |

O conhecimento coletivo validado da Bravo vive em outro repositório, fechado. Daqui só se **envia** — pelo `/salve`, com confirmação. Nunca se lê nem se edita o canônico a partir daqui.
