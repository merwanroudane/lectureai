"""
رسوم متحرّكة إضافية خاصّة بمحور « من يتعلّم؟ ومن يُدرَّب؟ ».
Extra animated diagrams for the “who learns / who is trained” lecture.

Author: Dr Merwan Roudane
"""

from __future__ import annotations

from lib.anim import _DEFS, _box


# ======================================================================
#  السلسلة المركزية: خبرة ← خوارزمية ← تدريب ← حالة متعلَّمة ← نموذج
# ======================================================================
def learned_state_chain() -> str:
    boxes = [
        (556, "الخبرة", "Experience E", "amber"),
        (420, "خوارزمية التعلّم", "Learning Algorithm A", "indigo"),
        (284, "التدريب", "Training / Fitting", "violet"),
        (148, "الحالة المتعلَّمة", "Learned State", "teal"),
        (12, "نموذج مدرَّب", "Trained Model h", "sky"),
    ]
    g = [_DEFS]
    for i, (x, ar, en, t) in enumerate(boxes):
        fs = 15 if len(ar) < 12 else 12
        g.append(_box(x, 40, 124, 80, ar, en, t, i * 0.12, 16, fs))
        if i < len(boxes) - 1:
            x2 = boxes[i + 1][0] + 124
            g.append(
                f'<path d="M {x} 80 L {x2 + 4} 80" stroke="#C6D0F2" stroke-width="2.8" '
                f'class="mra-flow" marker-end="url(#arrI)" style="animation-delay:{i * .2:.1f}s"/>'
            )
    g.append('<text x="346" y="152" class="mra-ts" text-anchor="middle">'
             'ما نتعلّم منه · كيف نستفيد منه · تنفيذ العملية · ما اكتسبه النموذج · ما نستعمله بعدها</text>')
    g.append('<text x="346" y="174" class="mra-te" text-anchor="middle">'
             'h = A(S) — the one chain to remember</text>')
    return f'<svg viewBox="0 0 692 188">{"".join(g)}</svg>'


# ======================================================================
#  خوارزمية التعلّم ليست المُحسِّن
# ======================================================================
def optimizer_vs_algorithm() -> str:
    g = [_DEFS]
    g.append('<rect x="14" y="14" width="664" height="150" rx="20" fill="#F8FAFF" '
             'stroke="#DCE4F8" stroke-width="1.6" stroke-dasharray="8 8"/>')
    g.append('<text x="346" y="38" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'إجراء التدريب الكامل · training procedure</text>')
    items = [
        (520, "النموذج + البيانات", "model + data", "amber"),
        (356, "دالّة الهدف", "loss / objective", "rose"),
        (192, "المُحسِّن", "optimizer", "violet"),
        (34, "حالة محدَّثة", "updated θ", "teal"),
    ]
    for i, (x, ar, en, t) in enumerate(items):
        g.append(_box(x, 56, 142, 72, ar, en, t, i * 0.12, 16, 13))
        if i < len(items) - 1:
            x2 = items[i + 1][0] + 142
            g.append(f'<path d="M {x} 92 L {x2 + 4} 92" stroke="#C6D0F2" stroke-width="2.6" '
                     f'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<path d="M 34 132 C 34 192, 620 192, 662 132" stroke="#A9E0CC" stroke-width="2.6" '
             'fill="none" class="mra-back" marker-end="url(#arrT)"/>')
    g.append('<text x="346" y="216" class="mra-ts" text-anchor="middle">'
             'المُحسِّن جزءٌ من إجراء التدريب — وليس التدريب كلَّه، ولا هو النموذج</text>')
    return f'<svg viewBox="0 0 692 228">{"".join(g)}</svg>'


# ======================================================================
#  التدريب مقابل الاستدلال
# ======================================================================
def train_vs_infer() -> str:
    g = [_DEFS]
    g.append('<rect x="14" y="14" width="664" height="94" rx="18" fill="#F4F7FF" stroke="#D5DEF7"/>')
    g.append('<text x="346" y="34" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'التدريب · Training</text>')
    g.append(_box(498, 44, 152, 52, "بيانات التدريب", "D_train", "amber", 0, 13, 13))
    g.append(_box(298, 44, 152, 52, "خوارزمية التعلّم", "algorithm A", "indigo", .1, 13, 12))
    g.append(_box(108, 44, 152, 52, "حالة متعلَّمة", "learned state θ̂", "teal", .2, 13, 13))
    g.append('<path d="M 494 70 L 454 70" stroke="#C6D0F2" stroke-width="2.6" class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<path d="M 294 70 L 264 70" stroke="#C6D0F2" stroke-width="2.6" class="mra-flow" marker-end="url(#arrI)"/>')

    g.append('<rect x="14" y="126" width="664" height="94" rx="18" fill="#F1FBF6" stroke="#C2E8D8"/>')
    g.append('<text x="346" y="146" class="mra-ts" text-anchor="middle" style="fill:#1E8E6A">'
             'الاستدلال · Inference</text>')
    g.append(_box(498, 156, 152, 52, "مشاهدة جديدة", "x_new", "sky", .3, 13, 13))
    g.append(_box(298, 156, 152, 52, "النموذج المثبَّت", "f( · ; θ̂ )", "violet", .4, 13, 13))
    g.append(_box(108, 156, 152, 52, "تنبّؤ ŷ", "prediction", "mint", .5, 13, 13))
    g.append('<path d="M 494 182 L 454 182" stroke="#A9E0CC" stroke-width="2.6" class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<path d="M 294 182 L 264 182" stroke="#A9E0CC" stroke-width="2.6" class="mra-flow" marker-end="url(#arrT)"/>')
    g.append('<path d="M 184 100 L 184 152" stroke="#B9C4F4" stroke-width="2.4" stroke-dasharray="5 5" '
             'class="mra-flow" marker-end="url(#arrI)"/>')
    g.append('<text x="346" y="242" class="mra-ts" text-anchor="middle">'
             'الحالة المتعلَّمة تُبنى مرّةً، ثمّ تُستعمل ملايين المرّات دون إعادة تعلّم</text>')
    return f'<svg viewBox="0 0 692 254">{"".join(g)}</svg>'


# ======================================================================
#  تنوّع «الحالة المتعلَّمة» بحسب النموذج
# ======================================================================
def learned_state_variety() -> str:
    leaves = [
        ("معاملات وأوزان", "coefficients · weights · biases", "indigo"),
        ("بنية شجرة وعتبات", "splits · thresholds · leaf values", "teal"),
        ("مراكز العناقيد", "cluster centroids", "amber"),
        ("أمثلة مخزَّنة", "stored training instances", "violet"),
        ("توزيع بَعْدي", "posterior distribution", "rose"),
    ]
    g = [_DEFS]
    g.append(_box(500, 118, 176, 76, "التدريب", "training on data", "sky", 0, 18, 17))
    for i, (ar, en, t) in enumerate(leaves):
        y = 14 + i * 58
        g.append(_box(84, y, 262, 48, ar, en, t, 0.1 + i * 0.09, 14, 13))
        g.append(
            f'<path d="M 496 156 C 430 156, 410 {y + 24}, 352 {y + 24}" fill="none" '
            f'stroke="#C6D0F2" stroke-width="2.4" class="mra-flow" marker-end="url(#arrI)" '
            f'style="animation-delay:{i * .15:.2f}s"/>'
        )
    g.append('<text x="346" y="330" class="mra-ts" text-anchor="middle">'
             '«الحالة المتعلَّمة» أعمّ من «الأوزان» — وهي التعبير الوحيد الذي يشمل كلّ النماذج</text>')
    return f'<svg viewBox="0 0 700 344">{"".join(g)}</svg>'


# ======================================================================
#  ثلاثة مستويات للحديث عن التعلّم
# ======================================================================
def three_levels() -> str:
    levels = [
        (470, "المستوى النظري", "Learning Theory", "البرنامج/الخوارزمية A تحوّل العيّنة S إلى فرضية h", "violet"),
        (248, "المستوى التنفيذي", "ML Practice", "نُدرّب نموذجًا على البيانات بخوارزمية تعلّم", "indigo"),
        (26, "المستوى الإحصائي", "Statistics", "نُلائم نموذجًا ونُقدّر معالمه من عيّنة", "teal"),
    ]
    g = [_DEFS]
    g.append('<text x="346" y="24" class="mra-ts" text-anchor="middle" style="fill:#3A4BBF">'
             'سؤال «من يتعلّم؟» له ثلاث إجابات صحيحة — لأنّ السؤال يُطرح على ثلاثة مستويات</text>')
    for i, (x, ar, en, note, t) in enumerate(levels):
        g.append(_box(x, 46, 200, 86, ar, en, t, i * 0.14, 18, 14))
        g.append(f'<text x="{x + 100}" y="152" class="mra-ts" text-anchor="middle" '
                 f'style="font-size:10.5px">{note}</text>')
    g.append('<text x="346" y="186" class="mra-te" text-anchor="middle">'
             'no contradiction — only three levels of abstraction</text>')
    return f'<svg viewBox="0 0 692 196">{"".join(g)}</svg>'
