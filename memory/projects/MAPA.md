# MAPA · projetos

Uma ficha por projeto. Leve, de propósito.

## Objetivo

Responder duas perguntas em dez segundos: **onde este projeto está** e **qual é o próximo passo**.

## A regra que impede a ficha de inchar

A ficha guarda **estado**. O entregável — documento, planilha, apresentação, código — mora em `content/drafts/{nome}/`.

Sem essa separação a ficha vira um documento gigante que ninguém lê, e o projeto perde justamente a informação que fazia ela ser útil.

## Formato

```markdown
# {nome-do-projeto}

- **Estado:** {ativo | pausado | aguardando alguém | concluído} — {onde está hoje, em 1-2 frases}
- **Resumo:** {o que é e o que entrega, para quem chegar sem contexto}
- **Próximo passo:** {a próxima ação concreta, com dono}
- **Artefatos:** `content/drafts/{nome}/`
- **Regra:** esta ficha é a fonte de estado do projeto; entregáveis e arquivos ficam no path de artefatos.
```

**Se não houver próximo passo, escrever "não definido"** em vez de inventar um. Projeto sem próximo passo é um diagnóstico — normalmente quer dizer que ele está travado ou morreu, e as duas coisas valem saber.

## Fichas

| Ficha | Estado | O que é |
|---|---|---|
| *(vazio)* | | |
