"""Create the exact ModernCV Classic Blue replica in PDF."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "files" / "Mohammad_Mahmudul_Hasan_Academic_CV.pdf"
FONTS = Path(r"C:\Windows\Fonts")

pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Bold", str(FONTS / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Italic", str(FONTS / "ariali.ttf")))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", str(FONTS / "arialbi.ttf")))
pdfmetrics.registerFontFamily(
    "Sans",
    normal="Sans",
    bold="Sans-Bold",
    italic="Sans-Italic",
    boldItalic="Sans-BoldItalic",
)

# ModernCV Classic Blue Palette
MCV_BLUE = colors.HexColor("#2970b6")
MCV_LINE = colors.HexColor("#3873b3")
MCV_TEXT = colors.HexColor("#1a1a1a")
MCV_MUTED = colors.HexColor("#555555")

STYLES = {
    "name_first": ParagraphStyle(
        "name_first",
        fontName="Sans",
        fontSize=24,
        leading=27,
        textColor=MCV_TEXT,
    ),
    "name_last": ParagraphStyle(
        "name_last",
        fontName="Sans-Bold",
        fontSize=24,
        leading=27,
        textColor=MCV_TEXT,
        spaceAfter=4,
    ),
    "title": ParagraphStyle(
        "title",
        fontName="Sans-Italic",
        fontSize=12,
        leading=15,
        textColor=MCV_BLUE,
    ),
    "contact": ParagraphStyle(
        "contact",
        fontName="Sans",
        fontSize=8.8,
        leading=12.5,
        textColor=MCV_MUTED,
        alignment=2,  # Right-aligned
    ),
    "left_label": ParagraphStyle(
        "left_label",
        fontName="Sans-Bold",
        fontSize=9,
        leading=12.2,
        textColor=MCV_MUTED,
        alignment=2,  # Right-aligned like ModernCV classic
    ),
    "entry_body": ParagraphStyle(
        "entry_body",
        fontName="Sans",
        fontSize=9,
        leading=12.2,
        textColor=MCV_TEXT,
    ),
    "list_item": ParagraphStyle(
        "list_item",
        fontName="Sans",
        fontSize=9,
        leading=12.2,
        textColor=MCV_TEXT,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=1.5,
    ),
    "ref_box": ParagraphStyle(
        "ref_box",
        fontName="Sans",
        fontSize=8.5,
        leading=11.5,
        textColor=MCV_TEXT,
    ),
}

COL_W_LEFT = 34 * mm
COL_W_RIGHT = 146 * mm
TOTAL_W = COL_W_LEFT + COL_W_RIGHT


class ModernCVSection(Flowable):
    """Draws a ModernCV section heading with an elegant blue horizontal line extending across."""

    def __init__(self, title: str, width: float = TOTAL_W, height: float = 7 * mm):
        super().__init__()
        self.title = title
        self.width = width
        self.height = height
        self.keepWithNext = True

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFont("Sans-Bold", 12)
        self.canv.setFillColor(MCV_BLUE)
        text_y = 1.5 * mm
        self.canv.drawString(0, text_y, self.title)
        text_w = self.canv.stringWidth(self.title, "Sans-Bold", 12)
        line_start_x = text_w + 3.5 * mm
        line_end_x = self.width
        self.canv.setStrokeColor(MCV_LINE)
        self.canv.setLineWidth(1.5)
        line_y = text_y + 1.2 * mm
        self.canv.line(line_start_x, line_y, line_end_x, line_y)
        self.canv.restoreState()


def cv_row(left_text: str, right_text: str) -> Table:
    p_left = Paragraph(left_text, STYLES["left_label"])
    p_right = Paragraph(right_text, STYLES["entry_body"])
    t = Table([[p_left, p_right]], colWidths=[COL_W_LEFT, COL_W_RIGHT])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 8),
                ("LEFTPADDING", (1, 0), (1, -1), 4),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
            ]
        )
    )
    return t


def make_header() -> Table:
    name_flowables = [
        Paragraph("Mohammad", STYLES["name_first"]),
        Paragraph("Mahmudul Hasan", STYLES["name_last"]),
        Paragraph("Project Lead, AI Engineer", STYLES["title"]),
    ]
    contact_text = (
        "Khilgaon, Dhaka, Bangladesh<br/>"
        "+8801521434403<br/>"
        '<font color="#2970b6"><link href="mailto:mahmudul18@iut-dhaka.edu">mahmudul18@iut-dhaka.edu</link></font><br/>'
        'LinkedIn: <font color="#2970b6"><link href="https://www.linkedin.com/in/fahome10bd/">fahome10bd</link></font><br/>'
        'GitHub: <font color="#2970b6"><link href="https://github.com/fahome10bd">fahome10bd</link></font><br/>'
        'ResearchGate: <font color="#2970b6"><link href="https://www.researchgate.net/profile/Mohammad-Mahmudul-Hasan">Mohammad-Mahmudul-Hasan</link></font>'
    )
    contact_flowable = Paragraph(contact_text, STYLES["contact"])
    t = Table([[name_flowables, contact_flowable]], colWidths=[105 * mm, 75 * mm])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


def make_references() -> Table:
    ref1 = (
        "<b>Mirza Fuad Adnan</b><br/>"
        "Assistant Professor<br/>"
        "Dept. of EEE, IUT<br/>"
        '<font color="#2970b6"><link href="mailto:adnan152616@gmail.com">adnan152616@gmail.com</link></font>'
    )
    ref2 = (
        "<b>Md. Thesun Al-Amin</b><br/>"
        "Assistant Professor<br/>"
        "Dept. of EEE, IUT<br/>"
        '<font color="#2970b6"><link href="mailto:thesun.eee@gmail.com">thesun.eee@gmail.com</link></font>'
    )
    ref3 = (
        "<b>Kaisar Imam</b><br/>"
        "Chief Technology Officer<br/>"
        "HawarIT Limited<br/>"
        '<font color="#2970b6"><link href="mailto:k.imam@hawarIT.com">k.imam@hawarIT.com</link></font>'
    )
    col_w = TOTAL_W / 3.0
    t = Table(
        [
            [
                Paragraph(ref1, STYLES["ref_box"]),
                Paragraph(ref2, STYLES["ref_box"]),
                Paragraph(ref3, STYLES["ref_box"]),
            ]
        ],
        colWidths=[col_w, col_w, col_w],
    )
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def build_pdf() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    story = []

    # Header
    story.append(make_header())
    story.append(Spacer(1, 3 * mm))

    # 1. Research Interests
    story.append(ModernCVSection("Research Interests"))
    story.append(
        cv_row(
            "",
            "My research objective is to advance the field of <b>3D Urban Modeling</b> by integrating <b>Geospatial AI (GeoAI)</b> with high-fidelity reconstruction techniques. I am specifically interested in investigating:",
        )
    )
    story.append(
        cv_row(
            "Core Focus",
            "<b>Autonomous Digital Twins:</b> Leveraging <b>Gaussian Splatting</b> and <b>CityGML</b> to automate the generation of photorealistic, large-scale city models.",
        )
    )
    story.append(
        cv_row(
            "Methodology",
            "<b>Spatial Intelligence:</b> Refining <b>Point Cloud Analytics</b> and <b>Computer Vision</b> pipelines for precise object localization and multi-temporal change detection in urban environments.",
        )
    )
    story.append(
        cv_row(
            "Vision",
            "Developing scalable, <b>Autonomous GIS Systems</b> that bridge the gap between <b>Remote Sensing</b> and real-time spatial data automation.",
        )
    )

    story.append(Spacer(1, 2.5 * mm))

    # 2. Education
    story.append(ModernCVSection("Education"))
    story.append(
        cv_row(
            "2017–2021",
            "<b>B.Sc. in Electrical and Electronic Engineering (EEE)</b>, Islamic University of Technology (IUT), Bangladesh, <i>CGPA: 3.76/4.00 (First Class Honors)</i>",
        )
    )
    story.append(
        cv_row(
            "Thesis",
            "<i>Quantifying Locomotive Features in EEG of Impaired Consciousness (Coma) with Distinctive Cerebral Rhythms</i>. Analyzed EEG time-series signals to identify discriminative features related to consciousness levels.",
        )
    )
    story.append(
        cv_row(
            "2014–2016",
            "<b>Higher Secondary Certificate (Science)</b>, Notre Dame College, Dhaka, <i>GPA: 5.00/5.00</i>. Received Government Scholarship.",
        )
    )
    story.append(
        cv_row(
            "2012–2014",
            "<b>Secondary School Certificate (Science)</b>, National Ideal College, Dhaka, <i>GPA: 5.00/5.00</i>",
        )
    )

    story.append(Spacer(1, 2.5 * mm))

    # 3. Professional Experience
    story.append(ModernCVSection("Professional Experience"))
    story.append(
        cv_row(
            "2024–Present",
            "<b>Project Lead, AI Department</b>, HawarIT Limited, Bangladesh. Leading AI and geospatial automation projects and managing multidisciplinary teams for GeoAI systems.",
        )
    )
    story.append(
        cv_row(
            "2023–2024",
            "<b>Senior AI Engineer</b>, HawarIT Limited, Bangladesh. Led advanced AI system design for photogrammetry, point cloud analytics, and spatial automation.",
        )
    )
    story.append(
        cv_row(
            "2021–2023",
            "<b>ML Engineer</b>, HawarIT Limited, Bangladesh. Developed machine learning and computer vision pipelines for geospatial applications.",
        )
    )

    story.append(Spacer(1, 2.5 * mm))

    # 4. Selected Technical & Research Projects
    story.append(ModernCVSection("Selected Technical & Research Projects"))
    story.append(
        cv_row(
            "3D Intelligence",
            "Developed AI-driven algorithms for semantic segmentation and BIM model extraction from large-scale aerial, mobile, and indoor LiDAR datasets. Implemented automated pipe detection and geometric property extraction, resulting in a 60% reduction in manual processing time with 95% extraction accuracy.",
        )
    )
    story.append(
        cv_row(
            "Localization",
            "Engineered a comprehensive end-to-end GeoAI pipeline for the automated detection and geospatial localization of 130 traffic sign and 33 street furniture classes from 360° street-view imagery. Utilized YOLOv5 and custom tracking algorithms to achieve over 95% detection accuracy and 92% localization precision.",
        )
    )
    story.append(
        cv_row(
            "Change Detection",
            "Developed a multi-temporal change detection system using deep learning to identify building extensions, new constructions, and demolitions from multi-year orthophotos. Integrated the system into a GIS-based web validation platform, achieving 88% accuracy and reducing manual inspection efforts by 65%.",
        )
    )
    story.append(
        cv_row(
            "City Modeling",
            "Built an automated pipeline for large-scale 3D CityGML reconstruction and photorealistic texture generation from high-resolution aerial imagery. Designed custom multi-view texture projection algorithms considering occlusion and view selection, maintaining a texture shift of less than 3 pixels.",
        )
    )
    story.append(
        cv_row(
            "Orthophoto QA",
            "Automated orthophoto production workflows by developing AI-based image quality assessment tools for cloud, shadow, and blur detection with 97% accuracy. Optimized seamline refinement and spatial validation using PostgreSQL/PostGIS and AHN point cloud data, cutting manual editing by 65%.",
        )
    )
    story.append(
        cv_row(
            "Pose Estimation",
            "Developed a camera pose estimation framework utilizing feature matching and tie-point generation to align new aerial imagery with historical orthophotos. Achieved a 2-pixel alignment accuracy, which effectively reduced manual aerial triangulation efforts by 90%.",
        )
    )
    story.append(
        cv_row(
            "Remote Sensing",
            "Deployed AI solutions using Sentinel multispectral imagery for multi-class crop classification, water quality assessment, and algae bloom detection. This innovative earth observation analytics framework secured 2nd place in an international innovation tender.",
        )
    )
    story.append(
        cv_row(
            "Signal Analysis",
            "Engineered an automated machine fault detection method using MATLAB signal processing to analyze accelerometer data. Successfully identified and localized four distinct fault types and automated the reporting process.",
        )
    )
    story.append(
        cv_row(
            "Astrophysics",
            "Processed and cleaned fragmented WMAP datasets to remove noise from Cosmic Microwave Background Radiation (CMBR). Developed algorithms to isolate primordial signals and produce clean sky-maps for astronomical analysis.",
        )
    )

    story.append(Spacer(1, 2.5 * mm))

    # 5. Publication
    story.append(ModernCVSection("Publication"))
    story.append(
        cv_row(
            "2021",
            'Hasan, M.M., et al. "Demystifying Deep Learning Models for Retinal OCT Disease Classification using Explainable AI." <i>2021 IEEE Asia-Pacific Conference on CSDE</i>. <font color="#2970b6"><link href="https://doi.org/10.1109/CSDE53843.2021.9718400">DOI: 10.1109/CSDE53843.2021.9718400</link></font>.',
        )
    )

    story.append(Spacer(1, 2.5 * mm))

    # 6. Technical Skills
    story.append(ModernCVSection("Technical Skills"))
    story.append(
        cv_row(
            "Programming",
            "Python, SQL, JavaScript, C, MATLAB, R.",
        )
    )
    story.append(
        cv_row(
            "AI/Vision",
            "PyTorch, TensorFlow, OpenCV, YOLO, FastAPI.",
        )
    )
    story.append(
        cv_row(
            "Geospatial",
            "GDAL, GeoPandas, PostgreSQL/PostGIS, QGIS, ArcGIS.",
        )
    )
    story.append(
        cv_row(
            "3D/Point Cloud",
            "Open3D, PCL, COLMAP, OpenMVS, CloudCompare.",
        )
    )

    story.append(Spacer(1, 2.5 * mm))

    # 7. Awards & Honors
    story.append(ModernCVSection("Awards & Honors"))
    awards = [
        "Excellent Performer (2024) and Borsho Shera (Best Performer of the Year (2022)), HawarIT Limited.",
        "1st Place, MATLAB Competition, AUST.",
        "Top 15, Dhaka.AI Deep Learning Competition.",
        "1st Prize, Nuclear Power Seminar, AUST.",
        "Government Scholarship, HSC.",
    ]
    awards_flowables = [
        Paragraph(f'<font color="#2970b6">&#9642;</font> {aw}', STYLES["list_item"])
        for aw in awards
    ]
    t_awards = Table(
        [[Paragraph("", STYLES["left_label"]), awards_flowables]],
        colWidths=[COL_W_LEFT, COL_W_RIGHT],
    )
    t_awards.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 8),
                ("LEFTPADDING", (1, 0), (1, -1), 4),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
            ]
        )
    )
    story.append(t_awards)

    story.append(Spacer(1, 2.5 * mm))

    # 8. References
    story.append(ModernCVSection("References"))
    t_ref_wrapper = Table(
        [[Paragraph("", STYLES["left_label"]), make_references()]],
        colWidths=[COL_W_LEFT, COL_W_RIGHT],
    )
    t_ref_wrapper.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 8),
                ("LEFTPADDING", (1, 0), (1, -1), 4),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
            ]
        )
    )
    story.append(t_ref_wrapper)

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Mohammad Mahmudul Hasan - CV",
        author="Mohammad Mahmudul Hasan",
    )
    doc.build(story)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
