import os
import glob
import arabic_reshaper
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

OUT = os.path.expanduser("~/youbi/pdf")

# البحث عن خط عربي في الهاتف
font_paths = [
    "/system/fonts/NotoNaskhArabic-Regular.ttf",
    "/system/fonts/NotoSansArabic-Regular.ttf",
    "/system/fonts/DroidSansArabic.ttf",
    "/system/fonts/DejaVuSans.ttf"
]

font_path = next((p for p in font_paths if os.path.exists(p)), None)

if not font_path:
    print("لم أجد خطاً عربياً. ابعثلي النتيجة باش نجهز الخط.")
    raise SystemExit

pdfmetrics.registerFont(TTFont("Arabic", font_path))

def ar(text):
    return arabic_reshaper.reshape(str(text))

courses = [
("01_intro_obstetrique", "مقدمة في علم التوليد", "Introduction à l'obstétrique", [
"تعريف علم التوليد ومجالاته ودور القابلة.",
"مراحل الحياة الإنجابية والمصطلحات الأساسية.",
"مفهوم الحمل الطبيعي ومتابعة الأم.",
"مفهوم الولادة وفترة ما بعد الولادة.",
"أخلاقيات المهنة وسرية المعلومات واحترام المريضة."
]),
("02_anatomie_appareil_genital", "تشريح الجهاز التناسلي الأنثوي", "Anatomie de l'appareil génital féminin", [
"الأعضاء التناسلية الخارجية والداخلية.",
"المبيض وقناتا فالوب والرحم وعنق الرحم والمهبل.",
"الدورة المبيضية والدورة الرحمية.",
"الهرمونات المرتبطة بالجهاز التناسلي.",
"التغيرات التشريحية والوظيفية خلال الحمل."
]),
("03_etapes_grossesse", "مراحل الحمل", "Les étapes de la grossesse", [
"تعريف الحمل وحساب عمر الحمل والمصطلحات.",
"الثلث الأول: التغيرات والتطورات الأساسية.",
"الثلث الثاني: نمو الجنين والتغيرات عند الأم.",
"الثلث الثالث: نضج الجنين والاستعداد للولادة.",
"المتابعة الدورية ومبادئ التثقيف الصحي."
]),
("04_developpement_foetal", "نمو الجنين", "Développement embryonnaire et fœtal", [
"الإخصاب وبداية التطور الجنيني.",
"الانقسامات الخلوية والانغراس.",
"تكوين الطبقات الجنينية وبداية تشكل الأعضاء.",
"نمو الأجهزة والأعضاء خلال المرحلة الجنينية.",
"نضج الجنين والعوامل المؤثرة في النمو."
]),
("05_placenta", "المشيمة ووظائفها", "Le placenta et ses fonctions", [
"تكوين المشيمة وبنيتها العامة.",
"الزغابات المشيمية والدوران الرحمي المشيمي.",
"تبادل الغازات والمواد الغذائية والفضلات.",
"الوظيفة الهرمونية والمناعة المشيمية.",
"مبادئ التعرف على بعض اضطرابات المشيمة."
]),
("06_suivi_grossesse", "متابعة الحمل", "Surveillance prénatale", [
"أهداف الاستشارة السابقة للولادة.",
"جمع التاريخ الصحي والاجتماعي للأم.",
"مبادئ تقييم صحة الأم والجنين.",
"الفحوصات والتحاليل خلال الحمل ومفهوم نتائجها.",
"التثقيف الصحي والتواصل والإحالة عند الحاجة."
]),
("07_changements_physiologiques", "التغيرات الفسيولوجية أثناء الحمل", "Modifications physiologiques de la grossesse", [
"التغيرات في الجهاز القلبي الوعائي والدم.",
"التغيرات التنفسية.",
"التغيرات الهضمية والاستقلابية.",
"التغيرات البولية والكلوية.",
"التغيرات الهرمونية والجلدية والعضلية."
]),
("08_accouchement", "مراحل الولادة", "Les étapes de l'accouchement", [
"تعريف المخاض والولادة ومصطلحاتهما.",
"المرحلة الأولى: اتساع عنق الرحم ومتابعة المخاض.",
"المرحلة الثانية: ولادة الجنين ومبادئ المراقبة.",
"المرحلة الثالثة: خروج المشيمة.",
"مبادئ الرعاية واحترام كرامة الأم وسلامتها."
]),
("09_postpartum", "فترة ما بعد الولادة", "Le post-partum", [
"تعريف فترة ما بعد الولادة والتغيرات الطبيعية.",
"التعافي الجسدي والتغيرات الهرمونية.",
"الرعاية النفسية والاجتماعية للأم.",
"الرضاعة والتغذية والراحة والتثقيف الصحي.",
"علامات تستوجب التقييم الطبي العاجل."
]),
("10_allaitement", "الرضاعة الطبيعية", "L'allaitement maternel", [
"تركيب حليب الأم ومكوناته العامة.",
"مراحل إنتاج الحليب والعوامل المؤثرة فيه.",
"فوائد الرضاعة للأم والرضيع.",
"مبادئ الوضعية والالتقام الصحيح.",
"الصعوبات الشائعة والدعم والتثقيف."
]),
("11_nouveau_ne", "حديث الولادة", "Le nouveau-né", [
"خصائص المولود في الفترة الانتقالية.",
"التكيف التنفسي والدوراني بعد الولادة.",
"التنظيم الحراري والتغذية والإخراج.",
"النظافة والرعاية الأساسية ومراقبة النمو.",
"مبادئ التعرف على علامات الخطر والإحالة."
]),
("12_nutrition_grossesse", "التغذية أثناء الحمل", "Nutrition pendant la grossesse", [
"مبادئ التغذية المتوازنة خلال الحمل.",
"المجموعات الغذائية والاحتياجات الغذائية.",
"أهمية الحديد وحمض الفوليك والكالسيوم.",
"سلامة الغذاء والترطيب.",
"التثقيف الغذائي ومراعاة الاحتياجات الفردية."
]),
("13_sciences_humaines", "العلوم الإنسانية والاجتماعية", "Sciences humaines et sociales", [
"مفاهيم علم النفس وعلم الاجتماع.",
"الأسرة والثقافة والصحة الإنجابية.",
"التواصل العلاجي والاستماع الفعال.",
"الأخلاقيات والحقوق والسرية المهنية.",
"العوامل الاجتماعية المؤثرة في صحة الأم والطفل."
]),
("14_memoire", "منهجية المذكرة المهنية", "Méthodologie du mémoire professionnel", [
"اختيار موضوع البحث وصياغة الإشكالية.",
"تحديد الأهداف والأسئلة والفرضيات.",
"البحث عن المراجع وتقييم موثوقيتها.",
"مبادئ المنهجية وجمع البيانات والأخلاقيات.",
"تنظيم المذكرة والتوثيق والعرض العلمي."
]),
("15_obstetrique_physio_1", "التوليد الفيزيولوجي الجزء الأول", "Obstétrique physiologique - Partie 1", [
"التكاثر والإخصاب والانغراس.",
"التشخيص العام للحمل ومراحله.",
"التغيرات الفيزيولوجية عند الأم.",
"تطور الجنين والمشيمة.",
"مبادئ المتابعة السابقة للولادة."
]),
("16_examens_biologiques", "الفحوصات البيولوجية", "Examens biologiques", [
"مبادئ التحاليل المخبرية ودورها.",
"فصائل الدم وعامل Rh ومفاهيم التوافق.",
"مبادئ تعداد الدم وفقر الدم.",
"التحاليل المرتبطة بمتابعة الحمل.",
"قراءة النتائج في إطارها الطبي وعدم تفسيرها منفردة."
]),
("17_sexologie", "علم الجنس", "Sexologie", [
"مفاهيم الصحة الجنسية والإنجابية.",
"التشريح والوظيفة الجنسية.",
"التغيرات الجنسية خلال مراحل الحياة.",
"التواصل واحترام الخصوصية والموافقة.",
"التثقيف والوقاية والإحالة للمختصين."
]),
("18_education_therapeutique", "التثقيف العلاجي", "Éducation thérapeutique", [
"مفهوم التثقيف الصحي والعلاجي.",
"تحديد احتياجات المتعلم والمريضة.",
"صياغة أهداف تعليمية واضحة.",
"اختيار وسائل التواصل والتعلم.",
"تقييم الفهم ومتابعة أثر التثقيف."
]),
("19_pmc_1", "PMC الجزء الأول - التسمية تحتاج تأكيداً", "PMC Partie 1 - intitulé à confirmer", [
"هذا الملف مؤقت إلى حين معرفة التسمية الكاملة للمقياس.",
"تحديد أهداف المقياس ومحتوياته من وثيقة المعهد.",
"إضافة المحاضرات بعد التحقق من البرنامج.",
"عدم اعتماد هذا الملف كمرجع دراسي رسمي."
]),
("20_obstetrique_physio_2", "التوليد الفيزيولوجي الجزء الثاني", "Obstétrique physiologique - Partie 2", [
"مبادئ الاستعداد للولادة.",
"الفيزيولوجيا العامة للمخاض.",
"مراحل الولادة ومراقبة الأم والجنين.",
"التغيرات الطبيعية بعد الولادة.",
"الرعاية والتثقيف خلال فترة ما بعد الولادة."
]),
("21_dietetique_infantile", "تغذية الرضيع والطفل", "Diététique infantile", [
"مبادئ تغذية الرضيع.",
"الرضاعة الطبيعية والتغذية التكميلية.",
"مراحل تطور احتياجات الطفل الغذائية.",
"سلامة الغذاء والنظافة.",
"التثقيف الغذائي ومتابعة النمو."
]),
("22_puericulture", "رعاية الطفل", "Puériculture", [
"النمو الجسدي والنفسي والحركي.",
"النظافة اليومية والعناية بالطفل.",
"النوم الآمن والبيئة المناسبة.",
"التغذية والتلقيح ومتابعة النمو.",
"التواصل مع الأسرة والتثقيف الصحي."
]),
("23_neonatalogie", "طب حديثي الولادة", "Néonatalogie", [
"مفاهيم طب حديثي الولادة.",
"التكيف بعد الولادة ومراقبة المولود.",
"الخداج ومفاهيم انخفاض وزن الولادة.",
"اليرقان الوليدي ومفاهيمه العامة.",
"علامات الخطر ومبادئ الإحالة والرعاية المتخصصة."
]),
("24_pmc_2", "PMC الجزء الثاني - التسمية تحتاج تأكيداً", "PMC Partie 2 - intitulé à confirmer", [
"هذا الملف مؤقت إلى حين معرفة التسمية الكاملة للمقياس.",
"تحديد أهداف المقياس ومحتوياته من وثيقة المعهد.",
"إضافة المحاضرات بعد التحقق من البرنامج.",
"عدم اعتماد هذا الملف كمرجع دراسي رسمي."
])
]

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "TitleArabic", parent=styles["Title"], fontName="Arabic",
    fontSize=20, leading=30, alignment=TA_CENTER,
    textColor=colors.HexColor("#087e91"), spaceAfter=16
)
ar_style = ParagraphStyle(
    "Arabic", parent=styles["Normal"], fontName="Arabic",
    fontSize=12, leading=22, alignment=TA_RIGHT, spaceAfter=8
)
fr_style = ParagraphStyle(
    "French", parent=styles["Normal"], fontName="Arabic",
    fontSize=10, leading=17, alignment=TA_LEFT, spaceAfter=8
)
small_style = ParagraphStyle(
    "Small", parent=styles["Normal"], fontName="Arabic",
    fontSize=9, leading=16, alignment=TA_RIGHT,
    textColor=colors.HexColor("#8a5b20")
)

os.makedirs(OUT, exist_ok=True)

for filename, name_ar, name_fr, topics in courses:
    path = os.path.join(OUT, filename + ".pdf")
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        rightMargin=45, leftMargin=45,
        topMargin=45, bottomMargin=45
    )
    story = []
    story.append(Paragraph(ar("YOUBI - السنة الثانية Sage-femme"), title_style))
    story.append(Paragraph(ar(name_ar), title_style))
    story.append(Paragraph(name_fr, fr_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        ar("حالة الوثيقة: محتوى تعليمي تمهيدي، بانتظار التحقق من البرنامج الحالي لمعهد القابلات بتلمسان. ليس محاضرة رسمية."),
        small_style
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph(ar("أهداف ومحاور المقياس"), ar_style))

    for i, topic in enumerate(topics, 1):
        story.append(Paragraph(ar(f"{i}. {topic}"), ar_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph(ar("مصادر التوثيق"), ar_style))
    story.append(Paragraph(
        ar("تضاف المراجع الجامعية ومحاضرات الأساتذة بعد التحقق من مصدرها وطبعتها وسنة نشرها. لا توجد إحالة جامعية موثقة مرفقة بهذا الملف حالياً."),
        ar_style
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        ar("تنبيه دراسي: هذا الملف للمراجعة الأكاديمية العامة فقط. لا يعوض دروس الأساتذة أو البروتوكولات الطبية المعتمدة أو التوجيه السريري."),
        small_style
    ))
    doc.build(story)
    print("تم إنشاء:", path)

print("\nYOUBI: انتهى إنشاء ملفات المقاييس.")
print("عدد الملفات:", len(courses))
