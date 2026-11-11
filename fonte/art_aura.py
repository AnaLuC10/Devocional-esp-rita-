"""Tema 'aura': visual clean, degradês suaves no lugar das ilustrações."""

def svg(w, h, body, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

# variações de aura (posições das manchas) para dar ritmo sem repetir
AURAS = [
    ('15% 20%', '85% 35%', '45% 95%'),
    ('80% 15%', '10% 60%', '70% 90%'),
    ('30% 85%', '90% 70%', '20% 10%'),
    ('60% 10%', '5% 40%', '95% 95%'),
    ('10% 90%', '75% 25%', '40% 40%'),
    ('90% 85%', '25% 20%', '55% 60%'),
]

def aura_css(k=0, strength=1.0):
    a, b, c = AURAS[k % len(AURAS)]
    s = strength
    return (f"background:"
            f"radial-gradient(circle at 50% 50%, rgba(255,255,255,{.55*s:.2f}) 0, transparent 32%),"
            f"radial-gradient(circle at {a}, rgba(240,150,178,{1*s:.2f}) 0, transparent 62%),"
            f"radial-gradient(circle at {b}, rgba(178,152,232,{1*s:.2f}) 0, transparent 62%),"
            f"radial-gradient(circle at {c}, rgba(247,184,150,{1*s:.2f}) 0, transparent 62%),"
            f"#EFD9E4;")

def mini(kind, seed=0):
    return ''

def divider(seed=0):
    return '<div class="divider"><span></span><i></i><span></span></div>'

def corner_spray(seed=1, mirror=False):
    return ''

def part_art(n):
    return ''

def cover_art():
    return ''

def icon(kind):
    col = {'flor': '#E79AB0', 'livro': '#A893D6', 'fone': '#F2B79A', 'nota': '#C9A3E3', 'biblia': '#D8A2C4'}.get(kind, '#E79AB0')
    return f'<span class="dotc" style="background:{col}"></span>'
