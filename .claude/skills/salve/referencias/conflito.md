# Quando dá conflito

Conflito acontece quando você e outra pessoa — ou você em outro computador — mexeram no mesmo arquivo antes de sincronizar. É normal, não é erro seu, e tem dois casos com tratamentos diferentes.

## Os dois casos

| | O que é | O que fazer |
|---|---|---|
| **A** | Cada lado **acrescentou** uma coisa diferente no mesmo arquivo | Ficam os dois. Resolve sozinho |
| **B** | Os dois lados mexeram **na mesma coisa** | Para. Só uma pessoa sabe qual versão vale |

**Na dúvida entre A e B, é B.** Resolver errado um caso B apaga trabalho de alguém em silêncio, e ninguém descobre — que é o pior tipo de erro possível num cérebro.

## Não decidir a olho

Distinguir A de B lendo é exatamente o tipo de coisa que a atenção erra. Use o verificador:

```bash
python skills/memoria/salve/referencias/conferir_conflito.py
```

Ele lê os três lados que o git guarda (como estava antes, o que veio de lá, o que veio daqui) e classifica cada arquivo. **Sem `--aplicar` ele não toca em nada.**

Para resolver, só quando **todos** forem caso A:

```bash
python skills/memoria/salve/referencias/conferir_conflito.py --aplicar
```

Se houver um único caso B, ele **não resolve nenhum** e explica por quê. É de propósito: resolver metade deixa a árvore num estado misto que ninguém consegue ler depois.

## O que ele exige para dizer "caso A"

Duas coisas, e as duas importam:

1. **Nenhum lado removeu linha** que existia antes. Um verificador que só compara "os títulos são diferentes" aprovaria uma remoção silenciosa — se um lado apagou uma decisão antiga, somar os dois mantém o apagamento e ninguém nota.
2. **Os dois lados não escreveram sob o mesmo título.** Título repetido quer dizer que os dois falaram da mesma coisa, e somar cria um arquivo que se contradiz.

## Onde ele nem tenta

Só automatiza os arquivos que crescem por acréscimo: `memory/context/pendencias.md`, `memory/context/decisoes/AAAA-MM.md` e as notas diárias.

`hot.md`, `MEMORY.md`, fichas de projeto e qualquer outra coisa são **caso B por construção** — são arquivos reescritos, não acrescentados, então conflito neles sempre quer dizer que duas versões disputam o mesmo lugar.

## Se for caso B

O verificador diz qual arquivo e por quê. Aí:

1. abrir o arquivo e olhar os dois lados;
2. decidir qual vale, ou juntar na mão;
3. `git add {arquivo}` e `git rebase --continue`.

**Nunca `git push --force`** para "resolver". Isso apaga o trabalho do outro lado no servidor.

## Conferir que o verificador ainda tem dentes

```bash
bash skills/memoria/salve/referencias/calibra_conflito.sh
```

Monta um repositório descartável, planta conflitos conhecidos e confere que ele acerta cada um. Vale rodar quando o script for alterado — verificador que sempre diz "tudo certo" é pior que não ter verificador, porque dá confiança falsa.
