---
name: cerebro
description: >
  Retoma o contexto no começo da sessão: confere a conexão, puxa o que mudou no GitHub,
  lê os arquivos-raiz e o que está quente em memory/, e devolve um raio-X do trabalho —
  o que foi feito, o que ficou decidido, o que está em aberto e qual o próximo passo.
  Use ao abrir o Claude Code, no começo do dia, ou quando começar uma conversa nova.
  Triggers: "/cerebro", "me atualiza", "onde a gente parou", "carrega meu contexto".
---

# /cerebro

> Acordar e lembrar de tudo. Não é relatório de máquina: é o momento em que eu volto a saber quem você é e no que estamos.

## Passo 0 — A conexão está de pé?

Rodar e **mostrar a saída**:

```bash
CEREBRO="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$CEREBRO" ]; then echo "SEM_REPO"; else
  echo "CEREBRO=$CEREBRO"
  git -C "$CEREBRO" remote -v | head -1
  ls "$CEREBRO"/{SOUL,USER,MEMORY,MAPA,AGENTS}.md 2>/dev/null
  ls -d "$CEREBRO"/memory/{context,projects} 2>/dev/null
fi
```

Interpretar **em linguagem normal**, nunca em jargão de git:

| O que apareceu | O que dizer |
|---|---|
| `SEM_REPO` | "Não achei o cérebro por aqui. Você abriu o Claude Code na pasta certa? Ele mora em `~/bravo/pessoal`." |
| Sem remote | "Seu cérebro está no computador mas não está ligado ao GitHub — então ele não tem cópia fora daqui. Quer que eu ligue?" |
| Falta arquivo-raiz | "Faltam alguns arquivos base. Parece que a configuração não terminou — quer rodar o `/iniciar`?" |
| Marcadores `{}` nos arquivos-raiz | "O cérebro existe mas nunca foi configurado. Vamos rodar o `/iniciar` primeiro." |
| Tudo presente | seguir |

---

## Passo 1 — Puxar o que mudou

O cérebro pode ter mudado em outro computador. Puxar antes de ler:

```bash
git -C "$CEREBRO" pull --rebase 2>&1
```

**Se pedir usuário ou senha, ou falhar autenticando:** parar e avisar em linguagem simples — *"a conexão com o GitHub caiu. Na próxima vez que a gente enviar, vai abrir uma janela pedindo pra você entrar na conta — é normal, é o Windows renovando o acesso. Te ajudo se travar."* Nunca travar em silêncio dentro da skill.

**Se reclamar de mudança não commitada:** é trabalho de outra sessão. Guardar de lado, puxar, e devolver:

```bash
git -C "$CEREBRO" stash push -u -m "cerebro-auto: antes do pull"
git -C "$CEREBRO" pull --rebase
git -C "$CEREBRO" stash pop
```

**Nunca commitar o que estava ali.** Não é seu.

---

## Passo 2 — Ler os arquivos-raiz

`SOUL.md` → `USER.md` → `MEMORY.md` → `MAPA.md` → `AGENTS.md`.

---

## Passo 3 — Ler o que está quente, e só isso

Abrir:

- `memory/hot.md` — o foco da semana;
- `memory/context/pendencias.md` — o que está em aberto;
- as notas dos últimos dias, se houver;
- `memory/context/decisoes/{mês atual}.md`;
- **as fichas de projeto que estiverem no "Foco imediato" do `hot.md`** — quantas forem, sem número fixo.

**Não abrir as outras fichas.** Contar quantas existem e informar:

```bash
ls -1 "$CEREBRO"/memory/projects/*.md 2>/dev/null | grep -v MAPA | wc -l
```

Ler quinze fichas todo dia gasta atenção e não muda decisão nenhuma. O que você precisa ao acordar é o que está quente e o que precisa fazer. Se você perguntar de um projeto frio, eu abro a ficha dele na hora.

Manter a **lista exata dos caminhos que eu realmente abri** — ela vai no raio-X, para você conferir se eu li o que devia. Nunca listar como lido um arquivo que eu só vi no `ls`.

**Se a nota mais recente tiver mais de 2 dias**, avisar. Nunca declarar o cérebro atualizado em silêncio quando o registro está velho.

---

## Passo 3.5 — Conferir o tamanho dos arquivos-raiz

Rápido, e **mostrar o resultado**:

```bash
for f in USER.md MEMORY.md; do
  echo "$f: $(wc -c < "$CEREBRO/$f") chars"
done
```

| Arquivo | Teto | Por que existe teto |
|---|---|---|
| `USER.md` | **1375** | É lido em **toda** sessão. Cada linha inútil aqui custa atenção em todas as conversas do dia |
| `MEMORY.md` | **2200** | Idem. Só cabe aqui o que evita erro toda semana |

Se passar, avisar sem alarme e propor onde cortar:

> "Seu `USER.md` está com {N} caracteres, o teto é 1375. Isso é lido em toda conversa nossa, então cada linha a mais me tira atenção do que importa. Quer que eu enxugue? O detalhe longo vai pra `memory/context/people/{slug}.md`, que eu leio só quando precisa."

**Avisar, não cortar sozinho.** É arquivo de identidade da pessoa.

## Passo 4 — O raio-X

Fechar sempre com isto, em primeira pessoa e sem voz de relatório. Profundidade no que está quente; o resto entra como contagem.

```
🧠 {DD/MM}

{Uma ou duas frases lendo o momento de verdade}

## O que eu li
- Raízes: {caminhos exatos}
- Contexto: {caminhos exatos}
- Projetos: {caminhos exatos}

## O que aconteceu por último
{síntese concreta das notas recentes}

## Última decisão
{data + a decisão + o que ela mudou na prática}

## Em aberto
| O que | Por que importa | Próximo passo |
|---|---|---|

## Foco quente
| Projeto | Onde está | Próximo passo |
|---|---|---|

Existem {N} fichas em memory/projects/. Qualquer uma fora do foco, é só pedir.

Minha leitura: {o que eu acho, curto e sincero}

Começamos por {recomendação} ou você quer puxar outra coisa?
```

Quando a ficha não tiver próximo passo, escrever **"não definido"** em vez de inventar. A ausência é um diagnóstico e pode virar pendência.

Se houver conquista recente, reconhecer. Se houver coisa atrasada ou projeto sem rumo, dizer sem rodeio. O objetivo é você sentir que eu cheguei pra trabalhar contigo, não que uma máquina terminou uma varredura.

## O que esta skill não faz

Não lê o cérebro inteiro, não abre ficha fria, não varre o `content/`. Ela lê o crítico e para. Curiosidade custa atenção, e atenção é o recurso escasso do começo do dia.
