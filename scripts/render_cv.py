"""Render the shared CV data as a readable, two-page ModernCV-style PDF."""

import json
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'files/Mohammad_Mahmudul_Hasan_Academic_CV.pdf'
BLUE = colors.HexColor('#2970b6')
TEXT = colors.HexColor('#1a1a1a')
MUTED = colors.HexColor('#555555')
WIDTH = 180 * mm


def register_fonts():
    fonts = Path('C:/Windows/Fonts')
    if (fonts / 'arial.ttf').exists():
        for name, file in [('Sans', 'arial.ttf'), ('Sans-Bold', 'arialbd.ttf'), ('Sans-Italic', 'ariali.ttf'), ('Sans-BoldItalic', 'arialbi.ttf')]:
            pdfmetrics.registerFont(TTFont(name, str(fonts / file)))
        pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='Sans-Bold', italic='Sans-Italic', boldItalic='Sans-BoldItalic')
        return 'Sans'
    return 'Helvetica'


FONT = register_fonts()
STYLES = {
    'body': ParagraphStyle('Body', fontName=FONT, fontSize=10.5, leading=14.2, textColor=TEXT),
    'label': ParagraphStyle('Label', fontName=FONT + '-Bold', fontSize=9.5, leading=13, textColor=MUTED, alignment=2),
    'first': ParagraphStyle('First', fontName=FONT, fontSize=24, leading=27, textColor=TEXT),
    'last': ParagraphStyle('Last', fontName=FONT + '-Bold', fontSize=24, leading=27, textColor=TEXT),
    'subtitle': ParagraphStyle('Subtitle', fontName=FONT, fontSize=10.5, leading=14, textColor=BLUE, spaceBefore=6),
    'contact': ParagraphStyle('Contact', fontName=FONT, fontSize=9.2, leading=12.5, textColor=MUTED, alignment=2),
    'reference': ParagraphStyle('Reference', fontName=FONT, fontSize=9.3, leading=12.8, textColor=TEXT),
}


def markup(value):
    return value.replace('–', '-').replace('—', '-').replace('‑', '-').replace('−', '-')


class Section(Flowable):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.height = 24
        self.keepWithNext = True

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(BLUE)
        self.canv.setFont(FONT + '-Bold', 12)
        self.canv.drawString(0, 7, self.title)
        start = self.canv.stringWidth(self.title, FONT + '-Bold', 12) + 10
        if start < self.width:
            self.canv.setStrokeColor(BLUE)
            self.canv.setLineWidth(0.7)
            self.canv.line(start, 11, self.width, 11)
        self.canv.restoreState()


def row(label, body):
    table = Table([[Paragraph(markup(escape(label)), STYLES['label']), Paragraph(markup(body), STYLES['body'])]], colWidths=[36 * mm, 144 * mm])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 12),
        ('RIGHTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return table


def header(cv):
    name = [Paragraph(escape(cv['first_name']), STYLES['first']), Paragraph(escape(cv['last_name']), STYLES['last']), Paragraph(markup(escape(cv['subtitle'])), STYLES['subtitle'])]
    contacts = []
    for item in cv['contact']:
        text = escape(item['text'])
        if item['url']:
            text = f'<font color="#2970b6"><a href="{escape(item["url"], quote=True)}">{text}</a></font>'
        contacts.append(text)
    table = Table([[name, Paragraph('<br/>'.join(contacts), STYLES['contact'])]], colWidths=[95 * mm, 85 * mm])
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 12)]))
    return table


def page_chrome(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT, 8.5)
    canvas.drawString(15 * mm, 9 * mm, 'Mohammad Mahmudul Hasan | Academic CV')
    canvas.drawRightString(A4[0] - 15 * mm, 9 * mm, f'Page {doc.page}')
    if doc.page > 1:
        canvas.setFillColor(BLUE)
        canvas.drawString(15 * mm, A4[1] - 11 * mm, 'Mohammad Mahmudul Hasan | Curriculum Vitae')
    canvas.restoreState()


def build_pdf():
    cv = json.loads((ROOT / '_data/cv.json').read_text(encoding='utf-8'))
    story = [header(cv)]
    current_page = 1
    for section in cv['sections']:
        if section['page'] != current_page:
            story.append(PageBreak())
            current_page = section['page']
        story.append(Section(section['title']))
        story.extend(row(item['label'], item['body']) for item in section['rows'])
        story.append(Spacer(1, 5))
    story.append(Section('References'))
    references = []
    for reference in cv['references']:
        references.append(Paragraph(f'<b>{escape(reference["name"])}</b><br/>{escape(reference["title"])}<br/>{escape(reference["organization"])}<br/><font color="#2970b6"><a href="mailto:{escape(reference["email"])}">{escape(reference["email"])}</a></font>', STYLES['reference']))
    table = Table([references], colWidths=[WIDTH / 3] * 3)
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 4)]))
    story.append(table)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=17 * mm, bottomMargin=17 * mm, title='Mohammad Mahmudul Hasan - Academic CV', author='Mohammad Mahmudul Hasan')
    doc.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)
    print(f'Generated {OUTPUT}')


if __name__ == '__main__':
    build_pdf()
