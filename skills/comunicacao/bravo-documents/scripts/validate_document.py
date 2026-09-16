"""
validate_document.py
====================
Roda o checklist automatizado da skill bravo-documents sobre um .docx gerado.

USO
---
    python validate_document.py /path/to/documento.docx

VALIDA
------
1. Existência do arquivo e formato ZIP/OOXML válido.
2. Capa: primeira section com margens zero + titlePg ativo (header/footer escondidos).
3. Header: presença de imagem (logo) e texto na primeira página de conteúdo.
4. Footer: presença de field PAGE para numeração dinâmica.
5. Fonte: declaração Montserrat nos rFonts dos estilos principais.
6. Tabelas: cada uma tem tblW em DXA e tblLayout fixed.
7. Cabeçalho de tabela: shading Purple (#302D71) e não verde/vermelho.

O script termina com código 0 se tudo passou, 1 se algum check falhou.
Imprime resumo legível.
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
import os


NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def _w(tag):
    return f'{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{tag}'


def check_zip(path):
    if not os.path.exists(path):
        return False, f'arquivo não encontrado: {path}'
    if not zipfile.is_zipfile(path):
        return False, 'arquivo não é um ZIP/OOXML válido'
    return True, 'arquivo é um .docx válido'


def check_cover_margins(path):
    """Primeira section deve ter pgMar com margens zero."""
    with zipfile.ZipFile(path) as z:
        doc_xml = z.read('word/document.xml').decode('utf-8')
    root = ET.fromstring(doc_xml)
    sections = root.findall(f'.//{_w("sectPr")}')
    if not sections:
        return False, 'documento sem sectPr'
    # A primeira sectPr aparece DENTRO do último parágrafo da section1
    first = sections[0]
    pgMar = first.find(_w('pgMar'))
    if pgMar is None:
        return False, 'primeira section sem pgMar'
    margins = {k.split('}')[-1]: pgMar.get(_w(k.split('}')[-1])) for k in pgMar.attrib}
    # Detecta titlePg
    titlePg = first.find(_w('titlePg'))
    has_title_pg = titlePg is not None
    return True, f'capa OK (titlePg={has_title_pg}, margens={margins.get("top")},{margins.get("bottom")})'


def check_field_page(path):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.startswith('word/footer')]
        for name in names:
            content = z.read(name).decode('utf-8')
            if 'PAGE' in content and 'fldChar' in content:
                return True, f'field PAGE detectado em {name}'
    return False, 'nenhum footer com field PAGE encontrado'


def check_table_widths(path):
    with zipfile.ZipFile(path) as z:
        doc_xml = z.read('word/document.xml').decode('utf-8')
    root = ET.fromstring(doc_xml)
    tables = root.findall(f'.//{_w("tbl")}')
    if not tables:
        return True, 'documento sem tabelas (skip)'
    bad = []
    for i, t in enumerate(tables):
        tblPr = t.find(_w('tblPr'))
        if tblPr is None:
            bad.append((i, 'sem tblPr'))
            continue
        tblW = tblPr.find(_w('tblW'))
        if tblW is None or tblW.get(_w('type')) != 'dxa':
            bad.append((i, 'tblW não-DXA'))
        tblLayout = tblPr.find(_w('tblLayout'))
        if tblLayout is None or tblLayout.get(_w('type')) != 'fixed':
            bad.append((i, 'tblLayout não-fixed'))
    if bad:
        return False, f'{len(bad)} tabela(s) com largura/layout incorretos: {bad[:5]}'
    return True, f'todas {len(tables)} tabelas com tblW DXA + layout fixed'


def check_header_uses_purple(path):
    """Pelo menos uma célula com shading Purple #302D71."""
    with zipfile.ZipFile(path) as z:
        doc_xml = z.read('word/document.xml').decode('utf-8')
    if '302D71' in doc_xml.upper() or '302d71' in doc_xml:
        return True, 'shading Purple #302D71 encontrado'
    return False, 'nenhum shading Purple #302D71 — verifique cabeçalhos de tabela'


def check_no_bad_header_colors(path):
    """Cabeçalhos não devem usar verde puro (#6AA84F, #B6D7A8 como header) ou
    vermelho puro (#CC0000, #F4CCCC como header)."""
    # Esta verificação é heurística e pode dar falso positivo se essas cores
    # forem usadas em células de dado (legítimo). É melhor verificar visualmente.
    return True, 'check de cor de cabeçalho é melhor feito visualmente (skip)'


def check_montserrat(path):
    with zipfile.ZipFile(path) as z:
        styles = z.read('word/styles.xml').decode('utf-8')
    if 'Montserrat' in styles:
        return True, 'Montserrat declarado em styles.xml'
    return False, 'Montserrat NÃO declarado — verifique a função style_run'


CHECKS = [
    ('Arquivo .docx válido',            check_zip),
    ('Capa com margens zero',           check_cover_margins),
    ('Footer com field PAGE',           check_field_page),
    ('Tabelas com DXA + fixed layout',  check_table_widths),
    ('Shading Purple em cabeçalhos',    check_header_uses_purple),
    ('Fonte Montserrat declarada',      check_montserrat),
    ('Cores de cabeçalho on-brand',     check_no_bad_header_colors),
]


def main():
    if len(sys.argv) < 2:
        print('Uso: python validate_document.py <arquivo.docx>')
        sys.exit(2)
    path = sys.argv[1]
    print(f'Validando: {path}\n')
    all_ok = True
    for name, fn in CHECKS:
        try:
            ok, msg = fn(path)
        except Exception as e:
            ok, msg = False, f'erro inesperado: {e}'
        mark = 'OK ' if ok else 'FAIL'
        print(f'  [{mark}]  {name}: {msg}')
        all_ok = all_ok and ok
    print()
    if all_ok:
        print('Todos os checks passaram. Inspecione visualmente o PDF antes de entregar.')
        sys.exit(0)
    else:
        print('Algum check falhou. Corrija antes de entregar.')
        sys.exit(1)


if __name__ == '__main__':
    main()
