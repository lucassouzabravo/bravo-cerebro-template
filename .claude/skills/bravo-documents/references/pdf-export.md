# Exportação para PDF — receita aprovada

PDF é formato de distribuição final na Bravo. .docx é onde o documento vive durante a iteração; .pdf é o que vai para o stakeholder externo, vai assinado, vira anexo de e-mail. Esta receita garante que a fidelidade do .docx sobreviva à conversão.

---

## 1. Caminho preferencial — Microsoft Word (cliente do usuário)

Quando o usuário tem Word instalado (caso comum na Bravo), o caminho de máxima fidelidade é o próprio Word:

**File → Save As → PDF**, com as opções:

- **Optimize for:** *Standard (publishing online and printing)* — preserva qualidade de imagens.
- **Options:**
  - Document properties — ON
  - Document structure tags for accessibility — ON
  - Bitmap text when fonts may not be embedded — **OFF** (mantém texto vetorial)
  - ISO 19005-1 compliant (PDF/A) — só se houver requisito de arquivamento legal
- **Save Options → Embed fonts in the file** — ON (essencial para Montserrat sobreviver em máquinas sem a fonte instalada)

Resultado: PDF de ~300-800KB para documento de 15-20 páginas com capa em imagem, fontes embedadas, links clicáveis, paginação dinâmica resolvida.

---

## 2. Caminho headless — LibreOffice (CI ou sem Word)

Quando o documento é produzido em um servidor ou no sandbox do Claude:

```bash
libreoffice --headless --convert-to pdf documento.docx --outdir /path/de/saida
```

**Cuidados específicos:**

- **Montserrat:** o LibreOffice headless do sandbox NÃO tem Montserrat instalado. Ele substituirá por uma fonte com serifa (DejaVu Serif tipicamente) na conversão. Isso é OK para verificação visual de layout — não é OK para entrega final ao stakeholder. Para entrega final, prefira o caminho Word do usuário.
- **Field PAGE:** LibreOffice resolve corretamente o field PAGE (paginação dinâmica). Verifique o PDF gerado.
- **Tabelas:** larguras DXA + layout fixed atravessam a conversão sem problema. Verifique mesmo assim.
- **Imagem de capa:** PNG A4 1654×2339 é renderizado sem perda perceptível.

---

## 3. Validação visual obrigatória

Independente do caminho, renderize as páginas como imagem e olhe:

```bash
# Cria diretório de preview e renderiza a 100 dpi
mkdir -p preview
pdftoppm -r 100 documento.pdf preview/p -png
```

Inspecione **todas** as páginas. Checklist específico para PDF:

- [ ] Capa cobre página inteira, sem qualquer borda branca.
- [ ] Logo da capa nítido, branco puro, sem retângulo opaco.
- [ ] Header do conteúdo: logo colorido com transparência, sem retângulo preto/branco.
- [ ] Linha separadora do header e do footer está visível.
- [ ] Paginação aparece em todas as páginas EXCETO capa (titlePg fez efeito).
- [ ] Fonte parece consistente. Se aparecer serifa em uma palavra que deveria ser sans, falta embedding.
- [ ] Tabelas com células bem dimensionadas, sem overflow.
- [ ] Caption das tabelas centralizada e legível.
- [ ] Callouts com cor de fundo e border-left intactos.
- [ ] Quotes com aspas tipográficas (`"` e `"`), não retas (`"`).

---

## 4. Conferência de embedding de fontes

```bash
# Lista as fontes embedadas
pdffonts documento.pdf
```

Procure `Montserrat` nas linhas. Se aparecer com `emb=yes`, está OK. Se aparecer `emb=no` ou aparecer fonte substituta (DejaVu, Arial), a Montserrat não foi embedada — corrija no Word (Save Options → Embed fonts) ou aceite a substituição se a entrega for interna.

---

## 5. PDF/A para arquivamento legal

Se o documento será arquivado em sistema regulatório (cobrança formal, comunicação obrigatória sob LGPD, contrato), exporte como PDF/A-2b:

- Word: PDF Options → ISO 19005-1 compliant (PDF/A).
- LibreOffice: `libreoffice --headless --convert-to pdf:writer_pdf_Export:'{"SelectPdfVersion":{"type":"long","value":"2"}}' documento.docx`

PDF/A garante visualização idêntica daqui a 20 anos. Custo: arquivos maiores e algumas restrições (formulários interativos, JavaScript bloqueados).

---

## 6. Compressão (quando o PDF passa de 5MB)

Capa em PNG 200 dpi pesa bastante. Se o PDF final passa de 5MB e precisa caber em e-mail:

```bash
# Comprime imagens para 150 dpi mantendo qualidade decente
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=out_compressed.pdf in.pdf
```

`/ebook` (150 dpi) é o sweet spot para documento corporativo. `/screen` (72 dpi) pixela a capa. `/printer` (300 dpi) é overkill para distribuição digital.

---

## 7. Erros comuns na conversão

**"Tudo virou Calibri ou Times New Roman."** Falta de Montserrat no ambiente. Caminhos: (i) instale Montserrat no sistema (Linux: copie para `/usr/share/fonts/truetype/montserrat/` + `fc-cache -f`); (ii) export pelo Word do usuário, que tem Montserrat instalada; (iii) aceite Inter ou Open Sans como fallback documentado.

**"A capa virou uma imagem dentro de uma página menor."** Margens da primeira section não estão zeradas. Reveja `setup_document()`.

**"O header aparece na capa."** Faltou `titlePg`. Reveja `setup_document()`.

**"A paginação começa em 1 na página de conteúdo, mas eu queria começar em 1 na capa."** O comportamento padrão da skill é: capa não tem paginação (titlePg + section sem footer), conteúdo começa em página 2. Se quiser numerar a capa também, remova `titlePg` da primeira section (não recomendado para documento corporativo).

**"Os links externos não abrem clicáveis no PDF."** LibreOffice resolve hyperlinks em DOCX. Se não estão clicáveis, verifique se os runs no DOCX usaram `Hyperlink` style. (No fluxo da skill, não usamos hyperlinks ainda — adicione se necessário.)
