"""عن المنصّة — About."""

import streamlit as st

from lib import anim, ui
from lib.content import GLOSSARY, platform_stats

ui.hero(
    "عن المنصّة",
    "About this platform",
    "منصّة نظريّة مُعمّقة في أسس التعلّم بالذكاء الاصطناعي، "
    "موجّهة إلى الباحثين وطلبة الدراسات العليا الذين يريدون أن يفهموا "
    "<b>جوهر الأفكار</b> قبل أن يكتبوا سطرًا من الشيفرة.",
    kicker="المحور الثامن · المرجع",
)

st.html(
    """<div style="border-radius:22px;padding:26px 30px;margin:6px 0 18px;
                   background:linear-gradient(135deg,#F3F6FF,#F7F1FF 55%,#EDFAF4);
                   border:1px solid #DDE4F8;text-align:center">
  <div style="font-size:.76rem;font-weight:800;letter-spacing:1px;color:#8392BE;direction:ltr">
    AUTHOR &amp; INSTRUCTOR</div>
  <div style="font-family:Tajawal,sans-serif;font-size:1.75rem;font-weight:800;
              color:#28356A;margin-top:8px">الدكتور مروان رودان</div>
  <div style="direction:ltr;font-size:1.02rem;font-weight:700;color:#5A6AE0;margin-top:2px">
    Dr Merwan Roudane</div>
  <div style="margin-top:14px;padding-top:12px;border-top:1px dashed #CBD6F3;
              font-size:.92rem;color:#56648F;line-height:2">
    إعداد المحتوى النظري · تصميم الرسوم التوضيحية · بناء المنصّة
  </div>
</div>"""
)

_s = platform_stats()
c1, c2, c3, c4 = st.columns(4)
c1.metric("محاور نظريّة", "⁦8⁩", border=True)
c2.metric("صفحات", f"⁦{_s['pages']}⁩", border=True)
c3.metric("رسوم متحرّكة", f"⁦{_s['diagrams']}⁩", border=True)
c4.metric("مصطلح في المعجم", f"⁦{len(GLOSSARY)}⁩", border=True)

# ======================================================================
ui.section("الفلسفة التي بُنيت عليها", "The philosophy behind it")

ui.cards_grid(
    [
        ("المعنى قبل الأداة", "meaning before tooling",
         "<p>لا سطر شيفرة واحدًا قبل أن يكون المفهوم واضحًا. "
         "من يفهم <b>لماذا</b> يستطيع إصلاح ما تعطّل؛ ومن يحفظ <b>كيف</b> يقف عاجزًا "
         "عند أوّل نتيجة غريبة.</p>", "indigo"),
        ("المصطلح بلغتيه", "both languages",
         "<p>كلّ مفهوم بالعربية مقرونٌ بمقابله الإنجليزي، "
         "لأنّ الأدبيات إنجليزية والفهم عربي — ولا تعارض بينهما.</p>", "teal"),
        ("الصورة تسبق الصيغة", "visual first",
         "<p>رسمٌ متحرّك واحد يُغني عن فقرة كاملة. "
         "كلّ فكرة بنيوية في المنصّة لها تمثيل بصري قبل أن تُكتب رياضيًّا.</p>", "amber"),
        ("الصدق المنهجي", "methodological honesty",
         "<p>ما تخفيه المقاييس يُذكر، وحدود كلّ أداة تُكتب، "
         "والمزالق تُعرض بوصفها جزءًا من المعرفة لا هامشًا عليها.</p>", "rose"),
    ]
)

# ======================================================================
ui.section("كيف نُظّمت المحاور", "How the sections are organised")

ui.steps(
    [
        ("الأسس", "Foundations",
         "ما معنى التعلّم؟ وما معنى الذكاء؟ وأين يقف تعلّم الآلة من الإحصاء وعلم البيانات؟"),
        ("الفلسفة ونظرية المعرفة", "Philosophy",
         "الاستقراء والاستنباط، الخوارزمية والنموذج، <b>من يتعلّم ومن يُدرَّب؟</b>، "
         "<b>حياة النموذج</b>، <b>فخاخ المصطلحات</b>، فضاء الفرضيات، الانحياز الاستقرائي."),
        ("البيانات والإحصاء", "Data &amp; Statistics",
         "تشريح البيانات، الميزة والهدف والتسمية، الجذور الإحصائية، الاحتمال وعدم اليقين."),
        ("أنماط التعلّم", "Paradigms",
         "تفكيك معنى «الإشراف»، التعلّم بلا إشراف، والأنماط الأخرى كلّها."),
        ("التدريب والأمثَلة", "Training",
         "ما يحدث حرفيًّا داخل الحلقة، ودالّة الخسارة، والمُحسِّنات، والانتظام."),
        ("التعميم والتقييم", "Generalisation",
         "التحيّز والتباين، إفراط التوفيق، البروتوكول النزيه، والمقاييس وما تُخفيه."),
        ("من النظرية إلى المشروع", "Practice",
         "دورة الحياة الكاملة، المزالق المنهجية، والمسؤولية الأخلاقية."),
        ("المرجع", "Reference",
         "معجم مصطلحي قابل للبحث، خارطة طريق، ومراجع مؤسِّسة."),
    ]
)

# ======================================================================
ui.section("ملاحظة تقنية", "A technical note")

ui.card(
    "كيف بُنيت هذه المنصّة",
    "<ul>"
    "<li><b>Streamlit</b> متعدّد الصفحات عبر <code>st.navigation</code> و<code>st.Page</code>.</li>"
    "<li>سمة فاتحة كاملة معرّفة في <code>.streamlit/config.toml</code> "
    "بخطوط <b>Cairo</b> و<b>Tajawal</b> العربية.</li>"
    "<li>اتّجاه <b>من اليمين إلى اليسار</b> مع شريط جانبي على اليمين، "
    "مع إبقاء الشيفرة والرياضيات بالاتّجاه اللاتيني.</li>"
    "<li>الرسوم <b>SVG متحرّكة بـ CSS و SMIL</b> دون أيّ JavaScript، "
    "تُعرض داخل إطارات مستقلّة لتحافظ على الخطوط والحركة.</li>"
    "<li>الرسوم البيانية التفاعلية بـ <b>Altair</b>، والحسابات مخزّنة بـ "
    "<code>st.cache_data</code>.</li>"
    "</ul>",
    en="implementation notes",
    t="violet",
)

anim.frame(
    anim.three_components(),
    "ونختم بما بدأنا به: كلّ خوارزمية تعلّم — مهما بلغت — تمثيلٌ وتقييمٌ وأمثَلة. لا رابع.",
    "Representation · Evaluation · Optimisation",
)

ui.quote(
    "الهدف من هذه المنصّة ليس أن تحفظ تعريفات، بل أن يتغيّر <b>نوع الأسئلة</b> "
    "التي تطرحها حين تجلس أمام بياناتك. فإن صرت تسأل: "
    "«ما انحيازي؟ وما هدفي البديل؟ ومن غاب عن عيّنتي؟ ومتى ينهار هذا؟» — "
    "فقد بلغت المقصود.",
    "الدكتور مروان رودان",
)

ui.footer("شكرًا على القراءة. ارجع إلى <b>المعجم</b> كلّما التبس عليك مصطلح.")
