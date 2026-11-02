#!/usr/bin/env python3
"""Build GRAPHICAL_ABSTRACT_FINAL.svg (2500x1000, 5:2 ratio) for the more-rice paper."""
import cairosvg, os

OUT = os.path.dirname(os.path.abspath(__file__))

# palette (color-blind friendly)
C_BG   = "#FFFFFF"
C_PANEL= "#F4F6F7"
C_LINE = "#4A5568"
C_TXT  = "#1A202C"
C_SUB  = "#4A5568"
C_BLUE = "#2B6CB0"   # observed / water
C_TEAL = "#2C7A7B"   # conditional
C_ORAN = "#C05621"   # modeled warning
C_GOLD = "#B7791F"   # wheat
C_GREEN= "#2F855A"   # rice
C_GRAY = "#718096"
C_RED  = "#C53030"

def txt(x, y, s, size=26, fill=C_TXT, anchor="middle", weight="normal", style=""):
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{style}>{s}</text>')

def rice_panicle(x, y, s=1.0, stroke=C_GREEN):
    """Simple rice panicle icon: stem + grains."""
    parts = [f'<g transform="translate({x},{y}) scale({s})" stroke="{stroke}" fill="{stroke}">',
             '<path d="M0,0 C0,-30 6,-52 14,-66" fill="none" stroke-width="4"/>']
    for dx, dy, r in [(14,-66,-25),(10,-56,-20),(17,-72,-32)]:
        parts.append(f'<ellipse cx="{dx}" cy="{dy}" rx="7" ry="16" transform="rotate({r} {dx} {dy})"/>')
    parts.append('</g>')
    return ''.join(parts)

def thermometer(x, y, s=1.0, stroke=C_BLUE):
    return (f'<g transform="translate({x},{y}) scale({s})" stroke="{stroke}" fill="none" stroke-width="4">'
            f'<rect x="-7" y="-60" width="14" height="50" rx="7"/>'
            f'<circle cx="0" cy="-2" r="11" fill="{stroke}"/>'
            f'<line x1="0" y1="-14" x2="0" y2="-50" stroke-width="5"/>'
            f'<line x1="8" y1="-45" x2="16" y2="-45"/><line x1="8" y1="-30" x2="16" y2="-30"/></g>')

def paddy(x, y, w=180, h=70):
    rows = ''.join(f'<line x1="{x}" y1="{y+i*h/4}" x2="{x+w}" y2="{y+i*h/4}" stroke="#90CDF4" stroke-width="2"/>' for i in range(1,4))
    seed = ''.join(rice_panicle(x+30+i*60, y+h-6, 0.45) for i in range(3))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#BEE3F8" stroke="{C_BLUE}" stroke-width="3"/>'
            f'{rows}{seed}')

def cloud_rain(x, y, s=1.0):
    drops = ''.join(f'<line x1="{x-26+i*20}" y1="{y+18*s}" x2="{x-32+i*20}" y2="{y+38*s}" stroke="{C_BLUE}" stroke-width="4"/>' for i in range(4))
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-45,10 a20,20 0 0,1 8,-38 a26,26 0 0,1 48,-6 a18,18 0 0,1 24,24 a14,14 0 0,1 -8,20 z" fill="#CBD5E0" stroke="{C_GRAY}" stroke-width="3"/>'
            f'</g>{drops}')

def soil_block(x, y, w=170, h=70, wet=True):
    col = "#9C6B30" if not wet else "#7B5A2E"
    plants = ''.join(f'<path d="M{x+30+i*55},{y} l0,-22 m0,0 l-9,-10 m9,10 l9,-10" stroke="{C_GREEN if wet else C_ORAN}" stroke-width="4" fill="none"/>' for i in range(3))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}" stroke="{C_LINE}" stroke-width="2.5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="6" fill="#68D391" opacity="0.55"/>{plants}')

def bar(x, y, w, h, fill, label=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{C_LINE}" stroke-width="2"/>'

def arrow(x1, y1, x2, y2, color=C_LINE, w=5):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#arr)"/>')

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="2500" height="1000" viewBox="0 0 2500 1000">')
svg.append('<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="%s"/></marker></defs>' % C_LINE)
svg.append(f'<rect width="2500" height="1000" fill="{C_BG}"/>')

# Title
svg.append(txt(1250, 52, "Rice diversification beyond traditional growing regions:", 40, weight="bold"))
svg.append(txt(1250, 96, "conditional feasibility requires cultivar, water and failure-pathway co-evaluation", 30, fill=C_SUB))

# Panel frames
pw, py, ph = 740, 130, 690
for i, label in enumerate(["1  Technology changes feasibility",
                            "2  Cultivation system sets water-failure pathways",
                            "3  Conditional food-supply resilience"]):
    px = 40 + i*(pw+40)
    svg.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{C_PANEL}" stroke="{C_LINE}" stroke-width="2.5"/>')
    svg.append(txt(px+pw/2, py+44, label, 28, weight="bold"))

# ---------- PANEL 1 ----------
px = 40
# climate-only screen -> fail
svg.append(thermometer(px+90, py+250, 1.1))
svg.append(txt(px+90, py+300, "climate-only", 22, fill=C_SUB))
svg.append(txt(px+90, py+326, "screen", 22, fill=C_SUB))
svg.append(txt(px+90, py+200, "✗", 40, fill=C_RED, weight="bold"))
svg.append(arrow(px+170, py+225, px+270, py+225))
# + management -> Hokkaido observed
svg.append(rice_panicle(px+330, py+250, 1.3))
svg.append(txt(px+345, py+300, "+ cultivar, nursery,", 21, fill=C_SUB))
svg.append(txt(px+345, py+324, "transplant, warm water", 21, fill=C_SUB))
svg.append(arrow(px+440, py+225, px+540, py+225))
svg.append(paddy(px+560, py+185, 160, 60))
svg.append(txt(px+640, py+290, "Hokkaido", 24, weight="bold", fill=C_BLUE))
svg.append(txt(px+640, py+316, "OBSERVED", 19, fill=C_BLUE, weight="bold"))
# GDD note
svg.append(f'<rect x="{px+40}" y="{py+360}" width="{pw-80}" height="110" rx="10" fill="#EBF4FA" stroke="{C_BLUE}" stroke-width="2"/>')
svg.append(txt(px+pw/2, py+402, "~900 GDD10 (Jun\u2013Sep)", 26, weight="bold", fill=C_BLUE))
svg.append(txt(px+pw/2, py+432, "system-specific observed lower bound", 20, fill=C_SUB))
svg.append(txt(px+pw/2, py+456, "not a universal threshold", 20, fill=C_SUB))
# EU hypothetical
svg.append(f'<rect x="{px+40}" y="{py+500}" width="{pw-80}" height="150" rx="10" fill="#FBF3E4" stroke="{C_GOLD}" stroke-width="2" stroke-dasharray="8,5"/>')
svg.append(txt(px+pw/2, py+540, "European candidate cells", 24, weight="bold", fill=C_GOLD))
svg.append(txt(px+pw/2, py+572, "(Rhine, Alsace, Loire, Saxony\u2026)", 19, fill=C_SUB))
svg.append(txt(px+pw/2, py+602, "hypothetical transfer \u2014 field", 20, fill=C_GOLD))
svg.append(txt(px+pw/2, py+628, "validation required", 20, fill=C_GOLD))

# ---------- PANEL 2 ----------
px = 40 + pw + 40
systems = [
    ("Irrigated lowland", C_TEAL, "conditional in Lower Danube \u2014",
     "delivery &amp; infrastructure, not discharge", "paddy"),
    ("Rainfed upland", C_ORAN, "modeled flowering moisture deficit",
     "88\u2013100% of yrs (continental EU cells)", "soil_dry"),
    ("Supplemental irrigation", C_BLUE, "less flooding, but critical-period",
     "water delivery still needed", "soil_wet"),
]
sy = py + 70
for name, col, l1, l2, kind in systems:
    svg.append(f'<rect x="{px+40}" y="{sy}" width="{pw-80}" height="168" rx="10" fill="#FFFFFF" stroke="{col}" stroke-width="2.5"/>')
    if kind == "paddy":
        svg.append(paddy(px+70, sy+28, 150, 58))
    elif kind == "soil_dry":
        svg.append(cloud_rain(px+120, sy+14, 0.8)); svg.append(soil_block(px+60, sy+92, 150, 58, wet=False))
    else:
        svg.append(cloud_rain(px+120, sy+14, 0.8)); svg.append(soil_block(px+60, sy+92, 150, 58, wet=True))
    svg.append(txt(px+460, sy+40, name, 25, weight="bold", fill=col))
    svg.append(txt(px+460, sy+95, l1, 20, fill=C_SUB))
    svg.append(txt(px+460, sy+122, l2, 20, fill=C_SUB))
    sy += 178
svg.append(txt(px+pw/2, sy+20, "deficits are modeled soil-moisture", 19, fill=C_GRAY))
svg.append(txt(px+pw/2, sy+46, "shortfalls, not observed crop failure", 19, fill=C_GRAY))

# ---------- PANEL 3 ----------
px = 40 + 2*(pw+40)
# wheat alone bar vs wheat+rice
svg.append(txt(px+150, py+90, "wheat alone", 22, fill=C_GOLD, weight="bold"))
svg.append(bar(px+60, py+110, 190, 60, C_GOLD))
svg.append(txt(px+155, py+147, "one crop, one failure mode", 17, fill="#5B4210"))
# drought arrow into it
svg.append(txt(px+150, py+230, "drought / shared shock", 20, fill=C_RED))
svg.append(arrow(px+150, py+250, px+150, py+300, C_RED))
svg.append(txt(px+150, py+335, "full exposure", 19, fill=C_RED))
# wheat + rice
svg.append(txt(px+560, py+90, "wheat + rice", 22, fill=C_GREEN, weight="bold"))
svg.append(bar(px+450, py+110, 110, 60, C_GOLD))
svg.append(bar(px+560, py+110, 110, 60, C_GREEN))
svg.append(txt(px+505, py+147, "wheat", 17, fill="#5B4210"))
svg.append(txt(px+615, py+147, "rice", 17, fill="#fff"))
svg.append(txt(px+560, py+230, "same shock \u2192 different pathways", 20, fill=C_TEAL))
svg.append(arrow(px+560, py+250, px+560, py+300, C_TEAL))
svg.append(txt(px+560, py+335, "only if joint failure", 19, fill=C_TEAL))
svg.append(txt(px+560, py+358, "dependence is low", 19, fill=C_TEAL))
# scenario numbers box
svg.append(f'<rect x="{px+60}" y="{py+400}" width="{pw-120}" height="150" rx="10" fill="#EDF7F0" stroke="{C_TEAL}" stroke-width="2"/>')
svg.append(txt(px+pw/2, py+438, "modeled severe-shortfall scenarios", 21, weight="bold", fill=C_TEAL))
svg.append(txt(px+pw/2, py+472, "Romania 20.3% \u2192 10.9%", 23, fill=C_TXT))
svg.append(txt(px+pw/2, py+504, "Kazakhstan 21.2% \u2192 3.0%", 23, fill=C_TXT))
svg.append(txt(px+pw/2, py+532, "scenario outcomes, not observed famine", 17, fill=C_GRAY))
svg.append(txt(px+pw/2, py+600, "non-rice comparators can win:", 20, fill=C_SUB))
svg.append(txt(px+pw/2, py+628, "Serbia \u2014 potato outperforms rice", 20, fill=C_SUB))

# ---------- CONCLUSION STRIP ----------
sy = py + ph + 25
svg.append(f'<rect x="40" y="{sy}" width="2420" height="120" rx="14" fill="#EDF2F7" stroke="{C_LINE}" stroke-width="2.5"/>')
svg.append(txt(1250, sy+48, "Feasibility + reliable water delivery + independent failure pathways \u2192 conditional resilience.", 27, weight="bold"))
svg.append(txt(1250, sy+86, "Potential field trials at selected irrigated sites only. No universal rice-expansion claim. Diversification of crops \u2260 diversification of failure modes.", 21, fill=C_SUB))

# ---------- LEGEND ----------
ly = sy + 140
items = [(C_BLUE, "observed evidence"), (C_ORAN, "modeled estimate"), (C_GOLD, "hypothetical transfer")]
lx = 620
for col, lab in items:
    svg.append(f'<rect x="{lx}" y="{ly-20}" width="26" height="26" rx="5" fill="{col}"/>')
    svg.append(txt(lx+40, ly+2, lab, 22, fill=C_SUB, anchor="start"))
    lx += 400
svg.append('</svg>')

src = ''.join(svg)
svg_path = os.path.join(OUT, "GRAPHICAL_ABSTRACT_FINAL.svg")
with open(svg_path, "w") as f:
    f.write(src)

cairosvg.svg2png(bytestring=src.encode(), write_to=os.path.join(OUT, "GRAPHICAL_ABSTRACT_FINAL.png"),
                 output_width=2656, output_height=1062)
cairosvg.svg2png(bytestring=src.encode(), write_to=os.path.join(OUT, "GRAPHICAL_ABSTRACT_PREVIEW.png"),
                 output_width=664, output_height=266)
print("wrote", svg_path)
