# TOOLS.md

Catálogo das ferramentas e integrações deste cérebro. Lido **sob demanda**, nunca no boot.

## Contrato de segurança

1. Este arquivo **nunca** guarda valor de token, senha, cookie ou chave. Só o **nome** da variável e **onde** ela mora.
2. Segredo vive em `.env` na raiz deste repositório, bloqueado pelo `.gitignore`. Se um segredo aparecer em qualquer arquivo versionado, ele é considerado vazado e precisa ser trocado — não basta apagar.
3. Token não entra em linha de comando nem em URL. Ele é lido de arquivo dentro do processo que o usa.
4. Acesso disponível não é autorização automática para publicar, enviar, comprar ou apagar.
5. Ferramenta nova só entra aqui depois de funcionar de verdade uma vez, com o teste registrado.
6. Quando uma integração quebrar, registrar aqui **o sintoma e a causa**, não só "não funciona".
7. Quando uma credencial for revogada ou trocada, atualizar a linha dela no mesmo dia.

## Onde as credenciais moram

| Referência segura | Local real | Regra |
|---|---|---|
| *(nenhum token)* | o acesso ao GitHub fica no **cofre do Windows**, guardado pelo Credential Manager | Não existe arquivo para vazar — é o desenho preferido |
| {VARIAVEL} | {LOCAL} | {REGRA} |

## Integrações ativas

| Ferramenta | Para que serve | Como está conectada | Testada em |
|---|---|---|---|
| GitHub | guarda e versiona este cérebro | Credential Manager, na conta de {PESSOA} | {DATA} |
| {FERRAMENTA} | {PARA_QUE} | {COMO} | {DATA} |

## Ferramentas locais

| Comando | Para que serve | Como conferir se está instalado |
|---|---|---|
| `git` | versiona o cérebro | `git --version` |
| *(nada além do git)* | falar com o GitHub | `git config --get credential.helper` deve responder `manager` |
| `python` | roda os utilitários de `scripts/` | `python --version` |

## Sistemas da Bravo que eu conheço mas não acesso

Preencher conforme aparecerem. Serve para eu não prometer o que não consigo fazer:

| Sistema | O que tem lá | Eu tenho acesso? |
|---|---|---|
| {SISTEMA} | {O_QUE_TEM} | não |

## Como manter este arquivo

Quando uma ferramenta, integração ou automação entrar, sair ou mudar de credencial, a linha dela é atualizada **no mesmo trabalho** que causou a mudança. Arquivo de ferramenta desatualizado é pior que arquivo vazio, porque parece confiável.
