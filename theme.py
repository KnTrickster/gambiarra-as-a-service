"""Cores, fontes e CSS do Prisma. Mexa aqui para mudar o visual."""

# nome na barra lateral -> (cor de fundo, cor do texto)
# nome na barra lateral -> (fundo da página, texto, superfície dos componentes, destaque)
THEMES = {
    "Suave (creme)": ("#FAF6E9", "#1A1A1A", "#EFE7CF", "#7A5C00"),
    "Alto (preto/branco)": ("#FFFFFF", "#000000", "#EAF1FF", "#003399"),
    "Escuro": ("#121212", "#F2F2F2", "#1E2A3A", "#6CB4FF"),
}

# fontes disponíveis (as duas primeiras vêm do Google Fonts)
FONTS = ["Atkinson Hyperlegible", "Lexend", "Arial"]

GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700"
    "&family=Lexend:wght@400;600&display=swap"
)


def build_css(font, size, line_height, letter_spacing, theme_name):
    bg, fg, surface, accent = THEMES[theme_name]
    return f"""<style>
@import url('{GOOGLE_FONTS_URL}');
.block-container p, .block-container li {{ font-family:'{font}',sans-serif; font-size:{size}px;
  line-height:{line_height}; letter-spacing:{letter_spacing}em; max-width:68ch; }}
.block-container {{ background:{bg}; color:{fg}; }}
.block-container p, .block-container li, .block-container h1,
.block-container h2, .block-container h3 {{ color:{fg}; }}
.block-container button {{ background:{surface} !important; border:1px solid {accent} !important; }}
.block-container button * {{ color:{fg} !important; }}
[data-testid="stFileUploader"] section {{ background:{surface} !important; border:1px solid {accent} !important; }}
[data-testid="stFileUploader"] section * {{ color:{fg} !important; }}
[data-testid="stAlert"] {{ background:{surface} !important; border:2px solid {accent}; border-radius:8px; }}
[data-testid="stAlert"] * {{ background:transparent !important; color:{fg} !important; }}
[data-testid="stAlert"] svg {{ fill:{accent} !important; }}
[data-testid="stHeader"] {{ background:{bg} !important; }}
[data-testid="stHeader"] * {{ color:{fg} !important; }}
[data-testid="stSidebar"] {{ background:{surface} !important; border-right:1px solid {accent}; }}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{ color:{fg} !important; }}
[data-testid="stHeader"] {{ background:{bg} !important; border-bottom:1px solid {accent}; }}
[data-testid="stTextArea"] textarea {{ background:{surface} !important; color:{fg} !important;
  caret-color:{fg}; border:1px solid {accent} !important; }}
[data-testid="stTextArea"] textarea::placeholder {{ color:{fg}; opacity:0.6; }}
[data-testid="stTextArea"] label p {{ color:{fg} !important; }}
[data-baseweb="select"] > div {{ background:{surface} !important; border:1px solid {accent} !important; }}
[data-baseweb="select"] * {{ color:{fg} !important; }}
[data-baseweb="popover"] ul {{ background:{surface} !important; }}
[data-baseweb="popover"] li, [data-baseweb="popover"] li * {{ color:{fg} !important; }}
</style>"""
