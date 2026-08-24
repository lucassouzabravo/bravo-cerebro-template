---
name: iniciar-verificar
description: >
  Prova que o cérebro funciona de ponta a ponta: roda um /salve de teste de verdade,
  confirma no GitHub que chegou nos dois lados, e valida com três perguntas que a pessoa
  entendeu o que sobe e o que não sobe para o cérebro coletivo. Chamada pelo /iniciar
  no passo 7, e é o único passo que declara a configuração concluída.
  Triggers: "/iniciar-verificar", "testa meu cérebro", "está funcionando?".
disable-model-invocation: true
---

# iniciar-verificar

> Passo 7 do `/iniciar`. É o passo que tem autoridade para dizer "está pronto" — e ele só diz isso com evidência na tela.

## O princípio

**Configuração não testada é configuração quebrada que ninguém descobriu ainda.**

A pessoa vai embora achando que funciona, tenta usar na terça, falha, e não sabe se o problema é ela ou a ferramenta. Por isso este passo faz um envio **real**, não simulado, e confirma no destino.

---

## Passo 1 — Uma captura de teste de verdade

Não invente conteúdo. Peça algo real e pequeno:

> "Pra fechar, vamos testar de verdade. Me conta uma coisa curta da Bravo que você explicaria pra alguém que entrou hoje — uma sigla, um passo de um processo, quem aprova alguma coisa. Uma ou duas frases bastam."

Escrever em `memory/context/bravo/{assunto}.md` com as palavras dela.

Se ela travar, ofereça a saída mais fácil: qualquer termo que ela usou nesta conversa e que você precisou perguntar o que era.

---

## Passo 2 — Rodar o `/salve` de verdade

Invocar `/salve`. Não simular, não descrever o que aconteceria: **rodar**.

Deixar a pessoa ver as duas fases acontecendo, e principalmente o **report da Fase B** — é a primeira vez que ela vê a lista de confirmação, e é o que ela vai encontrar todos os dias.

Depois que ela confirmar, conferir os dois lados e **mostrar a saída literal**:

```bash
echo "--- cérebro pessoal ---"
git -C ~/bravo/pessoal log --oneline -1 origin/main
git -C ~/bravo/pessoal show --stat --oneline origin/main | tail -5

echo "--- inbox da alçada ---"
git -C ~/bravo/inbox log --oneline -1 origin/staging
git -C ~/bravo/inbox ls-tree --name-only origin/staging "{slug}/"
```

Critério, e é objetivo:

- o arquivo aparece no `origin/main` do cérebro pessoal;
- a captura **e** o `.meta.yaml` aparecem no `origin/staging` do inbox;
- o `show --stat` **não mostra nada fora dos caminhos esperados**.

O terceiro item é o que ninguém confere e é o que mais importa. Se apareceu arquivo que não deveria, achamos um defeito agora, na hora certa.

Se o inbox estiver pendente de acesso, testar só a Fase A e dizer com clareza o que ficou faltando.

---

## Passo 3 — As três perguntas

Não é prova. É a última chance de corrigir um entendimento errado antes de a pessoa sair usando sozinha.

> "Três perguntas rápidas e a gente fecha. Se errar, não tem problema — é pra isso que eu pergunto agora."

**1.** *"Você escreve como funciona o processo de aprovação da sua área. Isso sobe pro cérebro da Bravo ou fica só aqui?"*
→ **Sobe.** É conhecimento da empresa — camada de Tarefas ou Papéis.

**2.** *"Você anota que o fulano tem entregado atrasado. Sobe?"*
→ **Não.** Gatilho 2, avaliação de pessoa. Fica só no cérebro dela, e eu bloqueio sozinho.

**3.** *"Você anota quanto a sua equipe bateu de meta esse mês, sem citar ninguém."*
→ **Sobe.** Número de área não é dinheiro com nome de gente. O gatilho 1 é sobre remuneração individual — salário, comissão, bônus de alguém.

A terceira é a que mais gera erro, e o erro é para o lado conservador (a pessoa acha que não sobe). Se ela errar essa, explique a diferença e siga — errar para o lado seguro é aceitável.

Se errar a **2**, não seguir: voltar aos três gatilhos e testar de novo com outro exemplo. É a que protege colega dela.

---

## Passo 4 — Veredito

Só declarar pronto o que passou. Se algo não passou, dizer **o quê**, **por quê** e **de quem depende**.

```
Testado de ponta a ponta:

  ✓ Captura escrita no cérebro pessoal
  ✓ Chegou no GitHub                    {commit}
  ✓ Chegou no inbox da {alçada}         {commit}
  ✓ Nada vazou fora dos caminhos esperados
  ✓ Os três gatilhos entendidos

Seu cérebro está no ar.
```

Formato quando algo ficou pendente:

```
  ✓ Captura escrita no cérebro pessoal
  ✓ Chegou no GitHub                    {commit}
  ⏳ Inbox da {alçada}                   aguardando o Lucas liberar acesso
      → quando sair, é só rodar /iniciar-estacao e depois /salve
```

**Não arredondar para cima.** Dizer "está tudo pronto" com um item pendente é exatamente o tipo de coisa que faz a pessoa perder a confiança na ferramenta na primeira vez que ela precisa de verdade.
