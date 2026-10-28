# -*- coding: utf-8 -*-
"""Контрольная работа № 1: практики 1–5."""
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(r"d:\вуз\алгосы")
OUT = ROOT / "Контрольная работа 1.docx"
FIG = ROOT / "_control_fig"
FIG.mkdir(exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"


def console_png(name, lines):
    path = FIG / name
    text = "\n".join(lines)
    rows = max(4, len(lines))
    fig, ax = plt.subplots(figsize=(8.2, 0.38 * rows + 0.4))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    ax.axis("off")
    ax.text(0.02, 0.98, text, color="#dcdcdc", fontsize=11, family="Consolas",
            va="top", ha="left", transform=ax.transAxes)
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def draw_directed(name, edges, pos, title, highlight=None):
    path = FIG / name
    G = nx.DiGraph()
    weighted = len(edges[0]) == 3
    if weighted:
        G.add_weighted_edges_from(edges)
    else:
        G.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color="#c6e6c6",
                           edgecolors="#2d5a2d", linewidths=1.3)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold")
    hl = set(highlight or [])
    normal = [(u, v) for u, v, *_ in (edges if weighted else [(a, b, 1) for a, b in edges]) if (u, v) not in hl]
    extra = [(u, v) for u, v, *_ in (edges if weighted else [(a, b, 1) for a, b in edges]) if (u, v) in hl]
    kw = dict(arrows=True, arrowstyle="-|>", arrowsize=16, connectionstyle="arc3,rad=0.04",
              min_source_margin=14, min_target_margin=14)
    if normal:
        nx.draw_networkx_edges(G, pos, edgelist=normal, ax=ax, width=1.5, edge_color="#333", **kw)
    if extra:
        nx.draw_networkx_edges(G, pos, edgelist=extra, ax=ax, width=2.6, edge_color="#c0392b", **kw)
    if weighted:
        labels = {(u, v): w for u, v, w in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=9)
    ax.set_title(title, fontsize=12)
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def draw_undirected(name, edges, pos, title, highlight=None):
    path = FIG / name
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color="#f7d774",
                           edgecolors="#7a5b00", linewidths=1.3)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold")
    hl = {frozenset(e) for e in (highlight or [])}
    widths, colors = [], []
    for u, v in G.edges():
        if frozenset((u, v)) in hl:
            widths.append(2.6)
            colors.append("#c0392b")
        else:
            widths.append(1.5)
            colors.append("#333")
    nx.draw_networkx_edges(G, pos, ax=ax, width=widths, edge_color=colors)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=9)
    ax.set_title(title, fontsize=12)
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


# Исправленные рисунки тетради 2 (веса и направления сверены с тетрадью).
pos_s1 = {1: (2.2, 1.2), 2: (1.1, 2.3), 3: (3.2, 0.15), 4: (0.0, 1.5), 5: (1.15, 0.0), 6: (3.3, 1.35)}
e_s1 = [(1, 2, 1), (1, 4, 7), (2, 3, 4), (3, 1, 2), (3, 4, 13), (4, 5, 1), (5, 3, 12), (5, 6, 5), (6, 3, 2)]
p_s1 = draw_directed("wb2_sam1.png", e_s1, pos_s1, "Практическая работа 2, задание 1")
p_s1_path = draw_directed("wb2_sam1_path.png", e_s1, pos_s1, "Кратчайший путь 1 → 4 → 5 → 6",
                          highlight=[(1, 4), (4, 5), (5, 6)])

e_h2 = [(1, 2, 4), (1, 3, 3), (1, 4, 7), (2, 4, 6), (2, 5, 4), (3, 6, 3), (3, 7, 4),
        (4, 7, 11), (5, 6, 7), (5, 8, 4), (6, 8, 8), (7, 8, 5)]
pos_h2 = {1: (0, 1.1), 2: (1.5, 2.2), 3: (2.2, 1.15), 4: (1.6, 0.0),
          5: (3.3, 2.3), 6: (3.5, 1.15), 7: (4.5, 0.15), 8: (5.3, 1.7)}
p_h2 = draw_undirected("wb2_hard2.png", e_h2, pos_h2, "Практическая работа 2, повышенная 2")
p_h2_path = draw_undirected("wb2_hard2_path.png", e_h2, pos_h2, "Кратчайший путь 1–3–7–8, длина 12",
                            highlight=[(1, 3), (3, 7), (7, 8)])

console_png("wb4_ba.png", [
    "python hard_1_ba.py",
    "Вершин всего: 1003",
    "Рёбер: 2003",
    "Топ-5 хабов (вершина, степень):",
    "  узел 0: степень 59",
    "  узел 1: степень 59",
    "  узел 2: степень 59",
    "  узел 3: степень 41",
    "  узел 5: степень 41",
])
console_png("wb5_1.png", [
    "python sam_1.py",
    "DFS: [1, 2, 4, 8, 5, 10, 9, 6, 3, 7]",
    "BFS: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
])
console_png("wb5_2.png", [
    "python sam_2.py",
    "{'A','B','C','D'}  двудольный: False",
    "{'E','F','G'}      двудольный: True   E=0 F=1 G=0",
    "{'H'}              двудольный: True   H=0",
    "{'I','J','K','L'}  двудольный: True   I=0 K=0 J=1 L=1",
])
console_png("wb5_3.png", [
    "python sam_3.py",
    "Топопорядок: ['A', 'C', 'F', 'B', 'E', 'H', 'D', 'G']",
    "Кратчайший путь: ['A', 'B', 'E', 'H']",
    "Длина: 3",
])


def set_run_font(run, name="Times New Roman", size=14, bold=False, italic=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def shade(paragraph, color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    pPr.append(shd)


def add_page_field(paragraph):
    run = paragraph.add_run()
    set_run_font(run, size=12)
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    i = OxmlElement("w:instrText")
    i.set(qn("xml:space"), "preserve")
    i.text = " PAGE "
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    run._r.append(b)
    run._r.append(i)
    run._r.append(e)


def add_toc(paragraph):
    run = paragraph.add_run()
    r = run._r
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r' TOC \o "1-1" \h \z \u '
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Оглавление обновится при открытии документа в Word."
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    r.append(b)
    r.append(instr)
    r.append(sep)
    r2 = OxmlElement("w:r")
    r2.append(placeholder)
    paragraph._p.append(r2)
    r.append(e)


doc = Document()
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.left_margin = Cm(3.0)
section.right_margin = Cm(1.5)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.different_first_page_header_footer = True

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(14)
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
pf = normal.paragraph_format
pf.line_spacing = 1.5
pf.space_after = Pt(6)
pf.first_line_indent = Cm(1.25)

for level in (1, 2):
    st = doc.styles[f"Heading {level}"]
    st.font.name = "Times New Roman"
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.font.bold = True
    st.font.size = Pt(16 if level == 1 else 14)
    st._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.space_before = Pt(12)
    st.paragraph_format.space_after = Pt(8)
    st.paragraph_format.first_line_indent = Cm(0)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.page_break_before = level == 1


def P(text="", *, center=False, bold=False, italic=False, size=14, indent=True, space_before=0, space_after=6, font="Times New Roman"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(0 if center or not indent else 1.25)
    if text:
        run = p.add_run(text)
        set_run_font(run, font, size, bold, italic)
    return p


def H(text, level=2):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        set_run_font(run, size=16 if level == 1 else 14, bold=True)
    return p


def code(text):
    for line in text.strip("\n").split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.left_indent = Cm(0.5)
        shade(p, "F3F3F3")
        run = p.add_run(line if line else " ")
        set_run_font(run, "Consolas", 10)
    P("", size=6, indent=False, space_after=4)


def pre(text):
    for line in text.strip("\n").split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.left_indent = Cm(1.0)
        run = p.add_run(line if line else " ")
        set_run_font(run, "Consolas", 11)
    P("", size=4, indent=False, space_after=2)


def img(path, width=15.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width))


def task(title):
    H(title, 2)


def label(text):
    P(text, bold=True, indent=False, space_before=8, space_after=2)


# ---------- титульный лист ----------
for _ in range(2):
    P("", center=True, indent=False, space_after=0)
P("МИНОБРНАУКИ РОССИИ", center=True, bold=True, indent=False, size=12, space_after=2)
P("Федеральное государственное бюджетное образовательное учреждение", center=True, indent=False, size=12, space_after=0)
P("высшего образования", center=True, indent=False, size=12, space_after=0)
P("«МИРЭА — Российский технологический университет»", center=True, bold=True, indent=False, size=12, space_after=8)
P("Институт перспективных технологий и индустриального программирования", center=True, indent=False, size=12, space_after=0)
P("Кафедра индустриального программирования", center=True, indent=False, size=12, space_after=0)

for _ in range(3):
    P("", center=True, indent=False, space_after=0)
P("КОНТРОЛЬНАЯ РАБОТА № 1", center=True, bold=True, indent=False, size=18, space_after=8)
P("по дисциплине «Алгоритмы и структуры данных»", center=True, indent=False, size=14, space_after=10)
P("Практические работы № 1, 2, 3, 4, 5", center=True, bold=True, indent=False, space_after=0)

for _ in range(4):
    P("", center=True, indent=False, space_after=0)
P("Выполнил: студент ________________________________", center=False, indent=False, space_after=2)
P("Группа: _________________________________________", indent=False, space_after=8)
P("Проверил: Преснецова Виктория Юрьевна", indent=False, space_after=2)

for _ in range(3):
    P("", center=True, indent=False, space_after=0)
P("Москва", center=True, indent=False, space_after=0)
P("2026", center=True, indent=False, space_after=0)

# титул без номера страницы
footer0 = section.first_page_footer
footer0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# ---------- основной раздел ----------
new_sec = doc.add_section(WD_SECTION.NEW_PAGE)
new_sec.page_width = Cm(21.0)
new_sec.page_height = Cm(29.7)
new_sec.left_margin = Cm(3.0)
new_sec.right_margin = Cm(1.5)
new_sec.top_margin = Cm(2.0)
new_sec.bottom_margin = Cm(2.0)
pg = OxmlElement("w:pgNumType")
pg.set(qn("w:start"), "2")
new_sec._sectPr.append(pg)
fp = new_sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_page_field(fp)

# оглавление — не Heading, чтобы не попало само в себя
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.first_line_indent = Cm(0)
p.paragraph_format.space_after = Pt(12)
r = p.add_run("СОДЕРЖАНИЕ")
set_run_font(r, size=16, bold=True)
toc_p = doc.add_paragraph()
toc_p.paragraph_format.first_line_indent = Cm(0)
add_toc(toc_p)

settings = doc.settings.element
upd = OxmlElement("w:updateFields")
upd.set(qn("w:val"), "true")
settings.append(upd)

W1 = ROOT / "рабочая_тетрадь_1"
W2 = ROOT / "рабочая_тетрадь_2"
W3 = ROOT / "рабочая_тетрадь_3"
W4 = ROOT / "рабочая_тетрадь_4"
W5 = ROOT / "рабочая_тетрадь_5"

# ===================== ПР 1 =====================
H("Практическая работа 1. Графы", 1)
P("Тема работы — способы задания графа, маршруты и эйлеровы циклы. Ниже выполнены задания для самостоятельной работы и задания повышенной трудности.")

task("Задание 1. Матрицы орграфа")
label("Формулировка.")
P("Для ориентированного графа G найти матрицу смежности, матрицу инцидентности и списки смежности.")
label("Ход решения.")
P("По рисунку дуги такие: 1→2, 2→3, 2→4, 3→5, 4→5, 5→1. В матрице смежности единица стоит в клетке (i, j), если есть дуга i→j. В матрице инцидентности для орграфа у начала дуги ставится −1, у конца +1.")
img(W1 / "sam_1_graf.png", 12)
label("Результат.")
P("Матрица смежности (порядок вершин 1, 2, 3, 4, 5):", indent=False)
pre("""    1  2  3  4  5
1   0  1  0  0  0
2   0  0  1  1  0
3   0  0  0  0  1
4   0  0  0  0  1
5   1  0  0  0  0""")
P("Матрица инцидентности. Рёбра e1=(1,2), e2=(2,3), e3=(2,4), e4=(3,5), e5=(4,5), e6=(5,1):", indent=False)
pre("""     e1  e2  e3  e4  e5  e6
1    -1   0   0   0   0   1
2     1  -1  -1   0   0   0
3     0   1   0  -1   0   0
4     0   0   1   0  -1   0
5     0   0   0   1   1  -1""")
P("Списки смежности: 1: 2;  2: 3, 4;  3: 5;  4: 5;  5: 1.")

task("Задание 2. Матрицы взвешенного графа")
label("Формулировка.")
P("Для неориентированного взвешенного графа найти матрицу смежности, матрицу инцидентности и списки смежности.")
label("Ход решения.")
P("Рёбра и веса: XY = 2, XZ = 4, YZ = 1, YW = 3, ZW = 5. В матрице смежности вместо единиц записаны веса. Матрица инцидентности строится без весов: 1, если вершина принадлежит ребру.")
img(W1 / "sam_2_graf.png", 12)
label("Результат.")
pre("""    X  Y  Z  W
X   0  2  4  0
Y   2  0  1  3
Z   4  1  0  5
W   0  3  5  0""")
P("Инцидентность, столбцы XY, XZ, YZ, YW, ZW:", indent=False)
pre("""    e1 e2 e3 e4 e5
X    1  1  0  0  0
Y    1  0  1  1  0
Z    0  1  1  0  1
W    0  0  0  1  1""")
P("Списки: X: Y, Z;  Y: X, Z, W;  Z: X, Y, W;  W: Y, Z.")

task("Задание 3. Граф по списку рёбер")
label("Формулировка.")
P("Построить граф G = (V, E), V = {1, 2, 3, 4, 5, 6}, E = {(1,2), (1,3), (1,5), (1,6), (2,3), (2,4), (2,6), (3,4), (3,5), (4,5), (4,6), (5,6)}.")
label("Ход решения.")
P("Каждая пара из E проводится одним неориентированным ребром. Дополнительно составлена матрица смежности: симметричная, без петель.")
img(W1 / "sam_3_graf.png", 12)
label("Результат.")
pre("""    1 2 3 4 5 6
1   0 1 1 0 1 1
2   1 0 1 1 0 1
3   1 1 0 1 1 0
4   0 1 1 0 1 1
5   1 0 1 1 0 1
6   1 1 0 1 1 0""")
P("Списки: 1: 2, 3, 5, 6;  2: 1, 3, 4, 6;  3: 1, 2, 4, 5;  4: 2, 3, 5, 6;  5: 1, 3, 4, 6;  6: 1, 2, 4, 5.")

task("Задание 4. Граф по списку рёбер")
label("Формулировка.")
P("Построить граф на вершинах {1,…,7} с рёбрами (1,4), (1,5), (1,6), (1,7), (2,4), (2,7), (3,4), (3,5), (3,6), (3,7), (4,7).")
label("Ход решения.")
P("Граф неориентированный. Вершины 5 и 6 соединены только с 1 и 3, вершина 2 — только с 4 и 7.")
img(W1 / "sam_4_graf.png", 13)
label("Результат.")
pre("""    1 2 3 4 5 6 7
1   0 0 0 1 1 1 1
2   0 0 0 1 0 0 1
3   0 0 0 1 1 1 1
4   1 1 1 0 0 0 1
5   1 0 1 0 0 0 0
6   1 0 1 0 0 0 0
7   1 1 1 1 0 0 0""")
P("Списки: 1: 4, 5, 6, 7;  2: 4, 7;  3: 4, 5, 6, 7;  4: 1, 2, 3, 7;  5: 1, 3;  6: 1, 3;  7: 1, 2, 3, 4.")

task("Задание 5. Граф по списку рёбер")
label("Формулировка.")
P("Построить граф на вершинах {1,…,8} с рёбрами (1,6), (1,8), (2,6), (2,7), (3,4), (3,5), (3,6), (3,8), (4,5), (4,6), (4,8), (7,8).")
label("Ход решения.")
P("Отмечаются все 12 рёбер. Вершина 5 смежна только с 3 и 4, вершина 7 — только с 2 и 8.")
img(W1 / "sam_5_graf.png", 14)
label("Результат.")
pre("""    1 2 3 4 5 6 7 8
1   0 0 0 0 0 1 0 1
2   0 0 0 0 0 1 1 0
3   0 0 0 1 1 1 0 1
4   0 0 1 0 1 1 0 1
5   0 0 1 1 0 0 0 0
6   1 1 1 1 0 0 0 0
7   0 1 0 0 0 0 0 1
8   1 0 1 1 0 0 1 0""")
P("Списки: 1: 6, 8;  2: 6, 7;  3: 4, 5, 6, 8;  4: 3, 5, 6, 8;  5: 3, 4;  6: 1, 2, 3, 4;  7: 2, 8;  8: 1, 3, 4, 7.")

task("Задание 6. Пути в орграфе")
label("Формулировка.")
P("Дан орграф с вершинами A–F и дугами (A,B), (A,C), (B,D), (C,D), (C,E), (D,E), (D,F), (E,F). Найти путь из A в F не короче трёх рёбер, проверить повтор вершин и существование пути без циклов.")
label("Ход решения.")
P("Граф ациклический: все дуги идут слева направо, вернуться в уже пройденную вершину нельзя. Перебор простых путей из A в F даёт пять маршрутов, самый короткий из них имеет два ребра, поэтому путь из трёх рёбер тоже есть.")
img(W1 / "sam_6_graf.png", 14)
label("Результат.")
P("Путь не короче трёх рёбер: A → B → D → F. Повторяющихся вершин в нём нет. Путь без циклов существует. Все простые пути A → F:")
pre("""A → B → D → F
A → B → D → E → F
A → C → D → F
A → C → D → E → F
A → C → E → F""")

task("Задание 7. Маршруты 1–7")
label("Формулировка.")
P("Дан неориентированный граф на вершинах 1–7 с рёбрами (1,2), (1,3), (2,4), (2,5), (3,5), (4,6), (5,6), (5,7), (6,7). Найти маршруты из 1 в 7, проверить простоту и указать кратчайший.")
label("Ход решения.")
P("Если разрешить повторять вершины, маршрутов бесконечно много: можно кружить по циклу 5–6–7. Поэтому выписаны все простые цепи (вершины не повторяются) и среди них выбраны самые короткие.")
img(W1 / "sam_7_graf.png", 14)
label("Результат.")
pre("""1-2-5-7
1-3-5-7
1-2-5-6-7
1-3-5-6-7
1-2-4-6-7
1-2-4-6-5-7
1-3-5-2-4-6-7""")
P("Все перечисленные маршруты простые. Кратчайшие содержат 3 ребра: 1–2–5–7 и 1–3–5–7.")

task("Задание повышенной трудности 1")
label("Формулировка.")
P("Для ориентированного взвешенного графа на 10 вершинах найти матрицу смежности, матрицу инцидентности и списки смежности.")
label("Ход решения.")
P("Дуги сняты с рисунка тетради: (1,2,4), (1,3,2), (2,4,7), (2,5,1), (2,6,3), (3,6,3), (3,7,6), (4,7,5), (5,7,8), (5,10,7), (6,8,6), (6,10,5), (7,9,2), (8,9,4), (9,10,9). В матрице смежности записан вес дуги, иначе 0.")
img(W1 / "hard_1_graf.png", 14)
label("Результат.")
P("Списки смежности (исходящие): 1: 2, 3;  2: 4, 5, 6;  3: 6, 7;  4: 7;  5: 7, 10;  6: 8, 10;  7: 9;  8: 9;  9: 10;  10: пусто. Ненулевые клетки матрицы смежности совпадают с этим списком и указанными весами. В матрице инцидентности 15 столбцов: −1 у начала дуги, +1 у конца.")

task("Задание повышенной трудности 2")
label("Формулировка.")
P("Построить граф на вершинах {1,…,9} с рёбрами (1,2), (1,3), (1,5), (1,9), (2,3), (2,6), (2,8), (3,4), (3,9), (4,5), (4,7), (4,8), (5,6), (5,7), (6,8), (6,9), (8,9).")
label("Ход решения.")
P("Неориентированный граф, 17 рёбер. Матрица смежности симметрична.")
img(W1 / "hard_2_graf.png", 12)
label("Результат.")
pre("""    1 2 3 4 5 6 7 8 9
1   0 1 1 0 1 0 0 0 1
2   1 0 1 0 0 1 0 1 0
3   1 1 0 1 0 0 0 0 1
4   0 0 1 0 1 0 1 1 0
5   1 0 0 1 0 1 1 0 0
6   0 1 0 0 1 0 0 1 1
7   0 0 0 1 1 0 0 0 0
8   0 1 0 1 0 1 0 0 1
9   1 0 1 0 0 1 0 1 0""")
P("Списки: 1: 2, 3, 5, 9;  2: 1, 3, 6, 8;  3: 1, 2, 4, 9;  4: 3, 5, 7, 8;  5: 1, 4, 6, 7;  6: 2, 5, 8, 9;  7: 4, 5;  8: 2, 4, 6, 9;  9: 1, 3, 6, 8.")

task("Задание повышенной трудности 3. Эйлеров цикл")
label("Формулировка.")
P("Проверить, эйлеров ли граф на вершинах A–H с заданными 13 рёбрами. Если нет — добавить минимум рёбер и найти эйлеров цикл.")
label("Ход решения.")
P("Степени: A=3, B=3, C=4, D=3, E=3, F=4, G=3, H=3. Нечётных вершин шесть, поэтому эйлерова цикла нет. Чтобы сделать все степени чётными, достаточно трёх новых рёбер, соединяющих нечётные вершины попарно: AE, BG, DH. Этих рёбер в исходном графе не было. Дальше цикл собирается обходом всех 16 рёбер без повторов.")
img(W1 / "hard_3_graf.png", 13)
img(W1 / "hard_3_euler_graf.png", 13)
label("Результат.")
P("Граф не эйлеров. После добавления (A,E), (B,G), (D,H) эйлеров цикл:")
pre("A-B-E-H-D-G-B-C-A-D-C-F-G-H-F-E-A")
P("Последовательность рёбер: AB, BE, EH, HD, DG, GB, BC, CA, AD, DC, CF, FG, GH, HF, FE, EA. Каждое ребро, включая три добавленных, входит ровно один раз.")

# ===================== ПР 2 =====================
H("Практическая работа 2. Алгоритм Дейкстры", 1)
P("Во всех заданиях ищется кратчайший путь во взвешенном графе без отрицательных рёбер. Метка вершины — длина лучшего уже найденного пути от источника. На каждом шаге постоянной становится наименьшая временная метка.")

task("Задание 1. Кратчайший путь 1 → 6")
label("Формулировка.")
P("Найти кратчайший путь в орграфе от вершины 1 до вершины 6.")
label("Ход решения.")
P("Дуги: 1→2 (1), 1→4 (7), 2→3 (4), 3→1 (2), 3→4 (13), 4→5 (1), 5→3 (12), 5→6 (5), 6→3 (2). Из 1 сразу получаем метки 2 = 1 и 4 = 7. Дуга 2→3 даёт вершине 3 метку 5, но из 3 в 6 выхода нет. Единственный вход в 6 — дуга 5→6, а в 5 ведёт только 4→5. Поэтому путь идёт через 4 и 5.")
img(p_s1, 14)
label("Результат.")
P("Кратчайший путь: 1 → 4 → 5 → 6. Длина 7 + 1 + 5 = 13.")
img(p_s1_path, 14)

task("Задание 2. Кратчайший путь 1–6")
label("Формулировка.")
P("Найти кратчайший путь от вершины 1 до вершины 6. На рисунке тетради стрелок нет, поэтому граф считается неориентированным.")
label("Ход решения.")
P("Рёбра: 1-2 (3), 1-4 (7), 1-5 (8), 2-3 (1), 2-4 (4), 3-4 (2), 3-6 (3), 4-5 (3), 4-6 (4), 5-6 (9). От 1 ближайшая вершина — 2 с меткой 3. Через неё вершина 3 получает метку 4, а из 3 ребро веса 3 ведёт сразу в 6. Обход через 4 даёт путь до 6 длины 10, он хуже.")
img(W2 / "sam_2_graf.png", 13)
label("Результат.")
P("Кратчайший путь: 1 – 2 – 3 – 6. Длина 3 + 1 + 3 = 7.")
img(W2 / "sam_2_path.png", 13)

task("Задание 3. Доставка S → T")
label("Формулировка.")
P("Склад S, точки A, B, C и торговый центр T. Затраты в минутах: S–A 5, S–B 10, A–C 3, A–T 12, B–C 2, C–T 4. Найти кратчайший маршрут алгоритмом Дейкстры.")
label("Ход решения.")
P("Из S метки A = 5 и B = 10. Из A вершина C получает 8, а прямой путь в T — 17. Из C путь в T равен 8 + 4 = 12, это лучше 17. Из B путь в C равен 12 и уже найденную метку 8 не улучшает.")
img(W2 / "sam_3_graf.png", 14)
label("Результат.")
P("Маршрут S → A → C → T, время 12 минут.")
img(W2 / "sam_3_path.png", 14)

task("Задание повышенной трудности 1. Пути от склада S")
label("Формулировка.")
P("Найти кратчайшие маршруты от склада S до складов A, B, C, D, E, F, G. Дороги направленные, веса в минутах: S→A 10, S→B 15, A→C 12, A→D 15, B→E 10, C→F 5, D→F 10, D→G 20, E→G 5, F→G 10.")
label("Ход решения.")
P("Дейкстра от S. Верхняя ветка обслуживает A, C, D и F, нижняя — B, E и G. До G путь через E короче, чем через F или D.")
img(W2 / "hard_1_graf.png", 15)
label("Результат.")
pre("""S   0
A  10   S → A
B  15   S → B
C  22   S → A → C
D  25   S → A → D
E  25   S → B → E
F  27   S → A → C → F
G  30   S → B → E → G""")

task("Задание повышенной трудности 2. Путь 1–8")
label("Формулировка.")
P("Найти кратчайший путь из вершины 1 в вершину 8 алгоритмом Дейкстры. Граф на рисунке неориентированный.")
label("Ход решения.")
P("Веса: 1-2 = 4, 1-3 = 3, 1-4 = 7, 2-4 = 6, 2-5 = 4, 3-6 = 3, 3-7 = 4, 4-7 = 11, 5-6 = 7, 5-8 = 4, 6-8 = 8, 7-8 = 5. Сначала фиксируется вершина 3 (метка 3), из неё 6 = 6 и 7 = 7. Вершина 2 даёт вершине 5 метку 8. До 8 сравниваются три входа: через 6 получается 14, через 7 получается 12, через 5 тоже 12.")
img(p_h2, 14)
label("Результат.")
P("Длина кратчайшего пути равна 12. Один из таких путей: 1 – 3 – 7 – 8 (3 + 4 + 5). Второй той же длины: 1 – 2 – 5 – 8 (4 + 4 + 4).")
img(p_h2_path, 14)

# ===================== ПР 3 =====================
H("Практическая работа 3. Максимальный поток и минимальный разрез", 1)
P("Поток ищется алгоритмом Форда–Фалкерсона: пока есть путь из источника в сток по ненасыщенным дугам, по нему пускается поток, равный минимуму остаточных ёмкостей. В задании 4 повышенной трудности пути выбираются поиском в ширину — это алгоритм Эдмондса–Карпа. По теореме о максимальном потоке и минимальном разрезе величина потока совпадает с ёмкостью разреза.")

task("Задание 1. Поток 1 → 6")
label("Формулировка.")
P("Найти наибольший поток из 1 в 6 алгоритмом Форда–Фалкерсона.")
label("Ход решения.")
P("Ёмкости: 1→2 = 3, 1→4 = 5, 4→2 = 4, 2→3 = 5, 4→5 = 2, 3→5 = 9, 3→6 = 5, 5→6 = 7. Пускаем 3 по пути 1-2-3-6, затем 2 по пути 1-4-5-6, затем ещё 2 по пути 1-4-2-3-6. После этого дуги 2→3 и 4→5 насыщены, нового пути в 6 нет.")
img(W3 / "sam_1_graf.png", 14)
label("Результат.")
P("Максимальный поток равен 7. Минимальный разрез: S' = {1, 2, 4}, дуги 2→3 и 4→5, ёмкость 5 + 2 = 7.")
img(W3 / "sam_1_flow.png", 14)

task("Задание 2. Поток S → T")
label("Формулировка.")
P("Найти максимальный поток из S в T.")
label("Ход решения.")
P("В сток входит только дуга F→T ёмкости 10, поэтому поток не больше 10. Путь S-A-C-E-F-T даёт 6, путь S-A-C-D-F-T даёт ещё 2, путь S-B-D-F-T даёт ещё 2. Дуга F→T насыщена.")
img(W3 / "sam_2_graf.png", 14)
label("Результат.")
P("Максимальный поток равен 10. Минимальный разрез — одна дуга F→T.")
img(W3 / "sam_2_flow.png", 14)

task("Задание 3. Поток S → T")
label("Формулировка.")
P("В тексте тетради написано «поток из 1 в 6», на рисунке сеть с вершинами S, A, B, C, D, E, F, T. Решение строится по рисунку.")
label("Ход решения.")
P("В сток входит только F→T ёмкости 7. Путь S-A-C-E-F-T пропускает 5, путь S-B-C-D-F-T пропускает оставшиеся 2.")
img(W3 / "sam_3_graf.png", 14)
label("Результат.")
P("Максимальный поток равен 7. Разрез — дуга F→T.")
img(W3 / "sam_3_flow.png", 14)

task("Задание повышенной трудности 1. Поток 1 → 9")
label("Формулировка.")
P("Найти наибольший поток из 1 в 9.")
label("Ход решения.")
P("Четыре увеличивающих пути: 1-5-9 на 21, 1-2-7-8-9 на 5, 1-5-4-6-9 на 12, 1-2-3-7-8-9 на 6. Дальше насыщены выходы 5→9, 4→6 и 7→8.")
img(W3 / "hard_1_graf.png", 14)
label("Результат.")
P("Максимальный поток равен 44. Разрез S' = {1, 2, 3, 4, 5, 7}, дуги 5→9, 4→6 и 7→8, ёмкость 21 + 12 + 11 = 44.")
img(W3 / "hard_1_flow.png", 14)

task("Задание повышенной трудности 2. Поток S → T")
label("Формулировка.")
P("Найти максимальный поток из S в T. Узкое место сети — дуга F→G ёмкости 6.")
label("Ход решения.")
P("Путь S-A-C-E-F-G-T даёт 4, путь S-B-D-E-F-G-T даёт 2. Дуга F→G насыщена.")
img(W3 / "hard_2_graf.png", 14)
label("Результат.")
P("Максимальный поток равен 6. Разрез — дуга F→G.")
img(W3 / "hard_2_flow.png", 14)

task("Задание повышенной трудности 3. Поток S → T")
label("Формулировка.")
P("Найти максимальный поток из S в T в сети с вершинами S, A–K, T.")
label("Ход решения.")
P("В T входят только дуги I→T (5), J→T (7) и K→T (10), сумма 22. Пять путей набирают ровно эту сумму: +5, +5, +2, +3 и +7. Все три входа в T насыщены.")
img(W3 / "hard_3_graf.png", 15)
label("Результат.")
P("Максимальный поток равен 22. Разрез — три дуги, входящие в T.")
img(W3 / "hard_3_flow.png", 15)

task("Задание повышенной трудности 4. Эдмондс–Карп")
label("Формулировка.")
P("Сеть S, A, B, C, D, T. Ёмкости: S→A 10, S→B 5, A→C 9, B→C 4, B→D 8, C→T 10, D→T 10. Найти максимальный поток алгоритмом Эдмондса–Карпа, число итераций, использованные пути и итоговый поток по рёбрам.")
label("Ход решения.")
P("Поиск в ширину каждый раз берёт кратчайший по числу дуг путь. Сначала S-A-C-T пропускает 9. Затем S-B-C-T пропускает 1: у C→T осталась единица. Затем S-B-D-T пропускает 4, потому что из S в B осталось 4. После этого из S в T пути нет.")
code("""
from collections import deque

cap = {
    'S': {'A': 10, 'B': 5},
    'A': {'C': 9},
    'B': {'C': 4, 'D': 8},
    'C': {'T': 10},
    'D': {'T': 10},
    'T': {},
}

def edmonds_karp(cap, s, t):
    flow = 0
    residual = {u: dict(vs) for u, vs in cap.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {}).setdefault(u, 0)
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in residual[u].items():
                if v not in parent and c > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            break
        path, v, bottleneck = [], t, 10**9
        while v != s:
            path.append(v)
            bottleneck = min(bottleneck, residual[parent[v]][v])
            v = parent[v]
        path.append(s)
        path.reverse()
        v = t
        while v != s:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u
        flow += bottleneck
        print(path, '+', bottleneck, 'сумма', flow)
    return flow
""")
label("Результат.")
P("Максимальный поток равен 14. Итераций три: S-A-C-T (+9), S-B-C-T (+1), S-B-D-T (+4). Итоговый поток: S→A 9/10, S→B 5/5, A→C 9/9, B→C 1/4, B→D 4/8, C→T 10/10, D→T 4/10. Минимальный разрез: S' = {S, A}, дуги S→B и A→C, ёмкость 14.")
img(W3 / "hard_4_graf.png", 14)
img(W3 / "hard_4_flow.png", 14)

# ===================== ПР 4 =====================
H("Практическая работа 4. Алгоритмы на графах (часть 2)", 1)
P("В работе построены минимальное остовное дерево, независимое множество, раскраска, проверен баланс знакового графа и рассмотрены модели сложных сетей.")

task("Задание 1. Минимальное остовное дерево")
label("Формулировка.")
P("Для графа с рёбрами (A,B,4), (A,C,7), (A,D,3), (B,C,5), (B,D,2), (B,E,6), (C,D,5), (D,E,2), (D,F,1), (E,F,9) найти MST алгоритмами Краскала и Прима (старт из A). Веса должны совпасть.")
label("Ход решения.")
P("Краскал берёт рёбра по возрастанию веса и отбрасывает те, что замыкают цикл. Порядок: D-F (1), B-D (2), D-E (2), A-D (3). Ребро A-B (4) замыкает треугольник ABD и отбрасывается. Дальше B-C (5) присоединяет последнюю вершину C. Прим из A сначала берёт самое дешёвое ребро наружу — A-D, затем D-F, D-B, D-E и B-C. Набор рёбер тот же.")
img(W4 / "sam_1_graf.png", 13)
label("Результат.")
P("Рёбра дерева: D-F, B-D, D-E, A-D, B-C. Суммарный вес 1 + 2 + 2 + 3 + 5 = 13. У Краскала и Прима вес совпадает.")
img(W4 / "sam_1_mst.png", 13)

task("Задание 2. Независимое множество")
label("Формулировка.")
P("Жадно найти приближённое максимальное независимое множество. Связи: A с B, C, D; B с A, D, E; C с A, D, E; D с A, B, C, E; E с B, C, D, F; F только с E. На каждом шаге записывать степени.")
label("Ход решения.")
P("Берётся вершина наименьшей степени, она включается в множество, затем удаляются она и все её соседи. Старт: степени A=3, B=3, C=3, D=4, E=4, F=1. Минимум у F. После удаления F и E остаются A, B, C, D со степенями 3, 2, 2, 3. Берётся B, вместе с ней уходят A и D. Остаётся C.")
img(W4 / "sam_2_graf.png", 14)
label("Результат.")
P("Независимое множество {B, C, F}. Ни одна пара из этих вершин не соединена ребром. Размер 3, больше в этом графе взять нельзя.")
img(W4 / "sam_2_ind.png", 14)

task("Задание 3. Раскраска Вельша–Пауэлла")
label("Формулировка.")
P("Раскрасить вершины графа из задания 2 алгоритмом Вельша–Пауэлла и найти хроматическое число.")
label("Ход решения.")
P("Вершины упорядочены по убыванию степени: D, E, A, B, C, F. Каждой даётся наименьший цвет, которого нет у уже покрашенных соседей. D получает цвет 1, E — цвет 2, A не смежна с E и получает цвет 2. B смежна с цветами 1 и 2, ей нужен цвет 3. C тоже получает цвет 3. F смежна только с E и получает цвет 1.")
label("Результат.")
P("Раскраска: D и F — цвет 1, E и A — цвет 2, B и C — цвет 3. В графе есть треугольники, поэтому меньше трёх цветов не хватит. Хроматическое число χ(G) = 3.")
img(W4 / "sam_3_color.png", 14)

task("Задание 4. Знаковый граф")
label("Формулировка.")
P("Агенты 1–5, отношения (1,2,+), (1,3,−), (2,3,−), (2,4,+), (3,4,−), (4,5,−), (1,5,−). Проверить структурный баланс. Если граф балансен, разбить агентов на две коалиции.")
label("Ход решения.")
P("Цикл сбалансирован, если число минусов в нём чётно. Треугольники 1-2-3 и 2-3-4 содержат по два минуса. Циклы через вершину 5 также содержат чётное число минусов. Плюсовая цепочка 1-2-4 собирает одну коалицию, вершины 3 и 5 оказываются по другую сторону от всех своих соседей.")
img(W4 / "sam_4_graf.png", 13)
label("Результат.")
P("Граф структурно сбалансирован. Коалиция I: {1, 2, 4}. Коалиция II: {3, 5}. Внутри первой коалиции рёбра положительные, между коалициями — отрицательные.")
img(W4 / "sam_4_cycle.png", 13)

task("Задание 5. Модель малого мира")
label("Формулировка.")
P("Кольцо из N = 8 вершин, каждый узел соединён с k = 2 ближайшими соседями. Найти начальный диаметр, добавить две дальние связи и объяснить их роль.")
label("Ход решения.")
P("При k = 2 граф — цикл C8. Противоположная вершина достигается за 4 шага, это и есть диаметр. Чистое перенаправление при степени 2 снова даёт цикл и диаметр не уменьшает, поэтому для эффекта малого мира к кольцу добавлены две хорды: 1–5 и 3–7.")
img(W4 / "sam_5_ring.png", 11)
label("Результат.")
P("Начальный диаметр равен 4. После хорд 1–5 и 3–7 диаметр равен 3: путь между противоположными вершинами сокращается за счёт моста. В больших сетях такие дальние связи уменьшают среднее расстояние примерно до log N, а локальные соседства сохраняются.")
img(W4 / "sam_5_rewire.png", 11)

task("Задание повышенной трудности 1. Сеть Барабаши–Альберт")
label("Формулировка.")
P("Написать программу: старт с полного графа на m0 = 3 вершинах, затем N = 1000 новых вершин, каждая соединяется с m = 2 уже существующими с вероятностью, пропорциональной степени. Вывести степени пяти крупнейших хабов.")
label("Ход решения.")
P("Список ends хранит концы рёбер с повторениями: вершина встречается в нём столько раз, какова её степень. Новый узел выбирает две различные вершины случайно из этого списка, после чего оба конца дописываются. Так вероятность выбора пропорциональна степени.")
code("""
import random
from collections import Counter
random.seed(42)
m0, N, m = 3, 1000, 2
ends = []
for i in range(m0):
    for j in range(i + 1, m0):
        ends.extend([i, j])
for new in range(m0, m0 + N):
    chosen = set()
    while len(chosen) < m:
        chosen.add(random.choice(ends))
    for v in chosen:
        ends.extend([v, new])
for v, d in Counter(ends).most_common(5):
    print(f'узел {v}: степень {d}')
""")
label("Результат.")
P("При фиксированном seed = 42 программа даёт 1003 вершины и 2003 ребра. Крупнейшие хабы — стартовые узлы 0, 1 и 2: к ним новые вершины присоединяются чаще всего.")
img(FIG / "wb4_ba.png", 14)

task("Задание повышенной трудности 2. Регистры памяти")
label("Формулировка.")
P("Переменные x1–x6 несовместимы, если одновременно находятся в памяти. Свести задачу к раскраске и найти минимум ячеек. Несовместимости: x1 с x2, x3, x4; x2 с x1, x3, x5; x3 с x1, x2, x6; x4 с x1, x5, x6; x5 с x2, x4, x6; x6 с x3, x4, x5.")
label("Ход решения.")
P("Ребро графа означает «нужны разные ячейки». Есть треугольник x1-x2-x3, поэтому цветов не меньше трёх. Пары без ребра можно посадить в одну ячейку: {x1, x5}, {x2, x6}, {x3, x4}. Эти три множества не пересекаются и покрывают все переменные.")
img(W4 / "hard_2_graf.png", 13)
label("Результат.")
P("Минимум регистров равен 3. Ячейка 1: x1 и x5. Ячейка 2: x2 и x6. Ячейка 3: x3 и x4.")
img(W4 / "hard_2_color.png", 13)

# ===================== ПР 5 =====================
H("Практическая работа 5. DFS и BFS", 1)
P("Соседи в списках смежности идут по возрастанию номера или по алфавиту. От этого порядка зависит конкретная последовательность DFS и то, какой из одинаково коротких путей выберет BFS.")

task("Задание 1. Обход DFS и BFS")
label("Формулировка.")
P("Дан неориентированный граф на 10 вершинах. Выполнить DFS и BFS от вершины 1, сравнить порядки посещения.")
label("Ход решения.")
P("Сначала по рисунку составлен словарь смежности. DFS реализован рекурсией: алгоритм уходит в первого непосещённого соседа и возвращается только из тупика. BFS реализован очередью и помечает вершину при постановке в очередь, чтобы не посетить её дважды.")
img(W5 / "sam_1_graf.png", 12)
code("""
from collections import deque

graph = {
    1: [2, 3], 2: [1, 4, 5], 3: [1, 6, 7],
    4: [2, 8], 5: [2, 8], 6: [3, 9],
    7: [3, 9], 8: [4, 5, 10], 9: [6, 7, 10], 10: [8, 9],
}

def dfs(graph, vertex, visited=None):
    if visited is None:
        visited = []
    visited.append(vertex)
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

print('DFS:', dfs(graph, 1))
print('BFS:', bfs(graph, 1))
""")
label("Результат.")
img(FIG / "wb5_1.png", 14)
P("DFS идёт вглубь левой ветки и добирается до вершины 3 только снизу: 1-2-4-8-5-10-9-6-3-7. BFS выдаёт вершины по уровням удаления от 1. Посещены все 10 вершин. Разница в том, что DFS держит один текущий путь, а BFS обходит сразу всю волну соседей.")

task("Задание 2. Компоненты связности и двудольность")
label("Формулировка.")
P("Найти все компоненты связности с помощью DFS. Для каждой проверить двудольность BFS-раскраской. Если компонента двудольна — вывести цвета, если нет — объяснить почему.")
label("Ход решения.")
P("Запуск DFS из каждой ещё не посещённой вершины собирает одну компоненту. Двудольность проверяется раскраской в два цвета: сосед должен получить противоположный цвет. Совпадение цветов у концов ребра означает конфликт.")
img(W5 / "sam_2_graf.png", 15)
code("""
from collections import deque

graph = {
    'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B', 'D'], 'D': ['C'],
    'E': ['F'], 'F': ['E', 'G'], 'G': ['F'], 'H': [],
    'I': ['J', 'L'], 'J': ['I', 'K'], 'K': ['J', 'L'], 'L': ['I', 'K'],
}

def components(graph):
    visited, result = set(), []
    for start in graph:
        if start in visited:
            continue
        stack, comp = [start], []
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            comp.append(v)
            stack.extend(nb for nb in graph[v] if nb not in visited)
        result.append(comp)
    return result

def bipartite(graph, nodes):
    color, queue = {nodes[0]: 0}, deque([nodes[0]])
    while queue:
        v = queue.popleft()
        for nb in graph[v]:
            if nb not in color:
                color[nb] = 1 - color[v]
                queue.append(nb)
            elif color[nb] == color[v]:
                return False, None
    return True, color
""")
label("Результат.")
img(FIG / "wb5_2.png", 15)
P("Компоненты: {A, B, C, D}, {E, F, G}, {H}, {I, J, K, L}. Первая не двудольна: A, B и C образуют треугольник, двум цветам его не раскрасить. Цепочка E-F-G красится как 0, 1, 0. Изолированная H двудольна. Цикл I-J-K-L чётный, доли {I, K} и {J, L}.")
img(W5 / "sam_2_color.png", 15)

task("Задание 3. Топологическая сортировка и кратчайший путь")
label("Формулировка.")
P("Дан ориентированный ациклический граф. Выполнить топологическую сортировку с помощью DFS. Найти кратчайший по числу рёбер путь от A до H с помощью BFS.")
label("Ход решения.")
P("В топосортировке вершина записывается после всех своих потомков, затем список разворачивается. Для пути BFS запоминает предшественника в момент первого посещения, а сам путь восстанавливается от H назад к A.")
img(W5 / "sam_3_graf.png", 13)
code("""
from collections import deque

graph = {
    'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['E', 'F'],
    'D': ['G'], 'E': ['G', 'H'], 'F': ['G'], 'G': [], 'H': [],
}

def topological_sort(graph):
    visited, result = set(), []
    def dfs(v):
        visited.add(v)
        for nb in graph.get(v, []):
            if nb not in visited:
                dfs(nb)
        result.append(v)
    for v in graph:
        if v not in visited:
            dfs(v)
    return result[::-1]

def shortest_path(graph, start, goal):
    parent, queue = {start: None}, deque([start])
    while queue:
        v = queue.popleft()
        if v == goal:
            break
        for nb in graph[v]:
            if nb not in parent:
                parent[nb] = v
                queue.append(nb)
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

print(topological_sort(graph))
path = shortest_path(graph, 'A', 'H')
print(path, len(path) - 1)
""")
label("Результат.")
img(FIG / "wb5_3.png", 14)
P("Топологический порядок: A, C, F, B, E, H, D, G. Для каждой дуги начало стоит в этом списке раньше конца. Кратчайший путь A → B → E → H имеет длину 3. Второй путь той же длины — A → C → E → H. Короче нельзя: в H входит только дуга из E, а до E от A минимум два ребра. BFS выбирает первый путь, потому что B попадает в очередь раньше C.")
img(W5 / "sam_3_path.png", 14)

doc.save(OUT)
print("saved", OUT)
