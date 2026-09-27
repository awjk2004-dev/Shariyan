from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Cm, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).parent
OUT = ROOT / "chapter4_shريان.docx"


def set_rtl(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ppr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    ppr.append(bidi)


def set_cell_rtl(cell):
    for paragraph in cell.paragraphs:
        set_rtl(paragraph)


def add_paragraph(document, text="", style=None, align=WD_ALIGN_PARAGRAPH.RIGHT):
    paragraph = document.add_paragraph(style=style)
    paragraph.alignment = align
    paragraph.add_run(text)
    if align == WD_ALIGN_PARAGRAPH.RIGHT:
        set_rtl(paragraph)
    return paragraph


def add_heading(document, text, level=1):
    paragraph = document.add_paragraph(style=f"Heading {level}")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    paragraph.add_run(text)
    set_rtl(paragraph)
    return paragraph


def add_code(document, text):
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = paragraph.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    paragraph.paragraph_format.left_indent = Cm(1)
    paragraph.paragraph_format.right_indent = Cm(1)
    return paragraph


def add_figure_placeholder(document, number, title):
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(f"مكان لقطة الشاشة: الشكل رقم {number} يوضح {title}.")
    run.bold = True
    paragraph.paragraph_format.space_before = Pt(8)
    paragraph.paragraph_format.space_after = Pt(8)
    return paragraph

def add_figure_image(document, filename, caption):
    image_path = ROOT / filename
    if not image_path.exists():
        return
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run().add_picture(str(image_path), width=Cm(15.5))
    caption_paragraph = document.add_paragraph()
    caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_paragraph.add_run(caption).bold = True


def add_table(document, headers, rows):
    table = document.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = header
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_rtl(cell)
        for run in cell.paragraphs[0].runs:
            run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = str(value)
            cells[index].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_rtl(cells[index])
    document.add_paragraph()
    return table


document = Document()
section = document.sections[0]
section.top_margin = Cm(2.2)
section.bottom_margin = Cm(2.2)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)

styles = document.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(13)
for style_name in ("Heading 1", "Heading 2", "Heading 3"):
    styles[style_name].font.name = "Arial"

cover = document.add_paragraph()
cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
cover.add_run("الفصل الرابع\n").bold = True
cover.add_run("التنفيذ والنتائج وتحليل النظام").bold = True
cover.runs[0].font.size = Pt(22)
cover.runs[1].font.size = Pt(20)
subtitle = document.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.add_run("منصة شريان للتبرع بالدم الرقمية").bold = True
subtitle.add_run("\nمدينة كسلا، السودان")
document.add_page_break()

add_heading(document, "4.1 مقدمة عن مرحلة التنفيذ", 1)
add_paragraph(document, "تمثل مرحلة التنفيذ المرحلة العملية التي تتحول فيها متطلبات البحث وتصميم النظام إلى منصة رقمية قابلة للاستخدام. وفي مشروع منصة شريان للتبرع بالدم الرقمية تم تنفيذ نظام يربط بين طالبي الدم والمتبرعين داخل مدينة كسلا، مع توفير آليات لإدارة الحسابات والطلبات والبحث والإشعارات والتقارير. ركز التنفيذ على بناء نظام واضح وسهل الاستخدام، مع المحافظة على سلامة البيانات وإمكانية تطوير المنصة مستقبلاً.")
add_paragraph(document, "تم تنفيذ المشروع خلال فصل دراسي واحد بواسطة عدد من طلاب مشروع التخرج، وتم تقسيم العمل إلى مراحل مترابطة. بدأت المرحلة الأولى بتحليل المشكلة وتحديد احتياجات المستخدمين، ثم تصميم قاعدة البيانات والعلاقات بين الجداول، وبعد ذلك إنشاء واجهات النظام وربطها بخدمات الخلفية. في المرحلة اللاحقة تم اختبار العمليات الأساسية، وتصحيح الأخطاء، وتجهيز التقارير والنتائج النهائية.")
add_heading(document, "4.1.1 مراحل تنفيذ النظام", 2)
add_paragraph(document, "مر تنفيذ النظام بالمراحل الآتية:")
add_paragraph(document, "المرحلة الأولى: تحليل المتطلبات، وفيها تم تحديد الفئات المستفيدة من النظام، مثل المتبرع، طالب الدم، ومدير النظام، وتحديد الخدمات التي يحتاجها كل مستخدم.")
add_paragraph(document, "المرحلة الثانية: تصميم النظام، وشملت تصميم مخطط قاعدة البيانات، وتحديد الجداول والحقول والعلاقات، وتصميم مسارات التنقل بين الشاشات.")
add_paragraph(document, "المرحلة الثالثة: تنفيذ قاعدة البيانات، حيث تم إنشاء قاعدة البيانات والجداول وإضافة القيود اللازمة لضمان صحة العلاقات وسلامة البيانات.")
add_paragraph(document, "المرحلة الرابعة: برمجة الواجهة الخلفية، باستخدام Python وFastAPI لإنشاء واجهات برمجة التطبيقات الخاصة بالمصادقة والمتبرعين والطلبات والرسائل والإشعارات والإدارة.")
add_paragraph(document, "المرحلة الخامسة: تنفيذ الواجهات الأمامية، باستخدام HTML وCSS وJavaScript لإنشاء شاشات متجاوبة وسهلة الاستخدام، مع استخدام رسوم CSS محلية لعرض المؤشرات دون الاعتماد على اتصال بالإنترنت.")
add_paragraph(document, "المرحلة السادسة: الاختبار والتقييم، وشملت اختبار التسجيل والدخول وإضافة الطلبات والبحث والتعديل والحذف والتقارير، ثم معالجة الأخطاء وتحسين تجربة المستخدم.")
add_heading(document, "4.1.2 الأدوات والبيئة المستخدمة", 2)
add_paragraph(document, "تم استخدام XAMPP لتوفير خادم محلي وقاعدة MySQL أثناء التطوير، كما تم استخدام phpMyAdmin لإنشاء قاعدة البيانات ومراجعة الجداول وتنفيذ أوامر SQL. استخدم محرر الأكواد Visual Studio Code لكتابة ملفات Python وHTML وCSS وJavaScript وإدارة ملفات المشروع. كما استخدمت بيئة Python الافتراضية لعزل مكتبات المشروع عن بقية البيئات الموجودة على الجهاز.")

add_heading(document, "4.2 بيئة التطوير", 1)
add_paragraph(document, "بيئة التطوير هي مجموعة البرمجيات والأدوات التي استخدمت لبناء منصة شريان واختبارها قبل تشغيلها بصورة فعلية. تم اختيار الأدوات بما يتناسب مع طبيعة النظام وحاجة المشروع إلى واجهة ويب وقاعدة بيانات وخدمات خلفية قابلة للتوسع.")
add_table(document, ["العنصر", "الوصف"], [
    ["نظام التشغيل", "Windows، واستخدم لتشغيل أدوات التطوير والخادم المحلي وقاعدة البيانات."],
    ["الخادم المحلي", "XAMPP لتشغيل MySQL، مع خادم FastAPI لتقديم خدمات النظام، وخادم HTTP محلي لعرض الواجهة."],
    ["لغة البرمجة الخلفية", "Python باستخدام إطار FastAPI لبناء واجهات API ومعالجة العمليات."],
    ["قاعدة البيانات", "MySQL لتخزين المستخدمين والمتبرعين وطلبات الدم والرسائل والإشعارات."],
    ["لغات وتقنيات الواجهة", "HTML لبناء هيكل الصفحات، CSS للتنسيق، JavaScript للتفاعل، Bootstrap للتصميم المتجاوب، وChart.js للتقارير المرئية."],
    ["محرر الأكواد", "Visual Studio Code لكتابة الأكواد وتنظيم المشروع وتشغيل الأوامر."],
    ["أداة إدارة قاعدة البيانات", "phpMyAdmin لإنشاء قاعدة البيانات والجداول وفحص السجلات وتنفيذ الاستعلامات."],
])
add_heading(document, "4.2.1 إعداد المشروع وتشغيله", 2)
add_paragraph(document, "تم إنشاء بيئة Python افتراضية باسم .venv، ثم تثبيت الحزم المطلوبة من ملف requirements.txt. بعد ذلك تم إعداد ملف البيئة .env ليحتوي على رابط قاعدة البيانات والمفاتيح السرية وعناوين CORS. يتم تشغيل خادم FastAPI من جذر المشروع، كما يتم تشغيل الواجهة من مجلد frontend بواسطة خادم HTTP محلي.")
add_code(document, "python -m venv .venv\n.\\.venv\\Scripts\\Activate.ps1\npython -m pip install -r requirements.txt\npython -m uvicorn backend.main:app --reload\npython -m http.server 5500 --directory frontend")

add_heading(document, "4.3 تنفيذ قاعدة البيانات", 1)
add_paragraph(document, "تم تنفيذ قاعدة البيانات بهدف تخزين بيانات النظام بصورة منظمة وتقليل تكرار البيانات وتسهيل عمليات البحث والتقارير. تم استخدام MySQL باعتبارها نظاماً شائعاً لإدارة قواعد البيانات العلائقية، وتكاملت مع SQLAlchemy في طبقة الخلفية. كما تم استخدام migrations لتتبع تغييرات مخطط قاعدة البيانات والمحافظة على إمكانية تحديثه بصورة منظمة.")
add_heading(document, "4.3.1 إنشاء قاعدة البيانات", 2)
add_code(document, "CREATE DATABASE shريان CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\nUSE shريان;")
add_paragraph(document, "بعد إنشاء قاعدة البيانات تم إنشاء الجداول الأساسية، ثم إضافة المفاتيح الأساسية والمفاتيح الخارجية والقيود الخاصة بالحقول. يسمح ذلك بربط المستخدم بملف المتبرع، وربط طلب الدم بمستخدم أنشأه، وربط الرسائل والإشعارات بالمستخدمين المعنيين.")
add_heading(document, "4.3.2 الجداول التي تم إنشاؤها", 2)
add_table(document, ["الجدول", "الغرض من الجدول", "أهم الحقول"], [
    ["users", "تخزين الحسابات وبيانات المستخدم الأساسية", "id، full_name، email، password_hash، phone، city، is_admin"],
    ["donors", "تخزين بيانات المتبرع وفصيلة الدم وحالة التوفر", "id، user_id، blood_type، available، last_donation"],
    ["blood_requests", "تخزين طلبات الدم وبيانات المريض والمستشفى", "id، requester_id، patient_name، blood_type، city، hospital، units، urgent، status"],
    ["messages", "تخزين الرسائل بين المستخدمين", "id، sender_id، recipient_id، request_id، content، read_at"],
    ["notifications", "تخزين الإشعارات الخاصة بالمستخدمين", "id، user_id، title، body، link، read_at"],
])
add_heading(document, "4.3.3 العلاقات بين الجداول", 2)
add_paragraph(document, "يرتبط جدول users بجدول donors بعلاقة واحد إلى واحد، لأن المستخدم يمكن أن يمتلك ملف متبرع واحداً. ويرتبط جدول users بجدول blood_requests بعلاقة واحد إلى متعدد، لأن المستخدم الواحد يمكن أن ينشئ عدة طلبات دم. كما يستخدم جدول messages معرف المرسل ومعرف المستلم للإشارة إلى جدول users، ويمكن أن يرتبط اختيارياً بطلب دم معين. أما جدول notifications فيرتبط بالمستخدم بعلاقة واحد إلى متعدد، لأن المستخدم يمكن أن يمتلك عدة إشعارات.")
add_heading(document, "4.3.4 جمل SQL لإنشاء الجداول", 2)
add_code(document, "CREATE TABLE users (\n  id INT PRIMARY KEY AUTO_INCREMENT,\n  full_name VARCHAR(120) NOT NULL,\n  email VARCHAR(255) NOT NULL UNIQUE,\n  password_hash VARCHAR(255) NOT NULL,\n  phone VARCHAR(30) NOT NULL,\n  city VARCHAR(100) NOT NULL,\n  is_admin BOOLEAN DEFAULT FALSE,\n  created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n);")
add_code(document, "CREATE TABLE donors (\n  id INT PRIMARY KEY AUTO_INCREMENT,\n  user_id INT NOT NULL UNIQUE,\n  blood_type VARCHAR(5) NOT NULL,\n  available BOOLEAN DEFAULT TRUE,\n  last_donation DATETIME NULL,\n  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE\n);")
add_code(document, "CREATE TABLE blood_requests (\n  id INT PRIMARY KEY AUTO_INCREMENT,\n  requester_id INT NOT NULL,\n  patient_name VARCHAR(120) NOT NULL,\n  blood_type VARCHAR(5) NOT NULL,\n  city VARCHAR(100) NOT NULL,\n  hospital VARCHAR(180) NOT NULL,\n  units INT DEFAULT 1,\n  urgent BOOLEAN DEFAULT TRUE,\n  status VARCHAR(20) DEFAULT 'open',\n  FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE\n);")
add_heading(document, "4.3.5 أمثلة على استعلامات SQL", 2)
add_code(document, "SELECT full_name, email, city FROM users WHERE city LIKE '%كسلا%';")
add_code(document, "SELECT u.full_name, d.blood_type FROM users u JOIN donors d ON d.user_id = u.id WHERE d.available = TRUE;")
add_code(document, "INSERT INTO blood_requests (requester_id, patient_name, blood_type, city, hospital, units) VALUES (1, 'أحمد محمد', 'O+', 'كسلا', 'مستشفى كسلا', 2);")
add_code(document, "UPDATE donors SET available = FALSE, last_donation = NOW() WHERE user_id = 1;")
add_code(document, "DELETE FROM notifications WHERE id = 10;")

add_heading(document, "4.4 تنفيذ واجهات النظام", 1)
add_paragraph(document, "تم تصميم واجهات النظام باللغة العربية وباتجاه من اليمين إلى اليسار، مع مراعاة وضوح النصوص وسهولة التنقل بين الصفحات. اعتمدت الواجهات على تقسيم الوظائف إلى شاشات مستقلة، بحيث يستطيع المستخدم الوصول إلى الخدمة المطلوبة دون خطوات معقدة. تم استخدام HTML لبناء المكونات، وCSS وBootstrap للتنسيق، وJavaScript لربط الواجهة بخدمات FastAPI.")
add_heading(document, "4.4.1 شاشة تسجيل الدخول", 2)
add_paragraph(document, "تتيح شاشة تسجيل الدخول للمستخدم إدخال البريد الإلكتروني وكلمة المرور. عند إرسال النموذج يتم إرسال البيانات إلى مسار المصادقة في FastAPI، وبعد نجاح التحقق يتم إرجاع رمز وصول JWT وتخزينه في المتصفح، ثم ينتقل المستخدم إلى الصفحات المسموح بها حسب صلاحياته.")
add_figure_placeholder(document, 1, "شاشة تسجيل الدخول")
add_figure_image(document, "login-screen.png", "الشكل رقم 1: لقطة فعلية لشاشة تسجيل الدخول")
add_heading(document, "4.4.2 الشاشة الرئيسية", 2)
add_paragraph(document, "تعد الشاشة الرئيسية نقطة الدخول إلى منصة شريان، وتعرض اسم المنصة ورسالتها الأساسية المتعلقة بإنقاذ الحياة في مدينة كسلا. تحتوي على روابط لإنشاء حساب، البحث عن متبرع، متابعة طلبات الدم، والاطلاع على قائمة متصدري العطاء. كما تقدم تعريفاً مختصراً بمسارات الاستخدام الرئيسية.")
add_figure_placeholder(document, 2, "الشاشة الرئيسية للمنصة")
add_figure_image(document, "home-screen.png", "الشكل رقم 2: لقطة فعلية للشاشة الرئيسية")
add_heading(document, "4.4.3 شاشة طلب دم", 2)
add_paragraph(document, "تمكن شاشة طلب دم المستخدم من إدخال اسم المريض، فصيلة الدم، المدينة أو الحي، المستشفى، عدد الوحدات، الملاحظات، وتحديد ما إذا كان الطلب عاجلاً. يتم التحقق من الحقول قبل الإرسال، ثم تحفظ البيانات في قاعدة البيانات وتصبح متاحة في لوحة الطلبات للمتبرعين.")
add_figure_placeholder(document, 3, "شاشة إنشاء طلب دم جديد")
add_heading(document, "4.4.4 شاشة لوحة الطلبات", 2)
add_paragraph(document, "تعرض لوحة الطلبات الطلبات المفتوحة في مدينة كسلا، وتوضح فصيلة الدم واسم المريض والمستشفى والحي وعدد الوحدات، مع تمييز الطلبات العاجلة. تساعد الشاشة المتبرع على مقارنة الطلبات واختيار الحالة التي يمكنه الاستجابة لها.")
add_figure_placeholder(document, 4, "لوحة طلبات الدم")
add_heading(document, "4.4.5 شاشة قائمة المتصدرين", 2)
add_paragraph(document, "تعرض شاشة قائمة المتصدرين المتبرعين المتاحين وفق مؤشر الجاهزية، وتوضح الترتيب والاسم والمدينة وفصيلة الدم والنقاط. تم توضيح أن النقاط مؤشر للجاهزية الحالية وليست سجلاً نهائياً لعدد عمليات التبرع، إلى أن تتم إضافة سجل مستقل لعمليات التبرع في مرحلة مستقبلية.")
add_figure_placeholder(document, 5, "قائمة متصدري العطاء")
add_figure_image(document, "leaderboard-screen.png", "الشكل رقم 5: لقطة فعلية لقائمة المتصدرين")
add_heading(document, "4.4.6 شاشة عن المنصة", 2)
add_paragraph(document, "توضح شاشة عن المنصة فكرة شريان والجهة المستفيدة والمشكلة التي يعالجها النظام، كما تشرح دور المنصة في تقليل الزمن اللازم للعثور على متبرع وربط الطلبات بالمتبرعين داخل مدينة كسلا.")
add_figure_placeholder(document, 6, "شاشة عن منصة شريان")
add_heading(document, "4.4.7 شاشة لوحة التحكم للأدمن", 2)
add_paragraph(document, "تتيح لوحة التحكم لمدير النظام متابعة الإحصاءات العامة، مثل عدد المستخدمين والمتبرعين والطلبات المفتوحة والطلبات العاجلة، بالإضافة إلى توزيع الطلبات حسب فصيلة الدم والمدينة. تستخدم اللوحة البيانات المجمعة لتوفير رؤية سريعة عن حالة المنصة، ويمكن عرض بعضها في رسوم بيانية باستخدام Chart.js.")
add_figure_placeholder(document, 7, "لوحة تحكم مدير النظام")

add_heading(document, "4.5 تنفيذ العمليات الأساسية", 1)
add_paragraph(document, "تتضمن العمليات الأساسية في منصة شريان إضافة البيانات وعرضها وتعديلها وحذفها والبحث فيها. تم تنفيذ هذه العمليات من خلال مسارات API في FastAPI، ثم استدعاؤها من JavaScript في الواجهة الأمامية. تعتمد كل عملية على التحقق من صحة المدخلات وصلاحيات المستخدم قبل تنفيذها.")
add_heading(document, "4.5.1 إضافة البيانات", 2)
add_paragraph(document, "تستخدم عملية الإضافة عند تسجيل مستخدم جديد أو إنشاء ملف متبرع أو إضافة طلب دم. يعالج FastAPI البيانات الواردة من النموذج بعد التحقق من الأنواع والقيم المطلوبة، ثم ينشئ السجل في قاعدة البيانات.")
add_code(document, "@router.post('', response_model=RequestOut, status_code=201)\ndef create_request(payload: RequestCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):\n    request = BloodRequest(requester_id=user.id, **payload.model_dump())\n    db.add(request)\n    db.commit()\n    db.refresh(request)\n    return request")
add_heading(document, "4.5.2 عرض البيانات", 2)
add_code(document, "@router.get('', response_model=list[RequestOut])\ndef list_requests(db: Session = Depends(get_db)):\n    query = select(BloodRequest).where(BloodRequest.status == RequestStatus.OPEN)\n    return list(db.scalars(query.order_by(BloodRequest.id.desc())))")
add_heading(document, "4.5.3 تعديل البيانات", 2)
add_paragraph(document, "تستخدم عملية التعديل لتحديث حالة الطلب أو حالة توفر المتبرع أو بيانات الحساب. يجب أن يتحقق النظام من أن المستخدم يملك السجل أو يمتلك صلاحية المدير قبل إجراء التعديل.")
add_code(document, "@router.patch('/{request_id}')\ndef update_request(request_id: int, payload: RequestUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):\n    request = db.get(BloodRequest, request_id)\n    if not request or request.requester_id != user.id:\n        raise HTTPException(status_code=404, detail='الطلب غير موجود')\n    for key, value in payload.model_dump(exclude_unset=True).items():\n        setattr(request, key, value)\n    db.commit()\n    db.refresh(request)\n    return request")
add_heading(document, "4.5.4 حذف البيانات", 2)
add_code(document, "@router.delete('/{request_id}', status_code=204)\ndef delete_request(request_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):\n    request = db.get(BloodRequest, request_id)\n    if not request or request.requester_id != user.id:\n        raise HTTPException(status_code=404, detail='الطلب غير موجود')\n    db.delete(request)\n    db.commit()")
add_heading(document, "4.5.5 البحث في البيانات", 2)
add_paragraph(document, "يتم البحث عن المتبرعين باستخدام فصيلة الدم والمدينة أو الحي، وتستخدم الاستعلامات شروطاً اختيارية حتى يستطيع المستخدم البحث بالفصيلة فقط أو بالمدينة فقط أو باستخدام الشرطين معاً.")
add_code(document, "async function loadDonors() {\n  const query = new URLSearchParams();\n  if (blood.value) query.set('blood_type', blood.value);\n  if (city.value) query.set('city', city.value);\n  const rows = await api('/donors?' + query.toString());\n  list.innerHTML = rows.map(row => renderDonor(row)).join('');\n}")

add_heading(document, "4.6 تنفيذ نظام التقارير", 1)
add_paragraph(document, "يهدف نظام التقارير إلى تحويل البيانات المخزنة إلى معلومات تساعد مدير النظام على فهم نشاط المنصة واتخاذ القرارات المناسبة. تم تصميم التقارير بحيث تعرض أعداد المستخدمين والمتبرعين والطلبات، وتوزيع الطلبات حسب الفصيلة والمدينة، وعدد الطلبات العاجلة والمغلقة.")
add_heading(document, "4.6.1 أنواع التقارير", 2)
add_paragraph(document, "تشمل التقارير تقريراً يومياً عن الطلبات الجديدة، وتقريراً عن المتبرعين المتاحين حسب الفصيلة والمدينة، وتقريراً عن الطلبات العاجلة، وتقريراً إحصائياً للإدارة يعرض إجمالي المستخدمين والمتبرعين والطلبات.")
add_heading(document, "4.6.2 طريقة إنشاء التقرير", 2)
add_paragraph(document, "يتم إنشاء التقرير من خلال استعلامات تجميعية في قاعدة البيانات، مثل COUNT لحساب عدد السجلات وGROUP BY لتقسيم النتائج حسب الفصيلة أو المدينة. يعيد FastAPI النتائج في صورة JSON، ثم تعرضها الواجهة في بطاقات أو جداول أو رسوم بيانية باستخدام Chart.js.")
add_code(document, "SELECT blood_type, COUNT(*) AS total\nFROM blood_requests\nWHERE DATE(created_at) = CURDATE()\nGROUP BY blood_type\nORDER BY total DESC;")
add_code(document, "SELECT city, COUNT(*) AS total\nFROM blood_requests\nWHERE status = 'open'\nGROUP BY city\nORDER BY total DESC;")
add_heading(document, "4.6.3 مثال على تقرير يومي ببيانات وهمية", 2)
add_table(document, ["المؤشر", "النتيجة اليومية"], [
    ["عدد المستخدمين الجدد", "12 مستخدماً"],
    ["عدد المتبرعين المتاحين", "28 متبرعاً"],
    ["طلبات الدم الجديدة", "9 طلبات"],
    ["الطلبات العاجلة", "4 طلبات"],
    ["أكثر فصيلة مطلوبة", "O+ بعدد 4 طلبات"],
    ["أكثر منطقة بها طلبات", "وسط كسلا بعدد 5 طلبات"],
])

add_heading(document, "4.7 عرض النتائج", 1)
add_paragraph(document, "بعد تشغيل النظام وإدخال بيانات وهمية للاختبار، يستطيع المستخدم إنشاء حساب وتسجيل بياناته كمتبرع أو إنشاء طلب دم. تظهر الطلبات المفتوحة في لوحة الطلبات، ويمكن البحث عن المتبرعين حسب فصيلة الدم والمدينة. كما يستطيع المدير الاطلاع على مؤشرات النظام من لوحة التحكم.")
add_heading(document, "4.7.1 آلية عمل النظام بصورة عامة", 2)
add_paragraph(document, "يبدأ المستخدم بفتح الشاشة الرئيسية ثم يختار إنشاء حساب أو تسجيل الدخول. بعد المصادقة يستطيع المتبرع إنشاء ملف يحدد فصيلة دمه وموقعه وحالته الحالية، بينما يستطيع طالب الدم إنشاء طلب يحدد الفصيلة والمستشفى وعدد الوحدات ودرجة الاستعجال. تحفظ البيانات في MySQL عبر FastAPI، ثم تعاد النتائج إلى الواجهة في صورة JSON وتعرض للمستخدم بطريقة منظمة.")
add_heading(document, "4.7.2 أمثلة على نتائج فعلية ببيانات وهمية", 2)
add_table(document, ["العملية", "البيانات المدخلة", "النتيجة"], [
    ["تسجيل متبرع", "محمد أحمد، O+، حي العرب", "تم إنشاء ملف المتبرع وظهر في نتائج البحث"],
    ["إنشاء طلب", "مريض يحتاج وحدتين من O+ في مستشفى كسلا", "تم حفظ الطلب وظهر كطلب عاجل مفتوح"],
    ["البحث", "الفصيلة O+ والمدينة كسلا", "ظهور المتبرعين المتاحين المطابقين للبحث"],
    ["تقرير الإدارة", "بيانات شهر افتراضي", "إظهار عدد المستخدمين والطلبات وتوزيع الفصائل"],
])
add_paragraph(document, "توضح هذه النتائج أن النظام يوفر دورة عمل مترابطة تبدأ من إدخال البيانات وتنتهي بعرضها والاستفادة منها في اتخاذ القرار. ويمكن استبدال البيانات الوهمية ببيانات حقيقية عند تشغيل النظام في بيئة الإنتاج.")

add_heading(document, "4.8 تحليل أداء النظام", 1)
add_heading(document, "4.8.1 السرعة", 2)
add_paragraph(document, "يعتمد النظام على استعلامات محددة وحقول مفهرسة مثل البريد الإلكتروني وفصيلة الدم والمدينة وحالة الطلب، مما يساعد على تقليل زمن البحث عند زيادة عدد السجلات. كما أن فصل الواجهة عن الخلفية يسمح بتحميل البيانات المطلوبة فقط بدلاً من تحميل جميع بيانات النظام في كل مرة.")
add_heading(document, "4.8.2 الدقة", 2)
add_paragraph(document, "تحققت الدقة من خلال استخدام نماذج تحقق في FastAPI وPydantic، ومن خلال القيود الموجودة في قاعدة البيانات مثل عدم تكرار البريد الإلكتروني وربط السجلات بالمفاتيح الخارجية. كما تمنع الواجهة إرسال بعض الحقول الفارغة أو القيم غير المنطقية.")
add_heading(document, "4.8.3 الاستقرار", 2)
add_paragraph(document, "تم اختبار المسارات الأساسية عدة مرات، كما تم استخدام إدارة الجلسات والتعامل مع الأخطاء وإرجاع رسائل مفهومة للمستخدم. أظهرت اختبارات المشروع نجاح العمليات الأساسية، مع بقاء الاعتماد على تشغيل MySQL وخادم FastAPI كشرط لعرض البيانات الحية.")
add_heading(document, "4.8.4 الأمان", 2)
add_paragraph(document, "يستخدم النظام تشفير كلمات المرور قبل تخزينها، ومصادقة JWT لحماية المسارات الخاصة، والتحقق من صلاحيات المدير. كما تم وضع الإعدادات الحساسة في ملف البيئة .env وعدم تضمينها في ملفات الواجهة. يحتاج النظام قبل النشر الفعلي إلى تغيير المفاتيح التجريبية وتفعيل HTTPS ووضع سياسات نسخ احتياطي ومراقبة للسجلات.")
add_heading(document, "4.8.5 سهولة الاستخدام", 2)
add_paragraph(document, "تمت مراعاة استخدام لغة عربية واضحة، وتقليل عدد الحقول المطلوبة، وتوفير روابط مباشرة للوظائف المهمة. كما أن التصميم المتجاوب يسمح باستخدام النظام من أجهزة الحاسوب والهواتف، مع تقسيم المحتوى إلى بطاقات وأقسام سهلة القراءة.")

add_heading(document, "4.9 مقارنة بين النظام اليدوي والنظام المحوسب", 1)
add_table(document, ["المعيار", "النظام اليدوي", "نظام منصة شريان المحوسب"], [
    ["السرعة", "يعتمد على الاتصالات والبحث الفردي وقد يتأخر", "يوفر بحثاً سريعاً وعرضاً فورياً للطلبات والمتبرعين"],
    ["الدقة", "تزداد احتمالية الخطأ أو تكرار البيانات", "تحقق آلي وقيود قاعدة بيانات تقلل الأخطاء"],
    ["التخزين", "دفاتر أو ملفات معرضة للفقد والتلف", "قاعدة بيانات مركزية قابلة للنسخ الاحتياطي"],
    ["البحث", "بحث يدوي يستغرق وقتاً طويلاً", "بحث حسب الفصيلة والمدينة والحي"],
    ["التقارير", "إعداد يدوي يحتاج إلى وقت وجهد", "تقارير وإحصاءات قابلة للتحديث والعرض البياني"],
    ["الأمان", "صعوبة ضبط صلاحيات الاطلاع والتعديل", "تسجيل دخول وصلاحيات ومفاتيح وصول"],
    ["التكلفة", "تكلفة تشغيلية مستمرة للاتصالات والأوراق", "تكلفة تأسيس وتشغيل أقل بعد تجهيز النظام"],
])

add_heading(document, "4.10 مناقشة النتائج ومدى تحقيق الأهداف", 1)
add_paragraph(document, "أظهرت نتائج التنفيذ أن منصة شريان حققت الجزء الأساسي من أهداف البحث، إذ وفرت نظاماً رقمياً موحداً لإدارة المتبرعين وطلبات الدم في مدينة كسلا. أصبح من الممكن تسجيل بيانات المتبرعين والبحث عنهم حسب الفصيلة والموقع، كما أصبح طالب الدم قادراً على إنشاء طلب واضح يحتوي على المعلومات التي يحتاجها المتبرع.")
add_paragraph(document, "ساهم النظام في معالجة مشكلة بطء العثور على متبرعين، لأن البحث أصبح يعتمد على بيانات مخزنة في قاعدة واحدة بدلاً من الاعتماد على الاتصالات والرسائل المتفرقة. كما ساعدت لوحة الطلبات والتقارير على تنظيم المعلومات، بينما وفرت المصادقة وصلاحيات المدير مستوى أفضل من التحكم في الوصول.")
add_heading(document, "4.10.1 النتائج الإيجابية", 2)
add_paragraph(document, "من أهم النتائج الإيجابية إنشاء منصة متخصصة لمدينة كسلا، وتوفير شاشات عربية واضحة، وربط الواجهة بواجهة API، وتوفير عمليات إدارة البيانات والتقارير، وإضافة قائمة متصدري العطاء كعامل تحفيزي للجاهزية.")
add_heading(document, "4.10.2 النقاط التي تحتاج إلى تحسين", 2)
add_paragraph(document, "تحتاج النسخة المستقبلية إلى إضافة سجل مستقل لعمليات التبرع حتى تصبح نقاط المتصدرين مبنية على تبرعات مؤكدة، وإضافة إشعارات خارجية مثل البريد أو الرسائل القصيرة، وتحسين التحقق من الحسابات، وإضافة نسخ احتياطي تلقائي ومراقبة أداء عند زيادة المستخدمين.")

add_heading(document, "4.11 التحديات التي واجهت التنفيذ", 1)
add_heading(document, "4.11.1 التحديات التقنية", 2)
add_paragraph(document, "واجه الفريق تحديات في تصميم العلاقات بين المستخدمين والمتبرعين والطلبات، خصوصاً عند التعامل مع العلاقات المتعددة والقيود الخاصة بالحذف. كما ظهرت تحديات في ضبط اتصال FastAPI بقاعدة MySQL، وفي توحيد شكل البيانات بين Python وJavaScript، وفي معالجة حالات عدم وجود بيانات أو فشل الخادم.")
add_paragraph(document, "تم التغلب على هذه التحديات بتقسيم المشروع إلى routers وschemas وmodels، واستخدام migrations لتتبع تغييرات قاعدة البيانات، وتطبيق التحقق قبل الحفظ، وإضافة رسائل خطأ واضحة، واختبار كل مسار بصورة مستقلة قبل ربطه بالواجهة.")
add_heading(document, "4.11.2 التحديات الإدارية", 2)
add_paragraph(document, "تمثلت التحديات الإدارية في ضيق مدة الفصل الدراسي والحاجة إلى تنسيق العمل بين أعضاء الفريق وتوزيع المهام بين قاعدة البيانات والخلفية والواجهة والتوثيق. عولجت هذه التحديات بوضع تقسيم واضح للمهام، ومراجعة التقدم بصورة دورية، وتحديد أولويات الوظائف الأساسية قبل الوظائف الإضافية.")
add_heading(document, "4.11.3 التحديات المتعلقة بالبيانات", 2)
add_paragraph(document, "لم تكن هناك قاعدة بيانات حقيقية جاهزة تغطي جميع متبرعي مدينة كسلا، لذلك استخدمت بيانات وهمية أثناء الاختبار. تم التعامل مع ذلك بتجهيز نماذج إدخال قابلة للتوسع، وإظهار رسائل مناسبة عند عدم توفر النتائج، والتأكيد على ضرورة إدخال بيانات صحيحة ومحدثة عند تشغيل النظام بصورة فعلية.")

add_heading(document, "4.12 خلاصة الفصل", 1)
add_paragraph(document, "تناول هذا الفصل مراحل تنفيذ منصة شريان للتبرع بالدم الرقمية، وبيئة التطوير والأدوات المستخدمة، وطريقة إنشاء قاعدة البيانات والجداول والعلاقات والاستعلامات. كما شرح تنفيذ الواجهات الرئيسية والعمليات الأساسية ونظام التقارير، ثم عرض النتائج وتحليل أداء النظام ومقارنته بالنظام اليدوي.")
add_paragraph(document, "خلص التنفيذ إلى أن المنصة توفر أساساً عملياً لنظام رقمي يساعد سكان مدينة كسلا على الوصول إلى المتبرعين وإدارة طلبات الدم بصورة أسرع وأكثر تنظيماً. وعلى الرغم من وجود تحسينات مستقبلية مطلوبة، فإن النسخة المنفذة حققت الوظائف الأساسية للبحث، التسجيل، إدارة الطلبات، التقارير، والتحكم الإداري، ومهدت لتطوير نظام أوسع قابل للاستخدام في مؤسسات صحية ومجتمعية مختلفة.")

document.save(OUT)
print(OUT)
