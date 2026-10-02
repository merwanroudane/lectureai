"""
رسوم متحرّكة لتصنيف أنواع التعلّم الأربعة عشر (تصنيف Jason Brownlee).

Animated diagrams for the fourteen types of learning.

Author: Dr Merwan Roudane
"""

from __future__ import annotations

from lib.anim import _DEFS, _FILL, _box, split2


# ======================================================================
#  1 — خريطة الأنواع الأربعة عشر
# ======================================================================
def taxonomy_14() -> str:
    groups = [
        ("مسائل التعلّم", "LEARNING PROBLEMS", "indigo",
         [("التعلّم بإشراف", "supervised"), ("التعلّم بلا إشراف", "unsupervised"),
          ("التعلّم المعزّز", "reinforcement")]),
        ("مسائل هجينة", "HYBRID PROBLEMS", "teal",
         [("شبه المُشرَف", "semi-supervised"), ("الذاتي الإشراف", "self-supervised"),
          ("متعدّد النُّسخ", "multi-instance")]),
        ("الاستدلال الإحصائي", "STATISTICAL INFERENCE", "violet",
         [("التعلّم الاستقرائي", "inductive"), ("الاستنباط", "deductive"),
          ("التعلّم النَّقْلي", "transductive")]),
        ("تقنيات التعلّم", "LEARNING TECHNIQUES", "amber",
         [("متعدّد المهامّ", "multi-task"), ("التعلّم النشط", "active"),
          ("التعلّم على الخطّ", "online"), ("التعلّم بالنقل", "transfer"),
          ("التجميع", "ensemble")]),
    ]
    cw, gap = 160, 18
    xs = [24 + i * (cw + gap) for i in range(4)]       # 24, 202, 380, 558
    g = [_DEFS]
    g.append('<text x="368" y="20" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'أربعة عشر نوعًا في أربع مجموعات — والمجموعات نفسها ليست من رتبة واحدة</text>')
    for i, (ar, en, t, members) in enumerate(groups):
        x = xs[3 - i]                                  # من اليمين إلى اليسار
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .12:.2f}s">'
                 f'<rect x="{x}" y="32" width="{cw}" height="48" rx="14" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2"/>'
                 f'<text x="{x + cw / 2}" y="54" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:13px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{x + cw / 2}" y="70" class="mra-te" text-anchor="middle" '
                 f'style="font-size:8.5px">{en}</text></g>')
        for j, (m_ar, m_en) in enumerate(members):
            y = 94 + j * 50
            g.append(f'<g class="mra-slide" style="animation-delay:{0.15 + i * .08 + j * .06:.2f}s">'
                     f'<rect x="{x + 6}" y="{y}" width="{cw - 12}" height="40" rx="11" '
                     f'fill="#FFFFFF" stroke="{stroke}" stroke-width="1.4"/>'
                     f'<text x="{x + cw / 2}" y="{y + 18}" text-anchor="middle" '
                     f'style="font-family:Cairo,sans-serif;font-size:11.5px;font-weight:700;'
                     f'fill:#33416D">{m_ar}</text>'
                     f'<text x="{x + cw / 2}" y="{y + 32}" class="mra-te" text-anchor="middle" '
                     f'style="font-size:8.5px">{m_en}</text></g>')
            g.append(f'<path d="M {x + cw / 2} {y - 12} L {x + cw / 2} {y - 4}" '
                     f'stroke="{stroke}" stroke-width="1.6" opacity=".7"/>')
    g.append('<text x="368" y="368" class="mra-ts" text-anchor="middle">'
             'المجموعتان الأوليان <tspan class=mra-b>مسائل</tspan>، والثالثة <tspan class=mra-b>منطقُ استدلال</tspan>، والرابعة <tspan class=mra-b>تقنيات</tspan> '
             'تُركَّب فوق أيّ مسألة</text>')
    return f'<svg viewBox="0 0 736 380">{"".join(g)}</svg>'


# ======================================================================
#  2 — التعلّم متعدّد النُّسخ: الحقيبة مُسمّاة والنُّسخ ليست كذلك
# ======================================================================
def multi_instance() -> str:
    import math
    import random

    random.seed(17)
    bags = [
        (520, "حقيبة 1", "موجبة  +", "teal", True),
        (300, "حقيبة 2", "سالبة  −", "rose", False),
        (80, "حقيبة 3", "؟ نتنبّأ بها", "sky", None),
    ]
    g = [_DEFS]
    g.append('<text x="350" y="20" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'التسمية على <tspan class=mra-b>الحقيبة</tspan> كلّها، لا على كلّ نسخة داخلها</text>')
    for bi, (x, name, lab, t, positive) in enumerate(bags):
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{bi * .14:.2f}s">'
                 f'<rect x="{x}" y="40" width="160" height="122" rx="20" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2.2"/></g>')
        for k in range(7):
            a = random.uniform(0, 6.283)
            r = random.uniform(10, 44)
            px = x + 80 + r * math.cos(a)
            py = 100 + r * math.sin(a) * 0.62
            # نسخة واحدة فقط «موجبة» حقًّا داخل الحقيبة الموجبة — والبقية مجهولة
            special = bool(positive) and k == 2
            col = "#1E8E6A" if special else "#AEBBE0"
            rr = 7 if special else 5.5
            cls = "mra-pulse" if special else ""
            g.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr}" fill="{col}" '
                     f'class="{cls}" opacity=".92"/>')
        g.append(f'<text x="{x + 80}" y="180" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:12.5px;font-weight:800;fill:{ink}">{name}</text>')
        g.append(f'<text x="{x + 80}" y="198" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:11.5px;font-weight:700;fill:{ink}">{lab}</text>')
    g.append('<text x="350" y="228" class="mra-ts" text-anchor="middle">'
             'تكفي <tspan class=mra-b>نسخة واحدة موجبة</tspan> لتصير الحقيبة موجبة — ولا نعرف أيّها هي</text>')
    g.append('<text x="350" y="248" class="mra-te" text-anchor="middle">'
             'a bag is positive if at least one instance is — but which one is unknown</text>')
    return f'<svg viewBox="0 0 700 260">{"".join(g)}</svg>'


# ======================================================================
#  3 — الاستقراء والاستنباط والنَّقْل
# ======================================================================
def three_inferences() -> str:
    g = [_DEFS]
    # القاعدة العامّة في القمّة
    g.append(_box(250, 26, 200, 66, "قاعدة عامّة / نموذج", "a general model", "violet", 0.1, 18, 13))
    # الأمثلة المُسمّاة (يمين) والنقاط المطلوبة (يسار)
    g.append(_box(470, 178, 200, 66, "أمثلة مُسمّاة", "labelled examples", "amber", 0, 18, 14))
    g.append(_box(30, 178, 200, 66, "نقاط نريد قيمتها", "points of interest", "sky", 0.2, 18, 13))

    # استقراء: من الأمثلة صعودًا إلى القاعدة
    g.append('<path d="M 520 174 C 500 130, 480 108, 452 90" fill="none" stroke="#EBA85A" '
             'stroke-width="3" class="mra-flow" marker-end="url(#arrA)"/>')
    g.append('<text x="516" y="120" class="mra-ts" text-anchor="middle" style="fill:#B9772A">استقراء</text>')
    g.append('<text x="516" y="136" class="mra-te" text-anchor="middle">induction</text>')

    # استنباط: من القاعدة نزولًا إلى النقاط
    g.append('<path d="M 248 90 C 220 108, 200 130, 180 174" fill="none" stroke="#A98BEB" '
             'stroke-width="3" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="186" y="120" class="mra-ts" text-anchor="middle" style="fill:#7149C6">استنباط</text>')
    g.append('<text x="186" y="136" class="mra-te" text-anchor="middle">deduction</text>')

    # نقل: مباشرةً من الأمثلة إلى النقاط دون المرور بالقمّة
    g.append('<path d="M 466 211 L 236 211" fill="none" stroke="#5CC6A4" stroke-width="3.4" '
             'stroke-dasharray="9 7" class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<text x="350" y="200" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'نَقْل · transduction</text>')
    g.append('<text x="350" y="268" class="mra-ts" text-anchor="middle">'
             'النَّقْل يقفز من الجزئي إلى الجزئي <tspan class=mra-b>دون بناء قاعدة عامّة أصلًا</tspan> — '
             'وهذا بالضبط ما يفعله k-أقرب جار</text>')
    g.append('<text x="350" y="288" class="mra-te" text-anchor="middle">'
             'Vapnik (1995): solve the problem you need, not a more general one</text>')
    return f'<svg viewBox="0 0 700 300">{"".join(g)}</svg>'


# ======================================================================
#  4 — التجميع: عدّة نماذج ثمّ دمج
# ======================================================================
def ensemble_vote() -> str:
    g = [_DEFS]
    g.append(_box(540, 96, 140, 70, "البيانات", "training data", "amber", 0, 16, 15))
    preds = [("نموذج 1", "0.81", "indigo", 18), ("نموذج 2", "0.74", "teal", 96),
             ("نموذج 3", "0.88", "sky", 174)]
    for i, (name, p, t, y) in enumerate(preds):
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{0.1 + i * .12:.2f}s">'
                 f'<rect x="320" y="{y}" width="150" height="54" rx="14" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.8"/>'
                 f'<text x="395" y="{y + 23}" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:12.5px;font-weight:800;fill:{ink}">{name}</text>'
                 f'<text x="395" y="{y + 40}" class="mra-m" text-anchor="middle">ŷ = {p}</text></g>')
        g.append(f'<path d="M 534 131 C 500 131, 500 {y + 27}, 474 {y + 27}" fill="none" '
                 f'stroke="#C6D0F2" stroke-width="2.3" class="mra-flow" marker-end="url(#arrI)" '
                 f'style="animation-delay:{i * .15:.2f}s"/>')
        g.append(f'<path d="M 316 {y + 27} C 280 {y + 27}, 270 131, 234 131" fill="none" '
                 f'stroke="#A9E0CC" stroke-width="2.3" class="mra-flow" marker-end="url(#arrT)" '
                 f'style="animation-delay:{i * .15:.2f}s"/>')
    g.append(_box(80, 96, 150, 70, "الدمج", "aggregate", "mint", 0.5, 16, 15))
    g.append('<path d="M 76 131 L 44 131" fill="none" stroke="#5CC6A4" stroke-width="2.6" '
             'class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<text x="24" y="136" class="mra-m" text-anchor="middle" style="fill:#1E8E6A">0.81</text>')
    g.append('<text x="350" y="256" class="mra-ts" text-anchor="middle">'
             'المتوسّط أو التصويت <tspan class=mra-b>يُقلّل التباين</tspan> دون أن يرفع التحيّز — وهذا كلّ سرّ الغابة العشوائية</text>')
    return f'<svg viewBox="0 0 700 268">{"".join(g)}</svg>'


# ======================================================================
#  5 — متعدّد المهامّ (بالتوازي) مقابل النقل (بالتتابع)
# ======================================================================
def multitask_vs_transfer() -> str:
    g = [_DEFS]
    # متعدّد المهامّ
    g.append('<rect x="14" y="14" width="672" height="112" rx="18" fill="#F4F7FF" stroke="#D5DEF7"/>')
    g.append('<text x="350" y="34" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'متعدّد المهامّ · multi-task — المهامّ تُتعلَّم <tspan class=mra-b>معًا</tspan></text>')
    g.append(_box(500, 46, 150, 62, "جذع مشترك", "shared trunk", "indigo", 0, 15, 13))
    for i, (ar, en) in enumerate([("مهمّة أ", "task A"), ("مهمّة ب", "task B")]):
        y = 44 + i * 36
        g.append(f'<rect x="300" y="{y}" width="128" height="30" rx="10" fill="url(#gTeal)" '
                 f'stroke="#A9E0CC" stroke-width="1.5" class="mra-pop" '
                 f'style="animation-delay:{0.1 + i * .1:.2f}s"/>')
        g.append(f'<text x="364" y="{y + 20}" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:11.5px;font-weight:700;fill:#1E8E6A">{ar} · '
                 f'<tspan class="mra-te">{en}</tspan></text>')
        g.append(f'<path d="M 496 77 C 470 77, 460 {y + 15}, 432 {y + 15}" fill="none" '
                 f'stroke="#C6D0F2" stroke-width="2.2" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="180" y="82" class="mra-ts" text-anchor="middle" style="font-size:10.5px">'
             'الإشارات تتبادل الفائدة وتعمل كانتظام متبادل</text>')

    # النقل
    g.append('<rect x="14" y="142" width="672" height="112" rx="18" fill="#F1FBF6" stroke="#C2E8D8"/>')
    g.append('<text x="350" y="162" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'التعلّم بالنقل · transfer — المهامّ تُتعلَّم <tspan class=mra-b>بالتتابع</tspan></text>')
    g.append(_box(500, 176, 150, 62, "مهمّة أ", "pre-training", "amber", .2, 15, 14))
    g.append(_box(290, 176, 150, 62, "نقل التمثيل", "frozen / fine-tuned", "violet", .3, 15, 12))
    g.append(_box(80, 176, 150, 62, "مهمّة ب", "downstream task", "mint", .4, 15, 14))
    g.append('<path d="M 496 207 L 448 207" stroke="#C6D0F2" stroke-width="2.4" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<path d="M 286 207 L 238 207" stroke="#A9E0CC" stroke-width="2.4" '
             'class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<text x="350" y="276" class="mra-ts" text-anchor="middle">'
             'الفرق ليس في النتيجة بل في <tspan class=mra-b>الزمن</tspan>: بالتوازي أم بالتتابع</text>')
    return f'<svg viewBox="0 0 700 288">{"".join(g)}</svg>'


# ======================================================================
#  6 — محاور التصنيف: لماذا لا تتنافى الأنواع؟
# ======================================================================
def orthogonal_axes() -> str:
    axes = [
        ("ما شكل الخبرة؟", "form of experience", "تسميات · بلا تسميات · مكافأة · حقائب", "indigo"),
        ("ما منطق الاستدلال؟", "logic of inference", "استقراء · استنباط · نَقْل", "violet"),
        ("متى تصل البيانات؟", "when data arrives", "دفعة واحدة · تدفّق مستمرّ", "sky"),
        ("من يختار الأمثلة؟", "who picks examples", "المصمّم · النموذج نفسه", "teal"),
        ("كم مهمّة وكم نموذجًا؟", "tasks and models", "مهمّة واحدة · عدّة مهامّ · عدّة نماذج", "amber"),
    ]
    g = [_DEFS]
    g.append('<text x="350" y="20" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'الأنواع الأربعة عشر <tspan class=mra-b>ليست أقسامًا متنافية</tspan> — إنّها إجابات على أسئلة مختلفة</text>')
    for i, (q, en, opts, t) in enumerate(axes):
        fill, stroke, ink = _FILL[t]
        y = 36 + i * 54
        g.append(f'<g class="mra-slide" style="animation-delay:{i * .11:.2f}s">'
                 f'<rect x="384" y="{y}" width="292" height="44" rx="13" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.7"/>'
                 f'<text x="530" y="{y + 19}" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:12px;font-weight:800;fill:{ink}">{q}</text>'
                 f'<text x="530" y="{y + 34}" class="mra-te" text-anchor="middle">{en}</text>'
                 f'<rect x="24" y="{y}" width="330" height="44" rx="13" fill="#FBFCFF" '
                 f'stroke="#E2E8FA" stroke-width="1.4"/>'
                 f'<text x="189" y="{y + 27}" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:11px;fill:#3C4A72">{opts}</text>'
                 f'<path d="M 380 {y + 22} L 358 {y + 22}" stroke="{stroke}" stroke-width="2.2" '
                 f'marker-end="url(#arrI)"/></g>')
    g.append('<text x="350" y="324" class="mra-ts" text-anchor="middle">'
             'مشروع واحد قد يكون <tspan class=mra-b>مُشرَفًا + بالنقل + على الخطّ + مجمَّعًا</tspan> في آنٍ واحد</text>')
    return f'<svg viewBox="0 0 700 336">{"".join(g)}</svg>'
