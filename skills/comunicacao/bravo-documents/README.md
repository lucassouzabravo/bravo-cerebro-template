# bravo-documents

Skill de construção de documentos longos Bravo em padrão consulting-grade. Sempre usada em conjunto com `bravo-brand-guidelines`.

**Ponto de entrada:** [`SKILL.md`](SKILL.md) — Claude lê este arquivo primeiro.

**Estrutura:**

```
bravo-documents/
├── SKILL.md                          ← manual completo da skill
├── scripts/
│   ├── bravo_doc_helpers.py          ← módulo Python com todos os helpers
│   ├── build_cover.py                ← gera PNG da capa full-bleed
│   ├── fix_logo_transparency.py      ← converte logos JPEG-como-PNG em PNG-alfa
│   └── validate_document.py          ← checklist automatizado pós-build
├── assets/
│   └── logos/
│       ├── bravo-logo-color-alpha.png    ← logo colorido com transparência REAL
│       └── bravo-logo-branco-alpha.png   ← logo branco com transparência REAL
└── references/
    ├── docx-construction.md          ← receita detalhada de DOCX
    ├── pdf-export.md                 ← exportação para PDF
    └── gdocs-conversion.md           ← conversão para Google Docs
```

**Para instalar como skill ativa:** copie este diretório inteiro para `<skills-plugin>/skills/bravo-documents/` (mesmo nível de `bravo-brand-guidelines`).
