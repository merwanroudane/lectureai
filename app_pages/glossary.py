"""المعجم المصطلحي — Bilingual glossary."""

import html

import streamlit as st

from lib import ui
from lib.content import CATEGORIES, GLOSSARY

ui.hero(
    "المعجم المصطلحي",
    "Bilingual glossary — Arabic / English",
    "كلّ مصطلح في هذه المنصّة مقرونٌ بمقابله الإنجليزي، لأنّ الأدبيات العلمية إنجليزية "
    "وستقرأها بالإنجليزية حتمًا. ابحث هنا بالعربية أو بالإنجليزية، "
    "أو تصفّح حسب المحور.",
    kicker="المحور الثامن · المرجع",
)

m1, m2, m3 = st.columns(3)
m1.metric("عدد المصطلحات", f"⁦{len(GLOSSARY)}⁩", border=True)
m2.metric("عدد المحاور", f"⁦{len(CATEGORIES)}⁩", border=True)
m3.metric("لغتان", "AR · EN", border=True)

# ----------------------------------------------------------------------
query = st.text_input(
    "ابحث عن مصطلح · search (Arabic or English)",
    placeholder="مثال: overfitting  ·  أو: التعميم  ·  أو: bias",
    key="gl_q",
)

cats = st.pills(
    "المحاور · filter by section",
    options=CATEGORIES,
    selection_mode="multi",
    default=None,
    key="gl_cats",
)

selected = set(cats) if cats else set(CATEGORIES)
q = (query or "").strip().lower()


def _match(row: tuple[str, str, str, str]) -> bool:
    en, ar, cat, definition = row
    if cat not in selected:
        return False
    if not q:
        return True
    return q in en.lower() or q in ar.lower() or q in definition.lower()


rows = [r for r in GLOSSARY if _match(r)]

st.caption(f"عُثر على **{len(rows)}** مصطلحًا من أصل **{len(GLOSSARY)}**.")

TONE_BY_CAT = {
    "الأسس والمفاهيم": "amber",
    "الفلسفة ونظرية المعرفة": "violet",
    "البيانات والإحصاء": "sky",
    "أنماط التعلّم": "indigo",
    "التدريب والأمثَلة": "teal",
    "التعميم والتقييم": "rose",
    "الممارسة والأخلاق": "mint",
}

if not rows:
    st.info(
        "لا نتائج لهذا البحث. جرّب كلمةً أقصر، أو امسح المرشّحات، "
        "أو ابحث بالمصطلح الإنجليزي.",
        icon=":material/search_off:",
    )
else:
    current = None
    for en, ar, cat, definition in sorted(rows, key=lambda r: (CATEGORIES.index(r[2]), r[0].lower())):
        if cat != current:
            current = cat
            ui.section(cat, cat)
        st.html(
            f"""<div class="mr-term" style="{ui.tone_vars(TONE_BY_CAT.get(cat, 'indigo'))}">
  <div class="ar">{html.escape(ar)}</div>
  <div class="en">{html.escape(en)}</div>
  <div class="body">{html.escape(definition)}</div>
</div>"""
        )

ui.footer("الصفحة التالية: <b>خارطة الطريق</b> — ماذا تدرس بعد هذه المنصّة؟")
