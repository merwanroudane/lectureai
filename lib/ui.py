"""
عناصر الواجهة المشتركة (RTL + بطاقات + عناوين).
Shared UI primitives for the Arabic, right-to-left AI foundations platform.

Author: Dr Merwan Roudane
"""

from __future__ import annotations

import html as _html

import streamlit as st

AUTHOR_AR = "الدكتور مروان رودان"
AUTHOR_EN = "Dr Merwan Roudane"
PLATFORM_AR = "أسس التعلّم في الذكاء الاصطناعي"
PLATFORM_EN = "Foundations of Learning in Artificial Intelligence"

# ----------------------------------------------------------------------
# لوحة الألوان — كلّها فاتحة ومشرقة، بلا ألوان داكنة
# ----------------------------------------------------------------------
TONES: dict[str, dict[str, str]] = {
    "indigo": {"bg1": "#F2F4FF", "bg2": "#E6EBFF", "line": "#C9D3FB", "ink": "#3A4BBF", "soft": "#8192EC"},
    "teal": {"bg1": "#EFFBF7", "bg2": "#DFF6EE", "line": "#B6E6D6", "ink": "#1E8E6A", "soft": "#5CC6A4"},
    "amber": {"bg1": "#FFF8EC", "bg2": "#FFEFD6", "line": "#F7DCAE", "ink": "#B9772A", "soft": "#EBA85A"},
    "rose": {"bg1": "#FFF2F4", "bg2": "#FFE4E9", "line": "#F8CBD4", "ink": "#C24A5E", "soft": "#EE8A9C"},
    "violet": {"bg1": "#F8F3FF", "bg2": "#EFE6FF", "line": "#DCCCF8", "ink": "#7149C6", "soft": "#A98BEB"},
    "sky": {"bg1": "#EFF7FF", "bg2": "#DEEEFF", "line": "#BCDBFA", "ink": "#2B6FC4", "soft": "#6FAAEE"},
    "mint": {"bg1": "#F1FBF2", "bg2": "#E2F6E6", "line": "#BFE7C8", "ink": "#2D8B47", "soft": "#72C98A"},
    "sand": {"bg1": "#FBF8F3", "bg2": "#F4EEE3", "line": "#E4D9C6", "ink": "#8C7445", "soft": "#C4AE80"},
}
TONE_CYCLE = ["indigo", "teal", "amber", "violet", "sky", "rose", "mint", "sand"]


def tone(name: str) -> dict[str, str]:
    return TONES.get(name, TONES["indigo"])


# ----------------------------------------------------------------------
# CSS العام — الاتجاه من اليمين إلى اليسار، والشريط الجانبي على اليمين
# ----------------------------------------------------------------------
_GLOBAL_CSS = """
<style>
/* ===== 1. الاتجاه العام RTL + نقل الشريط الجانبي إلى اليمين ===== */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stHeader"],
[data-testid="stMain"],
[data-testid="stSidebar"],
[data-testid="stBottomBlockContainer"] {
    direction: rtl;
}
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarNav"],
[data-testid="stNavSectionHeader"] { direction: rtl; text-align: right; }

/* في حاوية flex باتّجاه rtl يصبح الطفل الأوّل (الشريط الجانبي) على اليمين تلقائيًّا */
[data-testid="stAppViewContainer"] { flex-direction: row; }
[data-testid="stSidebar"] { width: 304px !important; min-width: 304px !important; }
[data-testid="stSidebar"] [data-testid="stNavSectionHeader"] {
    font-size: .68rem !important; letter-spacing: .9px; font-weight: 800;
    color: #6E7CAC !important; direction: ltr; text-align: right;
}
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] { direction: rtl; }

/* روابط التنقّل في الشريط الجانبي: المصطلح الإنجليزي يبقى LTR وبمحاذاة يمين */
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavLink"] span { text-align: right; }

/* ===== 2. محاذاة النصوص العربية ===== */
[data-testid="stMarkdownContainer"] { text-align: right; }
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { text-align: right; }
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol { padding-right: 1.4rem; padding-left: 0; }
[data-testid="stMarkdownContainer"] blockquote {
    border-right: 4px solid #B9C4F4; border-left: none;
    padding-right: 1rem; padding-left: 0; margin-right: 0;
    background: #F6F8FF; border-radius: 0 12px 12px 0;
}
[data-testid="stMarkdownContainer"] blockquote,
[data-testid="stMarkdownContainer"] blockquote p { color: #3E4D7C !important; font-weight: 500; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { direction: rtl; }
[data-testid="stExpander"] summary { direction: rtl; text-align: right; }

/* ===== 3. الشيفرة والرياضيات تبقى LTR =====
   ملاحظة دقيقة: خاصّية direction وحدها لا تكفي داخل فقرة RTL، لأنّها لا تُطبَّق
   ما لم تُفتح طبقة عزل ثنائي الاتّجاه. وبدون unicode-bidi تُعيد خوارزمية bidi
   ترتيب رموز KaTeX فتظهر المعادلة معكوسة. */
code, pre, .stCode, [data-testid="stCode"],
.katex, .katex-display, .katex-html, [data-testid="stLatex"],
[data-testid="stJson"], .stDataFrame, [data-testid="stDataFrame"] {
    direction: ltr !important;
    unicode-bidi: isolate !important;
    text-align: left !important;
}
.katex-display { text-align: center !important; display: block !important; }
.katex-display > .katex { display: inline-block !important; text-align: initial !important; }

/* الرسوم البيانية (Vega/Altair) تُرسم باتّجاه لاتيني حتّى لا تنقلب المحاور */
[data-testid="stVegaLiteChart"], .vega-embed, .vega-embed * ,
[data-testid="stPlotlyChart"] { direction: ltr !important; }

/* ===== 4. الجداول ===== */
[data-testid="stMarkdownContainer"] table { width: 100%; border-collapse: separate; border-spacing: 0; }
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td { text-align: right !important; }
[data-testid="stMarkdownContainer"] th { background: #EEF2FF; color: #2C3A6B; }

/* ===== 5. تنعيم ظهور العناصر ===== */
@keyframes mrFadeUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
.mr-anim { animation: mrFadeUp .55s cubic-bezier(.22,.9,.3,1) both; }

/* ===== 6. المكوّنات المخصّصة ===== */
.mr-hero {
    position: relative; overflow: hidden;
    border-radius: 24px; padding: 30px 34px 26px;
    background: linear-gradient(130deg, #EEF2FF 0%, #F4EEFF 42%, #E9F8F3 100%);
    border: 1px solid #DFE5F7;
    box-shadow: 0 18px 40px -28px rgba(60, 80, 180, .55);
    margin-bottom: 20px;
}
.mr-hero::after {
    content: ""; position: absolute; left: -70px; top: -90px;
    width: 260px; height: 260px; border-radius: 50%;
    background: radial-gradient(circle, rgba(140,165,255,.30), rgba(140,165,255,0) 68%);
    animation: mrFloat 9s ease-in-out infinite;
}
@keyframes mrFloat { 0%,100% { transform: translateY(0) } 50% { transform: translateY(26px) } }
.mr-hero-kicker {
    display:inline-flex; align-items:center; gap:8px;
    font-size:.78rem; font-weight:700; letter-spacing:.4px;
    color:#4457CF; background:rgba(255,255,255,.70); border:1px solid #D3DDF8;
    padding:5px 13px; border-radius:999px; margin-bottom:12px;
}
.mr-hero h1 { margin:0 0 6px; font-size:2.05rem; font-weight:800; color:#1F2B52; line-height:1.45; }
.mr-hero .en { direction:ltr; text-align:right; font-size:.95rem; font-weight:600;
               color:#6B7AA8; letter-spacing:.3px; margin-bottom:12px; }
.mr-hero p.lead { margin:0; font-size:1.02rem; line-height:2.1; color:#3C4A72; max-width:64ch; }

.mr-card {
    border-radius:18px; padding:18px 20px; margin:10px 0;
    border:1px solid var(--mr-line); background:linear-gradient(145deg,var(--mr-b1),var(--mr-b2));
    box-shadow:0 10px 26px -22px rgba(40,60,140,.6);
    transition:transform .25s ease, box-shadow .25s ease;
}
.mr-card:hover { transform:translateY(-3px); box-shadow:0 18px 34px -24px rgba(40,60,140,.7); }
.mr-card h4 { margin:0 0 8px; font-size:1.07rem; font-weight:800; color:var(--mr-ink);
              display:flex; align-items:center; gap:9px; }
.mr-card .en-tag { direction:ltr; font-size:.70rem; font-weight:700; color:#FFF;
                   background:var(--mr-soft); padding:3px 10px; border-radius:999px; margin-right:auto; }
.mr-card p, .mr-card li { font-size:.96rem; line-height:1.95; color:#32406B; margin:0 0 6px; }
.mr-card ul, .mr-card ol { margin:6px 0 0; padding-right:1.1rem; padding-left:0; }
.mr-card b { color:var(--mr-ink); }
.mr-card code { background:rgba(255,255,255,.75); padding:1px 6px; border-radius:6px;
                font-size:.82rem; color:#44538A; }

.mr-term {
    border-right:5px solid var(--mr-soft);
    background:linear-gradient(270deg,var(--mr-b1),#FFFFFF 85%);
    border-radius:14px 4px 4px 14px; padding:14px 18px; margin:10px 0;
}
.mr-term .ar { font-weight:800; font-size:1.06rem; color:var(--mr-ink); }
.mr-term .en { direction:ltr; text-align:right; font-family:'JetBrains Mono',monospace;
               font-size:.78rem; color:#8A96B8; margin-top:2px; }
.mr-term .body { font-size:.96rem; line-height:1.98; color:#36446E; margin-top:8px; }
.mr-term .body b { color:var(--mr-ink); }
.mr-term ul { margin:6px 0 0; padding-right:1.1rem; padding-left:0; }

.mr-quote {
    border-radius:16px; padding:18px 22px; margin:14px 0;
    background:linear-gradient(135deg,#FFFDF6,#FFF6E6);
    border:1px dashed #EBD7AC;
}
.mr-quote .q { font-size:1.03rem; line-height:2.05; color:#6B5520; font-weight:600; }
.mr-quote .src { margin-top:8px; font-size:.82rem; color:#A08A52; }

.mr-key {
    border-radius:18px; padding:18px 22px; margin:16px 0;
    background:linear-gradient(135deg,#F0FBF6,#E6F7F0);
    border:1px solid #BCE6D5;
}
.mr-key h4 { margin:0 0 10px; color:#1E8E6A; font-weight:800; font-size:1.05rem; }
.mr-key ol { margin:0; padding-right:1.3rem; padding-left:0; }
.mr-key li { font-size:.97rem; line-height:2; color:#2A4A3E; margin-bottom:5px; }
.mr-key b { color:#13765A; }

.mr-sec { display:flex; align-items:center; gap:12px; margin:28px 0 10px; }
.mr-sec .bar { width:6px; height:34px; border-radius:6px;
               background:linear-gradient(180deg,#8192EC,#5CC6A4); flex:none; }
.mr-sec .txt h3 { margin:0; font-size:1.34rem; font-weight:800; color:#22305A; }
.mr-sec .txt .en { direction:ltr; text-align:right; font-size:.74rem; font-weight:700;
                   color:#8A96B8; letter-spacing:.7px; text-transform:uppercase; }

.mr-chips { display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 4px; }
.mr-chip { direction:ltr; font-size:.78rem; font-weight:700; padding:5px 12px; border-radius:999px;
           background:#EEF2FF; color:#4457CF; border:1px solid #D3DDF8; }

.mr-footer {
    margin-top:34px; padding:18px 22px; border-radius:18px; text-align:center;
    background:linear-gradient(135deg,#F6F8FF,#FFF7F9);
    border:1px solid #E5EAFA; color:#5B6894; font-size:.88rem; line-height:1.95;
}
.mr-footer b { color:#3A4BBF; }

.mr-grid2 { display:grid; grid-template-columns:repeat(auto-fit,minmax(265px,1fr)); gap:12px; }

.mr-step { display:flex; gap:14px; align-items:flex-start; padding:14px 16px; margin:8px 0;
           border-radius:16px; background:linear-gradient(270deg,var(--mr-b1),#FFF 92%);
           border:1px solid var(--mr-line); }
.mr-step .num { flex:none; width:38px; height:38px; border-radius:12px; display:grid; place-items:center;
                font-weight:800; color:#fff; background:var(--mr-soft); font-size:1rem; }
.mr-step .t { font-weight:800; color:var(--mr-ink); font-size:1.01rem; margin-bottom:2px; }
.mr-step .d { font-size:.95rem; line-height:1.92; color:#37456E; }
.mr-step .d b { color:var(--mr-ink); }
.mr-step .e { direction:ltr; text-align:right; font-size:.72rem; color:#939FBE;
              font-family:'JetBrains Mono',monospace; margin-bottom:4px; }

.mr-compare { display:grid; grid-template-columns:1fr 1fr; gap:0; border-radius:18px;
              overflow:hidden; border:1px solid #DFE5F7; margin:12px 0; }
.mr-compare > div { padding:16px 18px; }
.mr-compare .l { background:linear-gradient(145deg,#F2F4FF,#E6EBFF); }
.mr-compare .r { background:linear-gradient(145deg,#EFFBF7,#DFF6EE); }
.mr-compare h5 { margin:0 0 8px; font-size:1.02rem; font-weight:800; }
.mr-compare .l h5 { color:#3A4BBF; } .mr-compare .r h5 { color:#1E8E6A; }
.mr-compare ul { margin:0; padding-right:1.1rem; padding-left:0; }
.mr-compare li { font-size:.93rem; line-height:1.9; color:#33416D; }
@media (max-width: 720px) { .mr-compare { grid-template-columns:1fr; } }
</style>
"""


def inject_global_css() -> None:
    """تُستدعى مرّة واحدة في الملف الرئيسي."""
    st.html(_GLOBAL_CSS)


# ----------------------------------------------------------------------
# مكوّنات جاهزة
# ----------------------------------------------------------------------
def _tv(t: str) -> str:
    c = tone(t)
    return (
        f"--mr-b1:{c['bg1']};--mr-b2:{c['bg2']};--mr-line:{c['line']};"
        f"--mr-ink:{c['ink']};--mr-soft:{c['soft']};"
    )


def tone_vars(t: str) -> str:
    """متغيّرات CSS للّون المطلوب — واجهة عامّة لـ _tv."""
    return _tv(t)


def hero(title_ar: str, title_en: str, lead: str, kicker: str = "محور نظري") -> None:
    st.html(
        f"""<div class="mr-hero mr-anim">
  <div class="mr-hero-kicker">&#9679; {_html.escape(kicker)}</div>
  <h1>{_html.escape(title_ar)}</h1>
  <div class="en">{_html.escape(title_en)}</div>
  <p class="lead">{lead}</p>
</div>"""
    )


def section(title_ar: str, title_en: str) -> None:
    st.html(
        f"""<div class="mr-sec mr-anim"><div class="bar"></div>
  <div class="txt"><h3>{_html.escape(title_ar)}</h3>
  <div class="en">{_html.escape(title_en)}</div></div></div>"""
    )


def card(title: str, body: str, en: str = "", t: str = "indigo", icon: str = "") -> None:
    tag = f'<span class="en-tag">{_html.escape(en)}</span>' if en else ""
    head = f"{icon} {_html.escape(title)}" if icon else _html.escape(title)
    st.html(f'<div class="mr-card mr-anim" style="{_tv(t)}"><h4>{head}{tag}</h4>{body}</div>')


def term(ar: str, en: str, body: str, t: str = "indigo") -> None:
    st.html(
        f"""<div class="mr-term mr-anim" style="{_tv(t)}">
  <div class="ar">{_html.escape(ar)}</div>
  <div class="en">{_html.escape(en)}</div>
  <div class="body">{body}</div></div>"""
    )


def quote(text: str, source: str = "") -> None:
    src = f'<div class="src">— {_html.escape(source)}</div>' if source else ""
    st.html(f'<div class="mr-quote mr-anim"><div class="q">&laquo; {text} &raquo;</div>{src}</div>')


def key_points(title: str, points: list[str]) -> None:
    items = "".join(f"<li>{p}</li>" for p in points)
    st.html(f'<div class="mr-key mr-anim"><h4>{_html.escape(title)}</h4><ol>{items}</ol></div>')


def chips(labels: list[str]) -> None:
    st.html(
        "<div class='mr-chips mr-anim'>"
        + "".join(f"<span class='mr-chip'>{_html.escape(x)}</span>" for x in labels)
        + "</div>"
    )


def steps(items: list[tuple[str, str, str]], t: str = "auto") -> None:
    """items = [(العنوان, المصطلح الإنجليزي, الشرح HTML), ...]"""
    out = []
    for i, (title, en, desc) in enumerate(items, 1):
        tn = TONE_CYCLE[(i - 1) % len(TONE_CYCLE)] if t == "auto" else t
        out.append(
            f"""<div class="mr-step mr-anim" style="{_tv(tn)};animation-delay:{i * 0.05:.2f}s">
  <div class="num">{i}</div>
  <div><div class="t">{_html.escape(title)}</div>
  <div class="e">{_html.escape(en)}</div>
  <div class="d">{desc}</div></div></div>"""
        )
    st.html("".join(out))


def cards_grid(items: list[tuple[str, str, str, str]]) -> None:
    """items = [(العنوان, المصطلح الإنجليزي, المتن HTML, اللون), ...]"""
    out = []
    for i, (title, en, body, t) in enumerate(items):
        out.append(
            f"""<div class="mr-card" style="{_tv(t)};animation-delay:{i * 0.05:.2f}s">
  <h4>{_html.escape(title)}<span class="en-tag">{_html.escape(en)}</span></h4>{body}</div>"""
        )
    st.html("<div class='mr-grid2 mr-anim'>" + "".join(out) + "</div>")


def compare(left_title: str, left_items: list[str], right_title: str, right_items: list[str]) -> None:
    lhs = "".join(f"<li>{x}</li>" for x in left_items)
    rhs = "".join(f"<li>{x}</li>" for x in right_items)
    st.html(
        f"""<div class="mr-compare mr-anim">
  <div class="l"><h5>{_html.escape(left_title)}</h5><ul>{lhs}</ul></div>
  <div class="r"><h5>{_html.escape(right_title)}</h5><ul>{rhs}</ul></div>
</div>"""
    )


def footer(page_note: str = "") -> None:
    note = f"<div>{page_note}</div>" if page_note else ""
    st.html(
        f"""<div class="mr-footer mr-anim">{note}
  <div>منصّة <b>{PLATFORM_AR}</b> &mdash; إعداد <b>{AUTHOR_AR}</b></div>
  <div style="direction:ltr">{PLATFORM_EN} &middot; <b>{AUTHOR_EN}</b></div>
</div>"""
    )
