---
name: iniciar-ambiente
description: >
  Prepara a máquina para o cérebro funcionar: confere o git, confirma que o Credential
  Manager (que vem junto com o Git for Windows) está ativo, e configura a identidade do
  git. Chamada pelo /iniciar no passo 2, mas pode ser usada sozinha quando a pessoa troca
  de máquina ou quando o envio para de funcionar.
  Triggers: "/iniciar-ambiente", "conecta meu github", "o push parou de funcionar".
disable-model-invocation: true
---

# iniciar-ambiente

> Passo 2 do `/iniciar`.

## A regra que não se quebra

**Você nunca digita credencial de ninguém.** Não digita senha, não digita token, não preenche formulário de login, não cola chave. Nem se a pessoa oferecer, nem para "adiantar".

Quem autentica é a pessoa, na tela dela.

Se ela colar um token no chat: avise que ele precisa ser **revogado** e gerado outro, porque passou por um canal que guarda histórico. Não use o token e não repita ele na resposta.

---

## O que a pessoa precisa ter, e é pouco

| O quê | Por quê | É instalação separada? |
|---|---|---|
| **Git** | sem ele não existe repositório | sim, e é a única |
| **Credential Manager** | é o que guarda o acesso ao GitHub | **não — vem dentro do Git** |
| Conta no GitHub | onde o cérebro fica guardado | não é programa |

> **Não instale o `gh` (GitHub CLI).** Ele é conveniente, mas é mais um programa para aprovar em máquina corporativa, e **não é necessário para nada** neste fluxo. Tudo que ele faria, o git comum e o navegador fazem.

---

## Passo 1 — Detectar o que já existe

Rodar e **mostrar a saída literal** antes de interpretar:

```bash
echo "--- git ---"
git --version 2>&1 || echo "AUSENTE"
echo "--- quem guarda a credencial ---"
git config --get credential.helper 2>&1 || echo "NENHUM"
echo "--- identidade ---"
echo "nome:  $(git config --global user.name  2>/dev/null || echo VAZIO)"
echo "email: $(git config --global user.email 2>/dev/null || echo VAZIO)"
```

| O que apareceu | O que fazer |
|---|---|
| git ausente | Passo 2 |
| `credential.helper` = `manager` | ótimo, é o esperado. Pular para o Passo 3 |
| `credential.helper` vazio | Passo 2.1 |
| identidade vazia | Passo 3 |

---

## Passo 2 — Instalar o Git (só se faltar)

Explique em uma frase, sem jargão:

> "O Git é o programa que faz essa pasta guardar histórico. É a única coisa que a gente precisa instalar."

**Windows:**

```bash
winget install --id Git.Git --source winget --accept-package-agreements --accept-source-agreements
```

Se o `winget` estiver bloqueado — comum em máquina corporativa — **não improvise instalação por script baixado da internet.** Mande o link oficial (`https://git-scm.com/download/win`), peça que a pessoa instale ou peça ao TI, e siga quando voltar.

Depois de instalar, **o terminal atual não enxerga o programa novo.** Isso é normal e é a causa nº 1 de "instalei e não funcionou". Peça para fechar e reabrir o Claude Code, e confirme:

```bash
git --version
```

### Passo 2.1 — Ligar o Credential Manager, se ele não estiver ativo

Ele vem junto com o Git for Windows, mas pode estar desligado:

```bash
git config --global credential.helper manager
git config --get credential.helper
```

---

## Passo 3 — Identidade do git

Todo registro no histórico leva nome e e-mail. Vazio, o envio falha com mensagem que não explica nada.

Perguntar **uma coisa por vez**, e usar o e-mail corporativo:

```bash
git config --global user.name  "{Nome Sobrenome}"
git config --global user.email "{nome}@gobravo.com.br"
git config --global user.name; git config --global user.email
```

---

## Passo 4 — Como a conta vai ser conectada, e por que ainda não é agora

Não existe passo de "fazer login" aqui, e isso confunde. Explique:

> "A conexão com o GitHub acontece sozinha na **primeira vez** que a gente for enviar alguma coisa. Vai abrir uma janela do navegador, você entra na sua conta, autoriza, e nunca mais precisa. O Windows guarda no cofre do sistema."

Isso acontece no **passo 6** do `/iniciar`, quando a estação for enviada pela primeira vez. Aqui a gente só deixa o terreno pronto.

**O que a pessoa vai ver:** uma janela pedindo para entrar no GitHub, com botão de autorizar. É legítimo — é o próprio Git pedindo.

---

## Passo 5 — Confirmação

```
Máquina pronta:

  ✓ git         {versão}
  ✓ credencial  Credential Manager ativo (veio junto com o Git)
  ✓ identidade  {Nome} · {email}
  ⏳ conta       conecta sozinha no primeiro envio, com janela do navegador
```

Se alguma linha não ficou verde, **dizer qual e por quê**, e não declarar o passo concluído.

---

## Quando algo não funciona

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `git: command not found` logo após instalar | O terminal não recarregou | Fechar e reabrir o Claude Code |
| `winget` bloqueado | Política da máquina | Link oficial, ou pedir ao TI. Não contornar |
| Pede usuário e senha no terminal, em texto | Credential Manager desligado | `git config --global credential.helper manager` |
| A janela do navegador não abre | Ambiente sem navegador padrão, ou política de SSO | Ver "Plano B" abaixo |
| `Authentication failed` depois de autorizar | Autorizou em outra conta (pessoal em vez da de trabalho) | Limpar a credencial guardada no **Gerenciador de Credenciais do Windows** e repetir |
| Funcionava e parou | Credencial expirou ou foi revogada | Repetir o primeiro envio; a janela abre de novo |

---

## Plano B — token, e só se o Credential Manager não der

**Só use isto se o Passo 4 falhar de verdade.** É pior por três motivos: é um segredo dentro de um arquivo, ele expira sem avisar, e ensina um hábito que a gente prefere que ninguém tenha.

Se for necessário:

1. A pessoa gera um token em `github.com/settings/tokens` — **fine-grained**, só nos repositórios dela, permissão de **Contents: Read and write**, validade curta.
2. **Ela cola num arquivo `.env` na raiz do cérebro, com as próprias mãos.** Você não digita, não vê e não repete o valor.
3. Confirmar que o `.gitignore` bloqueia o arquivo — **antes** de qualquer envio:

```bash
git check-ignore -v .env || echo "PARE: o .env NAO esta protegido"
```

Se essa linha não confirmar a proteção, **parar tudo**. Um token que entra no histórico do git fica lá para sempre, e apagar o arquivo depois não resolve.

4. Registrar em `TOOLS.md` apenas o **nome** da variável e onde ela mora — nunca o valor.
5. Avisar a data de expiração, para não virar o mistério de "parou de funcionar e ninguém sabe por quê".
