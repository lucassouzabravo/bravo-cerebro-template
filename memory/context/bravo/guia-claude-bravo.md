# Guia de uso do Claude na Bravo

> Documento oficial da AI Operations, entregue a quem recebe licença Claude.
> **Sensibilidade: interno Bravo.** Não encaminhar para fora da empresa.
> Todos os nomes, CPFs e valores usados como exemplo são fictícios.

Sumário executivo

Este guia é o material de referência do colaborador da Bravo que recebeu uma licença Claude. Ele consolida em um único lugar o que você precisa saber para tirar valor da ferramenta sem expor a empresa e os clientes a risco — sem virar especialista em IA.

Você não precisa entender como o modelo funciona por dentro. Precisa saber: (1) o que Claude faz bem e o que faz mal; (2) como conduzir uma conversa para ter resposta de qualidade; (3) o que pode e o que não pode entrar no Claude considerando o tipo de dado que circula na Bravo. Esses três pontos são o que separa um colaborador que economiza horas por semana de um que vai gerar trabalho extra para o time de governança.

| 5 / hábitos que decidem a qualidade do uso | 3 / níveis de classificação de dado Bravo | 1 / régua que cabe em um post-it | 90% / dos casos resolvidos com anonimização |

| --- | --- | --- | --- |

| COMO LER ESTE GUIA / Leia o documento inteiro uma vez na primeira semana. Depois, use as seções 3 (os cinco hábitos) e 4 (governança em uma régua) como referência de consulta sempre que tiver dúvida. As seções 1 e 2 explicam o porquê — são úteis quando alguém te pergunta 'mas por que não pode?'. O cartão da última página é o resumo que você cola embaixo do monitor. |

| --- |

Índice

1   O que Claude é, e o que ele faz bem

1.1  O que é um LLM, em uma frase

1.2  O que Claude faz bem · o que Claude faz mal

1.3  Alucinação: o erro que parece acerto

2   Como o Claude pensa em uma conversa

2.1  A janela de contexto e por que ela importa

2.2  Quando abrir nova conversa

2.3  Quando criar um Project

3   Os cinco hábitos que movem agulha

3.1  Diga o que quer antes do contexto

3.2  Mostre um exemplo do output que você quer

3.3  Itere — não recomece

3.4  Trabalho recorrente vira Project

3.5  Confira número e citação antes de virar decisão

4   Governança de dado em uma régua

4.1  A régua, em uma frase

4.2  Os três níveis de dado

4.3  Anonimização: o gesto de cinco segundos

4.4  Cinco regras do colaborador autorizado

5   Cartão de bolso e próximos passos

5.1  O cartão das cinco linhas

5.2  Quando pedir ajuda ao AI Operations

5.3  Para aprofundar

1.  O que Claude é, e o que ele faz bem

1.1  O que é um LLM, em uma frase

Claude é um LLM — Large Language Model. Em uma frase: um sistema treinado para prever a próxima palavra a partir do que você escreveu, com base em padrões aprendidos de muito texto.

Você não precisa entender muito mais do que isso. O importante é a implicação prática: Claude é excelente para trabalhar com texto — reescrever, resumir, estruturar, traduzir, brainstormar — e frágil quando o problema exige precisão factual sem fonte na mesa: cálculos, citações de lei, datas exatas, estatísticas. Lembre-se disso toda vez que estiver decidindo se confia ou não na resposta.

1.2  O que Claude faz bem · o que Claude faz mal

A tabela abaixo é o resumo mais útil que existe para o seu dia a dia. Use-a como filtro antes de começar uma tarefa: se o seu pedido cai do lado direito, pense em validar fonte ou em outra ferramenta.

| Faz bem (vai te economizar tempo) | Faz mal (vai te enganar com confiança) |

| --- | --- |

| Reescrever, resumir, traduzir, mudar tom. | Calcular com precisão (especialmente com muitas etapas). |

| Estruturar pensamento solto em formato organizado. | Lembrar de fato pontual com 100% de fidelidade. |

| Gerar rascunho que humano edita. | Citar fonte específica sem inventar. |

| Explicar conceito conhecido em outra linguagem. | Decidir com dado em tempo real sem ferramenta. |

| Extrair informação estruturada de texto bagunçado. | Aplicar regulação ou política sem o texto literal em mãos. |

Tabela 1. O que Claude faz bem vs. faz mal. (Fonte: AI Operations Bravo)

1.3  Alucinação: o erro que parece acerto

Alucinação é quando o modelo gera uma resposta plausível mas falsa, com a mesma confiança de uma resposta correta. Ele não sabe que não sabe — só completa o padrão.

Isso significa que Claude pode dizer 'o artigo 32 da LGPD determina X' com confiança total e estar errado. Sem o texto literal da lei no contexto, o risco é alto. O hábito operacional que decorre disso aparece no capítulo 3, prática nº 5: para qualquer número, data, citação ou regra que vai virar decisão, valide na fonte.

| Risco alto de alucinação | Risco baixo de alucinação |

| --- | --- |

| Fatos específicos pouco comuns (estatística de nicho, citação literal). | Reescrita ou resumo de texto que está na própria conversa. |

| Cálculo complexo sem ferramenta de execução. | Brainstorm sem compromisso de verdade. |

| Referências jurídicas, médicas ou regulatórias sem fonte anexada. | Estruturação de ideias soltas em tópicos. |

| “Quais clientes da Bravo têm tal perfil?” — ele não tem acesso. | Tradução de conteúdo comum. |

Tabela 2. Onde Claude alucina mais e onde alucina menos.

| “LLM erra com a mesma cara de quem acerta. Para qualquer número, data, citação ou regra que vai virar decisão, valida na fonte.” / — Régua de uso do colaborador Bravo |

| --- |

2.  Como o Claude pensa em uma conversa

2.1  A janela de contexto e por que ela importa

A janela de contexto é tudo que Claude “vê” em uma única conversa: suas instruções, os arquivos colados, o histórico do chat e a resposta que ele vai gerar. É grande, mas é finita.

Na prática, isso significa duas coisas. Primeira: quanto mais material você empurra para uma única conversa, mais diluída fica a atenção do modelo. É como pedir para alguém achar uma frase específica num calhamaço sem marcação. Segunda: em conversas muito longas, instruções antigas competem com novas e ele começa a misturar contextos ou repetir erros que já foram corrigidos. Não é falha técnica — é como a atenção funciona quando o contexto satura.

2.2  Quando abrir nova conversa

Regra simples: tarefa nova, conversa nova. Não tente fazer tudo numa thread infinita. Em vez disso, encerre a conversa atual quando o assunto mudar e comece outra com instruções claras no topo. Se a conversa atual tem aprendizado que você quer aproveitar, peça um resumo antes de fechar — e cole esse resumo como contexto inicial na próxima.

PROMPT · Resumo de meio-fio para usar no fim de conversa longa

| Antes de fecharmos, faça um resumo estruturado do que discutimos: / (1) decisões tomadas, (2) próximos passos definidos, / (3) pontos em aberto. Máximo 200 palavras. Vou usar esse resumo / para continuar em nova conversa. |

| --- |

2.3  Quando criar um Project

Project é um espaço persistente onde Claude já “conhece” o seu contexto: instruções de como ele deve se comportar e arquivos de referência que entram em toda conversa nova automaticamente. É a diferença entre repetir o setup toda vez e ir direto à tarefa.

| Use Project quando… | Não use Project quando… |

| --- | --- |

| Mesmo contexto, várias conversas ao longo da semana. | É uma tarefa única — abre chat normal. |

| Você se pega colando o mesmo bloco de contexto três vezes. | Você quer automatizar (use o time de n8n/Cowork). |

| Precisa que Claude “conheça” o seu jeito de trabalhar. | É exploração ou teste rápido sem chance de repetição. |

Tabela 3. Sinais de que um caso vira Project — ou não.

| SINAL CLARO DE HORA DE VIRAR PROJECT / Se você se ouvir dizendo “toda vez que eu vou fazer X, eu colo isso aqui”, “esqueci de incluir aquele documento de novo”, ou “sempre tem que explicar para ele que…”, é hora. Cinco minutos investidos montando o Project economizam meia hora por semana pelos próximos seis meses. |

| --- |

3.  Os cinco hábitos que movem agulha

Existem dezenas de truques de prompt. Este capítulo ignora a maioria deles e foca nos cinco hábitos que decidem se o seu uso de Claude vai render ou vai virar conversa boa que não chega a lugar nenhum. Cinco. Não cinquenta. É proposital.

3.1  Diga o que quer antes do contexto

A ordem em que você fala importa. Comece dizendo o que você quer no final, depois despeje o contexto necessário. Claude lê suas instruções na ordem em que você escreve, e as primeiras frases têm peso desproporcional na decisão de para onde focar a atenção.

PADRÃO RUIM · Contexto antes do objetivo

| Olha, semana passada teve uma reunião sobre carteira C, o gerente / disse que precisa de uma comunicação diferenciada, a Maria mandou / esse template que ela usou em 2023, o cliente médio tem 45 dias / de atraso, a gente quer manter tom firme mas não agressivo, ah e / tem aquela campanha de fim de ano que entrou agora, e... pode escrever? |

| --- |

PADRÃO BOM · Objetivo primeiro, contexto depois

| Preciso de um rascunho de e-mail para clientes da carteira C / com 45 dias de atraso. Tom firme mas não agressivo, 150 palavras, / com CTA para uma proposta de acordo. / Contexto: reunião da semana passada com o gerente da carteira indicou / necessidade de comunicação diferenciada. A Maria compartilhou template / de 2023 que pode servir de referência (cola abaixo se quiser usar). |

| --- |

| REGRA PRÁTICA / Antes de enviar um prompt longo, leia só o primeiro parágrafo dele. Se essa primeira linha não diz o que você quer no fim, reorganize. Vale para qualquer pedido com mais de três parágrafos de contexto. |

| --- |

3.2  Mostre um exemplo do output que você quer

Um exemplo bom vale dez instruções abstratas. Se você quer um relatório com certo estilo, cole um relatório anterior junto. Se quer um e-mail com certo tom, cole um e-mail que ficou bom. Linguagem natural não captura nuance de estilo — exemplo captura.

PADRÃO RUIM · Descrição abstrata de estilo

| Quero que seja profissional mas amigável, com um toque humano, / formal mas não engessado, conciso mas completo. |

| --- |

PADRÃO BOM · Exemplo concreto + adaptação

| Quero um e-mail no estilo deste aqui que mandei mês passado: / [cola e-mail anterior aqui] / Mantém o tom, adapta para o caso de hoje que é cliente carteira B / com 30 dias de atraso, primeira abordagem após reativação. |

| --- |

3.3  Itere — não recomece

Quando a resposta sai ruim, a tentação é abrir nova conversa e tentar de novo. Não faça isso. A primeira resposta ruim tem informação valiosa: você consegue dizer especificamente o que está errado, e o modelo já tem todo o contexto da tentativa anterior. Em vez de recomeçar, dê feedback no formato “o segundo parágrafo é redundante com o primeiro, o CTA ficou tímido, reescreve só essas duas partes”.

| ATENÇÃO / Recomeçar conversa apagando o aprendizado é o erro mais caro do uso diário. Você refaz o mesmo prompt, recebe a mesma resposta ruim, recomeça de novo. Isso é loop. Quebre o loop dando feedback específico — mesmo que pareça mais trabalhoso, é mais rápido. |

| --- |

Há uma exceção legítima: quando a conversa fica muito longa e Claude começa a se confundir — repetindo coisa corrigida três mensagens atrás, perdendo o fio —, vale recomeçar. Mas levando o aprendizado: abra a nova conversa com tudo que você já descobriu sobre o que funcionou e o que evitar.

3.4  Trabalho recorrente vira Project

Se você se pega colando o mesmo bloco de contexto em três conversas diferentes da mesma semana, vira Project. É onde a diferença entre “ferramenta legal” e “ferramenta que economiza horas” se materializa.

| Vira Project (contexto fixo) | Não vira Project (varia a cada uso) |

| --- | --- |

| Instruções de como Claude deve se comportar: tom, formato, restrições, persona. | Dado específico que muda a cada conversa: planilha do dia, e-mail específico, número de protocolo. |

| Arquivos de referência que sempre se aplicam: manual de processo, guia de estilo, política interna. | Conversa pontual de uma vez só, sem chance de repetição. |

| Vocabulário, jargão interno, abreviações da área que você usa diariamente. | Dados sensíveis que mudam a cada uso — eles seguem a régua do capítulo 4. |

Tabela 4. O que vira Project e o que não vira.

3.5  Confira número e citação antes de virar decisão

A regra de ouro. LLM erra cálculo, erra data, erra citação — com a mesma confiança com que acerta as outras coisas. A resposta vem bonita, estruturada, plausível. E errada.

| Categoria | Exemplo Bravo onde isso quebra |

| --- | --- |

| Cálculos com mais de duas etapas | “O total de juros sobre 18 meses a 2,3% ao mês, com amortização escalonada, é R$ 12.450.” Pode estar errado em qualquer dos passos. |

| Datas e prazos | “O cliente tem 67 dias de atraso, portanto vencimento da negociação seria 15/08.” Tanto o cálculo quanto a data podem estar inventados. |

| Citações de lei, regulação, contrato | “O artigo 42 do CDC veda essa prática.” O artigo pode existir mas dizer outra coisa — ou nem existir. Verifica na fonte. |

| Estatísticas, percentuais | “Carteira X tem 23% de inadimplência média.” Se o número não veio de uma base que você forneceu, presuma que foi inventado. |

| Nomes próprios em contexto técnico | “A Resolução BCB nº 4.892 trata disso.” Número e órgão podem estar trocados. Vale para nome de processo interno, sistema, produto. |

Tabela 5. Cinco categorias onde Claude erra com confiança.

| CRÍTICO / Esta é a única prática deste capítulo em que a falha tem consequência direta para cliente ou para a empresa. As outras quatro pioram qualidade. Esta, mal aplicada, gera decisão errada com base em alucinação. Trate como bloqueador no seu checklist pessoal antes de qualquer envio de comunicação ou relatório. |

| --- |

| “Claude é ótimo para reescrever, estruturar, resumir, brainstorm. Para número ou citação que vai virar decisão, ele te dá um rascunho. A conferência é sua.” / — Régua de uso do colaborador Bravo |

| --- |

4.  Governança de dado em uma régua

Bravo é fintech de resolução de dívidas. Os dados que circulam aqui — CPF, dívida, situação financeira, histórico de pagamento, comunicação com cliente — são dados pessoais sensíveis sob a LGPD. Governança não é teatro. Este capítulo é o que separa “uso responsável de IA” de “incidente de vazamento esperando para acontecer”.

4.1  A régua, em uma frase

| “Se você não colaria isso em um e-mail para um fornecedor desconhecido, não cola no Claude — nem na conta da empresa.” / — Régua operacional Bravo |

| --- |

Essa frase resolve 80% das suas decisões do dia a dia. Ela funciona porque transfere o critério para uma situação que você já mede mentalmente — quanto você expõe a um fornecedor de fora. Os 20% que sobram são casos limítrofes onde os três níveis abaixo entram.

4.2  Os três níveis de dado

| Nível | Tipo de conteúdo | Onde pode entrar |

| --- | --- | --- |

| 1 | Público ou sem dado sensível: artigo da internet, brainstorm abstrato sem cliente real, conteúdo de marketing publicado, perguntas conceituais. | Qualquer lugar — pessoal, free ou Team. |

| 2 | Interno operacional, sem identificar cliente: manual de processo, métricas agregadas, rascunho de comunicação para classe de clientes sem nomear ninguém. | Apenas conta Team da Bravo, com bom senso. Nunca em pessoal/free. |

| 3 | Cliente, credencial, confidencial estratégico: CPF, nome de cliente, contrato, dívida nominal, conversa real com cliente, senha/token, dado pré-divulgação. | Em pessoal/free: nunca. Em Team: com forte preferência por anonimização antes. |

Tabela 6. Os três níveis de classificação de dado da Bravo.

| EM DÚVIDA, ANONIMIZE OU PERGUNTE / Quando você não sabe se um conteúdo é Nível 2 ou Nível 3, use uma das duas saídas: anonimize antes de qualquer envio, ou consulte o responsável de AI Operations. Resposta em um dia é melhor que incidente — não há prêmio por improvisar nesse ponto. |

| --- |

4.3  Anonimização: o gesto de cinco segundos

Antes de pedir ajuda ao Claude com qualquer coisa que envolva pessoa real, faça uma passada rápida de anonimização. É um hábito de cinco segundos que evita 90% dos problemas potenciais.

| Dado real (não cole) | Substituição padrão (cole isto) |

| --- | --- |

| João da Silva | [Cliente A] |

| CPF 123.456.789-00 | [CPF] |

| Telefone (11) 99999-9999 | [TELEFONE] |

| R$ 4.523,87 (valor exato) | R$ ~4.500 (valor aproximado) ou [VALOR] |

| Contrato 7891234 | [CONTRATO] |

| Endereço específico | [ENDEREÇO] |

Tabela 7. Substituições padrão para anonimização (todos os exemplos são fictícios).

| REGRA PRÁTICA / Em 95% dos casos a qualidade da resposta de Claude não muda com anonimização — ele não precisa do CPF real para te ajudar a redigir uma comunicação. Quando muda, é raro e é exatamente onde vale parar e seguir o fluxo formal de uso de dado sensível com o time de AI Operations. |

| --- |

EXEMPLO BRAVO · Cobrança com e sem anonimização (dados fictícios)

| SEM anonimização (Nível 3 — NÃO faça): / "Preciso redigir uma cobrança para João da Silva, / CPF 123.456.789-00, telefone (11) 99999-9999, / contrato 7891234, valor R$ 4.523,87 em atraso há 47 dias." / COM anonimização (Nível 2 — OK): / "Preciso redigir uma cobrança para [Cliente A], / com débito aproximado de R$ 4.500 em atraso há cerca de 45 dias, / contrato pessoal de crédito." |

| --- |

4.4  Cinco regras do colaborador autorizado

Estas cinco regras cabem em um post-it. É proposital. Documentos de política longos não sobrevivem ao terceiro dia da operação — cinco regras curtas, sim.

1.  Use sempre a conta Team da Bravo (login com e-mail @bravo). Nunca pessoal para trabalho.

2.  Antes de colar qualquer coisa, pergunte: “Eu colaria isso em um e-mail para um fornecedor desconhecido?” Se a resposta for não, não cola.

3.  Dado de cliente: anonimize antes. Quase sempre o Claude funciona igual sem o dado real — e quando não funciona, vale parar e seguir o fluxo formal.

4.  Em dúvida sobre se algo pode entrar, pergunte ao time de AI Operations. Resposta em um dia é melhor que incidente.

5.  Não compartilhe credencial nenhuma. Nunca. Nem para testar. Senha, token, chave de API: fora do Claude, sem exceção.

| IMPORTANTE / Conta Team configurada é condição necessária — não suficiente. A infraestrutura corporativa protege o perímetro: contrato de não-treinamento, auditoria, controle de TI. O conteúdo do que entra continua sendo decisão sua. As cinco regras acima são exatamente para te ajudar a tomar essa decisão sem precisar consultar um documento de 40 páginas. |

| --- |

5.  Cartão de bolso e próximos passos

5.1  O cartão das cinco linhas

Se você fosse imprimir um cartão e colar embaixo do monitor, seria este. Cinco linhas. É o resumo operacional do guia inteiro.

| “5 hábitos com Claude: (1) diga o que quer antes do contexto. (2) mostre um exemplo do output que quer, quando possível. (3) quando sair ruim, conserta na mesma conversa — não recomeça. (4) trabalho recorrente vira Project. (5) confere número e citação antes de virar decisão.” / — Cartão de bolso do colaborador autorizado |

| --- |

| “Régua de dado: se você não colaria isso em um e-mail para um fornecedor desconhecido, não cola no Claude — nem na conta da empresa.” / — Régua operacional Bravo |

| --- |

5.2  Quando pedir ajuda ao AI Operations

Você não precisa virar especialista. Você precisa saber quando parar e consultar quem é. Estas são as situações em que o time de AI Operations quer ouvir de você — sem julgamento, sem fricção:

•  Você não tem certeza se um documento se enquadra como Nível 2 ou Nível 3 — anonimize ou pergunte antes de colar.

•  Você quer começar a usar Claude para um novo tipo de tarefa que não estava no caso de uso aprovado — vale uma conversa de cinco minutos para validar.

•  Você se pegou colando dado de cliente sem anonimizar — não esconde, comunica. O time prefere lidar com um incidente conhecido agora a descobrir um incidente desconhecido depois.

•  Você está pensando que sua tarefa virou “rodar X toda terça às 8h” — provavelmente já não é mais caso de Claude, é caso de automação. AI Operations te conecta com o time certo.

•  Você quer testar uma funcionalidade nova de Claude que apareceu — antes de usar com dado real, valide.

5.3  Para aprofundar

Este guia é proposital em ser curto. Se você quiser entender melhor como Claude funciona por dentro — sem virar engenheiro de IA — três recursos gratuitos cobrem 90% do que importa:

•  Andrej Karpathy · “Intro to Large Language Models” no YouTube. Uma hora, em inglês com legendas em português. O melhor vídeo único que existe sobre o que é um LLM e por que ele faz o que faz.

•  Curso em Vídeo · “Curso Gratuito de Inteligência Artificial” em PT-BR. Cobre prompts, LLMs, alucinações e uso prático. Conteúdo 100% gratuito.

•  Anthropic · docs.claude.com — documentação oficial. Use quando tiver dúvida específica de produto: Projects, Skills, Artifacts, limites de contexto.

| PRÓXIMO PASSO / Leia este guia uma vez na primeira semana. Imprima o cartão das cinco linhas (seção 5.1) e cole embaixo do monitor. Volte às seções 3 e 4 sempre que tiver dúvida. Se em algum momento você ficar inseguro sobre uma decisão de uso ou de dado, fale com o AI Operations — é exatamente para isso que o time existe. |

| --- |

— FIM DO GUIA DO COLABORADOR —
