"""Create the public, one-page academic CV from verified details only."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "files" / "Mohammad_Mahmudul_Hasan_Academic_CV.pdf"
FONTS = Path(r"C:\Windows\Fonts")

pdfmetrics.registerFont(TTFont("ArialCV", str(FONTS / "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialCV-Bold", str(FONTS / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("GeorgiaCV-Bold", str(FONTS / "georgiab.ttf")))
pdfmetrics.registerFontFamily("ArialCV", normal="ArialCV", bold="ArialCV-Bold")

INK = colors.HexColor("#142327")
GREEN = colors.HexColor("#146b58")
GRAY = colors.HexColor("#4d5f66")

STYLES = {
    "name": ParagraphStyle("name", fontName="GeorgiaCV-Bold", fontSize=18, leading=22, textColor=INK, spaceAfter=1),
    "role": ParagraphStyle("role", fontName="ArialCV-Bold", fontSize=9.5, leading=13, textColor=GREEN, spaceAfter=2),
    "contact": ParagraphStyle("contact", fontName="ArialCV", fontSize=7.8, leading=11, textColor=GRAY, spaceAfter=4),
    "heading": ParagraphStyle("heading", fontName="ArialCV-Bold", fontSize=8.8, leading=11.5, textColor=INK, spaceBefore=6, spaceAfter=2),
    "body": ParagraphStyle("body", fontName="ArialCV", fontSize=8.2, leading=11, textColor=INK, spaceAfter=2),
    "bullet": ParagraphStyle("bullet", fontName="ArialCV", fontSize=8.0, leading=10.6, textColor=INK, leftIndent=8, firstLineIndent=-6, spaceAfter=1.8),
    "small": ParagraphStyle("small", fontName="ArialCV", fontSize=7.8, leading=10.5, textColor=GRAY, spaceAfter=2),
}


def para(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


class PageCountCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = 0

    def showPage(self):
        self.pages += 1
        super().showPage()


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    body = [
        para("Mohammad Mahmudul Hasan", "name"),
        para("Project Lead, AI Engineer &nbsp;|&nbsp; Geospatial AI, 3D Urban Modeling & Point Clouds", "role"),
        para('Khilgaon, Dhaka, Bangladesh &nbsp;·&nbsp; +8801521434403 &nbsp;·&nbsp; <link href="mailto:mahmudul18@iut-dhaka.edu" color="#146b58">mahmudul18@iut-dhaka.edu</link> &nbsp;·&nbsp; <link href="https://github.com/fahome10bd" color="#146b58">github.com/fahome10bd</link> &nbsp;·&nbsp; <link href="https://www.linkedin.com/in/fahome10bd/" color="#146b58">linkedin.com/in/fahome10bd</link> &nbsp;·&nbsp; <link href="https://www.researchgate.net/profile/Mohammad-Mahmudul-Hasan" color="#146b58">ResearchGate</link>', "contact"),
        
        para("RESEARCH FOCUS", "heading"),
        para("Advancing <b>3D Urban Modeling</b> and <b>Autonomous GIS</b> by integrating Geospatial AI (GeoAI) with high-fidelity reconstruction: <b>Autonomous Digital Twins</b> (3D Gaussian Splatting & CityGML), <b>Spatial Intelligence</b> (point cloud analytics, sub-pixel camera pose estimation, and automated BIM extraction), and <b>Multi-Temporal Change Detection</b>."),
        
        para("EDUCATION", "heading"),
        para("<b>Islamic University of Technology (IUT), Bangladesh</b> — B.Sc. in Electrical and Electronic Engineering, 2017 – 2021"),
        para("CGPA: <b>3.76 / 4.00</b> (First Class Honours). Selected Coursework: Project & Thesis (A+ / A+), DSP (A), Neural Networks & Fuzzy Logic (A+).", "small"),
        para("<b>Thesis:</b> <i>Quantifying Locomotive Features in EEG of Impaired Consciousness (Coma) with Distinctive Cerebral Rhythms</i>. Analyzed EEG time-series to isolate discriminative spectral and temporal features characterizing depths of consciousness.", "small"),
        para("<b>Notre Dame College, Dhaka</b> — Higher Secondary Certificate (Science), 2014 – 2016. GPA: <b>5.00 / 5.00</b> (Government Scholarship).", "small"),
        
        para("PROFESSIONAL EXPERIENCE", "heading"),
        para("<b>HawarIT Limited, Bangladesh</b> — Project Lead, AI Department (2024–Present) &nbsp;|&nbsp; Senior AI Engineer (2023–2024) &nbsp;|&nbsp; ML Engineer (2021–2023)"),
        para("Lead multidisciplinary teams building AI and geospatial automation systems across photogrammetry, point clouds, and GIS platforms:", "small"),
        para("• <b>3D Point Cloud Intelligence & BIM Extraction:</b> Developed semantic segmentation and automated pipe/geometry extraction on aerial, mobile, and indoor LiDAR datasets (95% extraction accuracy, 60% manual modeling time reduction).", "bullet"),
        para("• <b>360° Street-View GeoAI Localization:</b> Built an end-to-end YOLOv5 and tracking pipeline detecting and localizing 130 traffic signs and 33 street furniture assets from vehicle 360° imagery (>95% detection accuracy, 92% geospatial localization precision).", "bullet"),
        para("• <b>Multi-Temporal Change Detection:</b> Engineered deep learning models detecting building extensions, construction, and demolitions from multi-year orthophotos; integrated into GIS web validation platform (88% accuracy, 65% manual inspection reduction).", "bullet"),
        para("• <b>3D CityGML Modeling & Texture Projection:</b> Built automated 3D CityGML reconstruction and occlusion-aware multi-view texture projection from aerial imagery, maintaining texture displacement &lt; 3 pixels.", "bullet"),
        para("• <b>Orthophoto Automation & Camera Pose Estimation:</b> Created AI image QA (cloud/shadow/blur detection, 97% accuracy), PostGIS/AHN LiDAR seamline optimization (65% edit reduction), and camera pose estimation (2px accuracy, 90% manual AT reduction).", "bullet"),
        
        para("PEER-REVIEWED PUBLICATION", "heading"),
        para('Tasnim Sakib Apon, <b>Mohammad Mahmudul Hasan</b>, Abrar Islam, and Md. Golam Rabiul Alam. “Demystifying Deep Learning Models for Retinal OCT Disease Classification using Explainable AI.” <i>2021 IEEE Asia-Pacific Conference on CSDE</i>. <link href="https://doi.org/10.1109/CSDE53843.2021.9718400" color="#146b58">doi:10.1109/CSDE53843.2021.9718400</link>.'),
        
        para("HONORS & SELECTED PROJECTS", "heading"),
        para("<b>Awards:</b> Excellent Performer (2024) & Borsho Shera (Best Performer of the Year 2022), HawarIT &nbsp;·&nbsp; 2nd Place, International Innovation Tender (Sentinel Earth Observation) &nbsp;·&nbsp; 1st Place, MATLAB Competition, AUST &nbsp;·&nbsp; Top 15, Dhaka.AI Deep Learning Competition."),
        para("<b>Earth Observation:</b> Sentinel multispectral AI for crop classification, water quality, and algae bloom detection. <b>Fault Detection:</b> Accelerometer signal processing in MATLAB. <b>Astrophysics:</b> WMAP CMBR primordial signal isolation and sky-map generation."),
        
        para("TECHNICAL SKILLS & REFERENCES", "heading"),
        para("<b>Skills:</b> Python, SQL, C, MATLAB &nbsp;|&nbsp; PyTorch, TensorFlow, OpenCV, YOLO, FastAPI &nbsp;|&nbsp; GDAL, GeoPandas, PostGIS, QGIS, CityGML &nbsp;|&nbsp; Open3D, PCL, COLMAP, Gaussian Splatting."),
        para("<b>Referees:</b> Mirza Fuad Adnan (Asst. Prof., IUT, adnan152616@gmail.com) &nbsp;·&nbsp; Md. Thesun Al-Amin (Asst. Prof., IUT, thesun.eee@gmail.com) &nbsp;·&nbsp; Kaisar Imam (CTO, HawarIT, k.imam@hawarIT.com).", "small"),
    ]

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Mohammad Mahmudul Hasan Academic CV",
        author="Mohammad Mahmudul Hasan"
    )
    
    # We will build and check page count
    test_canvas = PageCountCanvas
    doc.build(body, canvasmaker=test_canvas)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
