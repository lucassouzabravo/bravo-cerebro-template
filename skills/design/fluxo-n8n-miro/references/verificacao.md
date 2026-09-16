# Como verificar o desenho — as quatro provas, e os scripts prontos

> Escrito em 12/08/2026, depois de o Lucas achar a olho **dois defeitos que o meu verificador
> aprovou**: três ramos desenhados em cascata (topologia errada) e seis blocos 90px fora do eixo
> (desalinhamento). Nenhum dos dois é sobreposição, e era só sobreposição que eu media.

## A regra que resume este arquivo

> **Cada pergunta tem a sua prova. Escolher a prova pela facilidade é o erro que mais se repete.**

| Pergunta | Prova que responde | Prova que NÃO responde |
|---|---|---|
| O fluxo desenhado é o fluxo real? | ler `connections` do JSON | qualquer coisa visual |
| Algo está tapando algo? | verificador de sobreposição | print de frame inteiro |
| As peças de um bloco estão no mesmo eixo? | verificador de alinhamento | verificador de sobreposição |
| A folga da lista até a linha está certa? | medir `fim da lista − y da linha` | olhar e achar bonito |
| Alguma linha saiu na **diagonal**? | garantir junção **na geração** + **print** | verificador de sobreposição — ele não enxerga conector |
| **O que o quadro A manda é o que o quadro B devolve?** | **prova 7, `conferir_contrato.py`** | a prova cruzada JSON × gerador — ela conta **nós**, não campos |
| **O nó é do mesmo TIPO no quadro e no JSON?** | **prova 8, `conferir_tipo_no.py`** | a prova 6 conta nós e a 7 confere campo — nenhuma das duas olha tipo de nó |
| **O payload do trecho está COMPLETO, campo por campo?** | **prova 9, `conferir_payload_completo.py`** | nenhuma prova olhava CONTEÚDO de payload — quadro geometricamente perfeito e inútil pra construir passa em todas |
| **O board recebeu tudo que eu mandei?** | **`conferir_envio.py`** no `created_count` e no `failed_items` | o número que o gerador imprime, que é outra métrica (erro 34) |
| Está legível e bonito? | **print** | qualquer script |
| Está bom? | **o Lucas** | eu |

Rode as quatro primeiras **nesta ordem** antes de abrir o navegador. E depois abra o navegador
assim mesmo.

---

## Prova 1 — a topologia sai do JSON, não da cabeça

**Rode isto ANTES de posicionar qualquer nó.** Foi pular este passo que me fez desenhar
`7 → 8 → 9 → 10` em cascata quando o fluxo tem três ramos paralelos.

```python
# conn.py — imprime quem chama quem, com o número da saída e o da entrada
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
for src,v in d.get('connections',{}).items():
    for i,out in enumerate(v.get('main',[]) or []):
        for c in (out or []):
            print('%-38s [saida %d] -> %-38s [entrada %s]'%(src,i,c['node'],c.get('index',0)))
```

Como ler a saída:

| O que aparece | O que significa no desenho |
|---|---|
| o mesmo nó de origem em 2+ linhas | **ramificação**: ramos empilhados, nunca cascata |
| o mesmo nó de destino em 2+ linhas, com `entrada` diferente | junção: os ramos voltam a se encontrar ali |
| um nó que **nunca aparece como origem** | **ponta terminal**: grava e para, e o desenho tem que mostrar isso |
| `[saida 0]` e `[saida 1]` do mesmo nó | duas saídas nomeadas — num `Loop Over Items` são `done` e `loop` |

Uma cópia pronta para rodar deste script vive em `../scripts/conn.py`.

---

## Prova 2 — sobreposição

Lê o board, ignora **contenção** (texto dentro de card é pertencimento, não defeito) e lista os
pares que se cruzam de verdade.

```python
# le o arquivo salvo pelo canvas_read_as_svg (ele estoura o limite de tokens e vai pra disco)
import json,re,sys
svg=json.load(open(sys.argv[1],encoding='utf-8'))['svg']
def attr(a,n):
    m=re.search(n+r'="([^"]*)"',a); return m.group(1) if m else None
def fl(a,n,d=0.0):
    try: return float(attr(a,n))
    except: return d
for g in re.split(r'(?=<g )', svg):
    fm=re.search(r'data-frame="([^"]*)"',g)
    if not fm: continue
    rects=[]
    for m in re.finditer(r'<(rect|circle|ellipse|textArea)\b(.*?)(?:/>|>(.*?)</\1>)', g, re.S):
        tag,a=m.group(1),m.group(2)
        if 'data-type="frame"' in a: continue
        if tag in ('circle','ellipse'):
            r=fl(a,'r'); rx=fl(a,'rx',r); ry=fl(a,'ry',r)
            x,y,w,h=fl(a,'cx')-rx,fl(a,'cy')-ry,2*rx,2*ry
        else:
            x,y,w,h=fl(a,'x'),fl(a,'y'),fl(a,'width'),fl(a,'height')
        rects.append(dict(id=attr(a,'data-miro-id'),x=x,y=y,w=w,h=h,
                          c=(attr(a,'data-content') or '')[:40]))
    bad=0
    for i in range(len(rects)):
        for k in range(i+1,len(rects)):
            A,B=rects[i],rects[k]
            ox=min(A['x']+A['w'],B['x']+B['w'])-max(A['x'],B['x'])
            oy=min(A['y']+A['h'],B['y']+B['h'])-max(A['y'],B['y'])
            if ox>1 and oy>1:
                cont=(A['x']<=B['x'] and A['y']<=B['y'] and A['x']+A['w']>=B['x']+B['w'] and A['y']+A['h']>=B['y']+B['h']) or \
                     (B['x']<=A['x'] and B['y']<=A['y'] and B['x']+B['w']>=A['x']+A['w'] and B['y']+B['h']>=A['y']+A['h'])
                if not cont:
                    bad+=1
                    print('SOBREPOE %s(%.0f,%.0f) x %s(%.0f,%.0f) -> %.0f x %.0f'%(
                        A['id'],A['x'],A['y'],B['id'],B['x'],B['y'],ox,oy))
    mx=max(r['x']+r['w'] for r in rects); my=max(r['y']+r['h'] for r in rects)
    print('%s | %d elementos | %d sobreposicoes | extremos %.0f x %.0f'%(
        fm.group(1)[:34],len(rects),bad,mx,my))
```

⚠️ **A âncora importa mais que o script.** No read-back o `y` é o **topo**. Um verificador que
assuma centro **inventa defeito e esconde defeito ao mesmo tempo** — foi o que aconteceu em 12/08,
quando o mesmo board parado acusou 17 numa passada e 23 na outra.

⚠️ **E o read-back pode vir truncado (medido 13/08).** `canvas_read_as_svg` para em **500 elementos**
no board inteiro, sem avisar. Rodar o verificador em cima disso dá "0 sobreposições" sobre um
conjunto incompleto — e foi exatamente nos 13 elementos cortados que estava o defeito. **Antes de
confiar no resultado, comparar `item_count` da resposta com o número de elementos que o SVG traz.**

> **A saída melhor: verificar a geometria CALCULADA, antes de enviar.** O gerador conhece todos os
> elementos, não depende de read-back e não tem cap. Rodar sobreposição, alinhamento e folga no
> modelo, e usar o board só para confirmar que nada degradou (`failed_items`, `data-shape`) e para o
> print. Em 13/08 os quadros 02 e 03 saíram com 0 defeito na geometria calculada, e o board
> confirmou forma por forma.

Os **extremos** que ele imprime servem para dimensionar o frame — e o frame precisa ser criado já no
tamanho certo, porque encolher depois pode não funcionar (ver `miro-mcp.md`).

⚠️ **O ponto cego que este verificador nunca vai cobrir: traçado de conector.** Ele compara
retângulos, e conector não tem retângulo. Em 13/08 aprovou com nota máxima um quadro em que uma
linha cruzava o desenho inteiro na diagonal, porque origem e destino estavam em corredores
diferentes. **Não tente ensinar o verificador a ver isso** — resolva na geração: todo par de pontos
com `y` diferente recebe ponto de junção, sem exceção (`miro-mcp.md` → "O roteador desenha
DIAGONAL"). O print continua sendo o único juiz do traçado.

---

## Prova 3 — alinhamento (o que a sobreposição não vê)

Um bloco de trecho tem **quatro peças** e elas compartilham o eixo: faixa "sai do X · entra no Y",
lista, faixa "Observações" e cards cinza. Se você mover só duas, o desenho fica torto **sem nenhuma
sobreposição** — passa limpo na Prova 2 e o Lucas vê na hora.

```python
# emparelha a faixa de cima (#d0d0d0) com a faixa "Observações" (#ededed) da mesma coluna
# e marca quando os x não batem
faixas_topo = [r for r in rects if r['fill']=='#d0d0d0']
obs         = [r for r in rects if r['fill']=='#ededed' and r['c'].startswith('Observa')]
cards       = [r for r in rects if r['fill']=='#f5f5f5']
for t in sorted(faixas_topo,key=lambda r:(r['x'],r['y'])):
    cand=[o for o in obs if abs(o['x']-t['x'])<400 and 0 < o['y']-t['y'] < 3000]
    o=min(cand,key=lambda r:r['y']-t['y']) if cand else None
    marca = '' if (o and abs(o['x']-t['x'])<1) else '   <<< DESALINHADO'
    print('%-6.0f %-24s | %s%s'%(t['x'], t['c'][:24], ('%.0f'%o['x']) if o else 'SEM BLOCO DE OBS', marca))
```

Ele pega dois defeitos de uma vez:

- **`<<< DESALINHADO`** — as peças do bloco não compartilham o eixo;
- **`SEM BLOCO DE OBS`** — o trecho tem faixa e lista mas ninguém escreveu observação. Foi assim que
  descobri que o vão 6→7 nunca teve bloco de observações.

O card cinza tem que estar em `x_do_bloco + 40`. Conferir junto.

---

## Prova 4 — folga da lista até a linha

A lista de um trecho termina **20px acima** da linha, e a faixa "Observações" começa **20px abaixo**.
Como a altura do `<textArea>` é automática, isso só se confere medindo:

```python
fim   = lista['y'] + lista['h']      # y do read-back é topo
folga = linha_y - fim                # tem que dar 20 (aceitar 20 a 22)
```

E a correção usa a fórmula medida (ver `miro-mcp.md`):

```
y_enviar = (linha_y - 20 - altura) + altura/2 - 12
faixa_y  = (linha_y - 20 - altura) - 41
```

⚠️ **No bloco espelhado a conta inverte:** a lista fica **acima** da faixa "Campos"
(`fim = faixa_y − 15`). Um script que assuma "lista abaixo da faixa" acerta os blocos normais e
quebra exatamente o espelhado — aconteceu no nó 2.

---

## Prova 5 — o print, que é o que a pessoa vê

Nenhuma das quatro acima diz se está legível. Só o print diz.

```
navegar para:  <link publico>&moveToWidget=<id de um elemento da região>
esperar:       18 a 22 segundos (às vezes precisa de duas esperas)
print
```

Mecânica que economiza rodada:

| Detalhe | O que fazer |
|---|---|
| `moveToWidget` num `<textArea>` de 440 | cai em ~200% a 270% — bom para conferir uma peça |
| `moveToWidget` no **frame** | cai em ~4% — bom para ver a estrutura macro e as ramificações |
| a tecla `-` afasta um passo | **às vezes ignora o toque**; confira o percentual no canto antes de julgar |
| primeira tentativa vem em branco | a página ainda está carregando. **Repetir**, não reinterpretar |

**O que cada enquadramento responde:**

- **4% (frame inteiro):** os ramos estão empilhados? o loop fecha? há algum bloco órfão no meio do
  nada? — é aqui que a topologia aparece de verdade.
- **75% a 200%:** o bloco tem faixa, lista, linha, "Observações" e cards na ordem certa?
- **300%+:** a dobra é ortogonal? o ponto de junção está onde deveria?

Estorvos conhecidos: o banner "Sign up for free" cobre o topo; às vezes aparece um modal
**"Presentation started"** que volta a cada carregamento (fechar no *Cancel*); e o Chrome de
automação trava com sessão órfã (`Browser is already in use`) — matar **só** os processos cujo
command line contém `ms-playwright-mcp`, nunca o Chrome pessoal do Lucas.

---

## Prova 6 — o Lucas

Peso de hierarquia, "ficou bonito" e "isso conta a história certa?" não são mediveis. Em 12/08 ele
achou em uma frase o que quatro scripts aprovaram. **Mostrar sempre, e perguntar.**

---

## Prova 7 — o contrato entre quadros (14/08/2026)

> Nasceu porque o quadro 04 esperava receber `url_assinada` do quadro 05, que devolve `status`. Os
> dois quadros estavam individualmente certos, **as seis provas anteriores aprovaram os dois**, e o
> defeito só apareceu porque eu li os dois arquivos lado a lado por acaso.

Quando um fluxo chama outro, existe um contrato: o consumidor declara o que espera receber e o
produtor declara o que devolve. **Nenhuma prova de geometria ou de topologia olha isso** — a prova
cruzada JSON × gerador conta *nós*, e bater o número de nós não diz nada sobre os campos.

**A regra, e ela é assimétrica de propósito:**

> **O consumidor não pode esperar campo que o produtor não declara.**
> O produtor pode declarar campos a mais — o consumidor simplesmente ignora.

O inverso é que quebra: esperar campo que ninguém produz devolve vazio **em silêncio**, e vazio
dentro de um texto que vai ser avaliado por modelo vira nota errada sem nenhum erro de execução.

Implementação genérica, pronta para adaptar (troque a lista `PARES` pelos seus arquivos e
marcadores): `../scripts/conferir_contrato.py`.

**O mapa de quem chama quem é explícito no script, e tem que ser.** A chamada entre fluxos é um
`Execute Workflow`, cujo alvo é um id que só existe dentro do n8n — não há `connections` para ler.
Quadro novo entrando obriga a acrescentar o par ali.

O que ela achou na primeira execução, além do defeito que motivou: o quadro 05 **montava** a ficha
com `gcs_path` no nó 11 e **declarava devolver sem ele** no nó 13. Inconsistência interna de um
quadro só, invisível até o quadro 04 passar a esperar o campo.

### O que essa prova me ensinou sobre escrever prova (erro 37)

**Este script acusou defeito inexistente em 3 dos 4 contratos nas duas primeiras versões**, por dois
bugs meus: o marcador `canal: 'x'` casava com a primeira ocorrência (o normalizador) em vez da
última (o placar); e o regex não incluía `'` na classe à esquerda, então campo que abre uma string
Python não era visto e o conjunto saía **vazio** — o que faz todo campo esperado parecer ausente.

É exatamente o que já estava escrito aqui sobre o verificador de sobreposição de 12/08: **premissa
errada inventa defeito.** A diferença é que agora existe procedimento:

```
1. rodar no estado atual, que se acredita bom  -> tem que dar OK
2. reintroduzir o defeito conhecido de propósito -> tem que ACUSAR, e nomear o campo
3. restaurar e rodar de novo -> tem que dar OK
```

**Verificador que só foi visto aprovando não foi verificado.** Sem o passo 2 não se sabe se ele
enxerga o que promete enxergar, e "todos batem" pode significar "não olhei nada". Foi assim que
confirmei esta prova: com `gcs_path` removido do produtor ela imprimiu
`*** FALTA NO PRODUTOR: gcs_path`, e com ele de volta, `todos os contratos batem`.

## Prova 8 — o tipo do nó, quadro × JSON (18/08/2026)

**Nasceu de defeito real, no projeto Big Brother.** A decisão de trocar quatro nós de consulta de
`Metabase` para `HTTP Request` foi aplicada nos quadros, e o JSON do n8n continuou dizendo
`n8n-nodes-base.metabase`. Pior: dois JSONs ainda **nomeavam as consultas mortas** (`q12570`,
`q13954`) enquanto os quadros já diziam C3 e C4. Quem construísse pelo JSON ligaria a consulta velha
com o quadro certo do lado.

**Nem a prova 6 nem a prova 7 podiam ver isso.** A 6 conta nós e confere a numeração 1..N; a 7
confere campo entre quadros. **Tipo de nó não é olhado por nenhuma.** É a família dos erros 30 a 36:
o desenho certo e o material em volta mentindo.

### O que ela faz

Para cada nó, compara o tipo declarado na faixa `Campos · tipo: X` do gerador com o `type` do nó no
JSON, na mesma posição (o nó N do quadro é `nodes[N-1]` do JSON). A tradução entre o rótulo humano e
o id do n8n vive numa **tabela explícita**:

```python
TRADUCAO = {
    'code (javascript)': 'code',      'http request': 'httprequest',
    'postgres (insert)': 'postgres',  'loop over items': 'splitinbatches',
    'execute workflow': 'executeworkflow',  'openai (transcrever)': 'openai',
    ...
}
```

**A tabela ser explícita é o desenho, não preguiça:** rótulo novo sem entrada na tabela **quebra a
prova** em vez de passar em silêncio. Verificador que ignora o que não conhece é verificador que
aprova o desconhecido.

### Onde ela vive

`content/drafts/qualidade-bots-auditoria/fluxos-n8n/conferir_tipo_no_v3.py` — a versão do projeto,
com os cinco pares. Para outro fluxo, copiar e trocar `PARES`.

### Calibrada nos três passos, e o passo 3 pegou o autor dela

Bom → dois defeitos plantados, **um em cada lado** (um nó voltando a `metabase` no JSON, um rótulo
virando `Merge` no quadro) → acusou os dois, cada um nomeando o lado certo → restaurado → OK.

**E o passo 3 falhou de primeira, por erro meu**, que é exatamente o motivo de a calibração existir:
a âncora que eu usei para desfazer o defeito plantado no q02 **não era única** — `Merge` existe de
verdade em outros nós daquele quadro —, o `assert` estourou, e o SVG chegou a ser **regerado com o
defeito dentro**. A prova ficou vermelha e não deixou passar. Ver erro 38.

## Prova 9 — o payload do trecho está completo? (18/08/2026)

**Nasceu de pedido do Lucas, repetido três vezes na mesma conversa:**

> *"Se está saindo desse nó para esse cinco campos, é pra ter os cinco campos listados do que está
> saindo, no exemplo, completo."*

E o caso concreto que ele deu: no quadro 03, do nó 5 pro 6, o payload dizia `registros: [...]` — e
ele perguntou o que vai dentro de `registros`.

**Nenhuma prova anterior podia pegar isso.** Geometria passa, contagem de nós passa, contrato passa,
tipo de nó passa. **O quadro fica geometricamente perfeito e inútil para quem precisa construir o
fluxo a partir dele** — que é a única razão de o quadro existir.

### O que ela recusa, e o que ela aceita

| padrão | veredito |
|---|---|
| `[...]` · `{...}` | **recusa** — lista ou objeto escondido |
| `ou campo ausente` · `texto ou vazio` | **recusa** — dois casos possíveis, mostre os dois |
| `... até 473 uids` · `... 1 item por Meet` | **aceita** — diz QUANTOS faltam |
| `{ meet_id: 3915, ... ordem_do_meet: 2 }` | **aceita** — diz que o formato repete o de cima |

**Abreviação que informa é diferente de abreviação que esconde**, e a diferença está em dizer
quantos ou dizer que repete.

### Ela pegou 6 casos nos meus próprios payloads

Rodei depois de reescrever os cinco quadros "completos" à mão. Sobraram seis `[...]` e `{...}`
espalhados. **Escrever com atenção não garante completude; a varredura garante.**

### Calibrada nos três passos, e a limitação que a calibração revelou

Bom (83 trechos OK) → dois defeitos plantados, um em cada quadro → acusou os dois, nomeando trecho,
motivo e a linha → restaurado → OK.

⚠️ **No passo 3 ela passou VERDE com o `v3_q05.py` sintaticamente quebrado.** Eu errei o slice de
string ao desfazer o defeito plantado e deixei uma linha inválida; a prova 9 lê o texto do `.py` com
expressão regular e não executa nada, então não viu. **Ela não substitui rodar o gerador.** A ordem
correta é: **o gerador roda limpo primeiro, as provas depois.**
