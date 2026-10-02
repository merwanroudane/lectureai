"""
مكتبة الرسوم المتحركة (SVG + CSS) الخاصّة بالمنصّة.
Animated SVG diagram library — pure CSS/SMIL, no JavaScript.

كل الرسوم بألوان فاتحة ومشرقة، ومصمّمة لتُقرأ من اليمين إلى اليسار.

Author: Dr Merwan Roudane
"""

from __future__ import annotations

import html as _html
import re

import streamlit as st

# ======================================================================
#  CSS العام للرسوم المتحركة — يُحقن مرّة واحدة
# ======================================================================
_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Cairo:wght@400;600;700;800&family=Tajawal:wght@700;800&"
    'family=JetBrains+Mono:wght@400;600&display=swap">'
)

_ANIM_CSS = """
<style>
* { box-sizing: border-box; }
html, body { margin:0; padding:0; background:transparent; overflow:hidden; }
.mra-frame {
    position: relative; margin: 0; padding: 14px 14px 10px;
    border-radius: 20px; border: 1px solid #E2E8FA;
    background: linear-gradient(160deg, #FCFDFF 0%, #F5F8FF 55%, #F3FBF8 100%);
    box-shadow: 0 14px 34px -28px rgba(50,70,160,.6);
    animation: mraFadeUp .6s cubic-bezier(.22,.9,.3,1) both;
}
@keyframes mraFadeUp { from { opacity:0; transform:translateY(12px);} to { opacity:1; transform:none; } }
.mra-frame svg { display: block; width: 100%; max-width: 800px; height: auto;
                 margin: 0 auto; overflow: visible; }
.mra-cap {
    margin-top: 8px; padding-top: 8px; border-top: 1px dashed #DDE5F7;
    font-size: .86rem; color: #5B6894; text-align: center; line-height: 1.8;
}
.mra-cap span { display: block; direction: ltr; font-size: .72rem; color: #96A1C0;
                font-family: 'JetBrains Mono', monospace; letter-spacing: .3px; }

/* ---------- حركات عامة ---------- */
@keyframes mraFlow     { to   { stroke-dashoffset: -120; } }
@keyframes mraFlowBack { to   { stroke-dashoffset:  120; } }
@keyframes mraDraw     { to   { stroke-dashoffset: 0; } }
@keyframes mraPulse    { 0%,100% { opacity:.45; transform:scale(1); }
                         50%     { opacity:1;   transform:scale(1.16); } }
@keyframes mraBreathe  { 0%,100% { opacity:.25; } 50% { opacity:.75; } }
@keyframes mraFloatY   { 0%,100% { transform: translateY(0); }
                         50%     { transform: translateY(-7px); } }
@keyframes mraSpin     { to { transform: rotate(360deg); } }
@keyframes mraPop      { 0% { opacity:0; transform:scale(.6);} 60% { transform:scale(1.08);} 100%{opacity:1;transform:scale(1);} }
@keyframes mraBlink    { 0%,45% { opacity:0; } 55%,100% { opacity:1; } }
@keyframes mraSlideIn  { from { opacity:0; transform: translateX(26px);} to { opacity:1; transform:none; } }
@keyframes mraWidth    { from { transform: scaleX(0); } to { transform: scaleX(1); } }

.mra-flow   { stroke-dasharray: 9 11; animation: mraFlow 2.2s linear infinite; }
.mra-flow-s { stroke-dasharray: 7 9;  animation: mraFlow 3.4s linear infinite; }
.mra-back   { stroke-dasharray: 9 11; animation: mraFlowBack 2.6s linear infinite; }
.mra-pulse  { animation: mraPulse 2.4s ease-in-out infinite; transform-origin: center; }
.mra-breathe{ animation: mraBreathe 3.6s ease-in-out infinite; }
.mra-float  { animation: mraFloatY 3.2s ease-in-out infinite; }
.mra-pop    { animation: mraPop .7s cubic-bezier(.2,.9,.3,1.3) both; }
.mra-blink  { animation: mraBlink 3s ease-in-out infinite alternate; }
.mra-slide  { animation: mraSlideIn .7s cubic-bezier(.2,.9,.3,1) both; }

/* داخل مستند RTL ينقلب معنى text-anchor، فنثبّت الاتّجاه المنطقي للنصّ في SVG
   مع عزل ثنائي الاتّجاه حتّى تبقى الحروف العربية مرتّبة ترتيبها الصحيح. */
.mra-frame svg text { direction: ltr; unicode-bidi: isolate; }

.mra-b  { font-weight: 800; }          /* بديل <b> داخل SVG */
.mra-t  { font-family:'Cairo', sans-serif; font-size:13px; font-weight:700; fill:#2F3D66; }
.mra-ts { font-family:'Cairo', sans-serif; font-size:11px; font-weight:600; fill:#6B7AA8; }
.mra-te { font-family:'JetBrains Mono', monospace; font-size:9.5px; font-weight:600;
          fill:#9AA5C4; letter-spacing:.2px; direction:ltr; }
.mra-tb { font-family:'Tajawal', sans-serif; font-size:15px; font-weight:800; fill:#24325C; }
.mra-m  { font-family:'JetBrains Mono', monospace; font-size:11px; fill:#4B5B8C; }
</style>
"""


def inject_anim_css() -> None:
    """يزيل الحشو الافتراضي حول الإطارات المدمجة (iframes)."""
    st.html(
        """<style>
[data-testid="stIFrame"] { border: none !important; background: transparent !important;
                           color-scheme: normal; }
[data-testid="stIFrame"] iframe { border: none !important; background: transparent !important; }
</style>"""
    )


_DESIGN_W = 800          # أقصى عرض للرسم داخل الإطار (بالبكسل)
_FRAME_PAD = 22          # الحشو العلوي والسفلي للإطار
_CAP_LINE = 26           # ارتفاع السطر الواحد في التعليق
_CAP_CHARS = 58          # عدد الحروف العربية التي تسع السطر الواحد تقريبًا


def _svg_height(svg: str) -> int:
    """يحسب الارتفاع المعروض للرسم انطلاقًا من viewBox وعرض التصميم."""
    m = re.search(r'viewBox="\s*[\d.+-]+\s+[\d.+-]+\s+([\d.]+)\s+([\d.]+)', svg)
    if not m:
        return 320
    w, h = float(m.group(1)), float(m.group(2))
    return int(round(_DESIGN_W * h / w))


def _caption_height(caption: str, en: str) -> int:
    if not caption:
        return 0
    plain = re.sub(r"<[^>]+>", "", caption)
    lines = max(1, -(-len(plain) // _CAP_CHARS))
    return 20 + lines * _CAP_LINE + (18 if en else 0)


def frame(svg: str, caption: str = "", en: str = "") -> None:
    """
    يعرض رسمًا متحرّكًا داخل إطار مستقلّ.

    نستعمل ``st.iframe`` لأنّ ``st.html`` يُعقّم وسوم SVG ويحذفها،
    بينما يسمح الإطار المدمج بكامل إمكانات SVG وحركات CSS والخطوط العربية.
    الارتفاع يُحسب صراحةً من ``viewBox`` لتفادي القياس التلقائي غير المستقرّ.
    """
    cap = ""
    if caption:
        sub = f"<span>{_html.escape(en)}</span>" if en else ""
        cap = f'<div class="mra-cap">{caption}{sub}</div>'
    doc = (
        '<!doctype html><html dir="rtl" lang="ar"><head><meta charset="utf-8">'
        f"{_FONT_LINK}{_ANIM_CSS}</head><body>"
        f'<div class="mra-frame">{svg}{cap}</div></body></html>'
    )
    height = _svg_height(svg) + _FRAME_PAD + _caption_height(caption, en)
    st.iframe(doc, height=height)


# ======================================================================
#  أدوات مساعدة
# ======================================================================
_DEFS = """
<defs>
  <linearGradient id="gIndigo" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#EDF1FF"/><stop offset="100%" stop-color="#DCE4FF"/></linearGradient>
  <linearGradient id="gTeal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#EAFBF5"/><stop offset="100%" stop-color="#D5F4E9"/></linearGradient>
  <linearGradient id="gAmber" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#FFF7E8"/><stop offset="100%" stop-color="#FFEBCF"/></linearGradient>
  <linearGradient id="gRose" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#FFF1F4"/><stop offset="100%" stop-color="#FFE0E7"/></linearGradient>
  <linearGradient id="gViolet" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#F7F2FF"/><stop offset="100%" stop-color="#EBE1FF"/></linearGradient>
  <linearGradient id="gSky" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#EEF6FF"/><stop offset="100%" stop-color="#D9EBFF"/></linearGradient>
  <marker id="arrI" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#8192EC"/></marker>
  <marker id="arrT" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#5CC6A4"/></marker>
  <marker id="arrA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#EBA85A"/></marker>
  <marker id="arrR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#EE8A9C"/></marker>
</defs>
"""

_FILL = {
    "indigo": ("url(#gIndigo)", "#B9C4F4", "#3A4BBF"),
    "teal": ("url(#gTeal)", "#A9E0CC", "#1E8E6A"),
    "amber": ("url(#gAmber)", "#F3D6A6", "#B9772A"),
    "rose": ("url(#gRose)", "#F6C3CE", "#C24A5E"),
    "violet": ("url(#gViolet)", "#D8C6F6", "#7149C6"),
    "sky": ("url(#gSky)", "#AFD3F6", "#2B6FC4"),
    "mint": ("url(#gTeal)", "#BFE7C8", "#2D8B47"),
    "sand": ("url(#gAmber)", "#E4D9C6", "#8C7445"),
}


def _box(x, y, w, h, label, en="", t="indigo", delay=0.0, rx=14, fs=13):
    fill, stroke, ink = _FILL[t]
    sub = (
        f'<text x="{x + w / 2}" y="{y + h / 2 + 15}" class="mra-te" text-anchor="middle">{_html.escape(en)}</text>'
        if en
        else ""
    )
    dy = -4 if en else 5
    return f"""<g class="mra-pop" style="animation-delay:{delay:.2f}s">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>
  <text x="{x + w / 2}" y="{y + h / 2 + dy}" text-anchor="middle"
        style="font-family:'Cairo',sans-serif;font-size:{fs}px;font-weight:800;fill:{ink}">{_html.escape(label)}</text>
  {sub}</g>"""


def split2(text: str, around: int) -> tuple[str, str]:
    """يقسم النصّ إلى سطرين عند أقرب مسافة من الموضع المطلوب (لا يقطع كلمة)."""
    if len(text) <= around:
        return text, ""
    left = text.rfind(" ", 0, around + 1)
    right = text.find(" ", around)
    cut = left if left != -1 and (right == -1 or around - left <= right - around) else right
    if cut == -1:
        return text, ""
    return text[:cut].strip(), text[cut + 1:].strip()


def _node(cx, cy, r, label, t="indigo", delay=0.0, fs=12):
    fill, stroke, ink = _FILL[t]
    return f"""<g class="mra-pop" style="animation-delay:{delay:.2f}s">
  <circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="{stroke}" opacity=".22" class="mra-breathe"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>
  <text x="{cx}" y="{cy + 4}" text-anchor="middle"
        style="font-family:'Cairo',sans-serif;font-size:{fs}px;font-weight:800;fill:{ink}">{_html.escape(label)}</text>
</g>"""


# ======================================================================
#  1 — حلقة التعلّم الأساسية
# ======================================================================
def learning_loop() -> str:
    nodes = [
        (120, 70, "البيانات", "amber"),
        (330, 70, "النموذج", "indigo"),
        (540, 70, "التنبّؤ", "sky"),
        (540, 225, "المقارنة", "rose"),
        (230, 225, "التحديث", "teal"),
    ]
    g = []
    path = ("M 120 70 L 330 70 M 330 70 L 540 70 M 540 70 L 540 225 "
            "M 540 225 L 230 225 M 230 225 C 120 225 120 150 120 95")
    g.append(f'<path d="{path}" fill="none" stroke="#C6D0F2" stroke-width="2.6" class="mra-flow"/>')
    labels = [("التجربة", 225, 56), ("الاستدلال", 435, 56), ("الحقيقة", 568, 150),
              ("الخطأ", 385, 213), ("التعلّم", 96, 160)]
    for txt, x, y in labels:
        g.append(f'<text x="{x}" y="{y}" class="mra-ts" text-anchor="middle">{txt}</text>')
    for i, (x, y, lab, t) in enumerate(nodes):
        r = 46 if len(lab) > 8 else 40
        g.append(_node(x, y, r, lab, t, i * 0.12, 12 if len(lab) < 9 else 10))
    g.append(
        """<circle r="6" fill="#5A6AE0">
      <animateMotion dur="7s" repeatCount="indefinite" rotate="auto">
        <mpath href="#llp"/></animateMotion></circle>
      <path id="llp" d="M 120 70 L 330 70 L 540 70 L 540 225 L 230 225 C 120 225 120 150 120 95"
            fill="none" stroke="none"/>"""
    )
    return f'<svg viewBox="0 0 660 300">{_DEFS}{"".join(g)}</svg>'


# ======================================================================
#  2 — الدالة كصندوق
# ======================================================================
def function_box() -> str:
    g = [_DEFS]
    g.append('<path d="M 600 130 L 420 130" fill="none" stroke="#EBA85A" stroke-width="3" '
             'class="mra-flow" marker-end="url(#arrA)"/>')
    g.append('<path d="M 240 130 L 70 130" fill="none" stroke="#5CC6A4" stroke-width="3" '
             'class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<path d="M 330 40 L 330 85" fill="none" stroke="#A98BEB" stroke-width="2.6" '
             'stroke-dasharray="6 7" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append(_box(240, 85, 180, 90, "الدالة", "f( x ; θ )", "indigo", 0.1, 18, 16))
    g.append(_box(540, 100, 120, 60, "المدخلات", "X — features", "amber", 0.0, 14, 13))
    g.append(_box(10, 100, 120, 60, "المخرجات", "ŷ — prediction", "teal", 0.2, 14, 13))
    g.append(_box(258, 8, 144, 36, "المعاملات", "θ — parameters", "violet", 0.3, 12, 12))
    g.append('<text x="330" y="205" class="mra-ts" text-anchor="middle">'
             'النموذج = قاعدة تحويل ثابتة الشكل، متغيّرة المعاملات</text>')
    g.append('<text x="330" y="226" class="mra-te" text-anchor="middle">'
             'A model is a parameterised mapping from inputs to outputs</text>')
    return f'<svg viewBox="0 0 670 240">{"".join(g)}</svg>'


# ======================================================================
#  3 — دوائر AI / ML / DL
# ======================================================================
def ai_ml_dl() -> str:
    rings = [
        (300, 150, 290, 130, "#EEF2FF", "#B9C4F4", "الذكاء الاصطناعي", "ARTIFICIAL INTELLIGENCE", 28, "#3A4BBF"),
        (300, 158, 215, 100, "#EAF7FF", "#AFD3F6", "تعلّم الآلة", "MACHINE LEARNING", 74, "#2B6FC4"),
        (300, 168, 142, 70, "#EAFBF5", "#A9E0CC", "التعلّم العميق", "DEEP LEARNING", 122, "#1E8E6A"),
        (300, 180, 72, 36, "#FFF2F5", "#F6C3CE", "النماذج التوليدية", "GENERATIVE", 168, "#C24A5E"),
    ]
    g = [_DEFS]
    for i, (cx, cy, rx, ry, fill, stroke, ar, en, ty, ink) in enumerate(rings):
        g.append(
            f"""<g class="mra-pop" style="animation-delay:{i * 0.18:.2f}s">
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{stroke}" stroke-width="1.2"
           class="mra-breathe" style="animation-delay:{i * 0.4:.1f}s"/>
  <text x="{cx}" y="{ty}" text-anchor="middle"
        style="font-family:'Cairo',sans-serif;font-size:14px;font-weight:800;fill:{ink}">{ar}</text>
  <text x="{cx}" y="{ty + 14}" class="mra-te" text-anchor="middle">{en}</text></g>"""
        )
    return f'<svg viewBox="0 0 600 300">{"".join(g)}</svg>'


# ======================================================================
#  4 — الاستقراء مقابل الاستنباط
# ======================================================================
def induction_deduction() -> str:
    g = [_DEFS]
    g.append(_box(400, 30, 220, 62, "حالات جزئية مرصودة", "particular observations", "amber", 0, 16, 13))
    g.append(_box(400, 178, 220, 62, "حالات جديدة", "unseen cases", "sky", 0.2, 16, 13))
    g.append(_box(60, 100, 220, 70, "قاعدة / نموذج عام", "general rule — model", "indigo", 0.1, 16, 14))
    g.append('<path d="M 395 62 C 330 62 320 110 285 125" fill="none" stroke="#EBA85A" stroke-width="3" '
             'class="mra-flow" marker-end="url(#arrA)"/>')
    g.append('<path d="M 285 145 C 320 160 330 208 395 208" fill="none" stroke="#6FAAEE" stroke-width="3" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="345" y="88" class="mra-ts" text-anchor="middle">استقراء</text>')
    g.append('<text x="345" y="103" class="mra-te" text-anchor="middle">induction</text>')
    g.append('<text x="345" y="180" class="mra-ts" text-anchor="middle">استنباط</text>')
    g.append('<text x="345" y="195" class="mra-te" text-anchor="middle">deduction</text>')
    g.append('<text x="340" y="272" class="mra-ts" text-anchor="middle">'
             'التعلّم الآلي يصعد بالاستقراء ثم يهبط بالاستنباط — وهنا تكمن مخاطرته وقوّته معًا</text>')
    return f'<svg viewBox="0 0 650 290">{"".join(g)}</svg>'


# ======================================================================
#  5 — خط أنابيب التعلّم بإشراف
# ======================================================================
def supervised_pipeline() -> str:
    g = [_DEFS]
    rows = [("x₁", "3"), ("x₂", "7"), ("x₃", "1"), ("x₄", "9")]
    g.append('<rect x="505" y="40" width="150" height="170" rx="14" fill="url(#gAmber)" '
             'stroke="#F3D6A6" stroke-width="1.6"/>')
    g.append('<text x="580" y="28" class="mra-ts" text-anchor="middle">بيانات موسومة</text>')
    g.append('<text x="580" y="226" class="mra-te" text-anchor="middle">labelled data (X, y)</text>')
    for i, (f, lab) in enumerate(rows):
        y = 60 + i * 38
        g.append(
            f"""<g class="mra-pop" style="animation-delay:{i * 0.1:.2f}s">
  <rect x="580" y="{y}" width="62" height="28" rx="8" fill="#FFFFFF" stroke="#F0CF9B"/>
  <text x="611" y="{y + 19}" class="mra-m" text-anchor="middle">{f}</text>
  <rect x="518" y="{y}" width="52" height="28" rx="8" fill="#DFF6EE" stroke="#A9E0CC"/>
  <text x="544" y="{y + 19}" class="mra-m" text-anchor="middle" style="fill:#1E8E6A">{lab}</text></g>"""
        )
    g.append('<text x="611" y="52" class="mra-te" text-anchor="middle">X</text>')
    g.append('<text x="544" y="52" class="mra-te" text-anchor="middle">y</text>')
    g.append('<path d="M 500 95 L 400 95" stroke="#EBA85A" stroke-width="3" fill="none" '
             'class="mra-flow" marker-end="url(#arrA)"/>')
    g.append(_box(250, 62, 150, 72, "النموذج", "model f(·;θ)", "indigo", 0.25, 16, 15))
    g.append('<path d="M 245 95 L 160 95" stroke="#6FAAEE" stroke-width="3" fill="none" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append(_box(20, 68, 130, 56, "ŷ التنبّؤ", "prediction", "sky", 0.35, 14, 13))
    g.append('<path d="M 500 165 C 400 165 180 165 90 140" stroke="#EE8A9C" stroke-width="2.4" fill="none" '
             'stroke-dasharray="7 8" class="mra-back" marker-end="url(#arrR)"/>')
    g.append(_box(230, 190, 190, 52, "دالة الخسارة", "loss  L(y, ŷ)", "rose", 0.45, 14, 13))
    g.append('<path d="M 85 130 C 85 215 160 216 225 216" stroke="#EE8A9C" stroke-width="2.4" fill="none" '
             'class="mra-flow" marker-end="url(#arrR)"/>')
    g.append('<path d="M 325 186 C 325 160 325 150 325 140" stroke="#5CC6A4" stroke-width="2.6" fill="none" '
             'class="mra-back" marker-end="url(#arrT)"/>')
    g.append('<text x="415" y="212" class="mra-ts" text-anchor="middle">إشارة التصحيح</text>')
    g.append('<text x="415" y="228" class="mra-te" text-anchor="middle">error signal → update θ</text>')
    return f'<svg viewBox="0 0 670 250">{"".join(g)}</svg>'


# ======================================================================
#  6 — التجميع (تعلّم بدون إشراف)
# ======================================================================
def clustering() -> str:
    import math
    import random

    random.seed(11)
    centers = [(150, 90, "#8192EC", "#EDF1FF"), (330, 190, "#5CC6A4", "#EAFBF5"),
               (490, 95, "#EBA85A", "#FFF7E8")]
    g = [_DEFS]
    g.append('<rect x="10" y="10" width="620" height="250" rx="18" fill="#FCFDFF" stroke="#E6ECFA"/>')
    for ci, (cx, cy, col, soft) in enumerate(centers):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="78" fill="{soft}" opacity=".55" class="mra-breathe" '
                 f'style="animation-delay:{ci * 0.6:.1f}s"/>')
    for ci, (cx, cy, col, soft) in enumerate(centers):
        for k in range(10):
            a = random.uniform(0, 6.283)
            rr = random.uniform(8, 62)
            px = cx + rr * math.cos(a)
            py = cy + rr * math.sin(a) * 0.8
            sx, sy = random.uniform(60, 580), random.uniform(40, 230)
            dx, dy = sx - px, sy - py
            g.append(
                f'<circle cx="{px:.0f}" cy="{py:.0f}" r="5.5" fill="{col}" opacity=".88">'
                f'<animateTransform attributeName="transform" type="translate" '
                f'values="{dx:.0f} {dy:.0f}; 0 0; 0 0; {dx:.0f} {dy:.0f}" '
                f'keyTimes="0;0.35;0.85;1" dur="10s" repeatCount="indefinite" '
                f'calcMode="spline" keySplines="0.3 0 0.2 1;0 0 1 1;0.3 0 0.2 1"/></circle>'
            )
    for ci, (cx, cy, col, soft) in enumerate(centers):
        g.append(f'<g class="mra-pulse" style="animation-delay:{ci * 0.3:.1f}s">'
                 f'<path d="M {cx - 9} {cy} L {cx + 9} {cy} M {cx} {cy - 9} L {cx} {cy + 9}" '
                 f'stroke="{col}" stroke-width="3.4" stroke-linecap="round"/></g>')
        g.append(f'<text x="{cx}" y="{cy + 96}" class="mra-ts" text-anchor="middle" '
                 f'style="fill:{col}">عنقود {ci + 1}</text>')
    g.append('<text x="320" y="282" class="mra-te" text-anchor="middle">'
             'no labels given — structure is discovered, not taught</text>')
    return f'<svg viewBox="0 0 640 295">{"".join(g)}</svg>'


# ======================================================================
#  7 — الانحدار التدريجي
# ======================================================================
def gradient_descent() -> str:
    pts = []
    for i in range(61):
        x = 60 + i * 9
        t = (x - 330) / 190.0
        y = 60 + 150 * (t * t) * 0.92
        pts.append(f"{x:.0f},{y:.0f}")
    curve = "M " + " L ".join(pts)
    g = [_DEFS]
    g.append('<rect x="20" y="15" width="620" height="235" rx="18" fill="#FCFDFF" stroke="#E6ECFA"/>')
    g.append(f'<path d="{curve} L 600 240 L 60 240 Z" fill="url(#gIndigo)" opacity=".5"/>')
    g.append(f'<path d="{curve}" fill="none" stroke="#8192EC" stroke-width="3.4" stroke-linecap="round"/>')
    g.append(f'<path id="gdp" d="{curve}" fill="none" stroke="none"/>')
    g.append('<circle r="12" fill="#5A6AE0" opacity=".2"><animateMotion dur="5s" repeatCount="indefinite" '
             'keyPoints="0;0.5" keyTimes="0;1" calcMode="spline" keySplines="0.3 0 0.2 1">'
             '<mpath href="#gdp"/></animateMotion></circle>')
    g.append('<circle r="9" fill="#5A6AE0"><animateMotion dur="5s" repeatCount="indefinite" '
             'keyPoints="0;0.5" keyTimes="0;1" calcMode="spline" keySplines="0.3 0 0.2 1">'
             '<mpath href="#gdp"/></animateMotion></circle>')
    for i, k in enumerate([0.03, 0.10, 0.19, 0.30, 0.41]):
        x = 60 + k * 540
        t = (x - 330) / 190.0
        y = 60 + 150 * (t * t) * 0.92
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="#B9C4F4" class="mra-pop" '
                 f'style="animation-delay:{i * 0.15:.2f}s"/>')
    g.append('<line x1="60" y1="240" x2="612" y2="240" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<line x1="60" y1="240" x2="60" y2="40" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<text x="604" y="258" class="mra-te" text-anchor="end">θ  (parameter)</text>')
    g.append('<text x="46" y="48" class="mra-te" text-anchor="end">L(θ)</text>')
    g.append('<text x="330" y="232" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">الحدّ الأدنى</text>')
    g.append('<text x="470" y="80" class="mra-ts" text-anchor="middle">نقطة البداية (معاملات عشوائية)</text>')
    g.append('<text x="470" y="96" class="mra-te" text-anchor="middle">random initialisation</text>')
    return f'<svg viewBox="0 0 660 270">{"".join(g)}</svg>'


# ======================================================================
#  8 — نقص/حسن/إفراط التوفيق
# ======================================================================
def fit_spectrum() -> str:
    import math
    import random

    random.seed(5)
    base = [(30 + i * 14, 120 - 52 * math.sin(i / 6.2) + random.uniform(-9, 9)) for i in range(15)]
    panels = [
        ("نقص التوفيق", "underfitting", "#EBA85A", "M 25 95 L 230 72", "amber",
         "النموذج أبسط من الظاهرة"),
        ("توفيق جيّد", "good fit", "#5CC6A4", None, "teal", "يلتقط النمط ويتجاهل الضجيج"),
        ("إفراط التوفيق", "overfitting", "#EE8A9C", None, "rose", "يحفظ الضجيج كأنّه قانون"),
    ]
    g = [_DEFS]
    for pi, (ar, en, col, override, t, note) in enumerate(panels):
        ox = pi * 232
        g.append(f'<rect x="{ox + 12}" y="22" width="216" height="150" rx="16" fill="#FDFEFF" stroke="#E6ECFA"/>')
        for (px, py) in base:
            g.append(f'<circle cx="{ox + 12 + px * 0.88}" cy="{py * 0.93 + 14}" r="3.6" fill="#AEBBE0" opacity=".9"/>')
        if pi == 0:
            d = f"M {ox + 26} 112 L {ox + 220} 74"
        elif pi == 1:
            d = (f"M {ox + 26} 118 C {ox + 80} 36, {ox + 140} 150, {ox + 220} 60")
        else:
            seg = [f"{ox + 12 + px * 0.88:.0f},{py * 0.93 + 14:.0f}" for (px, py) in base]
            d = "M " + " L ".join(seg)
        g.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" '
                 f'stroke-dasharray="900" stroke-dashoffset="900" style="animation:mraDraw 2.2s '
                 f'{pi * 0.4:.1f}s ease-out forwards"/>')
        g.append(f'<text x="{ox + 120}" y="192" text-anchor="middle" '
                 f'style="font-family:Cairo,sans-serif;font-size:13.5px;font-weight:800;fill:{col}">{ar}</text>')
        g.append(f'<text x="{ox + 120}" y="207" class="mra-te" text-anchor="middle">{en}</text>')
        g.append(f'<text x="{ox + 120}" y="226" class="mra-ts" text-anchor="middle">{note}</text>')
    return f'<svg viewBox="0 0 700 240">{"".join(g)}</svg>'


# ======================================================================
#  9 — التحيّز والتباين (أهداف الرماية)
# ======================================================================
def bias_variance_targets() -> str:
    import math
    import random

    random.seed(3)
    cfg = [
        ("تحيّز منخفض · تباين منخفض", "low bias, low variance", 0, 0, 7, "#5CC6A4"),
        ("تحيّز منخفض · تباين مرتفع", "low bias, high variance", 0, 0, 30, "#6FAAEE"),
        ("تحيّز مرتفع · تباين منخفض", "high bias, low variance", 26, -20, 7, "#EBA85A"),
        ("تحيّز مرتفع · تباين مرتفع", "high bias, high variance", 26, -20, 30, "#EE8A9C"),
    ]
    g = [_DEFS]
    for i, (ar, en, bx, by, sp, col) in enumerate(cfg):
        ox = 20 + i * 170
        cx, cy = ox + 70, 86
        for rr, fill in [(60, "#F3F6FF"), (42, "#E6ECFC"), (24, "#D7E0F8"), (10, "#C2CEF3")]:
            g.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{fill}" stroke="#DCE3F6"/>')
        for k in range(9):
            a = random.uniform(0, 6.283)
            rr = abs(random.gauss(0, sp * 0.6))
            px = cx + bx + rr * math.cos(a)
            py = cy + by + rr * math.sin(a)
            g.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="4.4" fill="{col}" class="mra-pop" '
                     f'style="animation-delay:{(i * 9 + k) * 0.035:.2f}s"/>')
        g.append(f'<text x="{cx}" y="168" text-anchor="middle" '
                 f'style="font-family:Cairo,sans-serif;font-size:11.5px;font-weight:700;fill:{col}">{ar}</text>')
        g.append(f'<text x="{cx}" y="183" class="mra-te" text-anchor="middle">{en}</text>')
    return f'<svg viewBox="0 0 700 195">{"".join(g)}</svg>'


# ======================================================================
#  10 — تقسيم البيانات
# ======================================================================
def data_split() -> str:
    segs = [("التدريب", "train  70%", 0, 434, "#8192EC", "#EDF1FF"),
            ("التحقّق", "validation  15%", 434, 93, "#5CC6A4", "#EAFBF5"),
            ("الاختبار", "test  15%", 527, 93, "#EBA85A", "#FFF7E8")]
    g = [_DEFS]
    g.append('<rect x="20" y="18" width="620" height="34" rx="12" fill="#F3F6FF" stroke="#DDE4F8"/>')
    g.append('<text x="330" y="40" class="mra-ts" text-anchor="middle">مجموعة البيانات الكاملة</text>')
    g.append('<path d="M 330 56 L 330 82" stroke="#B9C4F4" stroke-width="2" stroke-dasharray="5 5" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    for i, (ar, en, ox, w, col, fill) in enumerate(segs):
        x = 20 + ox
        g.append(f'<g class="mra-pop" style="animation-delay:{0.25 + i * 0.18:.2f}s">'
                 f'<rect x="{x}" y="92" width="{w - 6}" height="52" rx="12" fill="{fill}" stroke="{col}" stroke-width="1.8"/>'
                 f'<text x="{x + (w - 6) / 2}" y="117" text-anchor="middle" '
                 f'style="font-family:Cairo,sans-serif;font-size:13px;font-weight:800;fill:{col}">{ar}</text>'
                 f'<text x="{x + (w - 6) / 2}" y="133" class="mra-te" text-anchor="middle">{en}</text></g>')
    g.append('<text x="237" y="168" class="mra-ts" text-anchor="middle">يراها النموذج ويتعلّم منها</text>')
    g.append('<text x="480" y="168" class="mra-ts" text-anchor="middle">تُضبط بها الخيارات</text>')
    g.append('<text x="573" y="186" class="mra-ts" text-anchor="middle" style="fill:#B9772A">'
             'لا تُلمس إلّا مرّة واحدة في النهاية</text>')
    return f'<svg viewBox="0 0 660 200">{"".join(g)}</svg>'


# ======================================================================
#  11 — تشريح جدول البيانات
# ======================================================================
def dataset_anatomy() -> str:
    cols = ["y الهدف", "x₃", "x₂", "x₁"]
    g = [_DEFS]
    x0, y0, cw, ch = 110, 56, 118, 34
    for ci, c in enumerate(cols):
        x = x0 + ci * cw
        fill = "#DFF6EE" if ci == 0 else "#EDF1FF"
        stroke = "#A9E0CC" if ci == 0 else "#C6D0F2"
        ink = "#1E8E6A" if ci == 0 else "#3A4BBF"
        g.append(f'<rect x="{x}" y="{y0}" width="{cw - 4}" height="{ch}" rx="9" fill="{fill}" stroke="{stroke}"/>')
        g.append(f'<text x="{x + cw / 2 - 2}" y="{y0 + 22}" text-anchor="middle" '
                 f'style="font-family:Cairo,sans-serif;font-size:12.5px;font-weight:800;fill:{ink}">{c}</text>')
    vals = [["1", "0.8", "12", "5"], ["0", "0.3", "7", "9"], ["1", "0.9", "15", "4"], ["0", "0.1", "3", "8"]]
    for ri, row in enumerate(vals):
        y = y0 + ch + 6 + ri * (ch - 3)
        for ci, v in enumerate(row):
            x = x0 + ci * cw
            fill = "#F4FCF8" if ci == 0 else "#FBFCFF"
            g.append(f'<rect x="{x}" y="{y}" width="{cw - 4}" height="{ch - 7}" rx="7" fill="{fill}" stroke="#E7EDF9"/>')
            g.append(f'<text x="{x + cw / 2 - 2}" y="{y + 18}" class="mra-m" text-anchor="middle">{v}</text>')
    g.append('<path d="M 100 70 L 100 190" stroke="#EBA85A" stroke-width="2.6" class="mra-flow" '
             'marker-end="url(#arrA)" marker-start="url(#arrA)"/>')
    g.append('<text x="60" y="120" class="mra-ts" text-anchor="middle" style="fill:#B9772A">الصفوف</text>')
    g.append('<text x="60" y="137" class="mra-ts" text-anchor="middle" style="fill:#B9772A">= أمثلة</text>')
    g.append('<text x="60" y="154" class="mra-te" text-anchor="middle">rows = samples</text>')
    g.append('<path d="M 575 40 L 232 40" stroke="#8192EC" stroke-width="2.6" class="mra-flow" '
             'marker-end="url(#arrI)"/>')
    g.append('<text x="400" y="28" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'الأعمدة = متغيّرات / ميزات (features)</text>')
    g.append('<text x="166" y="222" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'هذا العمود هو الهدف</text>')
    g.append('<text x="166" y="238" class="mra-te" text-anchor="middle">target / label  y</text>')
    g.append('<path d="M 166 200 L 166 182" stroke="#5CC6A4" stroke-width="2.4" marker-end="url(#arrT)"/>')
    return f'<svg viewBox="0 0 620 250">{"".join(g)}</svg>'


# ======================================================================
#  12 — العصبون (perceptron)
# ======================================================================
def perceptron() -> str:
    g = [_DEFS]
    ins = [("x₁", 60), ("x₂", 120), ("x₃", 180)]
    for i, (lab, y) in enumerate(ins):
        g.append(f'<circle cx="590" cy="{y}" r="20" fill="url(#gAmber)" stroke="#F3D6A6" stroke-width="1.6" '
                 f'class="mra-pop" style="animation-delay:{i * .1:.2f}s"/>')
        g.append(f'<text x="590" y="{y + 5}" class="mra-m" text-anchor="middle">{lab}</text>')
        g.append(f'<path d="M 568 {y} C 480 {y}, 450 120, 395 120" fill="none" stroke="#C6D0F2" '
                 f'stroke-width="2.4" class="mra-flow" style="animation-delay:{i * .2:.1f}s"/>')
        g.append(f'<text x="490" y="{y - 10 if i < 2 else y + 22}" class="mra-te" text-anchor="middle">w{i + 1}</text>')
    g.append('<circle cx="350" cy="120" r="46" fill="url(#gIndigo)" stroke="#B9C4F4" stroke-width="2"/>')
    g.append('<text x="350" y="112" text-anchor="middle" style="font-family:Cairo;font-size:12px;'
             'font-weight:800;fill:#3A4BBF">مجموع مرجّح</text>')
    g.append('<text x="350" y="132" class="mra-te" text-anchor="middle">Σ wᵢxᵢ + b</text>')
    g.append('<path d="M 302 120 L 262 120" stroke="#8192EC" stroke-width="2.6" class="mra-flow" '
             'marker-end="url(#arrI)"/>')
    g.append(_box(120, 90, 142, 60, "دالة التنشيط", "activation σ(·)", "violet", 0.3, 14, 12))
    g.append('<path d="M 115 120 L 72 120" stroke="#5CC6A4" stroke-width="2.6" class="mra-flow" '
             'marker-end="url(#arrT)"/>')
    g.append('<circle cx="40" cy="120" r="24" fill="url(#gTeal)" stroke="#A9E0CC" stroke-width="1.8" class="mra-pulse"/>')
    g.append('<text x="40" y="125" class="mra-m" text-anchor="middle" style="fill:#1E8E6A">ŷ</text>')
    g.append('<text x="350" y="208" class="mra-ts" text-anchor="middle">'
             'العصبون = ضربٌ وجمعٌ ثمّ انحناءة غير خطّية — ولا شيء أكثر</text>')
    g.append('<text x="350" y="226" class="mra-te" text-anchor="middle">'
             'a neuron is a weighted sum followed by one nonlinearity</text>')
    return f'<svg viewBox="0 0 640 240">{"".join(g)}</svg>'


# ======================================================================
#  13 — فضاء الفرضيات
# ======================================================================
def hypothesis_space() -> str:
    g = [_DEFS]
    g.append('<ellipse cx="330" cy="130" rx="300" ry="112" fill="#F6F8FF" stroke="#DCE3F6" stroke-width="2"/>')
    g.append('<text x="330" y="36" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'فضاء الفرضيات ℋ — كلّ النماذج التي تسمح بها بنيتك</text>')
    curves = [
        ("M 90 180 C 180 90, 280 200, 420 110", "#C9D3FB", 2, 0),
        ("M 90 160 C 190 200, 300 70, 440 150", "#C9D3FB", 2, 0),
        ("M 110 190 C 210 60, 320 210, 460 90", "#C9D3FB", 2, 0),
        ("M 100 120 C 200 170, 310 90, 450 170", "#C9D3FB", 2, 0),
        ("M 130 200 C 230 110, 330 180, 470 120", "#C9D3FB", 2, 0),
    ]
    for i, (d, col, wd, _) in enumerate(curves):
        g.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd}" opacity=".85" '
                 f'class="mra-breathe" style="animation-delay:{i * .5:.1f}s"/>')
    g.append('<path d="M 100 170 C 200 80, 310 190, 450 100" fill="none" stroke="#5CC6A4" stroke-width="4" '
             'stroke-linecap="round" stroke-dasharray="700" stroke-dashoffset="700" '
             'style="animation:mraDraw 2.6s .4s ease-out forwards"/>')
    g.append('<circle cx="450" cy="100" r="8" fill="#5CC6A4" class="mra-pulse"/>')
    g.append('<text x="520" y="96" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">الفرضية المختارة</text>')
    g.append('<text x="520" y="112" class="mra-te" text-anchor="middle">ĥ = argmin L</text>')
    g.append('<text x="330" y="258" class="mra-ts" text-anchor="middle">'
             'التدريب = بحث داخل هذا الفضاء عن العنصر الأقلّ خطأً — لا خلقٌ من عدم</text>')
    return f'<svg viewBox="0 0 660 275">{"".join(g)}</svg>'


# ======================================================================
#  14 — دورة حياة مشروع تعلّم الآلة
# ======================================================================
def lifecycle() -> str:
    import math

    stages = [
        ("صياغة السؤال", "framing"), ("جمع البيانات", "collection"),
        ("التنظيف", "cleaning"), ("الاستكشاف", "EDA"),
        ("هندسة الميزات", "features"), ("النمذجة", "modelling"),
        ("التقييم", "evaluation"), ("النشر والمراقبة", "deploy"),
    ]
    cx, cy, R = 330, 200, 150
    cols = ["amber", "sky", "teal", "violet", "indigo", "rose", "teal", "sky"]
    g = [_DEFS]
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#D7E0F6" stroke-width="2.6" '
             f'stroke-dasharray="10 12" class="mra-flow"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R - 46}" fill="#F7F9FF" stroke="#E6ECFA"/>')
    g.append(f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" '
             f'style="font-family:Tajawal;font-size:17px;font-weight:800;fill:#3A4BBF">دورة حياة</text>')
    g.append(f'<text x="{cx}" y="{cy + 18}" text-anchor="middle" '
             f'style="font-family:Tajawal;font-size:17px;font-weight:800;fill:#3A4BBF">المشروع</text>')
    g.append(f'<text x="{cx}" y="{cy + 38}" class="mra-te" text-anchor="middle">ML LIFECYCLE</text>')
    for i, (ar, en) in enumerate(stages):
        a = -math.pi / 2 + i * (2 * math.pi / len(stages))
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        fill, stroke, ink = _FILL[cols[i]]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .11:.2f}s">'
                 f'<circle cx="{px:.0f}" cy="{py:.0f}" r="40" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>'
                 f'<circle cx="{px:.0f}" cy="{py:.0f}" r="46" fill="none" stroke="{stroke}" opacity=".45" '
                 f'class="mra-breathe" style="animation-delay:{i * .3:.1f}s"/>'
                 f'<text x="{px:.0f}" y="{py - 2:.0f}" text-anchor="middle" '
                 f'style="font-family:Cairo;font-size:11px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{px:.0f}" y="{py + 13:.0f}" class="mra-te" text-anchor="middle">{en}</text></g>')
    return f'<svg viewBox="0 0 660 400">{"".join(g)}</svg>'


# ======================================================================
#  15 — حلقة التعلّم المعزّز
# ======================================================================
def rl_loop() -> str:
    g = [_DEFS]
    g.append(_box(400, 70, 190, 80, "العميل", "agent", "indigo", 0, 18, 16))
    g.append(_box(70, 70, 190, 80, "البيئة", "environment", "teal", 0.15, 18, 16))
    g.append('<path d="M 395 95 L 265 95" stroke="#8192EC" stroke-width="3" fill="none" class="mra-flow" '
             'marker-end="url(#arrI)"/>')
    g.append('<text x="330" y="84" class="mra-ts" text-anchor="middle">فعل aₜ</text>')
    g.append('<path d="M 70 128 C 20 128, 20 200, 120 200 L 540 200 C 620 200, 620 128, 585 128" '
             'stroke="#5CC6A4" stroke-width="3" fill="none" class="mra-back" marker-end="url(#arrT)"/>')
    g.append('<text x="330" y="192" class="mra-ts" text-anchor="middle">حالة جديدة sₜ₊₁ + مكافأة rₜ₊₁</text>')
    g.append('<text x="330" y="226" class="mra-te" text-anchor="middle">'
             'learning by consequence, not by example</text>')
    g.append('<text x="330" y="246" class="mra-ts" text-anchor="middle">'
             'لا معلّم يقول «الجواب الصحيح» — بل عالَمٌ يقول «هذا كان مجديًا»</text>')
    return f'<svg viewBox="0 0 660 260">{"".join(g)}</svg>'


# ======================================================================
#  16 — فجوة التعميم
# ======================================================================
def generalization_gap() -> str:
    import math

    tr, te = [], []
    for i in range(61):
        x = 70 + i * 8.6
        c = i / 60
        tr.append(f"{x:.0f},{215 - 140 * (1 - math.exp(-3.4 * c)):.0f}")
        te.append(f"{x:.0f},{215 - 140 * (1 - math.exp(-3.4 * c)) + 95 * (c ** 2.4):.0f}")
    g = [_DEFS]
    g.append('<rect x="30" y="18" width="610" height="212" rx="18" fill="#FCFDFF" stroke="#E6ECFA"/>')
    g.append('<line x1="70" y1="218" x2="610" y2="218" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<line x1="70" y1="218" x2="70" y2="40" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append(f'<path d="M {" L ".join(te)}" fill="none" stroke="#EE8A9C" stroke-width="3.2" '
             f'stroke-dasharray="1200" stroke-dashoffset="1200" style="animation:mraDraw 2.6s .3s ease-out forwards"/>')
    g.append(f'<path d="M {" L ".join(tr)}" fill="none" stroke="#5CC6A4" stroke-width="3.2" '
             f'stroke-dasharray="1200" stroke-dashoffset="1200" style="animation:mraDraw 2.6s .1s ease-out forwards"/>')
    g.append('<line x1="470" y1="96" x2="470" y2="168" stroke="#B9772A" stroke-width="2" stroke-dasharray="4 4" '
             'class="mra-flow"/>')
    g.append('<text x="470" y="88" class="mra-ts" text-anchor="middle" style="fill:#B9772A">فجوة التعميم</text>')
    g.append('<text x="470" y="186" class="mra-te" text-anchor="middle">generalisation gap</text>')
    g.append('<text x="596" y="62" class="mra-ts" text-anchor="end" style="fill:#C24A5E">خطأ الاختبار</text>')
    g.append('<text x="596" y="196" class="mra-ts" text-anchor="end" style="fill:#1E8E6A">خطأ التدريب</text>')
    g.append('<text x="604" y="238" class="mra-te" text-anchor="end">model complexity / epochs →</text>')
    g.append('<text x="56" y="48" class="mra-te" text-anchor="end">error</text>')
    return f'<svg viewBox="0 0 660 250">{"".join(g)}</svg>'


# ======================================================================
#  17 — تصنيف مقابل انحدار
# ======================================================================
def classification_vs_regression() -> str:
    import random

    random.seed(9)
    g = [_DEFS]
    g.append('<rect x="350" y="22" width="300" height="190" rx="18" fill="#FDFEFF" stroke="#E6ECFA"/>')
    g.append('<text x="500" y="14" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">التصنيف</text>')
    g.append('<path d="M 380 190 L 620 56" stroke="#8192EC" stroke-width="3" stroke-dasharray="520" '
             'stroke-dashoffset="520" style="animation:mraDraw 2s .2s ease-out forwards"/>')
    for k in range(13):
        x, y = random.uniform(375, 610), random.uniform(40, 200)
        above = (y < 190 - (x - 380) * 0.558)
        col = "#6FAAEE" if above else "#EBA85A"
        shape = (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5.2" fill="{col}"/>' if above
                 else f'<rect x="{x - 4.6:.0f}" y="{y - 4.6:.0f}" width="9.2" height="9.2" rx="2" fill="{col}"/>')
        g.append(f'<g class="mra-pop" style="animation-delay:{k * .05:.2f}s">{shape}</g>')
    g.append('<text x="500" y="230" class="mra-te" text-anchor="middle">y is a category — a boundary is learned</text>')
    g.append('<rect x="20" y="22" width="300" height="190" rx="18" fill="#FDFEFF" stroke="#E6ECFA"/>')
    g.append('<text x="170" y="14" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">الانحدار</text>')
    pts = []
    for k in range(16):
        x = 46 + k * 17
        y = 190 - (x - 46) * 0.52 + random.uniform(-18, 18)
        pts.append((x, y))
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#5CC6A4" class="mra-pop" '
                 f'style="animation-delay:{k * .05:.2f}s"/>')
    g.append('<path d="M 46 190 L 290 63" stroke="#1E8E6A" stroke-width="3" stroke-dasharray="520" '
             'stroke-dashoffset="520" style="animation:mraDraw 2s .2s ease-out forwards"/>')
    g.append('<text x="170" y="230" class="mra-te" text-anchor="middle">y is a number — a curve is fitted</text>')
    return f'<svg viewBox="0 0 670 240">{"".join(g)}</svg>'


# ======================================================================
#  18 — حلقة التدريب (أمامي / خلفي)
# ======================================================================
def training_loop() -> str:
    g = [_DEFS]
    g.append(_box(500, 40, 140, 58, "دفعة بيانات", "mini-batch", "amber", 0, 14, 13))
    g.append(_box(300, 40, 160, 58, "تمرير أمامي", "forward pass", "indigo", .1, 14, 13))
    g.append(_box(90, 40, 170, 58, "حساب الخسارة", "compute loss", "rose", .2, 14, 13))
    g.append(_box(90, 150, 170, 58, "المشتقّات", "backward pass", "violet", .3, 14, 13))
    g.append(_box(300, 150, 160, 58, "تحديث θ", "optimiser step", "teal", .4, 14, 13))
    g.append(_box(500, 150, 140, 58, "الدفعة التالية", "next batch", "sky", .5, 14, 13))
    g.append('<path d="M 496 69 L 466 69" stroke="#EBA85A" stroke-width="2.6" class="mra-flow" marker-end="url(#arrA)"/>')
    g.append('<path d="M 296 69 L 266 69" stroke="#8192EC" stroke-width="2.6" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<path d="M 175 102 L 175 146" stroke="#EE8A9C" stroke-width="2.6" class="mra-flow" marker-end="url(#arrR)"/>')
    g.append('<path d="M 264 179 L 296 179" stroke="#A98BEB" stroke-width="2.6" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<path d="M 464 179 L 496 179" stroke="#5CC6A4" stroke-width="2.6" class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<path d="M 640 150 C 666 130, 666 90, 640 70" stroke="#6FAAEE" stroke-width="2.6" fill="none" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="330" y="238" class="mra-ts" text-anchor="middle">'
             'حقبة (epoch) = مرور كامل على كلّ الدفعات · والتكرار هو التدريب</text>')
    return f'<svg viewBox="0 0 690 250">{"".join(g)}</svg>'


# ======================================================================
#  19 — التوزيع الاحتمالي
# ======================================================================
def distribution() -> str:
    import math

    def bell(mu, s, scale):
        pts = []
        for i in range(121):
            x = 40 + i * 4.8
            y = 200 - scale * math.exp(-((x - mu) ** 2) / (2 * s * s))
            pts.append(f"{x:.0f},{y:.0f}")
        return "M " + " L ".join(pts)

    g = [_DEFS]
    g.append('<rect x="20" y="16" width="620" height="206" rx="18" fill="#FCFDFF" stroke="#E6ECFA"/>')
    g.append(f'<path d="{bell(330, 95, 150)} L 616 200 L 40 200 Z" fill="url(#gIndigo)" opacity=".55"/>')
    g.append(f'<path d="{bell(330, 95, 150)}" fill="none" stroke="#8192EC" stroke-width="3.2"/>')
    g.append(f'<path d="{bell(210, 55, 118)}" fill="none" stroke="#5CC6A4" stroke-width="2.6" '
             f'stroke-dasharray="7 7" class="mra-flow"/>')
    g.append(f'<path d="{bell(455, 70, 95)}" fill="none" stroke="#EBA85A" stroke-width="2.6" '
             f'stroke-dasharray="7 7" class="mra-flow"/>')
    g.append('<line x1="40" y1="200" x2="620" y2="200" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<line x1="330" y1="200" x2="330" y2="52" stroke="#B9C4F4" stroke-width="2" stroke-dasharray="5 5"/>')
    g.append('<text x="330" y="44" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">المتوقَّع</text>')
    g.append('<text x="210" y="80" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">توزيع التدريب</text>')
    g.append('<text x="470" y="106" class="mra-ts" text-anchor="middle" style="fill:#B9772A">توزيع الواقع</text>')
    g.append('<text x="330" y="240" class="mra-te" text-anchor="middle">'
             'distribution shift: the world moves, the model does not</text>')
    return f'<svg viewBox="0 0 660 252">{"".join(g)}</svg>'


# ======================================================================
#  20 — سلّم التجريد: بيانات ← معلومة ← معرفة ← حكمة
# ======================================================================
def abstraction_ladder() -> str:
    rungs = [("بيانات خام", "data", "amber", 230), ("معلومة", "information", "sky", 200),
             ("معرفة", "knowledge", "teal", 170), ("قرار", "decision", "violet", 140),
             ("قيمة", "value", "indigo", 110)]
    g = [_DEFS]
    for i, (ar, en, t, w) in enumerate(rungs):
        fill, stroke, ink = _FILL[t]
        y = 220 - i * 44
        x = 330 - w / 2
        g.append(f'<g class="mra-slide" style="animation-delay:{i * .13:.2f}s">'
                 f'<rect x="{x:.0f}" y="{y}" width="{w}" height="38" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.7"/>'
                 f'<text x="330" y="{y + 18}" text-anchor="middle" style="font-family:Cairo;font-size:13px;'
                 f'font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="330" y="{y + 32}" class="mra-te" text-anchor="middle">{en}</text></g>')
        if i < len(rungs) - 1:
            g.append(f'<path d="M 330 {y} L 330 {y - 6}" stroke="{stroke}" stroke-width="2.4" '
                     f'marker-end="url(#arrI)" class="mra-flow"/>')
    g.append('<text x="330" y="282" class="mra-ts" text-anchor="middle">'
             'كلّ درجة تفقد تفاصيل وتربح معنى — وهذا هو التجريد</text>')
    return f'<svg viewBox="0 0 660 295">{"".join(g)}</svg>'


# ======================================================================
#  21 — ثلاثية التعلّم: تمثيل · تقييم · أمثَلة
# ======================================================================
def three_components() -> str:
    g = [_DEFS]
    trio = [("التمثيل", "Representation", "ما هي النماذج الممكنة؟", "indigo", 500),
            ("التقييم", "Evaluation", "كيف نحكم أن نموذجًا أفضل؟", "teal", 285),
            ("الأمثَلة", "Optimisation", "كيف نبحث عن الأفضل؟", "amber", 70)]
    for i, (ar, en, q, t, x) in enumerate(trio):
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .14:.2f}s">'
                 f'<rect x="{x}" y="40" width="160" height="120" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="1.9"/>'
                 f'<text x="{x + 80}" y="76" text-anchor="middle" style="font-family:Tajawal;font-size:17px;'
                 f'font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{x + 80}" y="94" class="mra-te" text-anchor="middle">{en.upper()}</text>'
                 f'<text x="{x + 80}" y="126" text-anchor="middle" style="font-family:Cairo;font-size:11px;'
                 f'fill:#4C5A86">{q}</text></g>')
        if i < 2:
            g.append(f'<path d="M {x - 6} 100 L {x - 48} 100" stroke="#C6D0F2" stroke-width="2.6" '
                     f'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="330" y="194" class="mra-ts" text-anchor="middle">'
             'كلّ خوارزمية تعلّم هي تركيب من هذه الثلاثة — لا رابع لها</text>')
    g.append('<text x="330" y="212" class="mra-te" text-anchor="middle">'
             'Domingos (2012): Learning = Representation + Evaluation + Optimisation</text>')
    return f'<svg viewBox="0 0 740 224">{"".join(g)}</svg>'


# ======================================================================
#  22 — المفاضلة بين الدقّة والتفسيرية
# ======================================================================
def accuracy_interpretability() -> str:
    models = [("انحدار خطّي", "Linear", 60, 210, "teal"), ("شجرة قرار", "Tree", 160, 180, "teal"),
              ("غابة عشوائية", "Random forest", 280, 130, "sky"), ("تعزيز متدرّج", "Boosting", 390, 105, "sky"),
              ("شبكة عميقة", "Deep net", 510, 70, "violet"), ("نموذج أساس", "Foundation model", 610, 52, "rose")]
    g = [_DEFS]
    g.append('<rect x="24" y="16" width="660" height="230" rx="18" fill="#FCFDFF" stroke="#E6ECFA"/>')
    g.append('<line x1="50" y1="238" x2="676" y2="238" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<line x1="50" y1="238" x2="50" y2="36" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<path d="M 60 216 C 220 196, 400 120, 650 52" fill="none" stroke="#C6D0F2" stroke-width="2.4" '
             'stroke-dasharray="8 9" class="mra-flow"/>')
    for i, (ar, en, x, y, t) in enumerate(models):
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .1:.2f}s">'
                 f'<circle cx="{x}" cy="{y}" r="11" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
                 f'<text x="{x}" y="{y - 20}" text-anchor="middle" style="font-family:Cairo;font-size:11px;'
                 f'font-weight:700;fill:{ink}">{ar}</text></g>')
    g.append('<text x="670" y="256" class="mra-te" text-anchor="end">← interpretability decreases</text>')
    g.append('<text x="36" y="34" class="mra-te" text-anchor="end">accuracy</text>')
    g.append('<text x="360" y="276" class="mra-ts" text-anchor="middle">'
             'كلّما ازدادت القدرة التنبّؤية، صَعُب أن تشرح «لماذا» — وهذه مقايضة لا مفرّ منها</text>')
    return f'<svg viewBox="0 0 710 290">{"".join(g)}</svg>'


# ======================================================================
#  23 — تسرّب البيانات
# ======================================================================
def data_leakage() -> str:
    g = [_DEFS]
    g.append(_box(400, 40, 200, 70, "بيانات التدريب", "train", "indigo", 0, 16, 14))
    g.append(_box(80, 40, 200, 70, "بيانات الاختبار", "test", "amber", .1, 16, 14))
    g.append('<path d="M 395 62 C 340 62, 340 62, 285 62" stroke="#EE8A9C" stroke-width="3.4" fill="none" '
             'class="mra-flow" marker-end="url(#arrR)"/>')
    g.append('<text x="340" y="46" class="mra-ts" text-anchor="middle" style="fill:#C24A5E">تسرّب!</text>')
    g.append('<text x="340" y="96" class="mra-te" text-anchor="middle">leakage</text>')
    g.append('<g class="mra-pulse"><circle cx="340" cy="62" r="20" fill="none" stroke="#EE8A9C" stroke-width="2"/></g>')
    g.append(_box(230, 160, 220, 60, "نتائج مبهرة… وكاذبة", "optimistic but invalid", "rose", .3, 14, 13))
    g.append('<path d="M 340 134 L 340 156" stroke="#EE8A9C" stroke-width="2.6" marker-end="url(#arrR)" class="mra-flow"/>')
    return f'<svg viewBox="0 0 690 235">{"".join(g)}</svg>'


# ======================================================================
#  24 — شريط تقدّم مفاهيمي (للصفحة الرئيسية)
# ======================================================================
def journey_rail(items: list[tuple[str, str]]) -> str:
    g = [_DEFS]
    n = len(items)
    w = 700
    g.append(f'<line x1="40" y1="60" x2="{w - 40}" y2="60" stroke="#D7E0F6" stroke-width="3" '
             f'stroke-dasharray="9 10" class="mra-flow"/>')
    tones = ["amber", "sky", "teal", "violet", "indigo", "rose"]
    for i, (ar, en) in enumerate(items):
        x = w - 40 - i * ((w - 80) / max(n - 1, 1))
        t = tones[i % len(tones)]
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .12:.2f}s">'
                 f'<circle cx="{x:.0f}" cy="60" r="17" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>'
                 f'<text x="{x:.0f}" y="65" text-anchor="middle" style="font-family:Cairo;font-size:12px;'
                 f'font-weight:800;fill:{ink}">{i + 1}</text>'
                 f'<text x="{x:.0f}" y="100" text-anchor="middle" style="font-family:Cairo;font-size:11.5px;'
                 f'font-weight:700;fill:#38466F">{ar}</text>'
                 f'<text x="{x:.0f}" y="115" class="mra-te" text-anchor="middle">{en}</text></g>')
    return f'<svg viewBox="0 0 {w} 130">{"".join(g)}</svg>'
