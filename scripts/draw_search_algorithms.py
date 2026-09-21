"""Draw the search algorithms of lecture 2 in the style of the course.

    uv run python scripts/draw_search_algorithms.py

Writes the algorithm listings of lectures 2, 3 and 4 as SVG, replacing the screenshots taken
from Russell and Norvig. The listings are the ones of the exercise sheets
(`exercises/exercises.sty`, `pseudocode` environment): keywords in bold, procedure names in
small capitals, variables in italics, each in its own colour. Roboto and the KaTeX faces are embedded from
`assets/fonts/`, since an SVG shown as an image cannot load fonts from the page.

Tokens of a line are sibling `<tspan>` elements inside one `<text>`, so that the renderer
advances the horizontal position itself and no font metric has to be guessed here.
"""

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

BLUE = "#356aaf"      # keywords
TEAL = "#2e7d73"      # procedure names
INK = "#2a2a2a"       # variables
GREY = "#6b6b6b"      # prose and punctuation

SIZE = 21           # body size
LINE = 1.65 * SIZE  # line height
INDENT = 1.7 * SIZE
MARGIN = 10

FACES = [("Roboto", 400, "normal", "Roboto-400-latin"),
         ("Roboto", 900, "normal", "Roboto-900-latin"),
         ("KaTeXItalic", 400, "normal", "KaTeX_Main-Italic"),
         ("KaTeXMain", 400, "normal", "KaTeX_Main-Regular"),
         ("KaTeXMathItalic", 400, "normal", "KaTeX_Math-Italic")]


def fonts(used):
    """Embed the faces a listing actually uses, and no others."""
    faces = []
    for family, weight, style, name in FACES:
        if family not in used:
            continue
        path = ROOT / "assets" / "fonts" / f"{name}.woff2"
        data = base64.b64encode(path.read_bytes()).decode()
        faces.append(f"@font-face {{ font-family: '{family}'; font-weight: {weight}; font-style: {style}; "
                     f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")
    return "<style>" + " ".join(faces) + "</style>"


def span(text, family="Roboto", weight=400, size=SIZE, fill=INK):
    return (f'<tspan font-family="{family}, sans-serif" font-weight="{weight}" font-size="{size:g}" '
            f'fill="{fill}">{escape(text)}</tspan>')


def kw(word):
    """A keyword, as \\kw{...} on the sheets."""
    return span(word, weight=900, fill=BLUE)


def proc(name):
    """A procedure name in small capitals, as \\proc{...} on the sheets."""
    out = ""
    for word in name.split("-"):
        if out:
            out += span("-", fill=TEAL)
        out += span(word[0].upper(), fill=TEAL) + span(word[1:].upper(), size=SIZE * 0.78, fill=TEAL)
    return out


def var(name):
    """A variable in italics, as \\pvar{...} on the sheets."""
    return span(name, family="KaTeXItalic", fill=INK)


def txt(words):
    return span(words, fill=GREY)


def gets():
    return span(" ← ", family="KaTeXMain", fill=INK)


def sym(text):
    """A mathematical symbol, from the KaTeX faces (∞, ≥, ≤)."""
    return span(text, family="KaTeXMain", fill=INK)


def greek(letter):
    """A Greek variable, italic as on the slides (KaTeX_Main-Italic has none)."""
    return span(letter, family="KaTeXMathItalic", fill=INK)


def line(level, tokens, y):
    x = MARGIN + level * INDENT
    return (f'<text x="{x:g}" y="{y:g}" xml:space="preserve">' + "".join(tokens) + "</text>")


def listing(name, lines, width, lecture="lec2"):
    height = MARGIN + len(lines) * LINE
    body = "".join(line(level, tokens, MARGIN + (i + 0.8) * LINE) for i, (level, tokens) in enumerate(lines))
    used = {family for family, *_ in FACES if f'font-family="{family},' in body}
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:g}" width="{width}" '
           f'height="{height:g}"><defs>{fonts(used)}</defs>{body}</svg>\n')
    out = ROOT / "figures" / lecture / f"{name}.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {width}x{height:g}")


HEADER = [kw("function "), proc("Graph-Search"), txt("("), var("problem"), txt(", "), var("fringe"), txt(") "),
          kw("returns "), txt("a solution, or failure")]

INSERT_FRINGE = [var("fringe"), gets(), proc("Insert"), txt("("), proc("Make-Node"), txt("("), proc("Initial-State"),
                 txt("["), var("problem"), txt("]), "), var("fringe"), txt(")")]
POP = [var("node"), gets(), proc("Remove-Front"), txt("("), var("fringe"), txt(")")]
EMPTY = [kw("if "), var("fringe"), txt(" is empty "), kw("then return "), txt("failure")]
GOAL = [kw("if "), proc("Goal-Test"), txt("("), var("problem"), txt(", "), proc("State"), txt("["), var("node"),
        txt("]) "), kw("then return "), var("node")]
EXPAND = [var("fringe"), gets(), proc("InsertAll"), txt("("), proc("Expand"), txt("("), var("node"), txt(", "),
          var("problem"), txt("), "), var("fringe"), txt(")")]

tree = [
    (0, [kw("function "), proc("Tree-Search"), txt("("), var("problem"), txt(", "), var("fringe"), txt(") "),
         kw("returns "), txt("a solution, or failure")]),
    (1, INSERT_FRINGE),
    (1, [kw("loop do")]),
    (2, EMPTY),
    (2, POP),
    (2, GOAL),
    (2, EXPAND),
]

graph = [
    (0, HEADER),
    (1, [var("closed"), gets(), txt("an empty set")]),
    (1, INSERT_FRINGE),
    (1, [kw("loop do")]),
    (2, EMPTY),
    (2, POP),
    (2, GOAL),
    (2, [kw("if "), proc("State"), txt("["), var("node"), txt("] is not in "), var("closed"), txt(" "), kw("then")]),
    (3, [txt("add "), proc("State"), txt("["), var("node"), txt("] to "), var("closed")]),
    (3, EXPAND),
    (1, [kw("end")]),
]

# Figure 3.1 of Russell and Norvig, without the caption of the book
simple = [
    (0, [kw("function "), proc("Simple-Problem-Solving-Agent"), txt("("), var("percept"), txt(") "),
         kw("returns "), txt("an action")]),
    (1, [kw("persistent"), txt(": "), var("seq"), txt(", an action sequence, initially empty")]),
    (2.6, [var("state"), txt(", some description of the current world state")]),
    (2.6, [var("goal"), txt(", a goal, initially null")]),
    (2.6, [var("problem"), txt(", a problem formulation")]),
    (0, []),
    (1, [var("state"), gets(), proc("Update-State"), txt("("), var("state"), txt(", "), var("percept"), txt(")")]),
    (1, [kw("if "), var("seq"), txt(" is empty "), kw("then")]),
    (2, [var("goal"), gets(), proc("Formulate-Goal"), txt("("), var("state"), txt(")")]),
    (2, [var("problem"), gets(), proc("Formulate-Problem"), txt("("), var("state"), txt(", "), var("goal"), txt(")")]),
    (2, [var("seq"), gets(), proc("Search"), txt("("), var("problem"), txt(")")]),
    (2, [kw("if "), var("seq"), txt(" = "), var("failure"), txt(" "), kw("then return "), txt("a null action")]),
    (1, [var("action"), gets(), proc("First"), txt("("), var("seq"), txt(")")]),
    (1, [var("seq"), gets(), proc("Rest"), txt("("), var("seq"), txt(")")]),
    (1, [kw("return "), var("action")]),
]

# Monte Carlo tree search, as lecture 3 describes it: selection by UCB1, one expansion,
# a random playout, then backpropagation along the path
mcts = [
    (0, [kw("function "), proc("MCTS"), txt("("), var("state"), txt(", "), var("budget"), txt(") "),
         kw("returns "), txt("an action")]),
    (1, [var("root"), gets(), proc("Make-Node"), txt("("), var("state"), txt(")")]),
    (1, [kw("while "), txt("time remains in "), var("budget"), kw(" do")]),
    (2, [var("n"), gets(), proc("Select"), txt("("), var("root"), txt(")")]),
    (2, [var("n'"), gets(), proc("Expand"), txt("("), var("n"), txt(")")]),
    (2, [var("reward"), gets(), proc("Simulate"), txt("("), var("n'"), txt(")")]),
    (2, [proc("Backpropagate"), txt("("), var("n'"), txt(", "), var("reward"), txt(")")]),
    (1, [kw("end")]),
    (1, [kw("return "), txt("the action leading to the child of "), var("root"), txt(" with the largest "),
         var("N")]),
    (0, []),
    (0, [kw("function "), proc("Select"), txt("("), var("n"), txt(") "), kw("returns "), txt("a node to expand")]),
    (1, [kw("while "), var("n"), txt(" is fully expanded and not terminal "), kw("do")]),
    (2, [var("n"), gets(), txt("the child of "), var("n"), txt(" maximising "), proc("UCB1")]),
    (1, [kw("end")]),
    (1, [kw("return "), var("n")]),
]

# Figure 5.7 of Russell and Norvig, without the caption of the book. The book
# writes Result(s, a) here, where s is the state of the enclosing call; it is
# spelled out as Result(state, a) so that the listing reads on its own.
alpha_beta = [
    (0, [kw("function "), proc("Alpha-Beta-Search"), txt("("), var("state"), txt(") "),
         kw("returns "), txt("an action")]),
    (1, [var("v"), gets(), proc("Max-Value"), txt("("), var("state"), txt(", "), sym("−∞"), txt(", "),
         sym("+∞"), txt(")")]),
    (1, [kw("return "), txt("the "), var("action"), txt(" in "), proc("Actions"), txt("("), var("state"),
         txt(") with value "), var("v")]),
    (0, []),
    (0, [kw("function "), proc("Max-Value"), txt("("), var("state"), txt(", "), greek("α"), txt(", "),
         greek("β"), txt(") "), kw("returns "), txt("a utility value")]),
    (1, [kw("if "), proc("Terminal-Test"), txt("("), var("state"), txt(") "), kw("then return "),
         proc("Utility"), txt("("), var("state"), txt(")")]),
    (1, [var("v"), gets(), sym("−∞")]),
    (1, [kw("for each "), var("a"), txt(" in "), proc("Actions"), txt("("), var("state"), txt(") "), kw("do")]),
    (2, [var("v"), gets(), proc("Max"), txt("("), var("v"), txt(", "), proc("Min-Value"), txt("("),
         proc("Result"), txt("("), var("state"), txt(", "), var("a"), txt("), "), greek("α"), txt(", "),
         greek("β"), txt("))")]),
    (2, [kw("if "), var("v"), txt(" "), sym("≥"), txt(" "), greek("β"), txt(" "), kw("then return "), var("v")]),
    (2, [greek("α"), gets(), proc("Max"), txt("("), greek("α"), txt(", "), var("v"), txt(")")]),
    (1, [kw("return "), var("v")]),
    (0, []),
    (0, [kw("function "), proc("Min-Value"), txt("("), var("state"), txt(", "), greek("α"), txt(", "),
         greek("β"), txt(") "), kw("returns "), txt("a utility value")]),
    (1, [kw("if "), proc("Terminal-Test"), txt("("), var("state"), txt(") "), kw("then return "),
         proc("Utility"), txt("("), var("state"), txt(")")]),
    (1, [var("v"), gets(), sym("+∞")]),
    (1, [kw("for each "), var("a"), txt(" in "), proc("Actions"), txt("("), var("state"), txt(") "), kw("do")]),
    (2, [var("v"), gets(), proc("Min"), txt("("), var("v"), txt(", "), proc("Max-Value"), txt("("),
         proc("Result"), txt("("), var("state"), txt(", "), var("a"), txt("), "), greek("α"), txt(", "),
         greek("β"), txt("))")]),
    (2, [kw("if "), var("v"), txt(" "), sym("≤"), txt(" "), greek("α"), txt(" "), kw("then return "), var("v")]),
    (2, [greek("β"), gets(), proc("Min"), txt("("), greek("β"), txt(", "), var("v"), txt(")")]),
    (1, [kw("return "), var("v")]),
]

# Inference by enumeration over the full joint distribution, as lecture 4 states it:
# fix the evidence, sum the hidden variables out, normalize
enumeration = [
    (0, [kw("function "), proc("Enumeration-Ask"), txt("("), var("Q"), txt(", "), var("e"), txt(", "),
         var("P"), txt(") "), kw("returns "), txt("a distribution over "), var("Q")]),
    (1, [var("b"), gets(), txt("an empty table over the values of "), var("Q")]),
    (1, [kw("for each "), txt("value "), var("q"), txt(" of "), var("Q"), txt(" "), kw("do")]),
    (2, [var("b"), txt("["), var("q"), txt("] "), gets(), txt("the sum of "), var("P"), txt("("), var("q"),
         txt(", "), var("h"), txt(", "), var("e"), txt(") over the assignments "), var("h")]),
    (1, [var("Z"), gets(), txt("the sum of "), var("b"), txt("["), var("q"), txt("] over the values "), var("q")]),
    (1, [kw("return "), var("b"), txt(" / "), var("Z")]),
]

if __name__ == "__main__":
    listing("tree-search", tree, 840)
    listing("graph-search", graph, 840)
    listing("problem-solving-agent", simple, 960)
    listing("mcts", mcts, 1000, lecture="lec3")
    listing("alpha-beta-search", alpha_beta, 1000, lecture="lec3")
    listing("enumeration", enumeration, 840, lecture="lec5")
