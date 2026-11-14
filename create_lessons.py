from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

lessons = [
("anatomie","01_anatomie","Anatomie humaine",
"Anatomie générale : organisation du corps humain, cellules, tissus, organes et appareils.",
"التشريح العام: تنظيم جسم الإنسان، الخلايا، الأنسجة، الأعضاء والأجهزة."),
("anatomie","02_appareil_genital","Appareil génital féminin",
"Les organes génitaux féminins comprennent les ovaires, les trompes, l'utérus, le vagin et la vulve.",
"يتكون الجهاز التناسلي الأنثوي من المبيضين وقناتي فالوب والرحم والمهبل والفرج."),
("obstetrique","03_grossesse","La grossesse",
"La grossesse est une période de développement embryonnaire puis fœtal. Le suivi médical permet de surveiller la santé maternelle et fœtale.",
"الحمل فترة نمو الجنين. تسمح المتابعة الطبية بمراقبة صحة الأم والجنين."),
("obstetrique","04_accouchement","L'accouchement",
"L'accouchement comprend le travail, la dilatation du col, la naissance et la délivrance. La surveillance relève de professionnels qualifiés.",
"تشمل الولادة المخاض واتساع عنق الرحم وخروج المولود ثم خروج المشيمة. تتم المتابعة من طرف مهنيين مؤهلين."),
("neonatologie","05_nouveau_ne","Le nouveau-né",
"La période néonatale correspond aux 28 premiers jours de vie. La surveillance porte notamment sur la respiration, la température et l'alimentation.",
"فترة حديثي الولادة تشمل أول 28 يوماً. تتم مراقبة التنفس ودرجة الحرارة والتغذية."),
("soins","06_hygiene","Hygiène hospitalière",
"L'hygiène hospitalière vise à prévenir les infections associées aux soins par l'hygiène des mains, le nettoyage et les précautions standard.",
"تهدف النظافة الاستشفائية إلى الوقاية من العدوى المرتبطة بالعلاج، عبر نظافة اليدين والتنظيف والاحتياطات القياسية.")
]

os.makedirs("pdf", exist_ok=True)
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "TitleCustom", parent=styles["Title"],
    alignment=TA_CENTER, textColor=colors.HexColor("#087F72")
)
body = styles["BodyText"]

for folder, filename, title, fr, ar in lessons:
    path = f"pdf/{folder}/{filename}.pdf"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(path, pagesize=A4)
    story = [
        Paragraph("YOUBI - SCIENCES PARAMEDICALES", title_style),
        Spacer(1, 20),
        Paragraph(title, styles["Heading1"]),
        Paragraph("Support pédagogique introductif - Français", styles["Heading2"]),
        Paragraph(fr, body),
        Spacer(1, 20),
        Paragraph("الشرح بالعربية", styles["Heading2"]),
        Paragraph(ar, body),
        Spacer(1, 25),
        Paragraph("Document pédagogique introductif. Ne remplace pas un cours officiel ni les protocoles médicaux.", styles["Italic"])
    ]
    doc.build(story)
    print("Créé:", path)

