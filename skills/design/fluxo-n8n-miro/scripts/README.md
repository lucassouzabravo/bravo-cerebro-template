# Scripts prontos da skill fluxo-n8n-miro

Implementação de referência do gerador declarativo descrito no `SKILL.md`
(seção "O SVG se gera por código"). Testados nesta pasta — `exemplo_uso.py`
roda limpo e `exemplo_uso.svg` é o resultado dele.

Nenhum arquivo aqui carrega dado de projeto ou de cliente: tudo foi
generalizado a partir da implementação real usada internamente, trocando
nomes de fluxo/campo específicos por placeholders genéricos.

| Arquivo | O que faz | Precisa adaptar? |
|---|---|---|
| `quadro.py` | O motor: classe `Quadro` com `forma()`, `bloco_no()`, `bloco_trecho()`, `conn()`, `ponto()`, `verifica()`, `verifica_conectores()`, `svg()`. Geometria e regras já calibradas — não mexer sem motivo. | Não, em geral. Só a paleta `COR` se quiser cores diferentes. |
| `legenda_fechamento.py` | `legenda()` desenha o bloco de leitura + swatches de cor/forma; `fecha()` dimensiona o frame, roda os dois verificadores e grava o `.svg`. | Sim: `CATS` e `FORMAS` são o vocabulário de categorias do exemplo — troque pelas categorias do seu fluxo. |
| `exemplo_uso.py` | Fluxo de exemplo completo (gatilho → consulta → decisão → 2 desfechos), com bloco de explicação, trecho de linha e ramificação. Rode `python exemplo_uso.py` pra ver o pipeline inteiro funcionando. | Sim — é o ponto de partida. Copie e troque nós, textos e coordenadas pelo seu fluxo. |
| `exemplo_uso.svg` | Saída do exemplo acima, já gerada. Abra num visualizador de SVG pra ver o resultado sem precisar rodar Python. | Não. |
| `conn.py` | Lê o `connections` de um JSON exportado do n8n e imprime a topologia real (quem manda pra quem). Rodar **antes** de desenhar qualquer nó — é o que decide lado a lado vs. ramificação. | Não — genérico, `python conn.py seu_fluxo.json`. |
| `conferir_envio.py` | Confere a resposta de um `canvas_create_from_svg`: `created_count` contra a fórmula (elementos + conectores + 1), formas degradadas, fontes trocadas. | Não — genérico, `python conferir_envio.py resposta.json <elementos> <conectores>`. |
| `conferir_json_x_miro.py` | Prova cruzada: o JSON do n8n e o gerador do Miro descrevem a mesma quantidade de nós? | **Sim, obrigatório.** A lista `PARES` no topo do arquivo tem nomes de exemplo — troque pelos seus arquivos `.py` e `.json`. |
| `conferir_contrato.py` | Prova 7: quando um fluxo chama outro, confere que todo campo que o consumidor espera existe no que o produtor declara devolver. | **Sim, obrigatório.** A lista `PARES` tem nomes de exemplo — troque pelos seus geradores e pelos marcadores de texto que você usa neles (ex.: um comentário `# RECEBE:` antes da lista de campos). |

## Ordem de uso recomendada

1. `conn.py` no JSON do fluxo, antes de desenhar qualquer coisa.
2. Copiar `exemplo_uso.py` como ponto de partida do seu quadro; adaptar nós,
   textos, categorias (via `legenda_fechamento.py`) e geometria.
3. `fecha()` já roda `verifica()` + `verifica_conectores()` — resolver tudo
   que aparecer antes de enviar ao board.
4. Depois de enviar com `canvas_create_from_svg`, rodar `conferir_envio.py`
   na resposta.
5. Se o seu fluxo tiver mais de um quadro que se chamam entre si, rodar
   `conferir_json_x_miro.py` e `conferir_contrato.py` com os `PARES`
   preenchidos para os seus arquivos.

Todo o resto — os 37 erros, a tabela de formas, a regra de ramificação, o
checklist de 37 itens — está documentado em prosa no `SKILL.md` e em
`../references/`. Este README cobre só o código.
