# Conversão para Google Docs — quando e como

**Regra de ouro:** não construa documento Bravo diretamente em Google Docs. Construa em .docx via esta skill e converta. O motivo é simples: a granularidade de controle do python-docx é incompatível com o editor visual do gdocs, e tentar reproduzir lá vira retrabalho.

Use gdocs apenas quando o destinatário **exige** edição colaborativa em tempo real (revisão simultânea por vários revisores, comentários inline com tagging por @, controle de versão automático).

---

## 1. Caminho: upload + conversão

1. Tenha o .docx final, validado e em qualidade de entrega.
2. No Google Drive: New → File Upload → selecione o .docx.
3. Após upload, clique com botão direito → Open with → Google Docs.
4. Drive cria uma cópia convertida em formato gdocs (extensão muda, mas o arquivo .docx original permanece).
5. Trabalhe na cópia convertida.

---

## 2. O que sobrevive bem na conversão

- Headings (H1, H2, H3) — preserva hierarquia e cor.
- Parágrafos de corpo — preserva alinhamento à esquerda.
- Bullets visuais (`•  texto`) — preserva.
- Numeração simples (`1. texto`) — preserva.
- Tabelas com larguras DXA — preserva.
- Imagens (capa, logos) — preserva, com tamanho original.
- Cores de fundo de célula — preserva.
- Field PAGE no footer — preserva como numeração automática.

---

## 3. O que quebra ou degrada

**Fonte Montserrat:** o Workspace da Bravo precisa ter Montserrat habilitada como fonte do workspace (Admin Console → Apps → Google Workspace → Drive and Docs → Service Settings → Fonts → custom). Se não tiver, o documento vai abrir em fonte padrão (Arial / Roboto). Pedir ao admin para habilitar é tarefa de 30 segundos — vale a pena pedir.

**Border-left grossa de callout/quote:** gdocs renderiza, mas a espessura pode parecer mais fina que no Word. Aceitável.

**Code blocks com Consolas:** se Consolas não está no workspace, vira fonte default. Para gdocs, considere `Courier New` (universalmente disponível) como alternativa — mas só para gdocs, mantenha Consolas no .docx.

**Capa em PNG A4:** gdocs converte a imagem como objeto flutuante na primeira página. Pode acabar com pequenas bordas brancas se as margens da primeira section não foram reconhecidas. Inspecione e ajuste manualmente: clique na imagem → Image options → Size & rotation → garanta 21 × 29.7 cm.

**Header/footer dependentes de section:** gdocs tem o conceito de "first page header/footer different" (equivalente ao `titlePg`), mas pode não vir ativo após conversão. Vá em Insert → Headers & footers → Options → Different first page, e marque.

**Field PAGE em footer customizado:** funciona, mas se o gdocs decidir recriar o footer, pode perder o estilo (8.5pt Grey Mid). Reformate manualmente se necessário.

---

## 4. Checklist pós-conversão para gdocs

Depois de abrir o .docx convertido como Google Doc, faça uma passada de revisão:

- [ ] Página 1 (capa) ocupa a página inteira, sem bordas brancas.
- [ ] Header da página 2+ tem logo nítido e título à direita.
- [ ] Footer tem paginação dinâmica funcionando (clique em uma página interna e veja o número).
- [ ] Tabelas mantêm largura igual à largura da página (não encolheram para o tamanho do conteúdo).
- [ ] Callouts mantêm cor de fundo e barra lateral.
- [ ] Fonte Montserrat aparece em todos os blocos. Se aparecer Arial, ajuste em Format → Styles → Update Normal style.
- [ ] H1 ainda quebra em nova página. (Em gdocs, edit estilo: Heading 1 → Page break before.)

---

## 5. Quando devolver para .docx

Se o documento precisa voltar para edição estrutural pesada (mais de 3-4 ajustes de fluxo, novos capítulos, mudança de paleta), exporte de volta para .docx e edite via python-docx:

**Em gdocs:** File → Download → Microsoft Word (.docx)

Aplique os ajustes via helpers da skill e re-suba para gdocs (sobrescrevendo, ou como nova versão). Editar estrutura pesada direto em gdocs vai gerar inconsistências.

---

## 6. Apps Script para automação leve

Para tarefas pequenas, repetitivas, **dentro** do gdocs após conversão (ex: trocar um placeholder, atualizar uma data em vários documentos), Apps Script resolve. Esqueleto:

```javascript
function updatePlaceholder() {
  const doc = DocumentApp.getActiveDocument();
  const body = doc.getBody();
  body.replaceText('{{CLIENT_NAME}}', 'Cliente Real');
  body.replaceText('{{DATE}}', Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'dd/MM/yyyy'));
}
```

Para mudanças estruturais (criar tabela complexa, inserir callout), python-docx é estrelas à frente de Apps Script. Use Apps Script só para edições textuais simples.
