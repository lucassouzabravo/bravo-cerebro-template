# Governança de IA na Bravo

> Consolidado pela AI Operations. É a política que vale para todo mundo que usa
> Claude na Bravo: como escolher a ferramenta certa, o que pode e o que não pode
> entrar, e como anonimizar.
>
> **Sensibilidade: interno Bravo.** Não encaminhar para fora da empresa.
> Todos os nomes, CPFs e valores usados como exemplo são fictícios.

## Tese operacional

AI Operations na Bravo não deve ser “balcão de licença Claude”. O papel correto é **tutor de uso adequado**: entender o caso, direcionar para a ferramenta certa, proteger dados da Bravo/clientes e garantir que quem receber licença extraia valor real.

A operação deve evitar dois erros simétricos:

1. **Liberar licença por pressão/vibe** — gera custo, baixo uso, risco e falta de rastreio de ROI.
2. **Bloquear IA por medo genérico** — perde produtividade e empurra pessoas para contas pessoais/free, que são mais perigosas.

A postura recomendada é: filtrar, orientar, redirecionar quando necessário e treinar uso responsável.

## Bloco 1 — Fundamentos de IA/LLM para AI Operations

### O que é um LLM

Claude é um LLM: sistema treinado para prever a próxima palavra/token a partir do texto de entrada. Ele não é banco de dados, não é sistema de regras e não “sabe” no sentido humano; ele gera respostas estatisticamente plausíveis.

### O que Claude/LLMs fazem bem

- Reescrever, resumir, traduzir e mudar tom.
- Estruturar pensamento solto em formatos úteis: e-mail, documento, roteiro, relatório.
- Gerar rascunho que humano revisa.
- Explicar conceitos conhecidos em linguagem mais simples.
- Extrair informação estruturada de texto bagunçado.
- Codar sob supervisão humana.

### O que Claude/LLMs fazem mal

- Calcular com precisão, especialmente contas com várias etapas.
- Lembrar fatos pontuais com 100% de fidelidade.
- Citar fonte específica sem inventar.
- Decidir com dado em tempo real sem ferramenta/base conectada.
- Aplicar regulação, política ou contrato sem o texto literal em mãos.
- Responder sobre dados internos/clientes da Bravo se esses dados não foram fornecidos em contexto seguro.

### Alucinação

Alucinação é resposta plausível, mas falsa, com a mesma confiança de uma resposta correta. Regra operacional:

> LLM erra com a mesma cara de quem acerta. Para qualquer número, data, citação ou regra que vira decisão, valide na fonte primária.

Risco alto: fatos específicos, citação legal/regulatória, cálculo complexo, dados de cliente não anexados, estatísticas de nicho.

Risco baixo: resumo/reescrita de conteúdo fornecido, brainstorm, tradução, estruturação de ideias.

### Janela de contexto e memória

Janela de contexto é tudo que o modelo vê em uma conversa: instruções, arquivos, histórico e resposta em geração. Ela é finita e a qualidade degrada em conversas longas porque a atenção se dilui.

Mitigações:

- Usar **Projects** quando o contexto é recorrente.
- Abrir conversa nova para tarefa nova.
- Colocar objetivo/formato/restrição no topo.
- Em conversa longa, pedir resumo de decisões/pendências/próximo passo e recomeçar com esse resumo.

### Chat, Project, Agent, Automação e RPA

| Categoria | Uso correto | Exemplo Bravo |
|---|---|---|
| Chat | Tarefa manual/pontual com julgamento humano | Redigir resposta para cliente difícil |
| Project | Chat com contexto persistente para tarefas recorrentes | Project de comunicação com cliente |
| Agent | LLM executando ações multi-etapa no mundo | Classificar e-mails e criar cards |
| Automação | Fluxo determinístico gatilho → ação | Lead novo → CRM → e-mail |
| RPA | Robô clicando em sistema legado sem API | Baixar relatório em sistema antigo |

Filtro-chave:

> Se é rodar X uma vez com julgamento, pode ser Claude. Se é rodar X toda terça às 8h sem você, é automação — Claude pode ser peça interna, não produto final.

### Claude: Project, Skill e Artifact

- **Project:** contexto persistente com instruções, arquivos e eventualmente memória. Usar quando há mesmo contexto em várias conversas.
- **Skill:** pacote de instrução/arquivos para tarefa especializada, como gerar docx/pptx/xlsx/PDF com mais qualidade.
- **Artifact:** saída renderizada/exportável ao lado do chat: documento, código, HTML, diagrama etc.

### Treino, inferência e retenção

- **Treino:** construção do modelo antes do produto. Usuário corporativo adequado não treina Claude com conversas.
- **Inferência:** uso do modelo para gerar resposta; toda conversa é inferência.
- **Retenção:** tempo de armazenamento do conteúdo; varia por conta/configuração.

Conta pessoal/free é problema para Bravo porque: pode haver uso para melhoria do produto, não há controle administrativo, não há contrato Bravo-Anthropic, histórico fica com a pessoa.

Conta Team bem configurada ajuda porque oferece não-treinamento contratual, controle administrativo, continuidade e base de conformidade — mas **não dispensa governança interna**.

## Bloco 2 — Filtro de adequação de licença/ferramenta

### Objetivo

Evitar aprovar licença Claude por inércia. Todo pedido deve virar conversa curta de diagnóstico com quatro saídas possíveis.

### Quatro saídas possíveis

1. **Aprovar** — caso concreto, recorrente, com julgamento humano em cada execução.
2. **Redirecionar** — outra ferramenta já resolve melhor: Gemini, Granola, n8n/Cowork/Zapier, Claude Code etc.
3. **Devolver** — problema é de processo, não de ferramenta.
4. **Pedir caso de uso** — pedido vem por vibe, sem caso real claro.

### Fluxo de sete perguntas

Rodar mentalmente em ordem e parar no primeiro sinal claro.

1. **É repetitivo e estruturado?**
   - Sinais: toda semana/mês, gatilho claro, output padronizado.
   - Caminho: automação n8n/Zapier/Cowork. Claude pode ser peça interna.
   - Resposta sugerida: “Isso tem cara de automação, não de Claude no dia a dia. Posso te conectar com o time que cuida de n8n/Cowork? Se Claude precisar entrar como peça, a gente desenha junto.”

2. **É uma vez, com contexto?**
   - Sinais: analisar documento, rascunhar proposta, destrinchar caso.
   - Caminho: Claude chat ou Project pode fazer sentido, mas continuar avaliando.

3. **Vive em planilha?**
   - Sinais: analisar base, categorizar linhas, gerar fórmula.
   - Caminho: considerar Gemini no Workspace antes, porque já está integrado/pago e roda no Sheets.
   - Exceção: análise pontual de planilha pequena pode caber em Claude.

4. **É reunião/transcrição?**
   - Caminho: Granola, já contratado.
   - Resposta sugerida: “Para reunião, a gente usa Granola. Já está contratado, faz transcrição e resumo. Te ajudo a configurar se precisar.”

5. **É código?**
   - Caminho: Claude Code, não Claude.ai genérico.

6. **Envolve dados de cliente?**
   - CPF, dívida, histórico de pagamento, contrato, lista de devedores, conversa real etc.
   - Caminho: nunca pessoal/free. Só Team corporativa e com governança/anonimização.

7. **A pessoa quer Claude porque ‘Claude é melhor’?**
   - Se não há caso real concreto, pedir caso de uso antes de aprovar.
   - Resposta sugerida: “Posso aprovar — mas antes me conta um caso real onde você ia usar essa semana. Sem caso de uso, fica difícil justificar a licença e rastrear retorno.”

### Tabela de roteamento rápido

| Situação | Caminho correto |
|---|---|
| Repetitivo e estruturado | n8n / Zapier / Cowork |
| Uma vez, com contexto | Claude chat ou Project |
| Vive em planilha | Gemini no Workspace |
| Reunião / transcrição | Granola |
| Código | Claude Code |
| Dado de cliente | Team corporativa, nunca free/pessoal |
| “Claude é melhor” sem caso | Pedir caso de uso |

### Armadilhas comuns

- “É só para começar, depois automatizamos” → aceitar experimento com prazo, ex.: reavaliar em 30 dias.
- “ChatGPT/Gemini não dá conta, só Claude” → pedir exemplo concreto de falha.
- “Meu gerente aprovou” → política não muda por pressão; escalar com documentação.
- “É confidencial, não posso dizer o caso” → caso de uso abstrato não viola confidencialidade.
- “Já uso conta pessoal, só quero migrar” → pode ser incidente em curso; entender o que já foi enviado antes de formalizar.

## Bloco 3 — Governança de dados Bravo

### Tese

Bravo é fintech de resolução de dívidas. Dados de CPF, dívida, situação financeira, histórico de pagamento e comunicação com cliente são altamente sensíveis sob LGPD. Governança não é teatro: é prevenção de incidente.

### Régua de uma frase

> Se você não colaria isso em um e-mail para um fornecedor desconhecido, não cola no Claude — nem na conta da empresa.

Essa frase resolve a maioria dos casos diários. Para casos limites, usar a classificação em três níveis.

### Três níveis de dado

| Nível | Conteúdo | Onde pode entrar |
|---|---|---|
| 1 | Público ou sem dado sensível: artigo público, brainstorm abstrato, conteúdo de aprendizagem, marketing já publicado | Qualquer lugar: pessoal, free ou Team |
| 2 | Interno operacional sem identificar cliente: manual de processo, métricas agregadas, rascunho para classe de clientes sem nomes | Apenas Team da Bravo, com bom senso |
| 3 | Cliente, credencial, confidencial estratégico: CPF, nome, telefone, contrato, dívida nominal, conversa real, senha/token, lista de devedores, M&A/jurídico sigiloso | Pessoal/free nunca. Team só com forte preferência por anonimização e fluxo aprovado quando indispensável |

Em dúvida entre Nível 2 e 3: anonimizar ou consultar AI Operations.

### Por que pessoal/free são proibidos para trabalho Bravo

Quatro motivos independentes:

1. Sem contrato Bravo-Anthropic.
2. Sem controle administrativo/auditoria/revogação pela TI.
3. Histórico fica com o colaborador e vai embora se ele sair.
4. Termos de uso/proteção são mais fracos; em free pode haver uso para melhoria do produto.

Resposta curta para insistência:

> Não pode — sem contrato com a Anthropic via essa conta, sem auditoria de TI, histórico vai embora com você e os termos de uso permitem treinamento/melhoria. Qualquer um desses problemas já bloqueia.

### Conta Team não dispensa governança

Team/Enterprise configurada corretamente oferece perímetro: contrato, não-treinamento, controle de usuários, auditoria/retenção. Mas o conteúdo colado continua sendo decisão humana; por isso os três níveis e treinamento seguem obrigatórios.

### Anonimização

Anonimizar resolve a maioria dos casos sem perder qualidade.

Substituições padrão:

| Dado real | Substituição |
|---|---|
| João da Silva | [Cliente A] |
| CPF 123.456.789-00 | [CPF] |
| Telefone | [TELEFONE] |
| R$ 4.523,87 | R$ ~4.500 ou [VALOR] |
| Contrato 7891234 | [CONTRATO] |
| Endereço | [ENDEREÇO] |

Regra: quase nunca há motivo para colar dado Nível 3 real em Claude; quase sempre dá para anonimizar.

### Sinais de alerta

- “Vou copiar a planilha inteira” → pode conter dado nominal/Nível 3.
- “Quero analisar conversas reais com clientes” → comunicação com cliente é Nível 3.
- “Já uso conta pessoal há meses” → possível incidente; investigar antes de aprovar.
- “Mas eu apago depois” → irrelevante; o dado já trafegou.
- “Vai ficar só comigo” → irrelevante; o risco é envio para fora do perímetro Bravo.

### Post-it do colaborador autorizado

1. Use sempre conta Team da Bravo; nunca pessoal para trabalho.
2. Antes de colar, pergunte se colaria em e-mail para fornecedor desconhecido.
3. Dado de cliente: anonimize antes.
4. Em dúvida, pergunte ao AI Operations.
5. Nunca compartilhe credencial: senha, token, chave, secret.

## Bloco 4 — Boas práticas de uso de Claude

### Objetivo

Ensinar poucos hábitos que mudam comportamento, não transformar colaborador em prompt engineer.

### Cinco hábitos que movem agulha

1. **Diga o que quer antes do contexto.**
   - Começar pelo output desejado reduz divagação.
   - Prompt longo deve ter objetivo, formato e restrição no primeiro parágrafo.

2. **Mostre exemplo do output que quer.**
   - “Profissional mas amigável” é vago; exemplo real captura nuance.
   - Obrigatório quando estilo Bravo/tom/comunicação é parte difícil.

3. **Itere, não recomece.**
   - Resposta ruim contém diagnóstico.
   - Dar feedback específico na mesma conversa é melhor que abrir outra e repetir prompt.
   - Exceção: conversa saturada/longa/confusa; recomeçar levando aprendizado.

4. **Trabalho recorrente vira Project.**
   - Se a pessoa cola o mesmo contexto três vezes na semana, montar Project.
   - Vira Project: instruções fixas, arquivos recorrentes, vocabulário/jargão, guias de estilo.
   - Não vira Project: planilha do dia, e-mail específico, número de protocolo, dado sensível variável.

5. **Confira número e citação antes de virar decisão.**
   - Claude erra cálculo, data, citação legal/regulatória, estatística e nomes próprios com confiança.
   - Para decisão, validar fonte, base ou conta.

### Cartão de bolso

> 5 hábitos com Claude: 1) diga o que quer antes do contexto; 2) mostre exemplo do output quando possível; 3) quando sair ruim, conserte na mesma conversa; 4) trabalho recorrente vira Project; 5) confira número e citação antes de virar decisão.

### Como ensinar sem perder eficácia

Evitar quatro falhas de tutor:

- Ensinar tudo de uma vez.
- Explicar antes de mostrar.
- Cair cedo demais em casos-limite.
- Não voltar depois para manutenção.

Correção: ensinar uma prática por conversa, demonstrar na interface, resolver caso real e revisitar uso a cada 4–6 semanas.

## Guia do colaborador — versão final de referência

O guia do colaborador consolida os blocos em linguagem de uso diário. Ele deve ser a referência entregue para quem recebe licença Claude.

### Mensagem central para colaborador

Você não precisa entender IA por dentro. Precisa saber:

1. O que Claude faz bem e mal.
2. Como conduzir conversa para ter resposta boa.
3. O que pode/não pode entrar no Claude considerando dados Bravo.

### Quando pedir ajuda ao AI Operations

- Dúvida se documento é Nível 2 ou 3.
- Novo tipo de tarefa fora do caso de uso aprovado.
- Uso acidental de dado de cliente sem anonimizar.
- Tarefa virou “rodar X toda terça às 8h” — pode ser automação.
- Funcionalidade nova de Claude antes de usar com dado real.

### Recursos de aprofundamento citados

- Andrej Karpathy — “Intro to Large Language Models” no YouTube.
- Curso em Vídeo — curso gratuito de Inteligência Artificial em PT-BR.
- Anthropic docs — docs.claude.com.

## Implicações para projetos de IA na Bravo

Estes documentos definem a base de várias frentes:

1. **Gestão de licenças Claude**
   - Criar intake de solicitação com caso de uso, tipo de dado, frequência, ferramenta candidata e saída do filtro.
   - Rastrear aprovação, redirecionamento, experimento com prazo e ROI.

2. **Governança de IA**
   - Transformar a régua dos 3 níveis em política simples, treinamento e checklist.
   - Criar fluxo de incidente/consulta para uso de conta pessoal ou envio indevido de dado.

3. **Capacitação de colaboradores autorizados**
   - Treinar cinco hábitos de Claude.
   - Entregar guia/cartão de bolso.
   - Rodar manutenção periódica de uso real.

4. **Workshops práticos com gerentes/líderes**
   - Usar dores reais para decidir se projeto prático é Claude Project, Gemini/Sheets, automação, Granola, Lovable, n8n etc.
   - Não ensinar ferramenta por moda; ensinar a partir de problema operacional.

5. **Projetos de automação**
   - Casos repetitivos e estruturados devem ir para n8n/Cowork/Zapier; Claude entra como componente quando necessário.

6. **Second brain / hub AI Operations**
   - Manter base com: filtro de licenças, política de dados, guias de uso, casos aprovados, redirecionamentos, incidentes, exemplos de prompts, Projects criados e materiais de treinamento.

## Frases-chave para reaproveitar

- “AI Operations não é vendedor de licença Claude — é tutor de uso adequado.”
- “Redirecionar não é dizer não; é dizer sim pelo caminho certo.”
- “Se você não colaria isso em um e-mail para um fornecedor desconhecido, não cola no Claude — nem na conta da empresa.”
- “Conta Team protege o perímetro; o conteúdo que entra continua sendo decisão humana.”
- “LLM erra com a mesma cara de quem acerta.”
- “Para número ou citação que vira decisão, Claude dá rascunho; a conferência é sua.”
- “Se você cola o mesmo contexto três vezes, vira Project.”
- “Trabalho recorrente e estruturado não é chat; é automação.”

## Perguntas de diagnóstico derivadas para futuras conversas

Para pedido de licença/ferramenta:

1. Qual caso real você usaria essa semana?
2. Isso acontece uma vez com contexto ou se repete com gatilho/saída clara?
3. O trabalho vive em planilha, reunião, código, documento ou sistema?
4. Envolve dado de cliente, credencial ou informação estratégica?
5. Que ferramenta já testou e onde ela falhou?

Para workshop com gerente:

1. Qual maior dificuldade/gargalo da sua rotina hoje?
2. Na sua visão, o que ajudaria a resolver ou aliviar esse problema?
3. Qual IA/ferramenta/tipo de aplicação você mais quer aprender agora — e por quê?
4. Se fizermos um workshop prático, qual problema real você gostaria de sair com um primeiro projeto encaminhado?
