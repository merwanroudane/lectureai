"""
رسوم متحرّكة لمحاور التمييز الاصطلاحي:
حياة النموذج، والأصدقاء الكاذبون، وفخاخ المصطلحات.

Animated diagrams for the terminology-precision pages.

Author: Dr Merwan Roudane
"""

from __future__ import annotations

from lib.anim import _DEFS, _FILL, _box, split2


# ======================================================================
#  1 — حياة النموذج: مُقدِّر غير مُلائَم ← fit ← نموذج مُلائَم
# ======================================================================
def estimator_lifecycle() -> str:
    g = [_DEFS]
    # الكائن قبل الملاءمة (يمين)
    g.append('<rect x="440" y="38" width="234" height="150" rx="18" fill="url(#gAmber)" '
             'stroke="#F3D6A6" stroke-width="1.8" class="mra-pop"/>')
    g.append('<text x="557" y="22" class="mra-ts" text-anchor="middle" style="fill:#B9772A">'
             'قبل التدريب · unfitted estimator</text>')
    g.append('<text x="557" y="68" text-anchor="middle" style="font-family:Cairo;font-size:14px;'
             'font-weight:800;fill:#B9772A">مُقدِّر مُهيَّأ فقط</text>')
    g.append('<text x="557" y="92" class="mra-m" text-anchor="middle">Ridge(alpha=1.0)</text>')
    g.append('<text x="557" y="118" class="mra-ts" text-anchor="middle">يحمل المُعاملات الفائقة</text>')
    g.append('<text x="557" y="140" class="mra-ts" text-anchor="middle">ولا يحمل أيّ شيء من البيانات</text>')
    g.append('<text x="557" y="168" class="mra-te" text-anchor="middle">no learned state yet</text>')

    # السهم
    g.append('<path d="M 434 113 L 300 113" stroke="#8192EC" stroke-width="3.4" fill="none" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="367" y="98" class="mra-m" text-anchor="middle">.fit(X, y)</text>')
    g.append('<text x="367" y="134" class="mra-ts" text-anchor="middle">حدَثُ التدريب</text>')

    # الكائن بعد الملاءمة (يسار)
    g.append('<rect x="26" y="38" width="234" height="150" rx="18" fill="url(#gTeal)" '
             'stroke="#A9E0CC" stroke-width="1.8" class="mra-pop" style="animation-delay:.5s"/>')
    g.append('<text x="143" y="22" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'بعد التدريب · fitted model</text>')
    g.append('<text x="143" y="66" text-anchor="middle" style="font-family:Cairo;font-size:14px;'
             'font-weight:800;fill:#1E8E6A">نموذج مُلائَم</text>')
    for i, attr in enumerate(["coef_", "intercept_", "n_features_in_"]):
        y = 92 + i * 26
        g.append(f'<rect x="48" y="{y - 14}" width="190" height="21" rx="7" fill="#FFFFFF" '
                 f'stroke="#BFE7D6" class="mra-blink" style="animation-delay:{0.8 + i * .2:.1f}s"/>')
        g.append(f'<text x="143" y="{y}" class="mra-m" text-anchor="middle" '
                 f'style="fill:#1E8E6A">{attr}</text>')
    g.append('<text x="143" y="178" class="mra-te" text-anchor="middle">'
             'trailing underscore = learned state</text>')

    g.append('<text x="350" y="212" class="mra-ts" text-anchor="middle">'
             'إنّه <tspan style="font-weight:800;fill:#C24A5E">الكائن نفسه</tspan> في الشيفرة '
             '— ولهذا بالضبط يقع الالتباس بين الخوارزمية والنموذج</text>')
    g.append('<text x="350" y="232" class="mra-te" text-anchor="middle">'
             'same Python object, mutated in place by fit()</text>')
    return f'<svg viewBox="0 0 700 242">{"".join(g)}</svg>'


# ======================================================================
#  2 — كلمة «استدلال» لها معنيان متعاكسان
# ======================================================================
def two_inferences() -> str:
    g = [_DEFS]
    # الاستدلال الإحصائي
    g.append('<rect x="14" y="14" width="672" height="104" rx="18" fill="#F4F7FF" stroke="#D5DEF7"/>')
    g.append('<text x="350" y="34" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'الاستدلال الإحصائي · Statistical inference</text>')
    g.append(_box(470, 44, 190, 58, "عيّنة مرصودة", "sample", "amber", 0, 14, 13))
    g.append(_box(44, 44, 190, 58, "معلمة المجتمع", "population parameter", "violet", .2, 14, 12))
    g.append('<path d="M 466 73 L 240 73" stroke="#8192EC" stroke-width="3" fill="none" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="352" y="62" class="mra-ts" text-anchor="middle">نستدلّ على <b>المجهول</b></text>')
    g.append('<text x="352" y="92" class="mra-te" text-anchor="middle">reasoning about what we cannot see</text>')

    # الاستدلال في تعلّم الآلة
    g.append('<rect x="14" y="132" width="672" height="104" rx="18" fill="#F1FBF6" stroke="#C2E8D8"/>')
    g.append('<text x="350" y="152" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'الاستدلال في تعلّم الآلة · ML inference (serving)</text>')
    g.append(_box(470, 162, 190, 58, "نموذج + مُدخَل", "model + x_new", "teal", .3, 14, 12))
    g.append(_box(44, 162, 190, 58, "تنبّؤ", "prediction ŷ", "mint", .45, 14, 13))
    g.append('<path d="M 466 191 L 240 191" stroke="#5CC6A4" stroke-width="3" fill="none" '
             'class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<text x="352" y="180" class="mra-ts" text-anchor="middle">نُشغّل <b>المعلوم</b></text>')
    g.append('<text x="352" y="210" class="mra-te" text-anchor="middle">just running a fixed function</text>')

    g.append('<text x="350" y="260" class="mra-ts" text-anchor="middle">'
             'كلمةٌ واحدة، عمليّتان مختلفتان تمامًا — وهذا أشهر «صديق كاذب» في الميدان</text>')
    return f'<svg viewBox="0 0 700 272">{"".join(g)}</svg>'


# ======================================================================
#  3 — مَعلَمي مقابل لا مَعلَمي: هل تنمو الحالة المتعلَّمة مع البيانات؟
# ======================================================================
def parametric_vs_nonparametric() -> str:
    g = [_DEFS]
    g.append('<rect x="24" y="16" width="652" height="206" rx="18" fill="#FCFDFF" stroke="#E6ECFA"/>')
    g.append('<line x1="72" y1="206" x2="640" y2="206" stroke="#C9D3FB" stroke-width="1.6"/>')
    g.append('<line x1="72" y1="206" x2="72" y2="40" stroke="#C9D3FB" stroke-width="1.6"/>')
    # لا مَعلَمي — ينمو
    pts = " L ".join(f"{72 + i * 14},{200 - i * 3.7:.0f}" for i in range(41))
    g.append(f'<path d="M {pts}" fill="none" stroke="#EE8A9C" stroke-width="3.4" '
             f'stroke-dasharray="900" stroke-dashoffset="900" '
             f'style="animation:mraDraw 2.4s .3s ease-out forwards"/>')
    # مَعلَمي — ثابت
    g.append('<path d="M 72 166 L 632 166" fill="none" stroke="#5CC6A4" stroke-width="3.4" '
             'stroke-dasharray="900" stroke-dashoffset="900" '
             'style="animation:mraDraw 2.4s .1s ease-out forwards"/>')
    g.append('<text x="624" y="44" class="mra-ts" text-anchor="end" style="fill:#C24A5E">'
             'لا مَعلَمي — k-NN، الأشجار العميقة، العمليات الغاوسية</text>')
    g.append('<text x="624" y="60" class="mra-te" text-anchor="end">'
             'non-parametric: state grows with n</text>')
    g.append('<text x="624" y="156" class="mra-ts" text-anchor="end" style="fill:#1E8E6A">'
             'مَعلَمي — الانحدار الخطّي، اللوجستي، الشبكة ذات البنية المثبَّتة</text>')
    g.append('<text x="624" y="190" class="mra-te" text-anchor="end">'
             'parametric: state size fixed in advance</text>')
    g.append('<text x="356" y="228" class="mra-te" text-anchor="middle">'
             'n  —  training sample size →</text>')
    g.append('<text x="84" y="36" class="mra-te" text-anchor="start">|learned state|</text>')
    g.append('<text x="350" y="252" class="mra-ts" text-anchor="middle">'
             'السؤال الفاصل ليس «كم معاملًا؟» بل: <b>هل يتحدّد عددها قبل رؤية البيانات؟</b></text>')
    return f'<svg viewBox="0 0 700 264">{"".join(g)}</svg>'


# ======================================================================
#  4 — تعلّم متلهّف مقابل تعلّم كسول: أين يقع الجهد؟
# ======================================================================
def eager_vs_lazy() -> str:
    g = [_DEFS]
    rows = [
        ("متلهّف · Eager", "الانحدار، الشجرة، الشبكة", "teal", 34, 150, 44),
        ("كسول · Lazy", "k-NN، الاستدلال القائم على الحالات", "rose", 136, 44, 150),
    ]
    for ar, note, t, y, w_fit, w_pred in rows:
        fill, stroke, ink = _FILL[t]
        g.append(f'<text x="676" y="{y + 14}" class="mra-ts" text-anchor="end" '
                 f'style="fill:{ink}">{ar}</text>')
        g.append(f'<text x="676" y="{y + 32}" class="mra-ts" text-anchor="end" '
                 f'style="font-size:10px">{note}</text>')
        # شريط التدريب
        g.append(f'<rect x="{380 - w_fit}" y="{y + 44}" width="{w_fit}" height="34" rx="10" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.6" class="mra-pop"/>')
        g.append(f'<text x="{380 - w_fit / 2}" y="{y + 66}" text-anchor="middle" '
                 f'style="font-family:Cairo;font-size:11px;font-weight:700;fill:{ink}">وقت التدريب</text>')
        # شريط التنبّؤ
        g.append(f'<rect x="{390 - w_fit - w_pred - 14}" y="{y + 44}" width="{w_pred}" height="34" rx="10" '
                 f'fill="#FFFFFF" stroke="{stroke}" stroke-width="1.6" stroke-dasharray="5 5" '
                 f'class="mra-pop" style="animation-delay:.2s"/>')
        g.append(f'<text x="{390 - w_fit - w_pred / 2 - 14}" y="{y + 66}" text-anchor="middle" '
                 f'style="font-family:Cairo;font-size:11px;font-weight:700;fill:{ink}">وقت التنبّؤ</text>')
    g.append('<text x="350" y="256" class="mra-ts" text-anchor="middle">'
             'الجهد الكلّي لا يختفي — بل <b>ينتقل</b>. والكسول يدفع الثمن في كلّ تنبّؤ.</text>')
    g.append('<text x="350" y="276" class="mra-te" text-anchor="middle">'
             'the work does not vanish, it moves</text>')
    return f'<svg viewBox="0 0 700 286">{"".join(g)}</svg>'


# ======================================================================
#  5 — كلمة «انحياز» بأربعة معانٍ مختلفة
# ======================================================================
def bias_four_meanings() -> str:
    panels = [
        ("الانحياز الإحصائي", "statistical bias", "فرقٌ منهجيّ بين التقدير والقيمة الحقيقية", "sky"),
        ("حدّ الانحياز", "bias term b", "المعامل الثابت المضاف داخل العصبون أو النموذج", "teal"),
        ("الانحياز الاستقرائي", "inductive bias", "الافتراضات التي تُرجّح فرضيةً على أخرى", "violet"),
        ("التحيّز الاجتماعي", "social bias", "ظلمٌ منهجيّ تجاه مجموعة بشرية", "rose"),
    ]
    g = [_DEFS]
    g.append('<text x="350" y="24" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'كلمة <tspan style="font-family:JetBrains Mono,monospace">bias</tspan> في بحثٍ واحد قد تحمل أربعة معانٍ لا صلة بينها</text>')
    for i, (ar, en, note, t) in enumerate(panels):
        n1, n2 = split2(note, 28)
        x = 20 + (3 - i) * 170
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .12:.2f}s">'
                 f'<rect x="{x}" y="42" width="160" height="112" rx="16" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.8"/>'
                 f'<text x="{x + 80}" y="72" text-anchor="middle" style="font-family:Cairo;'
                 f'font-size:12.5px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{x + 80}" y="89" class="mra-te" text-anchor="middle">{en}</text>'
                 f'<text x="{x + 80}" y="116" text-anchor="middle" style="font-family:Cairo;'
                 f'font-size:10px;fill:#4A5881">{n1}</text>'
                 f'<text x="{x + 80}" y="132" text-anchor="middle" style="font-family:Cairo;'
                 f'font-size:10px;fill:#4A5881">{n2}</text></g>')
    g.append('<text x="350" y="178" class="mra-ts" text-anchor="middle">'
             'اكتب دائمًا أيّ انحياز تقصد — فالقارئ لا يملك ما في ذهنك</text>')
    return f'<svg viewBox="0 0 700 190">{"".join(g)}</svg>'


# ======================================================================
#  6 — الخسارة ودالّة الهدف والمقياس: ثلاث طبقات لا واحدة
# ======================================================================
def loss_objective_metric() -> str:
    g = [_DEFS]
    layers = [
        (520, "خسارة المثال", "loss  L(yᵢ, ŷᵢ)", "sky", "لكلّ مثال على حدة"),
        (356, "الخطر التجريبي", "empirical risk  (1/n)ΣL", "indigo", "متوسّط على الدفعة"),
        (192, "دالّة الهدف", "objective  = risk + λΩ(θ)", "violet", "ما يُحسَّن فعلًا"),
        (28, "المقياس المُبلَّغ", "reported metric", "amber", "ما يُكتب في البحث"),
    ]
    for i, (x, ar, en, t, note) in enumerate(layers):
        g.append(_box(x, 48, 152, 72, ar, en, t, i * .12, 16, 13))
        g.append(f'<text x="{x + 76}" y="138" class="mra-ts" text-anchor="middle" '
                 f'style="font-size:10.5px">{note}</text>')
        if i < 3:
            g.append(f'<path d="M {x} 84 L {layers[i + 1][0] + 156} 84" stroke="#C6D0F2" '
                     f'stroke-width="2.6" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<path d="M 180 44 C 180 18, 600 18, 596 44" stroke="#EE8A9C" stroke-width="2.4" '
             'fill="none" stroke-dasharray="6 6" class="mra-back" marker-end="url(#arrR)"/>')
    g.append('<text x="388" y="26" class="mra-ts" text-anchor="middle" style="fill:#C24A5E">'
             'انتبه: المقياس الذي تُبلّغه ليس بالضرورة ما حسّنته الخوارزمية</text>')
    g.append('<text x="350" y="166" class="mra-te" text-anchor="middle">'
             'what you optimise ≠ what you report</text>')
    return f'<svg viewBox="0 0 700 178">{"".join(g)}</svg>'


# ======================================================================
#  7 — النموذج متغيّر عشوائي: نفس البيانات، بذور مختلفة
# ======================================================================
def stochastic_training() -> str:
    g = [_DEFS]
    g.append(_box(520, 80, 160, 74, "بيانات واحدة", "one dataset", "amber", 0, 16, 15))
    seeds = [("seed = 0", 14, "teal"), ("seed = 1", 92, "indigo"), ("seed = 2", 170, "rose")]
    for i, (lab, y, t) in enumerate(seeds):
        fill, stroke, ink = _FILL[t]
        g.append(f'<path d="M 514 117 C 440 117, 420 {y + 32}, 352 {y + 32}" fill="none" '
                 f'stroke="#C6D0F2" stroke-width="2.4" class="mra-flow" marker-end="url(#arrI)" '
                 f'style="animation-delay:{i * .18:.2f}s"/>')
        g.append(f'<text x="432" y="{y + 24}" class="mra-te" text-anchor="middle">{lab}</text>')
        g.append(f'<g class="mra-pop" style="animation-delay:{0.2 + i * .14:.2f}s">'
                 f'<rect x="96" y="{y + 8}" width="252" height="48" rx="14" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.7"/>'
                 f'<text x="222" y="{y + 32}" text-anchor="middle" style="font-family:Cairo;'
                 f'font-size:12px;font-weight:800;fill:{ink}">نموذج {i + 1}</text>'
                 f'<text x="222" y="{y + 47}" class="mra-te" text-anchor="middle">'
                 f'AUC = 0.8{3 + i}{1 + 2 * i}</text></g>')
    g.append('<text x="350" y="252" class="mra-ts" text-anchor="middle">'
             'نفس الخوارزمية + نفس البيانات ← <b>نماذج مختلفة</b>. '
             'النموذج إذن <b>متغيّر عشوائي</b>، لا شيء ثابت.</text>')
    g.append('<text x="350" y="272" class="mra-te" text-anchor="middle">'
             'always report the seed, and the variance across seeds</text>')
    return f'<svg viewBox="0 0 700 282">{"".join(g)}</svg>'


# ======================================================================
#  8 — من يفعل ماذا؟ سلسلة الفاعلين
# ======================================================================
def who_does_what() -> str:
    actors = [
        ("الباحث", "researcher", "يختار ويضبط ويحكم", "violet"),
        ("الخوارزمية", "algorithm", "تبحث وتستخرج", "indigo"),
        ("النموذج", "model", "يحمل ويتنبّأ", "teal"),
        ("البيانات", "data", "تُرصَد ولا تفعل شيئًا", "sand"),
    ]
    g = [_DEFS]
    g.append('<text x="350" y="22" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'اتّجاه الفعل يسير من اليمين إلى اليسار: الباحث يُشغّل الخوارزمية، '
             'والخوارزمية تُنتج النموذج، والنموذج يقرأ البيانات</text>')
    for i, (ar, en, verb, t) in enumerate(actors):
        x = 20 + (3 - i) * 170
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .12:.2f}s">'
                 f'<rect x="{x}" y="40" width="158" height="92" rx="16" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.8"/>'
                 f'<text x="{x + 79}" y="72" text-anchor="middle" style="font-family:Tajawal;'
                 f'font-size:16px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{x + 79}" y="89" class="mra-te" text-anchor="middle">{en}</text>'
                 f'<text x="{x + 79}" y="114" text-anchor="middle" style="font-family:Cairo;'
                 f'font-size:11px;fill:#4A5881">{verb}</text></g>')
        if i < 3:
            g.append(f'<path d="M {x} 86 L {x - 12} 86" stroke="#C6D0F2" stroke-width="2.4" '
                     f'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="350" y="158" class="mra-ts" text-anchor="middle">'
             '«البيانات تتعلّم» عبارة بلا معنى؛ و«ندرّب الخوارزمية» ملتبسة؛ '
             'و«نُدرّب النموذج بالخوارزمية» دقيقة</text>')
    return f'<svg viewBox="0 0 700 170">{"".join(g)}</svg>'
