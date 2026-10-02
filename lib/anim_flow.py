"""
رسوم متحرّكة للمحور الإجرائي: البروتوكول الكامل، التحقّق من البيانات،
وأشجار القرار المنهجية.

Animated diagrams for the operational-protocol pages.

Author: Dr Merwan Roudane
"""

from __future__ import annotations

from lib.anim import _DEFS, _FILL, _box, split2


# ======================================================================
#  أداة مساعدة: شجرة قرار من اليمين إلى اليسار
# ======================================================================
def _tree(root_ar: str, root_en: str, leaves: list[tuple[str, str, str, str]],
          note: str = "", w: int = 700) -> str:
    """leaves = [(شرط الفرع, العنوان, المصطلح الإنجليزي, اللون), ...]"""
    n = len(leaves)
    lh = 62
    top = 30
    total = n * lh
    g = [_DEFS]
    cy = top + total / 2 - lh / 2 + 12

    # الجذر
    g.append(f'<rect x="{w - 214}" y="{cy - 40}" width="196" height="80" rx="18" '
             f'fill="url(#gIndigo)" stroke="#B9C4F4" stroke-width="2" class="mra-pop"/>')
    g.append(f'<text x="{w - 116}" y="{cy - 8}" text-anchor="middle" '
             f'style="font-family:Cairo,sans-serif;font-size:12.5px;font-weight:800;'
             f'fill:#3A4BBF">{root_ar}</text>')
    g.append(f'<text x="{w - 116}" y="{cy + 12}" class="mra-te" text-anchor="middle">{root_en}</text>')

    for i, (cond, ar, en, t) in enumerate(leaves):
        y = top + i * lh + 24
        fill, stroke, ink = _FILL[t]
        g.append(f'<path d="M {w - 218} {cy} C {w - 300} {cy}, {w - 320} {y}, {w - 400} {y}" '
                 f'fill="none" stroke="#C6D0F2" stroke-width="2.3" class="mra-flow" '
                 f'marker-end="url(#arrI)" style="animation-delay:{i * .12:.2f}s"/>')
        g.append(f'<text x="{w - 310}" y="{y - 8}" class="mra-ts" text-anchor="middle" '
                 f'style="font-size:10px">{cond}</text>')
        g.append(f'<g class="mra-pop" style="animation-delay:{0.1 + i * .1:.2f}s">'
                 f'<rect x="{w - 660}" y="{y - 22}" width="256" height="44" rx="14" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.7"/>'
                 f'<text x="{w - 532}" y="{y - 3}" text-anchor="middle" style="font-family:Cairo,'
                 f'sans-serif;font-size:12px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{w - 532}" y="{y + 13}" class="mra-te" text-anchor="middle">{en}</text></g>')

    h = top + total + (36 if note else 16)
    if note:
        g.append(f'<text x="{w / 2}" y="{h - 10}" class="mra-ts" text-anchor="middle">{note}</text>')
    return f'<svg viewBox="0 0 {w} {h}">{"".join(g)}</svg>'


# ======================================================================
#  1 — الخريطة الكاملة: اثنتا عشرة مرحلة
# ======================================================================
def master_protocol() -> str:
    phases = [
        ("السؤال الميداني", "business question", "amber"),
        ("صياغة المسألة", "problem framing", "amber"),
        ("تحديد وحدة التحليل", "unit of analysis", "sky"),
        ("جمع البيانات", "data collection", "sky"),
        ("التحقّق من البيانات", "data validation", "rose"),
        ("التقسيم المبكّر", "split FIRST", "rose"),
        ("الاستكشاف", "EDA on train only", "violet"),
        ("هندسة الميزات", "feature engineering", "violet"),
        ("خطّ الأساس", "baseline", "teal"),
        ("النمذجة والضبط", "model & tune", "teal"),
        ("التقييم النهائي", "final evaluation", "indigo"),
        ("النشر والمراقبة", "deploy & monitor", "indigo"),
    ]
    bw, bh, gap = 150, 74, 18
    xs = [56 + i * (bw + gap) for i in range(4)]          # 56, 224, 392, 560
    rows_y = [78, 204, 330]
    g = [_DEFS]

    for idx, (ar, en, t) in enumerate(phases):
        r, c = divmod(idx, 4)
        # الصفّ الزوجي يسير من اليمين إلى اليسار، والفردي بالعكس (مسار متعرّج)
        x = xs[3 - c] if r % 2 == 0 else xs[c]
        y = rows_y[r]
        g.append(_box(x, y, bw, bh, ar, en, t, idx * 0.07, 16, 12.5))
        g.append(f'<circle cx="{x + bw - 14}" cy="{y + 13}" r="11" fill="#FFFFFF" '
                 f'stroke="{_FILL[t][1]}" stroke-width="1.5"/>')
        g.append(f'<text x="{x + bw - 14}" y="{y + 17}" text-anchor="middle" '
                 f'style="font-family:JetBrains Mono,monospace;font-size:10px;font-weight:700;'
                 f'fill:{_FILL[t][2]}">{idx + 1}</text>')

        if idx == len(phases) - 1:
            break
        nr, nc = divmod(idx + 1, 4)
        nx = xs[3 - nc] if nr % 2 == 0 else xs[nc]
        ny = rows_y[nr]
        if nr == r:  # داخل الصفّ نفسه
            if nx < x:
                g.append(f'<path d="M {x} {y + bh / 2:.0f} L {nx + bw + 4} {y + bh / 2:.0f}" '
                         f'stroke="#C6D0F2" stroke-width="2.4" class="mra-flow" marker-end="url(#arrI)"/>')
            else:
                g.append(f'<path d="M {x + bw} {y + bh / 2:.0f} L {nx - 4} {y + bh / 2:.0f}" '
                         f'stroke="#C6D0F2" stroke-width="2.4" class="mra-flow" marker-end="url(#arrI)"/>')
        else:  # نزول إلى الصفّ التالي
            g.append(f'<path d="M {x + bw / 2:.0f} {y + bh} L {nx + bw / 2:.0f} {ny - 4}" '
                     f'stroke="#C6D0F2" stroke-width="2.4" class="mra-flow" marker-end="url(#arrI)"/>')

    # حلقة راجعة كبرى: من التقييم النهائي عودةً إلى صياغة السؤال،
    # تمرّ في قناتين خاليتين (يسار الرسم وأعلاه) حتّى لا تقطع أيّ صندوق.
    g.append('<path d="M 56 367 L 30 367 L 30 46 L 635 46 L 635 74" fill="none" '
             'stroke="#EE8A9C" stroke-width="2.2" stroke-dasharray="7 8" '
             'class="mra-back" marker-end="url(#arrR)"/>')
    g.append('<text x="300" y="32" class="mra-ts" text-anchor="middle" style="fill:#C24A5E;'
             'font-size:10.5px">حلقة راجعة: ما يكشفه التقييم يُعيدك إلى الصياغة أو البيانات</text>')
    g.append('<text x="380" y="428" class="mra-ts" text-anchor="middle">'
             'اقرأ المسار متعرّجًا: من اليمين إلى اليسار، ثمّ انزل واعكس الاتّجاه</text>')
    return f'<svg viewBox="0 0 760 442">{"".join(g)}</svg>'


# ======================================================================
#  2 — تشريح المرحلة الواحدة: مُدخَل · عمل · مُخرَج · بوّابة
# ======================================================================
def phase_anatomy() -> str:
    g = [_DEFS]
    items = [
        (516, "المُدخَل", "input", "amber", "ما الذي يصلني من المرحلة السابقة؟"),
        (352, "العمل", "work", "indigo", "ما الذي أفعله بالضبط هنا؟"),
        (188, "المُخرَج", "output", "teal", "ما الأثر الملموس الذي أُسلّمه؟"),
    ]
    for i, (x, ar, en, t, q) in enumerate(items):
        g.append(_box(x, 44, 150, 70, ar, en, t, i * .12, 16, 15))
        g.append(f'<text x="{x + 75}" y="134" class="mra-ts" text-anchor="middle" '
                 f'style="font-size:10px">{q}</text>')
        if i < 2:
            g.append(f'<path d="M {x} 79 L {items[i + 1][0] + 154} 79" stroke="#C6D0F2" '
                     f'stroke-width="2.6" class="mra-flow" marker-end="url(#arrI)"/>')
    # البوّابة
    g.append('<path d="M 184 79 L 150 79" stroke="#EBA85A" stroke-width="2.6" '
             'class="mra-flow" marker-end="url(#arrA)"/>')
    g.append('<path d="M 76 44 L 142 79 L 76 114 L 10 79 Z" fill="url(#gAmber)" '
             'stroke="#F3D6A6" stroke-width="2" class="mra-pulse"/>')
    g.append('<text x="76" y="76" text-anchor="middle" style="font-family:Cairo,sans-serif;'
             'font-size:12px;font-weight:800;fill:#B9772A">بوّابة</text>')
    g.append('<text x="76" y="92" class="mra-te" text-anchor="middle">gate</text>')
    g.append('<text x="76" y="134" class="mra-ts" text-anchor="middle" style="font-size:10px">'
             'لا أعبر قبل أن أُجيب</text>')
    g.append('<text x="350" y="166" class="mra-ts" text-anchor="middle">'
             'لكلّ مرحلة <tspan class=mra-b>بوّابة عبور</tspan>: سؤالٌ إن لم تُجب عنه بوضوح فلا تنتقل — '
             'وإلّا ورثت الغموض كلّه إلى ما بعده</text>')
    return f'<svg viewBox="0 0 700 178">{"".join(g)}</svg>'


# ======================================================================
#  3 — الترتيب الآمن للعمليات (مقابل الترتيب المُسرِّب)
# ======================================================================
def safe_order() -> str:
    g = [_DEFS]
    # الترتيب الخاطئ
    g.append('<rect x="14" y="14" width="672" height="104" rx="18" fill="#FFF3F5" stroke="#F6C9D2"/>')
    g.append('<text x="350" y="34" class="mra-ts" text-anchor="middle" style="fill:#C24A5E">'
             'الترتيب المُسرِّب · the leaking order</text>')
    wrong = [(500, "كلّ البيانات", "all data"), (330, "تحضير + تقييس", "fit scaler on ALL"),
             (160, "ثمّ التقسيم", "then split")]
    for i, (x, ar, en) in enumerate(wrong):
        g.append(f'<rect x="{x}" y="46" width="160" height="50" rx="13" fill="#FFE7EC" '
                 f'stroke="#F4BCC8" stroke-width="1.6" class="mra-pop" style="animation-delay:{i * .1:.2f}s"/>')
        g.append(f'<text x="{x + 80}" y="68" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:12px;font-weight:800;fill:#C24A5E">{ar}</text>')
        g.append(f'<text x="{x + 80}" y="84" class="mra-te" text-anchor="middle">{en}</text>')
        if i < 2:
            g.append(f'<path d="M {x} 71 L {wrong[i + 1][0] + 164} 71" stroke="#EE8A9C" '
                     f'stroke-width="2.4" class="mra-flow" marker-end="url(#arrR)"/>')
    g.append('<text x="84" y="76" text-anchor="middle" style="font-family:Cairo,sans-serif;'
             'font-size:13px;font-weight:800;fill:#C24A5E">تسرّب</text>')

    # الترتيب الصحيح
    g.append('<rect x="14" y="132" width="672" height="104" rx="18" fill="#F1FBF6" stroke="#C2E8D8"/>')
    g.append('<text x="350" y="152" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'الترتيب الآمن · the safe order</text>')
    right = [(500, "كلّ البيانات", "all data"), (330, "التقسيم أوّلًا", "split FIRST"),
             (160, "تحضير على التدريب", "fit on train only"), (18, "تطبيق على الباقي", "transform")]
    for i, (x, ar, en) in enumerate(right):
        w = 160 if i < 3 else 132
        g.append(f'<rect x="{x}" y="164" width="{w}" height="50" rx="13" fill="#E3F7EE" '
                 f'stroke="#A9E0CC" stroke-width="1.6" class="mra-pop" style="animation-delay:{i * .1:.2f}s"/>')
        g.append(f'<text x="{x + w / 2}" y="186" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:12px;font-weight:800;fill:#1E8E6A">{ar}</text>')
        g.append(f'<text x="{x + w / 2}" y="202" class="mra-te" text-anchor="middle">{en}</text>')
        if i < 3:
            g.append(f'<path d="M {x} 189 L {right[i + 1][0] + (164 if i < 2 else 136)} 189" '
                     f'stroke="#5CC6A4" stroke-width="2.4" class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<text x="350" y="258" class="mra-ts" text-anchor="middle">'
             'قاعدة واحدة لا استثناء لها: <tspan class=mra-b>قسِّم قبل أن تلمس أيّ شيء</tspan></text>')
    return f'<svg viewBox="0 0 700 270">{"".join(g)}</svg>'


# ======================================================================
#  4 — طبقات التحقّق من البيانات
# ======================================================================
def data_contract() -> str:
    layers = [
        ("البنية", "schema", "هل الأعمدة المتوقَّعة موجودة بأنواعها؟", 620, "sky"),
        ("المجال", "range &amp; domain", "هل القيم داخل الحدود المعقولة؟", 540, "teal"),
        ("التفرّد", "uniqueness", "هل المعرّف فريد؟ هل ثمّة تكرار؟", 460, "mint"),
        ("الاكتمال", "completeness", "ما نسبة النقص في كلّ عمود؟ وما آليّته؟", 380, "amber"),
        ("الاتّساق", "consistency", "هل العلاقات بين الأعمدة منطقية؟", 300, "violet"),
        ("التمثيل", "representativeness", "هل العيّنة تمثّل من ستُطبَّق عليهم؟", 220, "rose"),
    ]
    g = [_DEFS]
    for i, (ar, en, q, w, t) in enumerate(layers):
        fill, stroke, ink = _FILL[t]
        x = (700 - w) / 2
        y = 20 + i * 46
        g.append(f'<g class="mra-slide" style="animation-delay:{i * .11:.2f}s">'
                 f'<rect x="{x:.0f}" y="{y}" width="{w}" height="38" rx="12" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.7"/>'
                 f'<text x="350" y="{y + 17}" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:12px;font-weight:800;fill:{ink}">{ar} · <tspan class="mra-te">{en}</tspan></text>'
                 f'<text x="350" y="{y + 32}" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:10px;fill:#4A5881">{q}</text></g>')
        if i < len(layers) - 1:
            g.append(f'<path d="M 350 {y + 38} L 350 {y + 44}" stroke="{stroke}" stroke-width="2.2" '
                     f'marker-end="url(#arrI)"/>')
    g.append('<text x="350" y="316" class="mra-ts" text-anchor="middle">'
             'ستّ طبقات تُفحَص <tspan class=mra-b>قبل</tspan> أيّ نموذج — وكلّ طبقة تُكتب كاختبار آليّ يُعاد تشغيله</text>')
    g.append('<text x="350" y="336" class="mra-te" text-anchor="middle">'
             'a data contract, not a one-off inspection</text>')
    return f'<svg viewBox="0 0 700 348">{"".join(g)}</svg>'


# ======================================================================
#  5 — كلمة «تحقّق» بثلاثة معانٍ في المشروع نفسه
# ======================================================================
def three_validations() -> str:
    items = [
        ("التحقّق من البيانات", "data validation", "هل البيانات سليمة وصالحة للاستعمال؟",
         "قبل كلّ شيء", "sky"),
        ("مجموعة التحقّق", "validation set", "أيّ نموذج ومُعاملات فائقة أختار؟",
         "أثناء النمذجة", "indigo"),
        ("التحقّق من النموذج", "model validation", "هل افتراضات النموذج صحيحة ويمثّل الواقع؟",
         "بعد التقدير", "violet"),
    ]
    g = [_DEFS]
    for i, (ar, en, q, when, t) in enumerate(items):
        q1, q2 = split2(q, 26)
        x = 24 + (2 - i) * 222
        fill, stroke, ink = _FILL[t]
        g.append(f'<g class="mra-pop" style="animation-delay:{i * .13:.2f}s">'
                 f'<rect x="{x}" y="38" width="208" height="124" rx="18" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.9"/>'
                 f'<text x="{x + 104}" y="70" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:13px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="{x + 104}" y="87" class="mra-te" text-anchor="middle">{en}</text>'
                 f'<text x="{x + 104}" y="114" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:10.5px;fill:#4A5881">{q1}</text>'
                 f'<text x="{x + 104}" y="130" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:10.5px;fill:#4A5881">{q2}</text>'
                 f'<text x="{x + 104}" y="151" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:10px;font-weight:700;fill:{ink}">{when}</text></g>')
    g.append('<text x="350" y="24" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'ثلاث عمليّات مختلفة تحمل الاسم نفسه في المشروع الواحد</text>')
    g.append('<text x="350" y="186" class="mra-ts" text-anchor="middle">'
             'حدّد دائمًا أيّ تحقّقٍ تقصد — فالثلاثة تقع في مراحل مختلفة ولأهداف مختلفة</text>')
    return f'<svg viewBox="0 0 700 198">{"".join(g)}</svg>'


# ======================================================================
#  6 — أشجار القرار
# ======================================================================
def problem_type_tree() -> str:
    return _tree(
        "ما طبيعة المُخرَج الذي تريده؟", "what is the output?",
        [
            ("فئة من مجموعة منتهية", "تصنيف", "classification", "indigo"),
            ("قيمة عددية متّصلة", "انحدار", "regression", "teal"),
            ("لا مُخرَج معلوم أصلًا", "تجميع أو تقليص أبعاد", "clustering / dim-reduction", "amber"),
            ("حالات نادرة جدًّا ومتنوّعة", "كشف شذوذ", "anomaly detection", "rose"),
            ("سلسلة قرارات بمكافأة", "تعلّم معزّز", "reinforcement learning", "violet"),
        ],
        "والسؤال السابق على هذا كلّه: <tspan class=mra-b>هل يحتاج الأمر تعلّم آلة أصلًا، أم تكفي قاعدة؟</tspan>",
    )


def split_decision_tree() -> str:
    return _tree(
        "ما بنية بياناتك؟", "what structure does the data have?",
        [
            ("ترتيب زمني يهمّ", "تقسيم زمني", "TimeSeriesSplit", "rose"),
            ("عدّة صفوف لنفس الكيان", "تقسيم بالمجموعات", "GroupKFold", "amber"),
            ("جوار مكاني", "تقسيم مكاني", "spatial / block split", "violet"),
            ("فئات غير متوازنة", "تقسيم طبقي", "StratifiedKFold", "sky"),
            ("لا شيء ممّا سبق", "تقسيم عشوائي", "KFold", "teal"),
        ],
        "<tspan class=mra-b>التقسيم العشوائي هو الحالة الأخيرة لا الأولى</tspan> — افحص البنية قبل أن تقسم",
    )


def metric_decision_tree() -> str:
    return _tree(
        "ما طبيعة الهدف وكلفة الخطأ؟", "target type and cost of error",
        [
            ("انحدار · الأخطاء الكبيرة أخطر", "RMSE", "root mean squared error", "indigo"),
            ("انحدار · فيه شواذّ حقيقية", "MAE أو هوبر", "MAE / Huber", "teal"),
            ("تصنيف متوازن", "دقّة و F1", "accuracy / F1", "sky"),
            ("تصنيف · الفئة نادرة", "PR-AUC أو الاسترجاع عند k", "PR-AUC / Recall@k", "rose"),
            ("القيمة الاحتمالية نفسها مستعملة", "لوغاريتمية أو برير", "log loss / Brier", "violet"),
        ],
        "واذكر دائمًا <tspan class=mra-b>خطّ أساس</tspan> بجانب المقياس — فالرقم وحده لا يعني شيئًا",
    )


# ======================================================================
#  7 — سُلّم خطوط الأساس
# ======================================================================
def baseline_ladder() -> str:
    rungs = [
        ("تخمين عشوائي", "random guess", 200, "sand"),
        ("الفئة الأشيع / المتوسّط", "majority class / mean", 260, "amber"),
        ("قاعدة ميدانية بسيطة", "simple domain rule", 320, "sky"),
        ("أداء الخبير البشري الحالي", "current human performance", 380, "teal"),
        ("أفضل ما نُشر في الأدبيات", "published state of the art", 440, "violet"),
    ]
    g = [_DEFS]
    for i, (ar, en, w, t) in enumerate(rungs):
        fill, stroke, ink = _FILL[t]
        y = 214 - i * 42
        x = (700 - w) / 2
        g.append(f'<g class="mra-slide" style="animation-delay:{i * .12:.2f}s">'
                 f'<rect x="{x:.0f}" y="{y}" width="{w}" height="36" rx="12" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.7"/>'
                 f'<text x="350" y="{y + 16}" text-anchor="middle" style="font-family:Cairo,sans-serif;'
                 f'font-size:12px;font-weight:800;fill:{ink}">{ar}</text>'
                 f'<text x="350" y="{y + 30}" class="mra-te" text-anchor="middle">{en}</text></g>')
        if i < len(rungs) - 1:
            g.append(f'<path d="M 350 {y} L 350 {y - 6}" stroke="{stroke}" stroke-width="2.2" '
                     f'marker-end="url(#arrI)"/>')
    g.append('<text x="350" y="24" class="mra-ts" text-anchor="middle" style="fill:#7149C6">'
             'نموذجك يجب أن يتسلّق هذا السُّلّم — ويُبلَّغ عن كلّ درجة بلغها</text>')
    g.append('<text x="350" y="276" class="mra-ts" text-anchor="middle">'
             'من لم يذكر خطّ الأساس، لم يُبلّغ نتيجةً بل رقمًا معلّقًا في الفراغ</text>')
    return f'<svg viewBox="0 0 700 288">{"".join(g)}</svg>'


# ======================================================================
#  8 — توزيع الجهد الحقيقي عبر المراحل
# ======================================================================
def effort_bars() -> str:
    rows = [
        ("صياغة السؤال وفهم الميدان", "framing", 12, "amber"),
        ("جمع البيانات والوصول إليها", "collection", 18, "sky"),
        ("التحقّق والتنظيف والتحضير", "validation &amp; cleaning", 35, "rose"),
        ("الاستكشاف وهندسة الميزات", "EDA &amp; features", 18, "violet"),
        ("النمذجة والضبط", "modelling", 8, "indigo"),
        ("التقييم والتفسير", "evaluation", 9, "teal"),
    ]
    g = [_DEFS]
    g.append('<text x="350" y="22" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'توزيع الزمن الحقيقي في مشروع حقيقي — لا كما يُتخيَّل</text>')
    for i, (ar, en, pct, t) in enumerate(rows):
        fill, stroke, ink = _FILL[t]
        y = 42 + i * 44
        bw = pct * 7
        g.append(f'<text x="676" y="{y + 20}" class="mra-ts" text-anchor="end" '
                 f'style="font-size:11.5px">{ar}</text>')
        g.append(f'<rect x="{326 - bw}" y="{y + 4}" width="{bw}" height="26" rx="8" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.5" class="mra-pop" '
                 f'style="animation-delay:{i * .12:.2f}s"/>')
        g.append(f'<text x="{322 - bw}" y="{y + 22}" text-anchor="end" class="mra-te" '
                 f'style="fill:{ink};font-size:11px">{pct}%</text>')
        g.append(f'<text x="330" y="{y + 32}" class="mra-te" text-anchor="start" '
                 f'style="font-size:9px">{en}</text>')
    g.append('<text x="350" y="316" class="mra-ts" text-anchor="middle">'
             'الجزء «الممتع» — النمذجة — أقلّ من <tspan class=mra-b>عُشر</tspan> المشروع</text>')
    return f'<svg viewBox="0 0 700 328">{"".join(g)}</svg>'
