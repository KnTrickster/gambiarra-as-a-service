"""Cores, fontes e CSS do Prisma. Mexa aqui para mudar o visual."""

# nome na barra lateral -> (cor de fundo, cor do texto)
THEMES = {
    "Suave (creme)": ("#FAF6E9", "#1A1A1A"),
    "Alto (preto/branco)": ("#FFFFFF", "#000000"),
    "Escuro": ("#121212", "#F2F2F2"),
}

# fontes disponíveis (as duas primeiras vêm do Google Fonts)
FONTS = ["Atkinson Hyperlegible", "Lexend", "Arial"]

GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700"
    "&family=Lexend:wght@400;600&display=swap"
)


def build_css(font, size, line_height, letter_spacing, theme_name):
    bg, fg = THEMES[theme_name]
    return f"""<style>
@import url('{GOOGLE_FONTS_URL}');
.block-container p, .block-container li {{ font-family:'{font}',sans-serif; font-size:{size}px;
  line-height:{line_height}; letter-spacing:{letter_spacing}em; max-width:68ch; }}
.block-container {{ background:{bg}; color:{fg}; }}
.block-container p, .block-container li, .block-container h1,
.block-container h2, .block-container h3 {{ color:{fg}; }}
</style>"""
