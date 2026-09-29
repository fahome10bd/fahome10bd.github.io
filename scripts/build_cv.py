"""Create the public, one-page academic CV from verified details only."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "files" / "Mohammad_Mahmudul_Hasan_Academic_CV.pdf"
FONTS = Path(r"C:\Windows\Fonts")

pdfmetrics.registerFont(TTFont("ArialCV", str(FONTS / "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialCV-Bold", str(FONTS / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("GeorgiaCV-Bold", str(FONTS / "georgiab.ttf")))
pdfmetrics.registerFontFamily("ArialCV", normal="ArialCV", bold="ArialCV-Bold")

INK = colors.HexColor("#182a2e")
GREEN = colors.HexColor("#176c5b")
GRAY = colors.HexColor("#50636a")

STYLES = {
    "name": ParagraphStyle("name", fontName="GeorgiaCV-Bold", fontSize=22, leading=27, textColor=INK, spaceAfter=2),
    "role": ParagraphStyle("role", fontName="ArialCV-Bold", fontSize=10, leading=14, textColor=GREEN, spaceAfter=5),
    "contact": ParagraphStyle("contact", fontName="ArialCV", fontSize=8.3, leading=12, textColor=GRAY, spaceAfter=5),
    "heading": ParagraphStyle("heading", fontName="ArialCV-Bold", fontSize=9.3, leading=13, textColor=INK, spaceBefore=10, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="ArialCV", fontSize=9, leading=12.6, textColor=INK, spaceAfter=4),
    "bullet": ParagraphStyle("bullet", fontName="ArialCV", fontSize=8.9, leading=12.3, textColor=INK, leftIndent=10, firstLineIndent=-8, spaceAfter=2.5),
    "small": ParagraphStyle("small", fontName="ArialCV", fontSize=8.3, leading=11.8, textColor=GRAY, spaceAfter=3),
}


def para(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    body = [
        para("Mohammad Mahmudul Hasan", "name"),
        para("Team Lead, AI Engineer  |  Computer vision, GIS and photogrammetry", "role"),
        para('Bangladesh  ·  <link href="https://github.com/fahome10bd" color="#176c5b">github.com/fahome10bd</link>  ·  <link href="https://www.linkedin.com/in/fahome10bd/" color="#176c5b">linkedin.com/in/fahome10bd</link>', "contact"),
        para("RESEARCH PROFILE", "heading"),
        para("AI engineering team lead with experience in algorithm development and system design for computer vision and GIS applications. My work spans photogrammetric orthophoto production, point-cloud processing, urban building-change analysis and road-asset inspection. Seeking graduate research in reliable geospatial AI and 3D mapping."),
        para("EDUCATION", "heading"),
        para("<b>Islamic University of Technology, Bangladesh</b> — BSc in Electrical and Electronic Engineering, completed 22 March 2021. CGPA <b>3.76/4.00</b>; first class with honours."),
        para("Selected coursework: Project and Thesis (A+ in both courses); Digital Signal Processing (A); Artificial Neural Networks and Fuzzy Logic (A+).", "small"),
        para("PROFESSIONAL EXPERIENCE", "heading"),
        para("<b>HawarIT Limited</b> — with the company since 2021; current role <b>Team Lead, AI Engineer</b>. Lead a six-member AI engineering team."),
        para("•  Develop algorithms and design systems for computer vision and GIS tasks using imagery and spatial data.", "bullet"),
        para("•  Work across AT-related processing, DSM/DTM, image rectification, seamlines, tiling, bridge editing and final orthophoto output.", "bullet"),
        para("•  Process and align point clouds across multiple trajectories, followed by segmentation and classification.", "bullet"),
        para("•  Support GIS digitization, multi-year building-change analysis and traffic-sign assessment from car-captured 360-degree imagery.", "bullet"),
        para("PEER-REVIEWED PUBLICATION", "heading"),
        para('Tasnim Sakib Apon, <b>Mohammad Mahmudul Hasan</b>, Abrar Islam, and Md. Golam Rabiul Alam. “Demystifying Deep Learning Models for Retinal OCT Disease Classification using Explainable AI.” <i>2021 IEEE Asia-Pacific Conference on Computer Science and Data Engineering (CSDE)</i>. <link href="https://doi.org/10.1109/CSDE53843.2021.9718400" color="#176c5b">doi:10.1109/CSDE53843.2021.9718400</link>.'),
        para("SELECTED RESEARCH AND PROJECTS", "heading"),
        para("<b>EEG undergraduate thesis:</b> signal analysis related to impaired consciousness and coma."),
        para("<b>Building change and mapping:</b> interpretation of construction, demolition and extensions from multi-year orthophotos; GIS digitization from imagery."),
        para('<b>Traffic detection:</b> earlier 21-label computer-vision project with a <link href="https://github.com/fahome10bd/Multi-Label-Vehicle-detection-based-on-AI" color="#176c5b">public repository</link>.'),
        para("TECHNICAL AREAS AND LANGUAGE", "heading"),
        para("Computer vision; GIS; algorithm development; system design; photogrammetric workflows; point-cloud alignment and classification; signal analysis; Python; MATLAB."),
        para("Bangla: native. English-medium instruction certificate available. IELTS pending.", "small"),
    ]

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm, title="Mohammad Mahmudul Hasan Academic CV", author="Mohammad Mahmudul Hasan")
    doc.build(body)
    print(OUTPUT)


if __name__ == "__main__":
    main()
