---
name: fluxo-n8n-miro
description: >-
  Desenha e explica fluxos do n8n num board do Miro, no padrão card + post-it que o Lucas validou.
  Cada nó vira um card cuja FORMA diz o que ele faz (retângulo processa, losango decide, círculo
  repete, hexágono chama fora, pílula dispara), com a explicação em post-it amarelo dentro do card,
  os campos preenchidos listados ao lado e o que passa entre os nós escrito no próprio conector.
  Use quando o pedido for documentar, desenhar, explicar ou arrumar um fluxo do n8n no Miro —
  inclusive a desconstrução dos fluxos existentes (Evaluador Cierres, MIB/Big Brother). Triggers:
  "desenha o fluxo no Miro", "documenta esse fluxo", "explica o fluxo visualmente", "arruma o
  fluxo do Miro", "monta o fluxograma do n8n".
---

# Fluxo do n8n no Miro

Desenho de fluxo que **explica enquanto mostra**. O problema que esta skill existe para matar:
fluxo bonito de um lado e um paredão de texto solto do outro, sem caixa, sem alinhamento e sem
dizer a que etapa se refere.

**Leia antes de desenhar:**

- `references/parametros.md` — **os números exatos que já funcionaram** (grade, ritmo vertical,
  geometria por forma, tipografia, paleta, ordem de criação). Comece por aqui: não recalibre o que
  já está medido.
- `references/padrao-visual.md` — o padrão completo, extraído elemento a elemento de uma
  referência real do Miro. É a lei do layout.
- `references/miro-mcp.md` — o que o board aceita e o que ele recusa em silêncio, com o comando
  pronto de cada peça.
- `references/verificacao.md` — **as seis provas e os scripts prontos.** A primeira delas (ler o
  `connections` do JSON) roda **antes** de posicionar qualquer nó, não no fim.
- `scripts/` — implementação de referência **pronta para rodar**: o motor (`quadro.py`), o
  fechamento (`legenda_fechamento.py`), um fluxo de exemplo completo (`exemplo_uso.py` +
  `exemplo_uso.svg`) e os quatro verificadores (`conn.py`, `conferir_envio.py`,
  `conferir_json_x_miro.py`, `conferir_contrato.py`). Ver `scripts/README.md`.

---

## Os 37 erros que já custaram rodada (não repita)

Os 9 primeiros são do fluxo de teste de 11/08; os 8 seguintes, da remontagem de 12/08; os 6
seguintes, da propagação do padrão para o fluxo inteiro, também em 12/08; os 6 de 13/08 são dos
quadros 02 a 05 e de uma natureza pior — **o board respondeu `success` e mentiu**; os **7 últimos**
(30 a 36) são de 14/08 e têm um traço em comum: **o desenho estava certo e o que mentiu foi o que
estava escrito em volta dele** — gerador desatualizado, JSON inexistente, número errado no handoff,
contagem comparada com a métrica errada, posição do frame lida do lugar errado, e uma
busca-e-substituição que corrompeu a frase que explicava a própria substituição.

Os erros 22 e 23 são caros porque **passaram no verificador**: um desenho pode ter zero sobreposição
e ainda assim contar uma mentira sobre o fluxo, ou estar desalinhado num eixo que o script não olha.
Geometria limpa não é desenho certo.

Os erros 24 a 26 são piores ainda, porque **quebram a própria conferência**: uma fórmula da skill
estava errada para o caso da criação, a ferramenta de conserto não conserta, e o read-back que
alimenta o verificador corta elementos sem avisar. Ver `references/miro-mcp.md` → "A semântica do
`y`, resolvida".

O erro 27 fecha o ciclo: **o verificador de geometria nunca vai ver traçado de conector.** Ele mede
retângulos. Uma diagonal cruzando o quadro inteiro passa nele com nota máxima — só o print pega. Por
isso o roteamento virou regra mecânica, e não item de bom senso.

| # | Erro | O que fazer |
|---|---|---|
| 1 | `<polygon>` para losango — virou retângulo **em silêncio**, sem erro | Usar `data-shape="rhombus"` num `<rect>` |
| 2 | Vão de 80px entre nós — o rótulo do conector atropelou dois cards | Vão de **300px** e rótulo de até ~16 caracteres |
| 3 | Ramificação descendo do losango cortou o post-it e a lista dele | Alternar o bloco de explicação para **cima** |
| 4 | `y` fixo em todas as listas de campos — cada uma nasceu numa altura | Ler a altura real do board e recalcular (2 passadas) |
| 5 | Escolhi 40px de folga "porque parecia bom" | Copiar a distância que **já existe** no desenho (15px) |
| 6 | Medi espaçamento em print de frame inteiro (faixa = 4 pixels) | Zoom via `?moveToWidget=<id>` e calibrar pela espessura da faixa |
| 7 | Movi rótulo da legenda sem restabelecer `width` — quebrou no meio da palavra | Restatar `width` junto de `x`/`y` |
| 8 | Editei filho de frame sem `data-frame` e sem o rect do frame — falhou | Usar o envelope completo do `<g>` |
| 9 | Afirmei que havia borda escura porque o read-back dizia `#1a1a1a` | Read-back **não** descreve o render: confirmar no print |
| 10 | Desenhei o fluxo na **vertical**, com as explicações em colunas ao lado | Horizontal, explicação abaixo do nó |
| 11 | Ramificação na **diagonal** — sem "acima" e "abaixo" da linha, etiqueta não tem onde ficar | Ortogonal, com pontos de junção |
| 12 | Conectei um ramo no **topo** do card e o outro na lateral | Só pelas **laterais**, sempre |
| 13 | Blocos encostados na ponta esquerda do trecho, com vazio à direita | Centralizar no **meio** de cada sobra de linha |
| 14 | Botei a lista dentro de um card — **quebrou o formato de lista** e virou texto corrido | Lista fica fora de card; só observação vai em card |
| 15 | Usei post-it amarelo para observação | Amarelo é só "o que faz"; observação é card cinza `rx=16` |
| 16 | Calculei posição confiando no `y` — que é **topo na criação e centro na atualização** | Escrever, ler, **medir a folga real**, ajustar |
| 17 | Disse "conferi" tendo rodado só o verificador, **sem abrir o board** | Verificador varre, print decide. Os dois, nessa ordem |
| 18 | Movi post-its declarando `<rect>` sem `data-type="sticky"` — **17 falharam de uma vez** | Stub de post-it existente **sempre** carrega `data-type="sticky"` |
| 19 | ~~Mandei o `y` da lista como topo; o Miro leu como **centro**~~ **CORRIGIDO em 13/08, ver erro 24** | Na **criação**, `y` é o topo. Não compensar |
| 20 | O script de ajuste assumiu "lista abaixo da faixa" e quebrou o **bloco espelhado** | No bloco espelhado a lista fica **acima** da faixa "Campos" |
| 21 | Insisti em encolher o frame; ele recusou **mesmo com todos os filhos dentro** | Frame só cresce com segurança. Dimensione **antes**, não depois |
| 22 | Desenhei 3 ramos paralelos **em cascata**, confundindo tempo de execução com topologia | Ler `connections` do JSON e desenhar o que está lá. Tempo vai na observação |
| 23 | Estreitei o bloco de 620 para 440 e movi **só a faixa de cima e a lista** | Bloco é **um conjunto**: faixa, lista, faixa "Observações" e cards andam juntos |
| 24 | Apliquei a fórmula `y + altura/2 − 12` **na criação** e as 24 listas nasceram meia altura abaixo do lugar: a de payload foi parar **em cima da linha do fluxo**, com o rótulo do conector escrito por cima dela | Na **criação** o `y` de um `<textArea>` é o **topo**. Mandar o topo desejado, sem conta nenhuma |
| 25 | Tentei consertar movendo as listas com `canvas_update_from_svg`: respondeu `24 updated`, ecoou o `y` novo, e **nenhuma se moveu** no board. Testei com −300px para ter certeza | `update` **não move `<textArea>`**. Acertar na criação; consertar exige apagar e recriar |
| 26 | Declarei "0 sobreposições" a partir de um read-back que **cortou 13 elementos em silêncio** | `canvas_read_as_svg` para em **500 elementos** no board inteiro. Conferir `item_count` contra o que o SVG traz |
| 27 | Liguei um nó do corredor 2000 direto ao loop do corredor 3600 e o roteador traçou uma **diagonal atravessando o quadro**. O verificador aprovou: ele mede caixas, não traçado | Conector entre `y` diferentes **exige ponto de junção**. É mecânico: `y_origem ≠ y_destino` → junção obrigatória |
| 28 | Pedi `ibm_plex_mono` e as 10 primeiras listas voltaram em `noto_sans`, sem erro nenhum | O nome aceito é **`Plex Mono`**. Conferir a fonte no read-back, igual se confere `data-shape` |
| 29 | Gerei o conteúdo do quadro 02 **sem acentos** enquanto o quadro 01, aprovado, tem acentuação correta | Copiar do quadro de referência também a **grafia**. Inconsistência de acento é visível e desqualifica o board inteiro |
| 30 | A diagonal do quadro 05 foi corrigida **à mão no board** em 13/08 e nunca voltou ao gerador. Um mês depois o `q05.py` ainda produzia o defeito: quem regerasse traria a diagonal de volta | **Correção no board sem correção no gerador é dívida silenciosa.** O gerador é a fonte; consertar só o resultado deixa a armadilha armada. Se o conserto foi manual, portar para o código no mesmo dia |
| 31 | Bloco espelhado (`cima=True`) de um nó perto do topo nasceu com `y` **negativo** — fora do frame. O verificador de sobreposição aprovou: ele compara elementos **entre si**, nunca contra os limites do frame | Prova nova no `verifica()`: `x < 0` ou `y < 0` é **FORA DO FRAME**. Antes de usar `cima=True`, conferir se a altura do bloco cabe entre o nó e o topo |
| 32 | O fluxo de áudio existia como **desenho no Miro e em mais lugar nenhum**: a decisão de 12/08 que o criou nunca virou JSON. A topologia dele não tinha fonte para o `conn.py` ler | **Todo quadro desenhado tem JSON correspondente**, mesmo que seja só esqueleto (nós + `connections`). Sem isso a regra "topologia vem do JSON" não tem de onde sair, e a próxima sessão desenha de memória |
| 33 | O handoff da sessão seguinte mandava conferir `created_count` **169** no quadro 05 e **1.145** no total. O gerador produz **168** e **1.144**: os números foram escritos no fim da sessão, antes do último ajuste do quadro. Quem seguisse o documento ia olhar o `created_count: 168` de um envio **correto** e concluir que o Miro tinha comido um elemento | **Número esperado em documento se copia da saída do gerador, na hora de escrever o documento — nunca de memória.** E ao ler um handoff, o primeiro passo é **regerar e comparar**: divergência é do documento até prova em contrário, porque o gerador é a fonte. Ver a regra abaixo |
| 34 | O número que o gerador imprime **não é** o `created_count` do board. O gerador diz `elementos: 168`; o Miro devolveu **196**. Comparar os dois reprova um envio perfeito — e é a mesma armadilha do erro 33, uma camada abaixo | **`created_count = elementos + conectores + 1 (o frame)`.** Medido nos cinco quadros em 14/08: 393 · 202 · 266 · 276 · 196, total **1.333** itens para 92 nós. Escrever a fórmula ao lado do número, nunca só o número |
| 35 | Mandei o frame em `translate(0,80000)` e ele nasceu **muito longe disso**, logo abaixo do frame criado no envio anterior. O `translate` que volta no `result_svg` é relativo, não a coordenada do board | **O composer ignora o `y` do `translate` e empilha cada documento novo abaixo do último.** Quem define a ordem no board é a **ordem de envio**, não o gerador: enviar em ordem numérica se a leitura do board importar. Conferir a posição real com `board_list_items` (`origin: center`), nunca pelo `translate` devolvido |
| 36 | Uma busca-e-substituição em massa de `TRK-8842` → `5f94d8f1` trocou também a frase que **explicava** a substituição, e ela passou a dizer *"não é 5f94d8f1 como os exemplos antigos diziam"* — afirmando o contrário do que o board mostra dois blocos ao lado | **Substituição em massa não distingue o dado da explicação sobre o dado.** Depois de trocar um identificador em lote, reler as frases que **citam** o valor antigo: elas são justamente as que precisam manter o valor antigo para fazer sentido |
| 37 | Escrevi a prova 7 e ela **acusou defeito inexistente em 3 dos 4 contratos**, duas versões seguidas: o marcador casava com a primeira ocorrência em vez da última, e o regex não via campo que abre uma string Python (conjunto vazio → tudo parece ausente). Eu quase "consertei" três quadros que estavam certos | **Verificador que só foi visto aprovando não foi verificado.** Calibrar em três passos: roda no estado bom (tem que dar OK) → reintroduz o defeito conhecido (tem que **acusar e nomear**) → restaura (tem que dar OK). Sem o passo do meio, "todos batem" pode significar "não olhei nada" |
| 38 | Ao **desfazer** um defeito plantado na calibração da prova 8, usei como âncora de substituição um trecho que **não era único** no arquivo (`Campos · tipo: Merge` — e `Merge` existe de verdade em outros nós do mesmo quadro). O `assert` estourou, e o SVG já tinha sido **regerado com o defeito dentro** | **Plantar defeito exige plano de remoção tão preciso quanto o de inserção.** Ancorar em trecho que inclui a linha seguinte, contar as ocorrências antes de trocar, e **regerar o artefato depois de restaurar**, nunca antes. Quem salvou foi a própria prova nova, que continuou vermelha |
| 39 | Reescrevi os cinco quadros com os payloads "completos" à mão e sobraram **6 `[...]` e `{...}`** escondendo campo. A prova 9, escrita depois, achou os seis. E ao desfazer um defeito plantado na calibração dela, um slice de string errado deixou o `v3_q05.py` **sem fechar uma string** — e a prova 9 passou VERDE, porque ela lê texto e não executa | **Atenção não é varredura.** Payload completo se prova com script, nunca com releitura. E **prova que lê texto não substitui rodar o gerador**: a ordem é gerador limpo primeiro, provas depois. Duas vezes no mesmo dia o passo 3 da calibração pegou erro meu na **remoção** do defeito plantado, não na inserção |
| 40 | O `v4_render.py` distribui ramo **sempre para baixo**: a cadeia principal fica no corredor 0 e cada ramo ganha o corredor seguinte, 1, 2, 3. Com os três subfluxos do q01 isso pôs **um na linha e dois embaixo**, a 3.630 e 5.131 px da linha — e com os dois gatilhos convergindo, um na linha e um 2.240 px abaixo. O Lucas viu no print em segundos: *"um monte de seta se sobrepondo, as ramificações toda erradas"* | **A regra de distribuição já estava escrita nesta skill e o gerador não a implementa: N ímpar usa a linha principal, N par não usa.** Três ramos = um acima, **um na linha**, um abaixo. Dois ramos = nenhum na linha, simétricos. Corredor precisa ter **sinal** (negativo = acima), não só crescer para baixo. E a distância de cada ramo sai da **altura do bloco de explicação** do nó daquele ramo, nunca de um valor fixo |
| 41 | Duas linhas chegando no mesmo nó dividiram o **último trecho horizontal** e ficaram uma sobre a outra: `Cron diario` ia direto a `Parametros da rodada`, e `Executar manualmente` subia por um cotovelo até a mesma altura em x=1460 e seguia horizontal até x=1900. De 1460 a 1900, duas setas no mesmo `y` | **Convergência de N entradas exige UM ponto de junção compartilhado, e dali um único segmento até o nó.** É a mesma regra que a seção do loop já enuncia ("sem esse ponto, as duas dividiriam o último trecho e ficariam uma sobre a outra") — ela vale para **toda** convergência, não só para o retorno do loop |
| 42 | A coluna vertical do cotovelo do ramo de baixo subiu em **x=1460**, e o bloco de explicação do trecho ocupa **x=1340 a 1700**. A linha atravessou o card de "Observações" inteiro. É o erro 3 de novo, agora vindo do gerador em vez da mão | **Coluna de dobra e bloco de trecho são faixas verticais que não podem coincidir.** A regra da seção de loop ("a coluna de subida fica ENTRE o bloco do trecho e o círculo") vale para qualquer dobra: calcular a coluna **fora** do intervalo `[x_bloco, x_bloco + largura]`, ou mover o bloco. Quem decide é aritmética, não olho |
| 43 | Declarei "0 sobreposições nos 5 quadros" e mandei ao board. Os erros 40, 41 e 42 estavam todos lá. O `verifica()` aprovou porque ele compara **caixa contra caixa** — e nenhum dos três é caixa sobre caixa: são **linha sobre caixa** e **linha sobre linha** | **O verificador de geometria mede o que é caixa; conector é invisível para ele (erro 27), e isso inclui as colunas de dobra que o próprio gerador calcula.** Como essas colunas são geradas por código, elas **podem** ser verificadas: tratar cada segmento vertical de dobra como um retângulo de 1px de largura e rodá-lo contra os cards. Sem isso, "0 sobreposições" só cobre metade do desenho e a outra metade vai para o board sem ninguém olhar |

**O padrão por trás da maioria:** eu confiei numa evidência que não podia responder à pergunta.
`success: true` não prova forma; read-back não prova aparência; print de frame inteiro não prova
espaçamento; verificador de geometria não prova que está bonito **nem** que não há sobreposição, se
a âncora estiver errada. **Escolha a evidência pela pergunta**, não pela facilidade.

---

## Regra que resume tudo

> **Todo texto pertence a um recipiente, e todo recipiente tem um rótulo acima dele.**
> Texto que não está dentro de nada está errado.

E a consequência: **linha significa uma coisa só, fluxo de execução.** Não existe linha tracejada
ligando explicação a nó. O pertencimento é dito por contenção, faixa e alinhamento — se você
sentiu falta de uma tracejada, o layout está errado, não faltando linha.

---

## A forma do card diz o que o nó faz

A cor diz de que categoria o nó é. A **forma** diz o que ele faz com o dado. As duas juntas
deixam o fluxo legível antes de qualquer leitura.

| O que o nó faz | Forma | Exemplos no n8n |
|---|---|---|
| **Dispara o fluxo** | pílula (`rect` com `rx` alto) | Webhook, Schedule, Manual Trigger, Execute Workflow Trigger |
| **Processa, transforma ou consulta** | **retângulo** (o padrão) | Set, Code, HTTP Request, Postgres, Metabase, OpenAI, Merge |
| **Decide um caminho** | **losango** (`data-shape="rhombus"`) | If, Switch, Filter |
| **Repete** | **círculo** | Loop Over Items, Split In Batches |
| **Sai do fluxo e volta** | **hexágono** (`data-shape="hexagon"`) | Execute Workflow, chamada a API de terceiro, subfluxo |
| **Espera** | elipse | Wait |
| **Encerra ou grava o resultado** | retângulo de canto forte (`rx="16"`) | gravação final na tabela, resposta ao webhook |

Retângulo é o padrão e a maioria: **só troque a forma quando o nó realmente fizer algo diferente**.
Fluxo com sete formas diferentes em nove nós não comunica nada.

### Como declarar cada forma (testado no board, 11/08/2026)

**Nunca use `<polygon>` para losango.** O Miro tenta adivinhar a geometria e, quando não
reconhece, vira retângulo **em silêncio** — sem erro e sem entrar em `failed_items`. Aconteceu no
teste: o losango virou retângulo e só apareceu ao ler o board de volta.

Declare o nome da forma num `<rect>`. Os tamanhos abaixo são os **corrigidos** depois do teste, já
com a área que o texto precisa. Todas as formas de uma fileira compartilham o **centro vertical**
(aqui, y = 620):

```xml
<!-- pílula de gatilho: retângulo com rx alto -->
<rect id="n1" x="60" y="580" width="280" height="80" rx="40" fill="#6C5CE7"
      data-content="Agenda diaria 8h"
      data-font-size="18" data-font-family="Roboto Mono" data-text-color="#FFFFFF"/>

<!-- processa: o retângulo padrão -->
<rect id="n2" x="640" y="580" width="280" height="80" fill="#2D9BF0"
      data-content="Busca aniversariantes" data-font-size="18" .../>

<!-- losango de decisão: 300x150, MAIOR que o retângulo por causa da área útil -->
<rect id="n3" x="1220" y="545" width="300" height="150" data-shape="rhombus"
      fill="#F2A33C" data-content="Achou alguem?" data-font-size="16" .../>

<!-- círculo de loop: r=78 -->
<circle id="n4" cx="1940" cy="620" r="78" fill="#F2A33C"
        data-content="Um por vez" data-font-size="15" .../>

<!-- hexágono de chamada externa: 280x120 -->
<rect id="n5" x="2380" y="560" width="280" height="120" data-shape="hexagon"
      fill="#00B86B" data-content="Envia WhatsApp" data-font-size="17" .../>

<!-- elipse de espera -->
<ellipse id="n6" cx="3100" cy="620" rx="145" ry="58" fill="#F2A33C"
         data-content="Espera 2s" data-font-size="18" .../>

<!-- encerra ou grava: canto forte -->
<rect id="n7" x="3540" y="580" width="280" height="80" rx="16" fill="#DA0063"
      data-content="Grava o log" data-font-size="18" .../>
```

**Confirmados por teste:** `rhombus`, `hexagon`, `circle`, `ellipse`, `rect` com e sem `rx`.
Qualquer outro nome do catálogo do Miro: testar e conferir no read-back antes de usar em entrega.

**Obrigatório depois de criar:** ler o board de volta com `canvas_read_as_svg` e conferir se cada
forma voltou como a que foi pedida. Degradação silenciosa não aparece na resposta de criação.

**Losango e círculo têm pouca área útil no meio**, e foi por isso que precisaram crescer (losango
de 280×120 para 300×150; círculo de r=60 para r=78). Mesmo grandes, o texto dentro deles é de 2 a
4 palavras. Se não couber, o detalhe vai no post-it, nunca espremido na forma.

---

## O fluxo corre na HORIZONTAL (regra do Lucas, 12/08)

Esquerda para a direita, sempre. Vertical foi testado e reprovado: *"fica uma coisa do lado da
outra"*, sem hierarquia. Na horizontal, o que explica o nó desce **abaixo dele**, e o que passa
**entre** os nós vive na linha.

```
        ┌─────────────────────────┐          ← ACIMA da linha, 20px:
        │ sai do 3 · entra no 4   │            faixa + a LISTA do que passa
        ├─────────────────────────┤
        │ 1 item:                 │
        │ { janela_dias: 30, ...} │
        └─────────────────────────┘
  ┌────┐                              ┌────┐
  │ NÓ │══════════════════════════════│ NÓ │   ← a linha
  └────┘                              └────┘
  ┌────┐ ┌─────────────────────────┐  ┌────┐
  │Oque│ │ Observações             │  │Oque│   ← ABAIXO da linha, 20px:
  │faz │ ├─────────────────────────┤  │faz │     faixa + cards cinza
  └────┘ │ ╭─────────────────────╮ │  └────┘
  ┌────┐ │ │ card cinza, rx=16   │ │  ┌────┐
  │post│ │ ╰─────────────────────╯ │  │post│
  │ it │ └─────────────────────────┘  │ it │
  └────┘                              └────┘
  ┌────┐                              ┌────┐
  │Camp│                              │Camp│
  └────┘                              └────┘
  │lista│                             │lista│
```

**O que sai de A É o que entra em B.** É um item só, nunca dois. O card na linha diz
"sai do 3 · entra no 4" e mostra o payload inteiro, com todos os detalhes.

**Amarelo é só para "o que faz".** Observação nunca é post-it amarelo: é card cinza claro
(`#F5F5F5`) de canto arredondado (`rx="16"`), letra preta. A cor separa "explicação do nó" de
"nota sobre o que passa".

**A lista fica fora de card.** Testado: enfiar a lista dentro de um card/sticky quebra o formato de
lista e vira texto corrido. Payload é `<textArea>` monoespaçado; só a observação vai em card.

---

## Proporção: tudo centralizado no trecho de linha

Esta é a regra que faz o desenho parecer feito por alguém, e não empurrado para a esquerda.

**Passo 1 — o nó vai no MEIO do trecho horizontal dele.** Meça a linha de ponta a ponta (da dobra
de origem até a dobra de destino) e ponha o centro do card no meio exato.

**Passo 2 — cada sobra de linha tem o próprio meio.** Sobrou linha à esquerda do nó e à direita.
Cada sobra recebe seu bloco (faixa + lista em cima, faixa + observações embaixo) **centrado no meio
dela**.

```
   |<------------------- trecho da linha ------------------->|
   |<---- sobra esq ---->|<-- NÓ -->|<---- sobra dir ------->|
            ▲                 ▲                ▲
         centro            centro           centro
      bloco esquerdo      o card         bloco direito
```

Sem isso, os blocos encostam na ponta esquerda e sobra um vazio à direita — e a distância do nó 3
para o 4 fica diferente da do 4 para o 6, mesmo com o mesmo vão.

**Passo 3 — um eixo vertical só.** Faixa "sai e entra", lista, faixa "Observações" e cards de
observação: todos com o **mesmo centro**. Imagine uma linha atravessando o meio dos quatro.

---

## Ramificação: nunca diagonal, nunca pelo topo

Duas leis, e as duas vieram de erro cometido:

1. **Linha de ramificação é sempre ortogonal.** Reta na horizontal, reta na vertical, e dobra. Nada
   de diagonal — na diagonal não existe "acima da linha" nem "abaixo da linha", e não há onde pôr
   as etiquetas.
2. **Conector entra e sai pelas LATERAIS do card.** Nunca pelo topo, nunca pela base. Se você
   conectar um pelo topo e outro pela lateral, o desenho fica torto e some a simetria.

**O padrão, e ele é espelhado na saída e na entrada:**

```
                       ┌──────┐
              ┌────────│ NÓ 4 │
              │        └──────┘
   ┌──────┐   │                    │   ┌──────┐
   │ NÓ 3 │───●────────────────────●───│ NÓ 6 │
   └──────┘   │                    │   └──────┘
              │        ┌──────┐    │
              └────────│ NÓ 5 │────┘
                       └──────┘
```

Sai do 3 pela lateral, corre reto, **uma coluna de dobra** manda uma linha para cima e outra para
baixo, e cada uma dobra e entra pela lateral do seu card. Na chegada, o espelho: cada card sai pela
lateral, corre, encontra a **coluna de dobra do destino**, e as duas entram juntas pela lateral do
nó de junção.

Com três ramificações: a mesma coluna de dobra, uma linha para cima, uma reta e uma para baixo.

**Como fazer a dobra na prática:** o Miro **ignora** `data-shape="elbowed"` — está medido em
`references/miro-mcp.md`. A dobra se constrói com **pontos de junção**: um `<circle r="5"
fill="#000000">` em cada canto, e conectores retos entre eles. Dois pontos alinhados no mesmo `y`
dão um segmento horizontal; no mesmo `x`, vertical. É determinístico e não depende do roteador.

O trecho horizontal precisa ser **longo** (≥1000px): é nele que as etiquetas moram.

### Ramificação com três ou mais ramos (medido em 12/08)

Mesma geometria, uma coluna de dobra só. O que muda é o **cálculo da altura de cada ramo**, e ele
não é livre: **quem manda é a altura do bloco de explicação do nó do ramo de cima.**

```
 ramo cima   y = Yc  ──●─────────[ NÓ ]─────────●──
                       │       explicação        │
                       │       desce até aqui ↓  │
 linha        y = 2600 ─●─────────[ NÓ ]─────────●──   dobra saída x=Xs
                       │                         │    dobra entrada x=Xe
 ramo baixo   y = Yb  ──●─────────[ NÓ ]─────────●──
```

**A conta, na ordem:**

1. Meça a altura do bloco de explicação de cada nó: `26 + 15 + (n_postits × 234) + ((n−1) × 30) + 40 + 26 + 15 + altura_da_lista`.
   Atalho medido: **3 post-its + lista longa ≈ 1400px**; 2 post-its + lista média ≈ 950px;
   2 post-its + lista curta ≈ 770px.
2. `Yc = 2600 − (altura do bloco do nó de cima) − 200` de folga. No Fluxo Geral deu **1000**.
3. `Yb = 2600 + (altura do bloco do nó do meio) + 300` de folga. Deu **3900**.
4. `Xs` = borda direita do nó de origem + ~360. `Xe` = borda esquerda do nó de destino − ~700.
5. Os nós dos ramos ficam todos no **mesmo x**, centrado entre `Xs` e `Xe`.

**Não copie 1800 de distância entre ramos** (o número da ramificação de dois ramos): com três nós de
alturas diferentes, distância fixa faz o bloco de cima invadir a linha do meio. Calcule.

**Não colidem, e é por isso:** o bloco de explicação de um nó fica no **x do nó** (centrado entre
`Xs` e `Xe`), e os blocos de trecho ficam no **x das sobras** (esquerda e direita). São faixas
verticais diferentes, então cada uma pode descer o quanto precisar.

---

## Lado a lado ou ramificação? A decisão é MECÂNICA, lida do JSON

> **Esta é a seção que mais custou.** Nas três rodadas de 12/08 o Lucas teve que me corrigir sobre
> isso, e as três vezes eu tinha decidido "no olho" em vez de ler o `connections`. Ele fechou assim:
> *"até a lógica de olhar quando faz sentido um card do fluxo ficar ao lado do outro e quando deve
> virar ramificação, essa lógica você precisa ter guardado."*
>
> **Não existe julgamento aqui.** Rode o `conn.py`, conte as setas, aplique a tabela.

### Passo 1 — conte as setas de cada nó no `connections`

```
saidas(N)  = quantas linhas do conn.py têm N como origem
entradas(N)= quantas linhas do conn.py têm N como destino
```

### Passo 2 — a tabela decide, sem opinião

| O que o JSON mostra | Desenho | Nunca |
|---|---|---|
| `saidas(A) = 1` e o destino tem `entradas = 1` | **lado a lado**, linha reta | — |
| `saidas(A) = N ≥ 2` | **N ramos empilhados** saindo de A | cascata `A→B→C` |
| `entradas(Z) = N ≥ 2` | **N ramos empilhados** convergindo em Z | um só ramo chegando |
| `saidas(A) = N` **e** os N voltam ao mesmo Z | ramificação **completa**: abre em A, fecha em Z | — |
| `saidas(A) = N` e um dos destinos **não aparece como origem** | esse ramo é **ponta terminal**: entra e morre | continuar a corrente por ele |
| nó com saídas nomeadas (`[saida 0]` e `[saida 1]`) | ramos empilhados, **rotulados** com o nome (`done` / `loop`) | tratar como se fossem iguais |
| `entradas(Z) = 1` mas vindo de um nó já desenhado longe | linha reta longa, ou dobra ortogonal | inventar nó intermediário |

**A pergunta que resolve 100% dos casos:** *"o nó B recebe de mais alguém além de A, ou A manda para
mais alguém além de B?"* Se a resposta for não para as duas, é lado a lado. Qualquer outra coisa é
ramificação.

### Passo 3 — o número de ramos define a geometria vertical

Isto também está medido, e a diferença entre 2 e 3 **não é escalar** — muda quem ocupa a linha
principal:

| N ramos | Quem fica na linha principal | Distribuição | Caso real no board |
|---|---|---|---|
| **2** | **ninguém** — a linha passa vazia entre eles | um acima, um abaixo, simétricos | `3 → (4, 5) → 6`: ramos em 1760 e 3560, linha 2600 vazia |
| **3** | **o ramo do meio**, no próprio `LINE_Y` | um acima, um na linha, um abaixo | `7 → (8, 9, 10) → 11`: ramos em 1000, **2600** e 3900 |
| **4** | ninguém | dois acima, dois abaixo | não ocorreu ainda — manter a simetria |
| **6** | **ninguém** | três acima, três abaixo | quadro 04: `saidas(2) = 6` consultas ao banco |
| **N ímpar** | o do meio | resto dividido acima e abaixo | — |

**A regra em uma linha:** **N par não usa a linha principal; N ímpar usa.** Errar isso deixa o
desenho assimétrico e a linha principal “sobrando” no meio do nada.

E a **altura** de cada ramo não é fixa: sai da altura do bloco de explicação do nó daquele ramo (ver
"Ramificação com três ou mais ramos" e a tabela de alturas em `references/parametros.md`). Copiar
1800 de distância porque funcionou na de dois ramos **quebra** quando os nós têm alturas diferentes.

### Muitos ramos quase iguais: fiel na topologia, enxuto no conteúdo (13/08)

O quadro 04 tem `saidas(2) = 6`: seis consultas ao banco saindo do mesmo nó e voltando ao mesmo
merge. Seis ramos empilhados, portanto — a tabela não abre exceção por estética. Mas seis blocos de
explicação quase idênticos são o **paredão de texto** que esta skill existe para matar.

A saída não é agrupar ramo (isso mentiria sobre o fluxo). É escolher **onde** o bloco mora:

| Onde | Quantos blocos | Por quê |
|---|---|---|
| trecho de **saída**, antes da coluna de dobra | **um só** | ali o fio ainda é um: o payload é o mesmo para os seis |
| cada **perna de volta**, depois do ramo | **um por ramo** | ali os payloads divergem de verdade, cada um entra numa entrada diferente do merge |

E a razão vai escrita num card de observação no próprio quadro, senão a próxima pessoa lê como
descuido. **Repetição que o desenho não precisa é ruído; ramo que o JSON tem é obrigação.**

### O erro que essa tabela existe para impedir

Eu tinha escrito aqui que os três coletores do Fluxo Geral *"parecem paralelos e não são"*, porque o
tempo da rodada é a soma dos três — e desenhei `7 → 8 → 9 → 10` em cascata. O JSON dizia:

```
Normalizar base (7) → Executar Fluxo WhatsApp
Normalizar base (7) → Executar Fluxo Aircall
Normalizar base (7) → Executar Fluxo Meeting
   os três → Juntar retorno (11), entradas 0, 1 e 2
```

`saidas(7) = 3` e `entradas(11) = 3`: ramificação completa, três ramos. **Confundi tempo de execução
com topologia.** Que o n8n rode um por vez é verdade, e é verdade que vai num **card de observação** —
não no traçado. O Lucas pegou em uma frase: *"o fluxo oito não entra no fluxo nove."*

O mesmo erro estava no corpo do loop: `saidas(Abrir clientes do grupo) = 2`, e `Gravar conversa
completa` **nunca aparece como origem** — é ponta terminal. Eu tinha desenhado a cascata
`17 → 18 → 19 → 20`.

> **Tempo de execução, ordem de leitura e "fica mais bonito" NÃO entram nesta decisão.**
> Só o `connections`.

---

## O nó de loop, desenhado inteiro (validado pelo Lucas em 12/08)

O `Loop Over Items` é o desenho mais difícil do n8n, e o Lucas fechou a forma dele mandando um print
do canvas real: **`done` sai por cima, `loop` sai por baixo, o corpo do loop corre no corredor de
baixo, e o retorno volta por um corredor mais baixo ainda até a entrada do próprio loop.**

```
                                      ramo done
                           ┌───────────●──────────[ RESUMO ]
                           │
   [ANTERIOR]────●───( LOOP )●        pin recebe DUAS linhas
                 │         │  └───●──[ A ]──●──[ B ]──[ C ]──●   ramo loop
                 │         pout    │              dobra do    │
                 │                 └──[ D ]      corpo        │
                 │                     ponta terminal         │
                 └────────────────────────────────────────────●
                              corredor de retorno
```

**As quatro regras que fazem isso funcionar:**

1. **O ponto de entrada recebe duas linhas, e isso é de propósito.** A linha do nó anterior chega
   por **horizontal** e a do retorno chega por **vertical**, no mesmo `<circle r="5">`. Dali sai um
   **único segmento curto** até o círculo do loop. Sem esse ponto, as duas dividiriam o último
   trecho e ficariam uma sobre a outra — e não há como o roteador do Miro evitar isso.
2. **A coluna de subida do retorno fica ENTRE o bloco do trecho e o círculo.** No Fluxo Geral: bloco
   do trecho ocupa 17000–17440, a coluna sobe em **17800**, o círculo começa em 18000. Aperte isso e
   a linha atravessa o bloco.
3. **O corredor de retorno passa por baixo de TUDO.** Meça o fundo do bloco de explicação mais baixo
   do corpo do loop e desça mais 300 a 500. No Fluxo Geral o mais baixo terminava em 6540 e o
   corredor ficou em **7000**.
4. **O círculo é menor que o card** (r=110 contra 440 de largura), então a faixa de 440 dele fica
   centrada no centro do círculo: `x = cx − 220`.

**Ponta terminal existe e precisa aparecer.** No corpo do loop do Fluxo Geral, `Gravar conversa
completa` recebe do nó anterior e **não alimenta ninguém** — o `connections` do JSON não o lista como
origem. Isso vai para um ramo próprio que simplesmente termina, e a observação diz por quê: *"é
ponta final: grava e para. Quem devolve o fio pro loop é o outro ramo."* Desenhar ponta terminal
dentro da corrente principal inventa um fluxo que não existe.

---

## Anatomia de um nó no board

Foi esta a montagem validada no board (empilhada, uma coluna por nó):

```
   ├────────── 280 ──────────┤   ├── 300 (vão) ──┤

   ╔═════════════════════════╗                        ← forma na cor da categoria,
   ║     NOME DO NÓ          ║ ──── "N clientes" ───▶   nome igual ao do n8n
   ╚═════════════════════════╝                          rótulo do conector no vão
              ↕ 42 (da forma MAIS ALTA da fileira)
   ┌─────────────────────────┐
   │ O que faz               │  faixa cinza, largura TOTAL do card
   └─────────────────────────┘
              ↕ 15
        ┌───────────────┐
        │   post-it     │        200x130, recuado 40 — mais estreito que a faixa
        │   amarelo     │
        └───────────────┘
              ↕ 30
   ┌─────────────────────────┐
   │ Campos                  │  faixa cinza, largura TOTAL
   └─────────────────────────┘
              ↕ 15  ← igual ao espaço da faixa pro post-it. Mesma régua.
     1. campo = valor
     2. campo = valor          lista, width 260, recuada 10
```

Os números exatos, com o cálculo do `y` da lista, estão em `references/parametros.md`.

- **Faixa cinza** ocupa a largura inteira do card. **Post-it não.** Esse desencontro é o que faz
  uma ler como título e a outra como conteúdo. Se as duas tiverem a mesma largura, viram duas
  listras e a hierarquia morre.
- **Campos** ficam num bloco à direita ou abaixo, sob a própria faixa, alinhados como irmãos do
  post-it.
- **O que passa entre os nós** vai no `data-content` do conector. É nativo do Miro, mas o rótulo
  fica **em cima da linha, centralizado**, e não desvia de nada. Então: vão entre nós de **pelo
  menos 300px** e rótulo de até ~16 caracteres. O detalhe longo vai no post-it, nunca na linha.
- **Entre uma faixa e o bloco abaixo dela, 15px — sempre o mesmo valor**, seja post-it ou lista de
  campos. A distância da lista para a faixa dela tem que ser igual à do post-it para a faixa dele.
  Não escolha um valor novo: copie o que já existe no desenho.
- **A lista de campos exige duas passadas.** O `y` de um `<textArea>` é âncora de **centro**, e a
  altura dele é automática, então listas com número de linhas diferente nascem em alturas
  diferentes com o mesmo `y`. Crie, leia a altura real no board, e reposicione com
  `y = topo_desejado + altura/2 − 12`. Detalhe e medições em `references/miro-mcp.md`.

### O bloco de explicação pode ficar ACIMA do nó (regra do Lucas, 11/08)

A ordem de leitura é a mesma; o que muda é o sentido. Acima do nó, lê-se **de baixo para cima**:

```
       lista de campos          ↑
       ┌───────────┐            │  ordem de leitura
       │ Campos    │            │  de baixo pra cima
       └───────────┘            │
       ┌───────────┐            │
       │ post-it   │            │
       └───────────┘            │
       ┌───────────┐            │
       │ O que faz │            │
       └───────────┘            │
       ┌═══════════┐
       ║  NÓ       ║   ← o card fica na base do bloco
       └═══════════┘
```

Mesmos espaçamentos, mesma largura, mesmo tudo. Só o sentido inverte.

**Para que serve:** liberar corredor. Se a explicação está embaixo, o espaço de baixo está ocupado
e uma ramificação que descer vai cortar o post-it e a lista. Alternar o bloco para cima libera o
caminho de baixo, e vice-versa.

### Ramificação pode ir para qualquer lado; descrição não

| | Onde pode ficar |
|---|---|
| **Ramificação** (conector para outro nó) | cima, baixo, lados **e diagonal** |
| **Descrição** (faixa, post-it, lista) | cima, baixo ou lado. **Nunca diagonal.** |

**Quando um nó tem várias ramificações:** decida primeiro para onde vão os desvios, depois
posicione a descrição no lado que sobrou. Se o nó tem três saídas e o espaço aperta, puxe as
ramificações na **diagonal** — é o recurso que existe justamente para isso.

**Se faltar espaço em cima:** cresça o frame para cima e mantenha a legenda colada no topo. Canvas
é infinito; aperto de espaço nunca é motivo para sobrepor.

---

## Texto grande vira vários post-its, nunca um bloco

Se a explicação de um nó não cabe confortavelmente em um post-it, ela **não vira um post-it
maior**: vira uma pilha de post-its, um por ideia, empilhados na ordem de leitura.

```
Objetivo do nó        →  post-it 1  (o que ele entrega)
Como ele faz          →  post-it 2  (o mecanismo)
Pegadinha             →  post-it 3  (o que quebra se mexer)
```

**Uma ideia por post-it.** Um post-it com quatro assuntos é o mesmo texto corrido de antes,
só que amarelo.

Quando os assuntos forem de naturezas diferentes, cada pilha ganha a própria faixa cinza
titulando: "O que faz", "Campos", "Saída", "Cuidado".

---

## Cores: sistema, não gosto

1. **Antes de desenhar, escreva a legenda.** Escolha UM critério — tipo de nó, ou subfluxo dono
   (WhatsApp, Aircall, Meeting) — e mantenha no desenho inteiro.
2. Uma cor significa **uma coisa só**. Se azul é banco, nada mais é azul.
3. A legenda fica visível num canto do board, com quadradinho de cor e nome.
4. Teto de **6 a 8 cores**. Acima disso o olho não decora e vira arco-íris: agrupe e diferencie
   por texto.
5. Cores distinguíveis entre si. Nada de dois azuis parecidos para coisas diferentes.
6. **Post-it é sempre amarelo**, em qualquer categoria. Amarelo significa "explicação".

---

## Nada pode tapar nada

**Proibido:** card sobre card, texto sobre texto, linha atravessando card, rótulo em cima da
linha, nota invadindo a borda de outro elemento.

**Permitido, e não é sobreposição:** elemento **contido** em outro (texto no card, post-it na
coluna). Contido é pertencimento, e é o que o padrão pede.

> O teste: **algum elemento ficou parcialmente escondido?** Se sim, está errado.

No Miro isso é técnico, não só estético: **texto colocado por cima de forma é descartado pelo
board** (ver `references/miro-mcp.md`). E como profundidade é ordem de criação, **as linhas têm
que ser criadas antes das formas**, senão a linha fica por cima e tapa o card.

Espaçamento: texto nunca encosta na borda do próprio recipiente; entre textos irmãos, mais que
uma altura de linha; entre cards, vão constante maior que o respiro interno; linha só toca o card
no ponto da seta. Cruzamento inevitável, a linha **contorna**.

---

## Passo 0 — pedir o link público ANTES de começar

**Sem link público eu não consigo conferir o que desenhei.** O navegador que eu abro não está
logado na conta do Miro, então uma URL comum de board devolve tela de login. E conferir é
obrigatório nesta skill: `success: true` não prova nada sobre o desenho.

Então, **na primeira mensagem**, se o Lucas ainda não mandou o link de compartilhamento, pedir
assim (e só começar depois de recebê-lo):

> Antes de eu desenhar, preciso do **link público de visualização** do board, senão eu não consigo
> abrir para conferir o resultado no final.
>
> No Miro: botão **Share** no canto superior direito → em "Anyone with the link" escolher
> **Anyone with the link** com permissão **Can view** → **Copy link**.
>
> O link vem com `?share_link_id=...` no fim. É esse que eu preciso.

Guardar as duas coisas para usar depois:

| Preciso de | Para |
|---|---|
| URL do board (`https://miro.com/app/board/<id>=/`) | criar e editar via MCP |
| Link público (`...?share_link_id=<n>`) | abrir no navegador e conferir |

Se o Lucas disser que não quer tornar público, avisar em uma linha: **eu consigo criar e consigo
ler a estrutura de volta, mas não consigo ver o desenho renderizado** — então a checagem visual
(texto espremido, respiro, hierarquia) fica com ele.

---

## O SVG se gera por código, e o verificador roda ANTES de enviar (13/08)

Os quadros 01 a 03 foram montados escrevendo SVG à mão e cada um custou rodadas de conserto. Os
quadros 04 e 05 saíram limpos de primeira, e a diferença foi só uma: **um gerador declarativo em
Python que constrói o modelo, verifica o modelo e só então emite o SVG.**

```
lista de nós (dados)  →  bloco_no() / bloco_trecho()  →  modelo em memória
                                                              │
                                              verifica(modelo)│  sobreposição + alinhamento + folga
                                                              ↓
                                                       emite o SVG  →  canvas_create_from_svg
```

Por que isso muda o jogo:

| Verificar no read-back | Verificar no modelo |
|---|---|
| depende do board responder | roda offline, em milissegundos |
| **corta em 500 elementos** e mente | conhece todos os elementos |
| a âncora do `y` é ambígua | a âncora é a que você escreveu |
| descobre o defeito **depois** de sujar o board | descobre **antes** de existir |

As funções que valeram a pena e devem ser recriadas em qualquer novo gerador:

- **`bloco_no(...)`** — monta faixa + post-its + faixa "Campos" + lista de uma vez, com `cima=True`
  para o bloco espelhado e um `base=` opcional para unificar o `y` da faixa ao longo de um corredor.
  Manter as 4 peças numa função só é o que impede o erro 23 (mover metade do bloco).
- **`bloco_trecho(...)`** — o conjunto de cima e de baixo da linha, centrado na sobra.
- **`verifica(modelo)`** — as provas 2, 3 e 4 rodando na geometria calculada, **mais a de fora do
  frame** (erro 31).
- **`verifica_conectores(modelo)`** — a prova que faltava (erro 27, e é o que pegou o erro 30).
  Regra mecânica, sem julgamento: registrar o centro de cada nó e de cada ponto de junção e, para
  todo par ligado, **se `dx > 2` e `dy > 2` ao mesmo tempo, é diagonal**. Um par legítimo é
  horizontal (`dy ≈ 0`) ou vertical (`dx ≈ 0`). Saída esperada:
  `OK: 0 sobreposicoes, 0 desalinhamentos, 0 diagonais`.
- **prova cruzada `JSON × gerador`** — conta os nós dos dois lados e confere que os números do
  desenho formam `1..N` sem furo nem repetição. Existe porque em 14/08 o quadro 05 e o JSON
  desenhavam fluxos diferentes e ninguém tinha percebido. **A ordem de declaração no gerador não
  importa** (os nós são declarados por corredor); o que importa é o conjunto. Implementação
  genérica, pronta para adaptar: `scripts/conferir_json_x_miro.py`.

- **prova de contrato entre quadros** — quando um fluxo chama outro, confere que todo campo que o
  consumidor espera existe no que o produtor declara devolver. Nasceu do defeito de um quadro
  esperar um campo que o outro não devolvia, que **as seis provas anteriores aprovaram** porque
  nenhuma delas olha campo. Detalhe e a regra assimétrica em `references/verificacao.md` →
  "Prova 7". Implementação genérica: `scripts/conferir_contrato.py`.
- **`conferir_envio.py`** — o que rodar na resposta de cada `canvas_create_from_svg`: `created_count`
  contra a fórmula, `failed_items`, `skipped`, `data-shape` de cada nó, fonte devolvida, tipos
  preservados. Existe porque essa conferência é sempre a mesma e refazê-la à mão a cada envio é
  onde entra o erro de leitura. Implementação: `scripts/conferir_envio.py`.

Implementação de referência: `scripts/` (`quadro.py` + `legenda_fechamento.py` +
`exemplo_uso.py` rodável + os dois conferidores acima). Ver `scripts/README.md` para o que cada
arquivo faz e o que precisa adaptar para o seu fluxo.

### O envio em si: o que custa e o que a ferramenta não faz (medido em 14/08)

Isto não é detalhe de conforto — muda como se planeja a sessão:

| Fato | Consequência prática |
|---|---|
| O parâmetro `svg` do `canvas_create_from_svg` é **string inline**, teto de 200.000 caracteres. **Não aceita caminho de arquivo** | O conteúdo inteiro do `.svg` atravessa a conversa a cada envio: de 43k a 88k caracteres por quadro, 292k nos cinco. É o item mais caro da sessão, e é irredutível |
| A **resposta** estoura o limite de tokens e vai para arquivo em disco | Não dá para ler a resposta direto. Extrair com script (`conferir_envio.py`), nunca tentar ler o `result_svg` inteiro |
| Enviar os cinco quadros de uma vez **não cabe** com a checagem dos 37 itens | Planejar em duas sessões: uma envia e confere integridade, a outra roda a checagem visual com contexto limpo. Prometer as duas na mesma é o que não fecha |

**Consequência de projeto:** vale o gerador emitir SVG enxuto. Cada atributo redundante em 340
elementos é custo pago duas vezes — na leitura do arquivo e na escrita do parâmetro.

⚠️ **Duas pegadinhas do gerador em si:** dois módulos que envolvem `sys.stdout` para UTF-8 derrubam
o segundo com `I/O operation on closed file` — o `utf8()` precisa de guarda de idempotência. E o
verificador do modelo **continua cego para traçado de conector** (erro 27): junção é regra na
geração, não achado da conferência.

### O gerador é a fonte — e isso vale para os NÚMEROS, não só para a geometria

Três erros seguidos (30, 32 e 33) são a mesma falha vestida de três jeitos: **o desenho estava
certo e o que estava escrito em volta dele mentiu.** Vale a pena ver os três lado a lado, porque
individualmente cada um parece descuido isolado e juntos são um padrão:

| # | O que ficou velho | Quem pagaria a conta |
|---|---|---|
| 30 | o **gerador**, consertado só no board | quem regerasse traria a diagonal de volta |
| 32 | o **JSON**, que nunca existiu para o quadro 05 | a sessão seguinte desenharia de memória |
| 33 | o **handoff**, com `created_count` de antes do último ajuste | quem enviasse reprovaria um envio correto |

**A regra, em uma frase: artefato derivado do gerador se copia da saída dele no momento de
escrever, nunca de memória e nunca de uma rodada anterior.** Isso cobre contagem de elementos, de
conectores, de nós, tamanho de SVG e coordenada de frame.

E o lado da leitura, que é onde o erro 33 morde: **ao abrir um handoff, o passo 1 é regerar e
comparar com o que o documento afirma.** Divergência entre documento e gerador é **do documento**
até prova em contrário. O caminho errado é presumir que o gerador regrediu e sair caçando defeito no
código — ou, pior, aceitar o número do documento e reprovar um envio que estava certo.

Por que este é o mais traiçoeiro dos três: número errado em documento **não falha em nada**. O
gerador roda limpo, o board aceita, tudo responde verde, e o defeito só aparece como uma conclusão
errada na cabeça de quem lê — numa sessão nova, sem contexto para desconfiar do número, lendo um
arquivo escrito justamente para ser a fonte de verdade daquele momento. É a família de defeito que
esta skill inteira persegue: **produz resultado plausível e errado, e ninguém acusa erro.**

---

## Como executar

0. **Retomando de um handoff? Regere e compare ANTES de qualquer coisa.** Rodar os geradores e a
   prova cruzada, e conferir cada número que o documento afirma (contagem de elementos, de
   conectores, de nós) contra a saída real. **Divergência é do documento até prova em contrário** —
   foi o erro 33. Corrigir o documento primeiro; sair caçando defeito no gerador, ou aceitar o
   número velho, custa a rodada.
0. **O JSON existe e está atualizado?** Se o fluxo mudou por decisão e o JSON não acompanhou, o
   `conn.py` vai ler a topologia **velha** e o desenho nasce errado — foi o erro 32. Se o fluxo nem
   tem JSON, criar o esqueleto (nós + `connections`) **antes** de desenhar: um dicionário Python com
   `nodes` (id, tipo, posição) e `connections` (o mesmo formato que o n8n exporta) já basta para o
   `scripts/conn.py` ler.
1. **Rodar o `conn.py` no JSON e desenhar a topologia dele.** Não é opcional e não é o último passo:
   é o primeiro. Quem chama quem, quantas saídas cada nó tem, e quem nunca aparece como origem
   (ponta terminal). Script em `references/verificacao.md`. **Pular isto foi o erro nº 22.**
2. **Dimensionar o frame com folga, agora.** Some a largura da grade e a altura do ramo mais baixo
   com o bloco dele, e acrescente margem. **Frame cresce, mas pode nunca mais encolher** (erro nº 21).
3. **Escrever a legenda de cores e a lista de nós** com forma e cor de cada um, antes de gerar
   qualquer SVG. Apresentar ao Lucas se o fluxo for grande.
4. **Planejar os corredores antes de posicionar qualquer explicação.** Para cada nó, decidir
   primeiro para onde saem as ramificações; só depois escolher se o bloco de explicação fica
   acima, abaixo ou ao lado. **Fazer o inverso é o que gera sobreposição** — foi o erro nº 3.
   Com três ou mais ramos, calcular a altura de cada um pela altura do bloco de explicação.
5. **Gerar o SVG por código** (ver a seção acima), na ordem: frame → legenda → conectores → formas →
   faixas → post-its → listas (conectores antes das formas por causa da profundidade). **Rodar o
   `verifica()` no modelo antes de enviar** — defeito descoberto aqui não chega a sujar o board.
   Nessa hora, varrer a lista de conectores: **todo par com `y_origem ≠ y_destino` recebe ponto de
   junção**, sem exceção e sem julgamento (erro 27).
6. **Criar** com `canvas_create_from_svg`. Iterações seguintes com `canvas_update_from_svg`,
   sempre partindo do último `result_svg`. Ao mexer em elemento existente, o stub carrega o **tipo**
   (`data-type="sticky"` em post-it), não só a geometria — erro nº 18.
7. **Se a resposta reportar dimensão alterada**, reposicionar antes de qualquer outra coisa.
8. **Ler o board de volta com `canvas_read_as_svg`, sempre.** `success: true` não prova que saiu
   o que você pediu: o Miro degrada forma que não reconhece e ignora pedido de roteamento **sem
   reportar nada**. Conferir, item por item, se `data-shape` e geometria voltaram como enviados.
9. **A lista tem que nascer no lugar certo: não existe segunda passada.** `canvas_update_from_svg`
   **não move `<textArea>`** (erro 25). Na criação o `y` é o topo, e a altura é
   `28 × linhas` para campos (Plex Mono 20) e `19,7 × linhas` para payload (Roboto Mono 14),
   mantendo 33 e 50 caracteres por linha. Detalhe em `references/miro-mcp.md`.
10. **Rodar as provas 2, 3 e 4** de `references/verificacao.md`: sobreposição, **alinhamento** e folga
    da lista. A de alinhamento existe porque a de sobreposição aprova desenho torto — erro nº 23.
10d. **Rodar a prova 9** (`conferir_payload_completo.py`): nenhum payload de trecho
    esconde campo em `[...]` ou `{...}`. O quadro existe para alguem CONSTRUIR o fluxo
    a partir dele; payload resumido passa em todas as outras provas e nao serve.

10c. **Se existe JSON do n8n, rodar a prova 8** (`conferir_tipo_no.py`): o tipo de cada
    nó bate entre o quadro e o JSON? Decisão de arquitetura aplicada num material e não no
    outro é o defeito mais comum deste projeto, e nenhuma outra prova olha tipo.

10b. **Se um quadro chama outro, rodar a prova 7** (`conferir_contrato.py`): todo campo que o
    consumidor espera existe no que o produtor declara devolver? Nenhuma outra prova olha campo, e
    dois quadros individualmente corretos podem estar mentindo um sobre o outro — erro na origem do
    defeito `url_assinada` × `status` de 14/08.
11. **ABRIR NO NAVEGADOR E OLHAR.** Este passo não é opcional e não pode ser substituído pelo
   read-back. Com o link público do Passo 0:

   ```
   navegar para:  <link publico>&moveToWidget=<id do frame>
   esperar:       14 a 16 segundos (o canvas leva para renderizar)
   print
   ```

   Detalhes que economizam rodada:
   - `moveToWidget` com o **id do frame** enquadra o fluxo inteiro; com o id de um widget pequeno
     dá zoom nele (uma faixa 280×26 rende ~599%).
   - O print às vezes estoura o tempo de espera na primeira tentativa. **Repetir**, não
     reinterpretar.
   - Ampliar regiões do print (recorte + escala) para julgar detalhe. O print inteiro serve para
     ver sobreposição; não serve para medir espaçamento.

12. **Medir espaçamento com zoom, nunca em print de frame inteiro.** Navegue para uma faixa com
   `&moveToWidget=<id>` (o zoom sai igual em qualquer coluna, porque todas as faixas têm o mesmo
   tamanho), calibre a escala pela espessura conhecida da faixa (26px) e só então meça. Em print
   de frame inteiro a faixa tem 4 pixels e a medição é ruído — já produziu tanto falso "está
   perfeito" quanto falso "está quebrado" nesta skill.
13. **Olhar o frame inteiro em ~4% para julgar TOPOLOGIA.** É o único enquadramento em que dá para
    ver se os ramos estão empilhados, se o loop fecha e se sobrou bloco órfão. Detalhe se julga
    ampliado; estrutura se julga afastado.
14. **Mostrar ao Lucas com `board_show`** e pedir o olho dele. Mesmo depois de eu olhar, quem
    aprova é ele: peso de hierarquia e "ficou bonito" não são medíveis.
15. Corrigir só o que deu NÃO. Não refazer do zero.

**Nunca dizer que terminou sem ter aberto o board no navegador.** A ordem das provas é:
`success: true` (chegou) → read-back (estrutura certa) → **print (é isso que a pessoa vê)** →
olho do Lucas (está bom).

---

## Checagem (sim ou não, olhando o desenho)

**Estrutura e conteúdo**

1. Algum texto está fora de um recipiente? (tem que ser NÃO)
2. Todo recipiente tem faixa de rótulo acima dele?
3. Existe legenda de cores visível no board?
4. Alguma cor é usada para duas categorias? (tem que ser NÃO)
5. A forma de cada nó corresponde ao que ele faz na tabela de formas?
6. Algum elemento está parcialmente escondido por outro? (tem que ser NÃO)
7. Algum texto encosta na borda do recipiente? (tem que ser NÃO)
8. Alguma linha passa por cima de um card? (tem que ser NÃO)
9. Algum post-it tem mais de uma ideia dentro? (tem que ser NÃO)
10. Algum losango ou círculo tem texto espremido? (tem que ser NÃO)
11. Algum texto quebrou no meio da palavra? (tem que ser NÃO)

**Layout horizontal**

12. O fluxo corre da esquerda para a direita, com a explicação abaixo de cada nó?
13. Todo trecho de linha tem, **acima**, a faixa + lista do que passa, e **abaixo**, a faixa
    "Observações" + os cards cinza?
14. A lista está **fora** de card, e a observação **dentro** de card cinza com canto arredondado?
15. Amarelo aparece **só** em "o que faz"? (observação amarela = NÃO)
16. Fim da lista até a linha = **20px**, e linha até a faixa "Observações" = **20px**?

**Proporção**

17. Cada nó está no **meio** do trecho horizontal dele?
18. Cada bloco está centrado no meio da **sobra** de linha dele (esquerda e direita)?
19. Faixa, lista, faixa de observação e cards compartilham o **mesmo centro** vertical?
20. Toda faixa tem **440**, toda lista **440** e todo card interno **360**?

**Alinhamento (o que o verificador de sobreposição NÃO pega)**

21. A faixa de cima, a lista, a faixa "Observações" e os cards do mesmo trecho têm o **mesmo x**?
22. Todo card cinza está em `x_do_bloco + 40`, e todo post-it em `x_do_card + 40`?
23. Existe algum trecho com faixa e lista mas **sem** bloco de "Observações"? (tem que ser NÃO)

**Ramificação e topologia**

24. Alguma linha de ramificação está na diagonal? (tem que ser NÃO)
25. Algum conector entra pelo **topo ou pela base** de um card? (tem que ser NÃO — só laterais)
26. A dobra é feita com **pontos de junção** e conectores retos?
27. O trecho horizontal do ramo tem pelo menos 1000px para as etiquetas caberem?
28. **O desenho bate com o `connections` do JSON, linha por linha?** Nó com duas saídas virou dois
    ramos empilhados, e não uma cascata?
29. **Todo nó que nunca aparece como origem no JSON está desenhado como ponta terminal?**
30. Cada ramo tem altura calculada pelo bloco de explicação dele, ou você copiou um número fixo?
31. **Ramificação de 2 ramos deixou a linha principal VAZIA entre eles, e a de 3 pôs um ramo NA
    linha?** (N par não usa a linha principal; N ímpar usa)
32. Todo par de cards lado a lado passa no teste *"nenhum dos dois se conecta a mais ninguém"*?
33. **Todo conector cujos dois pontos estão em corredores diferentes (`y` diferente) passa por ponto
    de junção?** Ligação direta vira diagonal, e o verificador **aprova** — só o print pega.

**Consistência com o board**

34. A grafia bate com o quadro de referência já aprovado — acentuação, maiúsculas, nome de nó igual
    ao do n8n? (quadro fora do padrão de acento desqualifica o board inteiro)

**Prova**

35. Todo conector tem `data-start`/`data-end` e ponta de seta no destino?
36. O board foi **aberto no navegador** e os itens acima foram julgados **olhando o print**?
    (se for NÃO, a checagem não valeu — refazer olhando)
37. A **estrutura** foi julgada no frame inteiro (~4%), e não só as peças ampliadas?

Fechar só quando todos derem SIM em duas rodadas seguidas. Não declarar pronto sem a tabela.

> **Os itens 21 a 23 e 28 a 30 existem porque o verificador aprovou um desenho errado.** Em 12/08
> o script deu 0 sobreposições num quadro que tinha três ramos desenhados em cascata e seis blocos
> 90px fora do eixo. O Lucas achou os dois a olho. **Geometria limpa não é desenho certo.**

> **Nunca responda "conferi" sem ter aberto o board.** Em 12/08 eu rodei verificador de geometria,
> ele deu números conflitantes, e eu escrevi que ia parar — sem olhar. O Lucas mandou dois prints
> e achou em segundos duas sobreposições que o verificador não pegou. Verificador serve para
> **varrer**; print serve para **decidir**. Os dois, nessa ordem, sempre.

---

## Para deixar iterando sozinho

```
/goal os 37 itens da checagem da skill fluxo-n8n-miro dão SIM em duas rodadas seguidas, com a
tabela de cada rodada impressa na conversa e uma observação concreta do que foi visto no board
em cada item, ou pare após 20 turnos e liste o que não fechou
```

Ligar o auto mode junto, senão trava pedindo permissão a cada chamada.
Para encerrar antes: `/goal clear` **sozinho** — texto depois do `clear` vira condição nova.

---

## Proveniência

*Padrão extraído e validado em 11/08/2026: a referência foi reconstruída só a partir do guia e
medida contra o original (9 de 9 blocos estruturais, desvio máximo de 6px). Artefatos da validação
em `content/drafts/padrao-visual-fluxos/`.*

*Amadurecido em 12/08/2026 contra o Fluxo Geral do Projeto Big Brother, em três rodadas de correção
do Lucas:*

| Rodada | O que o Lucas corrigiu | O que virou regra |
|---|---|---|
| 1 | *"na vertical fica uma coisa do lado da outra"* | layout horizontal, blocos na linha, proporção |
| 2 | mandou o print do loop do n8n | `done` por cima, corpo por baixo, retorno por corredor |
| 3 | *"o fluxo oito não entra no fluxo nove"* · *"não estão centralizados"* | topologia vem do JSON; bloco é conjunto de 4 peças |

*Estado ao fim de 12/08: 21 nós, 288 elementos, 0 sobreposições, 19 blocos de trecho com folga de
20 a 22px. A cada rodada eu tinha declarado o desenho pronto, e a cada rodada ele achou algo que os
meus scripts aprovaram. **O verificador nunca foi o juiz — ele é a peneira grossa.***

*Fechado em 13/08/2026 com os quadros 02 a 05 do Projeto Big Brother (50 nós e 790 itens em uma
sessão), e **aprovado pelo Lucas sem nenhuma correção de design** — a primeira vez que isso acontece.
O que mudou em relação a 12/08 não foi cuidado, foi método:*

| 12/08 | 13/08 |
|---|---|
| SVG escrito à mão | **gerador declarativo**, com `verifica()` rodando no modelo antes de enviar |
| verificação pelo read-back (que trunca em 500) | verificação na **geometria calculada** |
| decisão de ramificação no olho | tabela mecânica lida do `conn.py` |
| print no fim, para confirmar | print **no meio**, e foi ele que pegou os dois defeitos reais |

*Os dois defeitos que só o print pegou: as 24 listas do quadro 02 meia altura abaixo do lugar
(erros 24 e 25) e a diagonal do quadro 05 (erro 27). Nenhum script viu nenhum dos dois.*

*Estendido em 14/08/2026 no redesenho dos cinco quadros v2 (71 → 92 nós, 1.144 elementos, 184
conectores), com os erros 30 a 33. **A natureza deles é diferente de tudo que veio antes:** nos 29
primeiros, o desenho estava errado. Nestes quatro, o desenho estava **certo** — o que mentiu foi o
material em volta dele. Gerador consertado só no board (30), quadro sem JSON (32), número de
elemento escrito de memória num handoff (33).*

*O erro 33 nasceu ao retomar o próprio handoff desta sessão: ele mandava conferir 169 elementos no
quadro 05 e o gerador produz 168. Foi pego porque o passo 1 do handoff manda regerar antes de
enviar — se o envio tivesse vindo primeiro, um resultado correto teria sido reprovado. **A defesa
contra documentação velha é a mesma contra board velho: reexecutar a fonte e comparar.***

*Fechado em 14/08/2026 com os cinco quadros v2 no board (`created_count` 393 · 202 · 266 · 276 · 196
= **1.333 itens**, `failed_items` vazio nos cinco, formas e fontes conferidas no read-back, e print
de topologia de cada um). Os erros 34 a 36 nasceram durante esse envio, e nenhum deles é de desenho:*

| # | O que mentiu | Como apareceu |
|---|---|---|
| 34 | a métrica de comparação | 168 do gerador contra 196 do board — a fórmula não estava escrita em lugar nenhum |
| 35 | a coordenada do frame | `translate(0,80000)` virou y=122.200; o composer empilha por ordem de envio |
| 36 | a frase que explicava a correção | a substituição em massa de `TRK-8842` reescreveu a própria explicação dela |

*O padrão dos sete (30 a 36) agora está claro: **quando o desenho fica certo, o defeito migra para
o que descreve o desenho.** Gerador, JSON, handoff, fórmula de conferência, coordenada e prosa
explicativa — todos são artefatos derivados, e todos envelhecem em silêncio. A prova de cada um é
sempre a mesma: reexecutar a fonte e comparar com o que o artefato afirma.*

*Depois do envio, em 17/08, duas ferramentas saíram desse padrão e viraram parte da skill: a
**prova 7** (contrato entre quadros), que é a única que olha campo em vez de nó, e o
**`conferir_envio.py`**, que fixa a conferência da resposta do board num script em vez de na
memória de quem envia. As duas nasceram de defeito real desta sessão, não de previsão.*

*E o **erro 37** saiu de escrever a própria prova 7: ela acusou defeito inexistente em 3 dos 4
contratos, duas versões seguidas, e eu quase "consertei" três quadros que estavam certos. Virou o
procedimento de calibração em três passos (bom → ruim de propósito → bom). **A ironia é o registro
mais útil aqui:** a skill já dizia desde 12/08 que premissa errada inventa defeito, e mesmo assim eu
escrevi um verificador novo e olhei só o resultado verde. Saber a regra não substitui executá-la.*
