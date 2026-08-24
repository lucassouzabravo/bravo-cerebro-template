---
name: iniciar-ambiente
description: >
  Prepara a máquina para o cérebro funcionar: confere e instala o git e o gh (o programa
  que fala com o GitHub), conecta a conta da pessoa ao GitHub, e configura a identidade
  do git. Chamada pelo /iniciar no passo 2, mas pode ser usada sozinha quando a pessoa
  troca de máquina ou quando o push para de funcionar.
  Triggers: "/iniciar-ambiente", "conecta meu github", "instala o gh".
disable-model-invocation: true
---

# iniciar-ambiente

> Passo 2 do `/iniciar`. Instala software e autentica conta — por isso é `disable-model-invocation`.

## A regra que não se quebra

**Você nunca digita credencial de ninguém.** Não digita senha, não digita token, não preenche formulário de login, não cola chave. Nem se a pessoa oferecer, nem se ela pedir, nem para "adiantar".

O caminho correto é o `gh` mostrar um código, a pessoa abrir o navegador **dela**, colar o código e autorizar. Você mostra as instruções e espera.

Se a pessoa colar um token no chat: avise que ela deve **revogá-lo** e gerar outro, porque ele passou por um canal que guarda histórico. Não use o token, não repita ele na resposta.

---

## Passo 1 — Detectar o que já existe

Rodar e **mostrar a saída literal** antes de interpretar:

```bash
echo "--- git ---"; git --version 2>&1 || echo "AUSENTE"
echo "--- gh ---";  gh --version  2>&1 | head -1 || echo "AUSENTE"
echo "--- conta github ---"; gh auth status 2>&1 | head -5 || echo "NAO CONECTADO"
echo "--- identidade git ---"
echo "nome:  $(git config --global user.name 2>/dev/null  || echo VAZIO)"
echo "email: $(git config --global user.email 2>/dev/null || echo VAZIO)"
```

Leia a saída e classifique em um dos quatro estados. **Não pule para instalar sem olhar** — na maioria das máquinas o git já está lá.

| Estado | O que fazer |
|---|---|
| Tudo presente e conectado | Pular para o Passo 5 (confirmação) |
| `gh` ausente | Passo 2, depois 3, depois 4 |
| `gh` presente, conta não conectada | Passo 3 e 4 |
| Identidade do git vazia | Passo 4 |

> ⚠️ **`gh` instalado nem sempre aparece no PATH da sessão atual.** Se `gh --version` falhar mas a pessoa disser que já instalou, conferir os caminhos usuais antes de instalar de novo:
> ```bash
> ls "$PROGRAMFILES/GitHub CLI/gh.exe" "$LOCALAPPDATA/Programs/GitHub CLI/gh.exe" 2>/dev/null
> ```
> Se existir ali, o problema é PATH — resolver reabrindo o terminal, não reinstalando.

---

## Passo 2 — Instalar o `gh`

Explique antes, em uma frase, sem jargão:

> "Vou instalar um programinha oficial do GitHub. Ele é o que deixa eu criar e atualizar seu repositório sem você precisar mexer no site."

**Windows** (o caso padrão na Bravo):

```bash
winget install --id GitHub.cli --source winget --accept-package-agreements --accept-source-agreements
```

**macOS:**

```bash
brew install gh
```

Depois de instalar, **o terminal atual não enxerga o programa novo**. Isso é normal e é a causa nº1 de "instalei e não funcionou". Peça para a pessoa fechar e reabrir o Claude Code, e confirme na volta:

```bash
gh --version
```

Se o `winget` não existir na máquina, não improvise instalação por script baixado da internet. Mande o link oficial (`https://cli.github.com`), peça para ela instalar pelo instalador, e siga quando voltar.

---

## Passo 3 — Conectar a conta

Explique o que vai acontecer **antes** de rodar, para a pessoa não se assustar com o código na tela:

> "Agora você conecta sua conta. Vai aparecer um código de 8 caracteres aqui. Você copia, abre o link que eu vou te dar, cola lá e autoriza. Eu não vejo sua senha em momento nenhum."

```bash
gh auth login --hostname github.com --git-protocol https --web
```

Mostre a saída literal — o código está nela. Espere a pessoa confirmar que autorizou.

Conferir, e mostrar a saída:

```bash
gh auth status
```

Tem que aparecer `Logged in to github.com as {conta}`. Se não aparecer, **não seguir**: repetir o passo. Configuração meio-feita quebra três passos depois, longe da causa.

Aproveitar que o `gh` já autenticou e deixar o git usar essa credencial:

```bash
gh auth setup-git
```

Isso evita a pessoa ter que digitar login a cada envio.

---

## Passo 4 — Identidade do git

Todo registro no histórico leva nome e e-mail. Se estiverem vazios, o envio falha com uma mensagem que não explica nada.

Perguntar **uma coisa por vez**, e usar o e-mail corporativo:

```bash
git config --global user.name  "{Nome Sobrenome}"
git config --global user.email "{nome}@gobravo.com.br"
```

Conferir e mostrar:

```bash
git config --global user.name; git config --global user.email
```

---

## Passo 5 — Confirmação

Fechar com o quadro do que ficou pronto, sem enfeite:

```
Máquina pronta:

  ✓ git        {versão}
  ✓ gh         {versão}
  ✓ conta      conectada como {usuário}
  ✓ identidade {Nome} · {email}
```

Se alguma linha não ficou verde, **dizer qual e por quê**, e não declarar o passo concluído.

---

## Quando algo não funciona

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `gh: command not found` logo depois de instalar | O terminal não recarregou o PATH | Fechar e reabrir o Claude Code |
| `winget` não existe | Windows sem App Installer | Instalar pelo site oficial `cli.github.com` |
| O navegador não abriu sozinho | Ambiente sem navegador padrão | Mostrar a URL e o código para a pessoa abrir na mão |
| `gh auth status` diz não autenticado depois de autorizar | Autorizou em outra conta, ou fechou antes de concluir | Rodar `gh auth login` de novo e acompanhar até o fim |
| Push pede usuário e senha | `gh auth setup-git` não rodou | Rodar `gh auth setup-git` |
| A pessoa tem duas contas GitHub | Autenticou na pessoal em vez da de trabalho | `gh auth status` mostra qual; trocar com `gh auth switch` |
