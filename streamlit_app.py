"""
منصّة « أسس التعلّم في الذكاء الاصطناعي »
Foundations of Learning in Artificial Intelligence — an Arabic, theory-first platform.

إعداد: الدكتور مروان رودان — Dr Merwan Roudane
"""

from __future__ import annotations

import streamlit as st

from lib import anim, ui

st.set_page_config(
    page_title="أسس التعلّم في الذكاء الاصطناعي — Dr Merwan Roudane",
    page_icon=":material/neurology:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# حقن الأنماط العامة (RTL + الشريط الجانبي على اليمين + الرسوم المتحركة)
ui.inject_global_css()
anim.inject_anim_css()


def P(path: str, title: str, icon: str, default: bool = False):
    return st.Page(f"app_pages/{path}", title=title, icon=icon, default=default)


NAV = {
    "FOUNDATIONS": [
        P("home.py", "الرئيسية · Home", ":material/home:", default=True),
        P("what_is_learning.py", "ما معنى التعلّم؟ · Learning", ":material/psychology:"),
        P("intelligence.py", "الذكاء والآلة · Intelligence", ":material/smart_toy:"),
        P("ai_map.py", "خريطة الميدان · AI Map", ":material/map:"),
    ],
    "PHILOSOPHY": [
        P("induction.py", "الاستقراء والاستنباط · Induction", ":material/compare_arrows:"),
        P("algorithm_model.py", "خوارزمية أم نموذج؟ · Model", ":material/memory:"),
        P("who_learns.py", "من يتعلّم؟ · Who Learns", ":material/help_center:"),
        P("model_life.py", "حياة النموذج · Model Life", ":material/timeline:"),
        P("term_traps.py", "فخاخ المصطلحات · Term Traps", ":material/translate:"),
        P("function_hypothesis.py", "فضاء الفرضيات · Hypothesis", ":material/function:"),
        P("inductive_bias.py", "الانحياز الاستقرائي · Bias", ":material/balance:"),
    ],
    "DATA & STATISTICS": [
        P("data_anatomy.py", "تشريح البيانات · Data Anatomy", ":material/table_chart:"),
        P("features_targets.py", "الميزات والتسميات · Labels", ":material/label:"),
        P("statistics.py", "الجذور الإحصائية · Statistics", ":material/analytics:"),
        P("probability.py", "الاحتمال · Probability", ":material/casino:"),
    ],
    "PARADIGMS OF LEARNING": [
        P("supervised.py", "التعلّم بإشراف · Supervised", ":material/school:"),
        P("unsupervised.py", "التعلّم بلا إشراف · Unsupervised", ":material/bubble_chart:"),
        P("other_paradigms.py", "أنماط أخرى · Paradigms", ":material/alt_route:"),
    ],
    "TRAINING": [
        P("training.py", "ما معنى التدريب؟ · Training", ":material/fitness_center:"),
        P("loss_optimisation.py", "الخسارة والأمثَلة · Loss", ":material/trending_down:"),
    ],
    "EVALUATION": [
        P("generalization.py", "التعميم · Generalisation", ":material/insights:"),
        P("evaluation.py", "التقييم · Evaluation", ":material/fact_check:"),
    ],
    "PRACTICE & PROTOCOL": [
        P("workflow.py", "دورة المشروع · Workflow", ":material/lan:"),
        P("protocol.py", "البروتوكول الكامل · Protocol", ":material/checklist_rtl:"),
        P("data_validation.py", "التحقّق من البيانات · Validation", ":material/fact_check:"),
        P("decision_guide.py", "دليل القرارات · Decisions", ":material/account_tree:"),
        P("pitfalls.py", "المزالق · Pitfalls", ":material/warning:"),
        P("ethics.py", "الأخلاق · Ethics", ":material/gavel:"),
    ],
    "REFERENCE": [
        P("glossary.py", "المعجم · Glossary", ":material/menu_book:"),
        P("roadmap.py", "خارطة الطريق · Roadmap", ":material/flag:"),
        P("about.py", "عن المنصّة · About", ":material/person:"),
    ],
}

page = st.navigation(NAV, position="sidebar")

# ---------------------------------------------------------------- الشريط الجانبي
with st.sidebar:
    st.html(
        """<div style="padding:14px 14px 12px;margin-bottom:6px;border-radius:16px;
                       background:linear-gradient(140deg,#FFFFFF,#E9EFFF);
                       border:1px solid #D3DDF8;text-align:center">
  <div style="font-family:Tajawal,sans-serif;font-size:1.02rem;font-weight:800;color:#2C3A6B;line-height:1.6">
    أسس التعلّم في الذكاء الاصطناعي</div>
  <div style="direction:ltr;font-size:.66rem;font-weight:700;color:#7C89B0;
              letter-spacing:.6px;margin-top:3px">FOUNDATIONS OF AI LEARNING</div>
  <div style="margin-top:9px;padding-top:8px;border-top:1px dashed #C9D4F2;
              font-size:.76rem;color:#55639A">إعداد <b style="color:#3A4BBF">الدكتور مروان رودان</b></div>
  <div style="direction:ltr;font-size:.68rem;color:#8A96B8">Dr Merwan Roudane</div>
</div>"""
    )

    st.html(
        """<div style="padding:10px 12px;border-radius:14px;background:#FFFFFFAA;
                       border:1px dashed #C9D4F2;font-size:.75rem;color:#5B6894;line-height:1.85">
  هذه منصّة <b>نظريّة</b> بالدرجة الأولى: هدفها أن تفهم <b>جوهر</b> الأفكار
  ومعانيها قبل أن تكتب سطرًا واحدًا من الشيفرة.</div>"""
    )

    st.html(
        f"""<div style="margin-top:12px;padding-top:10px;border-top:1px solid #D3DDF8;
                        font-size:.7rem;color:#8A96B8;text-align:center;line-height:1.7">
  {len([p for v in NAV.values() for p in v])} صفحة · 8 محاور<br>
  <span style="direction:ltr">© 2026 Dr Merwan Roudane</span></div>"""
    )

page.run()
