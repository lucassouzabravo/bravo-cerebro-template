# Registro de skills

Índice para descoberta. A skill de verdade mora em `skills/{categoria}/{nome}/SKILL.md`; `.claude/skills/` é gerado e **nunca** se edita à mão.

Depois de criar ou alterar qualquer skill:

```bash
python scripts/sync_runtime_adapters.py
```

## Início — rodam uma vez, na configuração

| Skill | O que faz | Ação externa |
|---|---|---|
| `iniciar` | Orquestra a configuração inteira, chamando as seis abaixo na ordem | sim |
| `iniciar-ambiente` | Instala o `gh`, conecta a conta ao GitHub, configura a identidade do git | sim |
| `iniciar-repo` | Cria o repositório pessoal a partir do template e clona o inbox da alçada | sim |
| `iniciar-entrevista` | Entrevista e preenche `SOUL.md`, `USER.md` e `MEMORY.md` | não |
| `iniciar-contexto` | Semeia projetos, pendências, pessoas e o conhecimento da Bravo | não |
| `iniciar-estacao` | Abre a pasta da pessoa dentro do inbox da alçada | sim |
| `iniciar-verificar` | Testa de ponta a ponta e valida o entendimento dos três gatilhos | sim |

## Memória — o dia a dia

| Skill | O que faz | Ação externa |
|---|---|---|
| `cerebro` | Retoma o contexto no começo da sessão e devolve o raio-X | não |
| `salve` | Guarda no cérebro pessoal e propõe o que vale para o cérebro da Bravo | sim |

## Pensamento

| Skill | Quando usar |
|---|---|
| `grilling` | Testar uma decisão que já tem forma. "O que você acha disso?" |
| `idea-refine` | Lapidar uma ideia que ainda está crua demais para virar plano |

## Planejamento

Formam uma cadeia, nesta ordem:

| Skill | Quando usar |
|---|---|
| `brainstorming` | Antes de começar. Por quê, o quê, como, riscos |
| `writing-plans` | A direção está clara e o trabalho tem vários passos |
| `executing-plans` | Existe plano em arquivo para tocar |
| `verification-before-completion` | Antes de dizer que terminou. Sempre |

## As regras deste registro

- **Nome único no cérebro inteiro.** O Claude Code usa uma pasta plana, então duas categorias com o mesmo nome de pasta colidem. O gerador aborta se acontecer.
- **Skill que faz ação externa** (instala, autentica, envia ao GitHub) leva `disable-model-invocation: true` no frontmatter. Ela só roda quando a pessoa pede — nunca por iniciativa do modelo.
- **Skill nova passa pela pessoa antes de nascer.** Skill errada muda comportamento futuro, o que pesa mais que uma anotação errada.
- **Pasta igual não é skill igual.** Antes de renomear, fundir ou apagar, conferir para que ela serve e quem a chama.
