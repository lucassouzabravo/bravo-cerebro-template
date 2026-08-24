# Padrão visual dos relatórios da Bravo

> Como deixar relatório, dashboard e material visual com cara de Bravo.
> **Sensibilidade: interno Bravo.** Não é segredo, mas também não é material público.

A diretoria da Bravo tem régua alta de apresentação. Este arquivo existe para você não ter que reexplicar o padrão toda vez que pedir um relatório — o seu assistente lê daqui.

## A regra que vale mais que todas

**Design nunca pode roubar clareza do conteúdo.** Se ficou bonito e ilegível, está errado.

## Relatório no chat

Quando a resposta vier direto na conversa, sem virar arquivo, ela precisa ser escaneável — dá para bater o olho e entender status, prioridade e risco sem ler tudo.

| Marcador | Quando usar |
|---|---|
| ✅ | bom, confirmado, caminho recomendado |
| ⚠️ | atenção, risco, ressalva, precisa confirmar |
| ❌ | ruim, bloqueado, não recomendado |
| 💰 | preço, custo, impacto financeiro |
| 🎯 | a recomendação, o foco |
| 📌 | contexto que não pode passar batido |
| 🚀 | próximo passo, ação |

Blocos curtos, títulos visuais, separador leve, ranking quando houver comparação. **Emoji serve para hierarquia, não para enfeite** — usado demais vira carnaval e para de funcionar.

## Relatório em arquivo (HTML ou PDF)

### A estrutura

```text
OBJETIVO / DIAGNÓSTICO CENTRAL
        ↓
FRENTES · PILARES · BLOCOS   (2 a 5, não mais)
        ↓
CARDS   (entregável, risco, métrica, responsável)
        ↓
PIPELINE INFERIOR   (o fluxo, ou os próximos passos)
```

Um bloco central forte no topo. Abaixo, de 2 a 5 blocos. Dentro de cada um, cards pequenos. No rodapé, o fluxo ou os princípios.

### O visual

- fundo escuro (navy/preto), painéis translúcidos com borda fina;
- espaçamento generoso — nada apertado, nada poluído;
- composição simétrica sempre que der;
- tipografia limpa e corporativa; **Montserrat** quando for HTML;
- ícones minimalistas e geométricos.

### A paleta

| Uso | Cor |
|---|---|
| Fundo | `#05070D` · `#071426` |
| Azul principal | `#00AEEF` · `#2F80FF` |
| Brilho / destaque | `#7DEBFF` |
| Texto | `#F4F7FB` |
| Texto secundário | `#AAB7C8` |
| Bordas | `rgba(125,235,255,0.25)` |

E a cor diz do que o bloco trata:

| Cor | Assunto |
|---|---|
| Azul / ciano | tecnologia, IA, arquitetura, estratégia |
| Verde | pessoas, treinamento, operação |
| Dourado | negócio, comercial, dinheiro, prioridade executiva |
| Roxo | pesquisa, inteligência, conteúdo |
| Vermelho / âmbar | risco, urgência, bloqueio |

### O card

Título curto · no máximo 5 bullets · status ou prioridade quando ajudar · cor de borda pela categoria. Card que precisa de parágrafo não é card, é seção.

## Por tipo de entrega

| Entrega | Centro | Blocos | Rodapé |
|---|---|---|---|
| Relatório executivo | o diagnóstico | situação · risco · oportunidade · plano · decisão | próximos passos |
| Arquitetura de projeto | o projeto | frentes de trabalho | fluxo operacional |
| Próximos passos | o objetivo da semana | Hoje · Próximo · Depois | execução → validação → ajuste |

## Anti-padrões

- neon demais sem hierarquia;
- texto minúsculo e ilegível dentro de imagem;
- muitas cores sem função;
- imagem bonita sem próximo passo claro;
- transformar todo relatório em pôster — às vezes um diagrama limpo resolve melhor;
- conteúdo denso dentro de imagem gerada por IA. Para texto denso, **HTML ou PDF**; imagem serve de capa e visão conceitual.
