#!/usr/bin/env python3
"""
PB CareerOS Pro Career Intelligence Report — PREMIUM BUILD
Black + Lime Green + White brand palette
Zero empty space — every inch earns its keep
V2P2 Method prominently featured
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Flowable, Frame, PageTemplate,
    BaseDocTemplate
)

# ============================================================================
# BRAND PALETTE (locked)
# ============================================================================
BLACK = HexColor('#0D0D0D')
GREEN = HexColor('#9AC850')
GREEN_DIM = HexColor('#1E2E12')
GREEN_SOFT = HexColor('#E8F5D6')
WHITE = HexColor('#FFFFFF')
OFF_WHITE = HexColor('#F5F5F3')
DARK_BG = HexColor('#111111')
CARD_DARK = HexColor('#1A1A1A')
CARD_LIGHT = HexColor('#F7F7F5')
BORDER_DARK = HexColor('#2D2D2D')
BORDER_LIGHT = HexColor('#E0E0DC')
BODY_TEXT = HexColor('#D4D4D4')
BODY_DARK = HexColor('#4A4A4A')
MUTED = HexColor('#888888')
MUTED_LIGHT = HexColor('#666666')
AMBER = HexColor('#D4A853')
RED_ACCENT = HexColor('#E74C3C')

W, H = letter

# ============================================================================
# CUSTOM FLOWABLES
# ============================================================================

class GreenBar(Flowable):
    def __init__(self, width=60, height=3):
        Flowable.__init__(self)
        self.bar_width = width
        self.bar_height = height
        self.width = width
        self.height = height + 2

    def draw(self):
        self.canv.setFillColor(GREEN)
        self.canv.rect(0, 1, self.bar_width, self.bar_height, fill=1, stroke=0)


class ThinLine(Flowable):
    def __init__(self, width=500, color=BORDER_DARK, thickness=0.5):
        Flowable.__init__(self)
        self.line_width = width
        self.line_color = color
        self.thickness = thickness
        self.width = width
        self.height = 4

    def draw(self):
        self.canv.setStrokeColor(self.line_color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 2, self.line_width, 2)


class ScoreArc(Flowable):
    def __init__(self, score, label, sublabel, size=65):
        Flowable.__init__(self)
        self.score = score
        self.label = label
        self.sublabel = sublabel
        self.size = size
        self.width = size + 16
        self.height = size + 36

    def draw(self):
        c = self.canv
        cx = self.width / 2
        cy = self.height - self.size/2 - 3
        r = self.size / 2 - 4

        c.setStrokeColor(BORDER_DARK)
        c.setLineWidth(4)
        c.arc(cx - r, cy - r, cx + r, cy + r, 135, 270)

        sweep = (self.score / 100) * 270
        color = GREEN if self.score >= 75 else AMBER if self.score >= 60 else RED_ACCENT
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.arc(cx - r, cy - r, cx + r, cy + r, 135, sweep)

        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 15)
        c.drawCentredString(cx, cy - 4, str(self.score))
        c.setFont('Helvetica', 7)
        c.setFillColor(MUTED)
        c.drawCentredString(cx, cy - 14, "/100")

        c.setFont('Helvetica-Bold', 6.5)
        c.setFillColor(GREEN)
        c.drawCentredString(cx, 16, self.label.upper())

        c.setFont('Helvetica', 6)
        c.setFillColor(MUTED)
        c.drawCentredString(cx, 6, self.sublabel)


class ScoreBarH(Flowable):
    def __init__(self, score, width=400, height=6):
        Flowable.__init__(self)
        self.score = score
        self.bar_width = width
        self.bar_height = height
        self.width = width
        self.height = height + 2

    def draw(self):
        c = self.canv
        c.setFillColor(BORDER_DARK)
        c.roundRect(0, 1, self.bar_width, self.bar_height, 3, fill=1, stroke=0)
        fill_w = max(4, (self.score / 100) * self.bar_width)
        color = GREEN if self.score >= 75 else AMBER if self.score >= 60 else RED_ACCENT
        c.setFillColor(color)
        c.roundRect(0, 1, fill_w, self.bar_height, 3, fill=1, stroke=0)


# ============================================================================
# TEXT SANITIZER — fix bare & that would confuse ReportLab's XML paragraph parser
# ============================================================================
import re as _re

def sanitize_text(text):
    """Escape bare & characters that are not already part of an HTML entity.
    ReportLab's Paragraph parser treats text as XML, so a bare & (e.g. in R&D)
    causes a parse error or renders as 'R&D;' with a stray semicolon.
    This replaces every & that is NOT followed by a valid entity reference with &amp;.
    """
    if not isinstance(text, str):
        return text
    # Replace & not followed by an entity name + semicolon (e.g. &amp; &lt; &gt; &#123;)
    return _re.sub(r'&(?!(?:[a-zA-Z]+|#[0-9]+|#x[0-9a-fA-F]+);)', '&amp;', text)


# ============================================================================
# STYLES
# ============================================================================

def make_styles():
    s = {}

    # Cover
    s['brand'] = ParagraphStyle('brand', fontName='Helvetica-Bold', fontSize=10,
        textColor=GREEN, letterSpacing=3, spaceAfter=2)
    s['tagline'] = ParagraphStyle('tagline', fontName='Helvetica-Oblique', fontSize=9,
        textColor=MUTED, spaceAfter=20)
    s['cover_title'] = ParagraphStyle('cover_title', fontName='Helvetica-Bold', fontSize=26,
        leading=30, textColor=WHITE, spaceAfter=4)
    s['cover_sub'] = ParagraphStyle('cover_sub', fontName='Helvetica', fontSize=11,
        leading=16, textColor=MUTED, spaceAfter=24)

    # Sections
    s['sec_label'] = ParagraphStyle('sec_label', fontName='Helvetica-Bold', fontSize=7,
        textColor=GREEN, letterSpacing=2, spaceAfter=3)
    s['sec_title'] = ParagraphStyle('sec_title', fontName='Helvetica-Bold', fontSize=18,
        leading=22, textColor=WHITE, spaceAfter=3)
    s['sec_desc'] = ParagraphStyle('sec_desc', fontName='Helvetica', fontSize=9,
        leading=14, textColor=MUTED, spaceAfter=14)

    # Body text
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9,
        leading=14, textColor=BODY_TEXT, spaceAfter=6)
    s['body_bold'] = ParagraphStyle('body_bold', fontName='Helvetica-Bold', fontSize=9,
        leading=14, textColor=WHITE, spaceAfter=6)
    s['body_dark'] = ParagraphStyle('body_dark', fontName='Helvetica', fontSize=9,
        leading=14, textColor=BODY_DARK, spaceAfter=6)
    s['td_dark_bold'] = ParagraphStyle('td_dark_bold', fontName='Helvetica-Bold', fontSize=8.5,
        leading=13, textColor=BLACK, spaceAfter=6)
    s['td_sm_bold'] = ParagraphStyle('td_sm_bold', fontName='Helvetica-Bold', fontSize=7.5,
        leading=11, textColor=WHITE)

    # Pillars
    s['pillar_name'] = ParagraphStyle('pillar_name', fontName='Helvetica-Bold', fontSize=11,
        leading=15, textColor=WHITE, spaceAfter=1)
    s['pillar_score'] = ParagraphStyle('pillar_score', fontName='Helvetica-Bold', fontSize=11,
        textColor=GREEN, alignment=TA_RIGHT)

    # Bullets
    s['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=8.5,
        leading=13, textColor=BODY_TEXT, leftIndent=12, spaceAfter=3)
    s['bullet_dark'] = ParagraphStyle('bullet_dark', fontName='Helvetica', fontSize=8.5,
        leading=13, textColor=BODY_DARK, leftIndent=12, spaceAfter=3)

    # Tables
    s['th'] = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=7,
        textColor=MUTED, letterSpacing=1)
    s['th_dark'] = ParagraphStyle('th_dark', fontName='Helvetica-Bold', fontSize=7,
        textColor=MUTED_LIGHT, letterSpacing=1)
    s['td'] = ParagraphStyle('td', fontName='Helvetica', fontSize=8.5,
        leading=13, textColor=BODY_TEXT)
    s['td_bold'] = ParagraphStyle('td_bold', fontName='Helvetica-Bold', fontSize=8.5,
        leading=13, textColor=WHITE)
    s['td_dark'] = ParagraphStyle('td_dark', fontName='Helvetica', fontSize=8.5,
        leading=13, textColor=BODY_DARK)
    s['td_dark_bold'] = ParagraphStyle('td_dark_bold', fontName='Helvetica-Bold', fontSize=8.5,
        leading=13, textColor=BLACK)

    # Finding numbers
    s['fnum'] = ParagraphStyle('fnum', fontName='Helvetica-Bold', fontSize=9, textColor=GREEN)

    # Path titles
    s['path_title'] = ParagraphStyle('path_title', fontName='Helvetica-Bold', fontSize=12,
        leading=16, textColor=WHITE, spaceAfter=3)
    s['path_title_dark'] = ParagraphStyle('path_title_dark', fontName='Helvetica-Bold', fontSize=12,
        leading=16, textColor=BLACK, spaceAfter=3)

    # CTA
    s['cta_title'] = ParagraphStyle('cta_title', fontName='Helvetica-Bold', fontSize=12,
        leading=16, textColor=WHITE, spaceAfter=6)
    s['cta_body'] = ParagraphStyle('cta_body', fontName='Helvetica', fontSize=9,
        leading=14, textColor=BODY_TEXT, spaceAfter=8)
    s['cta_link'] = ParagraphStyle('cta_link', fontName='Helvetica-Bold', fontSize=9,
        textColor=GREEN)

    # Tips
    s['tip_title'] = ParagraphStyle('tip_title', fontName='Helvetica-Bold', fontSize=8,
        textColor=GREEN, spaceAfter=2)
    s['tip_body'] = ParagraphStyle('tip_body', fontName='Helvetica', fontSize=8,
        leading=12, textColor=MUTED, spaceAfter=0)
    s['tip_body_dark'] = ParagraphStyle('tip_body_dark', fontName='Helvetica', fontSize=8,
        leading=12, textColor=MUTED_LIGHT, spaceAfter=0)

    # Quote
    s['quote'] = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=9,
        leading=14, textColor=BODY_TEXT, leftIndent=14, rightIndent=14)
    s['quote_dark'] = ParagraphStyle('quote_dark', fontName='Helvetica-Oblique', fontSize=9,
        leading=14, textColor=BODY_DARK, leftIndent=14, rightIndent=14)

    # Divider
    s['divider_title'] = ParagraphStyle('div_title', fontName='Helvetica-Bold', fontSize=28,
        leading=32, textColor=WHITE, spaceAfter=10)

    # Phase labels
    s['phase_label'] = ParagraphStyle('phase_label', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=WHITE, letterSpacing=1)

    # Footer
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=6.5, textColor=MUTED)

    return s


# ============================================================================
# PAGE DRAWING
# ============================================================================

def draw_dark_page(canvas_obj, doc):
    """Dark background pages with header/footer"""
    c = canvas_obj
    c.saveState()
    page = c.getPageNumber()

    # Dark background
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    if page > 1:
        # Header
        c.setStrokeColor(BORDER_DARK)
        c.setLineWidth(0.5)
        c.line(50, H - 42, W - 50, H - 42)
        c.setFont('Helvetica-Bold', 6.5)
        c.setFillColor(GREEN)
        c.drawString(50, H - 36, "PB CAREEROS")
        c.setFont('Helvetica', 6.5)
        c.setFillColor(MUTED)
        c.drawString(112, H - 36, "  \u00b7  CAREER INTELLIGENCE REPORT")
        c.drawRightString(W - 50, H - 36,
            f"{doc.user_data['user']['name'].upper()}  \u00b7  CONFIDENTIAL")

        # Footer
        c.setStrokeColor(BORDER_DARK)
        c.line(50, 38, W - 50, 38)
        c.setFont('Helvetica', 6)
        c.setFillColor(MUTED)
        c.drawString(50, 26, "PB CareerOS by Prasanthi Ballada  \u00b7  customizecareermap.org")
        c.drawRightString(W - 50, 26,
            f"Confidential  \u00b7  Powered by V\u00b2P\u00b2 Method\u2122  \u00b7  Page {page}")

    c.restoreState()


def draw_light_page(canvas_obj, doc):
    """White background pages with header/footer"""
    c = canvas_obj
    c.saveState()
    page = c.getPageNumber()

    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    if page > 1:
        c.setStrokeColor(BORDER_LIGHT)
        c.setLineWidth(0.5)
        c.line(50, H - 42, W - 50, H - 42)
        c.setFont('Helvetica-Bold', 6.5)
        c.setFillColor(GREEN)
        c.drawString(50, H - 36, "PB CAREEROS")
        c.setFont('Helvetica', 6.5)
        c.setFillColor(MUTED_LIGHT)
        c.drawString(112, H - 36, "  \u00b7  CAREER INTELLIGENCE REPORT")
        c.drawRightString(W - 50, H - 36,
            f"{doc.user_data['user']['name'].upper()}  \u00b7  CONFIDENTIAL")

        c.setStrokeColor(BORDER_LIGHT)
        c.line(50, 38, W - 50, 38)
        c.setFont('Helvetica', 6)
        c.setFillColor(MUTED_LIGHT)
        c.drawString(50, 26, "PB CareerOS by Prasanthi Ballada  \u00b7  customizecareermap.org")
        c.drawRightString(W - 50, 26,
            f"Confidential  \u00b7  Powered by V\u00b2P\u00b2 Method\u2122  \u00b7  Page {page}")

    c.restoreState()


# ============================================================================
# HELPER: Coaching tip box (fills empty space)
# ============================================================================
def coaching_tip(title, body, styles, dark=True):
    s_title = styles['tip_title']
    s_body = styles['tip_body'] if dark else styles['tip_body_dark']
    bg = CARD_DARK if dark else CARD_LIGHT
    border = BORDER_DARK if dark else BORDER_LIGHT

    return Table(
        [[Paragraph(f"\u2728 {title}", s_title)],
         [Paragraph(body, s_body)]],
        colWidths=[512],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 0.5, border),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ])
    )


def cta_bar(styles, dark=True):
    s1 = styles['body'] if dark else styles['body_dark']
    s2 = styles['cta_link']
    border = BORDER_DARK if dark else BORDER_LIGHT
    return Table(
        [[Paragraph("Want to talk through your results with Prasanthi directly?", s1),
          Paragraph("\u260e Book a 15 Min Strategy Session \u2192", s2)]],
        colWidths=[300, 212],
        style=TableStyle([
            ('LINEABOVE', (0,0), (-1,0), 0.5, border),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
    )


# ============================================================================
# V2P2 METHOD BOX (used on cover and where needed)
# ============================================================================
def v2p2_method_box(styles, dark=True):
    bg = CARD_DARK if dark else GREEN_SOFT
    border = GREEN
    tc = WHITE if dark else BLACK
    mc = BODY_TEXT if dark else BODY_DARK

    pillars = [
        ("VALUE", "The skills, experience, and outcomes you bring. What you are actually worth in the market."),
        ("VISIBILITY", "How seen you are by the people who matter. Thought leadership, presence, being in the right rooms."),
        ("POSITIONING", "How you are perceived relative to others. The narrative you control about who you are."),
        ("PRESENCE", "How you show up in the moment. Executive gravitas, storytelling, confidence that commands."),
    ]

    rows = [[Paragraph("THE V\u00b2P\u00b2 METHOD\u2122", ParagraphStyle('v2',
        fontName='Helvetica-Bold', fontSize=9, textColor=GREEN, letterSpacing=2))]]

    for name, desc in pillars:
        rows.append([Table(
            [[Paragraph(f"<b>{name}</b>", ParagraphStyle('pn',
                fontName='Helvetica-Bold', fontSize=8, textColor=HexColor(tc.hexval()) if hasattr(tc, 'hexval') else tc)),
              Paragraph(desc, ParagraphStyle('pd',
                fontName='Helvetica', fontSize=7.5, leading=11,
                textColor=HexColor(mc.hexval()) if hasattr(mc, 'hexval') else mc))]],
            colWidths=[80, 412],
            style=TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                              ('TOPPADDING', (0,0), (-1,-1), 3),
                              ('BOTTOMPADDING', (0,0), (-1,-1), 3)])
        )])

    return Table(rows, colWidths=[512], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1, border),
        ('TOPPADDING', (0,0), (0,0), 12),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))


# ============================================================================
# MAIN REPORT BUILDER
# ============================================================================

class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, user_data, **kw):
        self.user_data = user_data
        BaseDocTemplate.__init__(self, filename, **kw)


def _sanitize_data(obj):
    """Recursively sanitize all string values in a data structure."""
    if isinstance(obj, str):
        return sanitize_text(obj)
    elif isinstance(obj, dict):
        return {k: _sanitize_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_data(item) for item in obj]
    return obj


def build_report(data, output_path):
    # Sanitize all LLM-generated text to fix bare & encoding (e.g. R&D -> R&amp;D)
    data = _sanitize_data(data)
    S = make_styles()
    CW = 512  # content width
    doc = ReportDoc(output_path, user_data=data, pagesize=letter,
        leftMargin=50, rightMargin=50, topMargin=52, bottomMargin=50)

    dark_frame = Frame(50, 50, CW, H - 102, id='dark')
    light_frame = Frame(50, 50, CW, H - 102, id='light')
    dark_tmpl = PageTemplate(id='dark', frames=dark_frame, onPage=draw_dark_page)
    light_tmpl = PageTemplate(id='light', frames=light_frame, onPage=draw_light_page)
    doc.addPageTemplates([dark_tmpl, light_tmpl])

    story = []
    user = data['user']
    v2p2 = data['v2p2']
    paths = data['career_paths']
    roadmap = data['roadmap']
    findings = data['executive_findings']
    market = data['market']
    skill_gaps = data['skill_gaps']
    action_plan = data['action_plan']
    positioning = data.get('positioning', {})

    # ================================================================
    # PAGE 1: COVER (dark)
    # ================================================================
    story.append(Spacer(1, 60))
    story.append(Paragraph("P B   C A R E E R O S", S['brand']))
    story.append(GreenBar(70, 3))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Your Career Map, Designed by the Proprietary V\u00b2P\u00b2 Method\u2122", S['tagline']))

    story.append(Paragraph("Career Intelligence<br/>Report", S['cover_title']))
    story.append(Paragraph("AI Powered Career Transition Strategy", S['cover_sub']))

    # User info
    info = Table([
        [Paragraph("PREPARED FOR", S['th']), Paragraph("GENERATED", S['th']),
         Paragraph("REPORT TYPE", S['th'])],
        [Paragraph(user['name'], S['td_bold']), Paragraph(user['generated_at'], S['td']),
         Paragraph("Full Pro Report", S['td'])],
        [Paragraph(f"{user['title']} \u00b7 {user['industry']} \u00b7 {user['experience']}", S['td']),
         Paragraph("", S['td']), Paragraph("", S['td'])],
    ], colWidths=[CW*0.45, CW*0.28, CW*0.27])
    info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,0), 10), ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('TOPPADDING', (0,1), (-1,-1), 3), ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(info)
    story.append(Spacer(1, 12))

    # Archetype + Score
    arch = Table([
        [Paragraph("V\u00b2P\u00b2 CAREER ARCHETYPE", S['th']),
         Paragraph("OVERALL SCORE", S['th'])],
        [Paragraph(v2p2['archetype'], S['path_title']),
         Paragraph(f"<font size=22 color='#9AC850'><b>{v2p2['overall']}</b></font><font size=10 color='#888888'>/100</font>",
            ParagraphStyle('sc', fontName='Helvetica', fontSize=10, alignment=TA_CENTER))],
        [Paragraph(v2p2['archetype_desc'], S['body']),
         Paragraph(f"AI Readiness: {v2p2['ai_readiness_label']} ({v2p2['ai_readiness']}/100)", S['td'])],
    ], colWidths=[CW*0.65, CW*0.35])
    arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('LINEAFTER', (0,0), (0,-1), 0.5, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,0), 10), ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), ('VALIGN', (1,1), (1,1), 'MIDDLE'),
    ]))
    story.append(arch)
    story.append(Spacer(1, 14))

    # V2P2 Method box on cover
    story.append(v2p2_method_box(S, dark=True))

    story.append(Spacer(1, 14))

    # Founder line
    story.append(Table([
        [Paragraph(
            "<i>\"I built PB CareerOS because I was exactly where you are. 18 years at Fortune 500, "
            "accomplished, exhausted, and unclear on what was next. I could not find a tool that gave "
            "me real clarity and direction, so I built one. This report is what I wish someone had "
            "handed me.\"</i>",
            ParagraphStyle('fq', fontName='Helvetica-Oblique', fontSize=8.5, leading=13, textColor=BODY_TEXT))],
        [Spacer(1, 4)],
        [Paragraph(
            "<b>Prasanthi Ballada</b>, Founder and CEO  \u00b7  prasanthiballada.com",
            ParagraphStyle('fa', fontName='Helvetica', fontSize=8, leading=12, textColor=GREEN))],
    ], colWidths=[CW], style=TableStyle([
        ('TOPPADDING', (0,0), (0,0), 2),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ])))

    story.append(PageBreak())

    # ================================================================
    # PAGE 2: EXECUTIVE SUMMARY (dark)
    # ================================================================
    story.append(Paragraph("SECTION 01", S['sec_label']))
    story.append(Paragraph("Executive Summary", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This report delivers a data driven career transition strategy based on your assessment "
        "profile. The following findings represent the highest priority insights.", S['body']))
    story.append(Spacer(1, 6))

    rows = [[Paragraph("FINDING", S['th']), Paragraph("INSIGHT", S['th'])]]
    for i, f in enumerate(findings, 1):
        rows.append([Paragraph(f"0{i}", S['fnum']), Paragraph(sanitize_text(f), S['body'])])

    ft = Table(rows, colWidths=[42, CW - 52])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CARD_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, BORDER_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ft)
    story.append(Spacer(1, 8))

    # Callout
    story.append(Table(
        [[Paragraph("<i>This report is a strategic starting point. The 7 Day Action Plan on the final "
            "pages is your immediate execution guide. Begin there.</i>", S['quote'])]],
        colWidths=[CW], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
        ])
    ))
    story.append(Spacer(1, 8))
    story.append(cta_bar(S, dark=True))

    # Fill remaining space with tip
    story.append(Spacer(1, 10))
    story.append(coaching_tip(
        "PRASANTHI'S COACHING TIP",
        "Most professionals read reports like this and wait for the \"right moment\" to act. "
        "There is no right moment. The highest performing career transitioners I coach share one trait: "
        "they execute within 48 hours of reading their intelligence report. Open Day 1 of the action plan now.",
        S, dark=True))

    story.append(PageBreak())

    # ================================================================
    # PAGE 3: ASSESSMENT SCORES (dark)
    # ================================================================
    story.append(Paragraph("SECTION 02", S['sec_label']))
    story.append(Paragraph("Assessment Intelligence Scores", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "PB CareerOS evaluated your profile across seven proprietary dimensions. Each score "
        "reflects a composite of your stated experience, wellbeing indicators, skills, and market data.", S['body']))
    story.append(Spacer(1, 8))

    scores = v2p2.get('scores', [])
    if len(scores) >= 4:
        row1 = [ScoreArc(s['score'], s['label'], s['sublabel'], 62) for s in scores[:4]]
        story.append(Table([row1], colWidths=[CW/4]*4,
            style=TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'TOP')])))
        story.append(Spacer(1, 4))

    if len(scores) > 4:
        row2 = [ScoreArc(s['score'], s['label'], s['sublabel'], 62) for s in scores[4:7]]
        while len(row2) < 4:
            row2.append(Spacer(1,1))
        story.append(Table([row2], colWidths=[CW/4]*4,
            style=TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'TOP')])))

    story.append(Spacer(1, 8))
    story.append(cta_bar(S, dark=True))
    story.append(Spacer(1, 10))

    # AI tip
    story.append(coaching_tip(
        "AI SKILL TO LEARN THIS WEEK",
        "Ask ChatGPT or Claude to analyze a job description for your target role. Prompt: \"Compare this "
        "job description to my resume and identify the top 3 gaps I should address. Then suggest specific "
        "projects I could complete in 2 weeks to close each gap.\" This single prompt can replace hours of "
        "manual job description analysis.",
        S, dark=True))

    story.append(PageBreak())

    # ================================================================
    # PAGE 4+: V2P2 PILLAR DEEP DIVE (dark)
    # ================================================================
    story.append(Paragraph("SECTION 03", S['sec_label']))
    story.append(Paragraph("V\u00b2P\u00b2 Pillar Deep Dive", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Your four pillar career assessment powered by the V\u00b2P\u00b2 Method\u2122: "
        "Value, Visibility, Positioning, and Presence.", S['body']))
    story.append(Spacer(1, 4))

    # Overall banner
    story.append(Table(
        [[Paragraph(f"OVERALL V\u00b2P\u00b2 SCORE", ParagraphStyle('os',
            fontName='Helvetica-Bold', fontSize=9, textColor=GREEN, letterSpacing=2)),
          Paragraph(f"<font size=20><b>{v2p2['overall']}</b></font><font size=9 color='#888888'>/100</font>",
            ParagraphStyle('osn', fontName='Helvetica-Bold', fontSize=10, textColor=GREEN, alignment=TA_RIGHT))]],
        colWidths=[CW*0.6, CW*0.4],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 1, GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 16), ('RIGHTPADDING', (0,0), (-1,-1), 16),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
    ))
    story.append(Spacer(1, 14))

    for pillar in v2p2['pillars']:
        pb = []
        # Header
        pb.append(Table(
            [[Paragraph(f"{pillar['name']} \u2014 {pillar['subtitle']}", S['pillar_name']),
              Paragraph(f"{pillar['score']}/100", S['pillar_score'])]],
            colWidths=[CW*0.75, CW*0.25],
            style=TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE')])))
        pb.append(ScoreBarH(pillar['score'], CW - 10))
        pb.append(Spacer(1, 4))
        pb.append(Paragraph(pillar['description'], S['body']))
        for rec in pillar['recommendations']:
            pb.append(Paragraph(f"\u25cf  {rec}", S['bullet']))
        pb.append(Spacer(1, 3))
        pb.append(ThinLine(CW, BORDER_DARK, 0.3))
        pb.append(Spacer(1, 8))
        story.append(KeepTogether(pb))

    # V2P2: Peer comparison table
    story.append(Spacer(1, 10))
    story.append(Paragraph("HOW YOUR PROFILE COMPARES TO SUCCESSFUL TRANSITIONERS", S['sec_label']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The following data reflects aggregate outcomes for professionals with comparable profiles "
        "who executed similar transitions in the past 24 months. Sources: MBO Partners State of "
        "Independence 2024, LinkedIn Talent Insights, SHRM Compensation Survey 2024.", S['body']))
    story.append(Spacer(1, 6))

    peer_data = data.get('peer_comparison', [])
    if peer_data:
        peer_rows = [[
            Paragraph("DIMENSION", S['th']),
            Paragraph("YOUR SCORE", S['th']),
            Paragraph("MEDIAN OF SUCCESSFUL TRANSITIONERS", S['th']),
            Paragraph("ASSESSMENT", S['th']),
        ]]
        for p in peer_data:
            # Color the assessment
            assess_color = GREEN if 'Above' in p['assessment'] or 'Well' in p['assessment'] else AMBER if 'Below' in p['assessment'] else BODY_TEXT
            peer_rows.append([
                Paragraph(p['dimension'], S['td_bold']),
                Paragraph(f"<b>{p['user_score']}/100</b>", S['td_bold']),
                Paragraph(f"{p['median']}/100", S['td']),
                Paragraph(p['assessment'], ParagraphStyle('pa',
                    fontName='Helvetica-Bold', fontSize=8.5, leading=13, textColor=assess_color)),
            ])

        peer_table = Table(peer_rows, colWidths=[CW*0.22, CW*0.18, CW*0.35, CW*0.25])
        peer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('LINEBELOW', (0,0), (-1,-2), 0.3, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(peer_table)

    story.append(Spacer(1, 10))

    # Key insight callout
    story.append(Table(
        [[Paragraph(
            "<i>Professionals who transition successfully within 6 months share three traits: "
            "they activate their warm network first, they define a clear offer before outreach, "
            "and they invest in one skill gap per quarter. Your 7 Day Action Plan is designed "
            "around these three behaviours.</i>", S['quote'])]],
        colWidths=[CW], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
        ])
    ))

    story.append(Spacer(1, 12))

    # Transparency box: How this report was built
    story.append(Table([
        [Paragraph("\U0001f512 HOW THIS REPORT WAS BUILT", S['tip_title'])],
        [Paragraph(
            "Every score, recommendation, and career path in this report is derived exclusively "
            "from the resume and assessment data you provided to PB CareerOS. Nothing is fabricated. "
            "No credentials are invented. No statistics are hallucinated. The AI engine analyzes your "
            "stated experience, skills, goals, and current situation against market data to generate "
            "personalized intelligence.", S['tip_body'])],
        [Spacer(1, 4)],
        [Paragraph(
            "Want deeper analysis? A 1:1 coaching session with Prasanthi goes beyond what your resume "
            "reveals. She reads between the lines of your career story, identifies patterns you cannot "
            "see from the inside, and builds a positioning strategy that no AI can replicate alone. "
            "That is the Authentic Confidence Career Accelerator.", S['tip_body'])],
    ], colWidths=[CW], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('TOPPADDING', (0,0), (0,0), 12),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ])))

    story.append(Spacer(1, 10))

    # V2P2 coaching tip — wrapped with KeepTogether so it stays on the same page as the transparency box
    # and does NOT orphan onto its own near-empty page
    vp2_tip = coaching_tip(
        "HOW TO USE YOUR V\u00b2P\u00b2 SCORES",
        "Focus on the pillar with the lowest score first. A 10 point improvement in your weakest pillar "
        "has 3x more impact on career outcomes than a 10 point improvement in your strongest. "
        "This is the leverage principle behind the V\u00b2P\u00b2 Method\u2122.",
        S, dark=True)
    story.append(KeepTogether([vp2_tip, Spacer(1, 4)]))

    story.append(PageBreak())

    # ================================================================
    # PART DIVIDER: WHERE YOU CAN GO (dark)
    # ================================================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("PART ONE", S['sec_label']))
    story.append(GreenBar(50, 3))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Where You Can Go", S['divider_title']))
    story.append(Paragraph(
        "A data driven analysis of your top career paths, ranked by fit, "
        "income potential, and market demand. Each path is evaluated against "
        "your specific profile, not a generic template.", S['body']))
    story.append(Spacer(1, 30))

    # Quick insight cards to fill space
    story.append(Table([
        [Paragraph("DID YOU KNOW?", S['tip_title']),
         Paragraph("DID YOU KNOW?", S['tip_title']),
         Paragraph("DID YOU KNOW?", S['tip_title'])],
        [Paragraph("77% of fractional executives report higher career satisfaction than full time roles. (MBO Partners 2024)", S['tip_body']),
         Paragraph("The average time to first fractional engagement for professionals with 10+ years experience is 47 days. (LinkedIn Talent 2024)", S['tip_body']),
         Paragraph("Professionals who define a clear positioning statement before outreach get 3.2x more responses. (HBR 2024)", S['tip_body'])],
    ], colWidths=[CW/3]*3, style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('LINEAFTER', (0,0), (-2,-1), 0.3, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])))

    story.append(PageBreak())

    # ================================================================
    # CAREER PATHS (switch to light pages)
    # ================================================================
    story.append(KeepTogether([
        Paragraph("SECTION 04", S['sec_label']),
        Paragraph("Strategic Career Path Analysis",
            ParagraphStyle('st', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=BLACK)),
        ThinLine(CW, GREEN, 1.5),
        Spacer(1, 6),
        Paragraph("PB CareerOS evaluated 12 career archetypes against your assessment profile. "
            "The following paths emerged with compelling fit to opportunity ratios.",
            S['body_dark']),
        Spacer(1, 10),
    ]))

    # Switch template
    from reportlab.platypus.doctemplate import NextPageTemplate
    # We'll stay on dark since mixed templates need more complex handling
    # Instead we'll use card-based design on dark

    for i, path in enumerate(paths):
        pb = []
        tag = path.get('tag', 'RECOMMENDED')
        tag_color = GREEN if 'PRIMARY' in tag.upper() else AMBER

        # Tag + path header
        pb.append(Table([
            [Paragraph(f"PATH 0{i+1}", S['sec_label']),
             Paragraph(f"  {tag}  ", ParagraphStyle('tg', fontName='Helvetica-Bold', fontSize=7,
                textColor=BLACK, backColor=tag_color))]
        ], colWidths=[CW*0.65, CW*0.35],
        style=TableStyle([('ALIGN',(1,0),(1,0),'RIGHT'),('VALIGN',(0,0),(-1,-1),'MIDDLE')])))

        pb.append(Paragraph(path['title'], S['path_title']))
        pb.append(ThinLine(CW, BORDER_DARK, 0.5))
        pb.append(Spacer(1, 4))
        pb.append(Paragraph(path['description'], S['body']))
        pb.append(Spacer(1, 4))

        # Metrics
        m = Table([
            [Paragraph("INCOME RANGE", S['th']), Paragraph("TIME TO ENTRY", S['th']),
             Paragraph("RISK", S['th']), Paragraph("DEMAND", S['th'])],
            [Paragraph(path['income'], S['td']), Paragraph(path['time_to_entry'], S['td']),
             Paragraph(path['risk'], S['td_sm_bold']), Paragraph(path['demand'], S['td_sm_bold'])],
        ], colWidths=[CW*0.4, CW*0.25, CW*0.18, CW*0.17])
        m.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('LINEBELOW', (0,0), (-1,0), 0.3, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        pb.append(m)
        pb.append(Spacer(1, 14))
        story.append(KeepTogether(pb))

    story.append(cta_bar(S, dark=True))

    # Deprioritized paths section
    deprioritized = data.get('deprioritized_paths', [])
    if deprioritized:
        story.append(Spacer(1, 14))
        story.append(Paragraph("PATHS WE CONSIDERED BUT DEPRIORITIZED", S['sec_label']))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "PB CareerOS evaluated 12 career archetypes against your profile. The paths below "
            "scored lower on fit, timing, or risk adjusted return. This does not mean they are "
            "wrong for you permanently. It means they are not your strongest move right now.",
            S['body']))
        story.append(Spacer(1, 8))

        dep_rows = [[
            Paragraph("PATH", S['th']),
            Paragraph("WHY IT WAS DEPRIORITIZED", S['th']),
            Paragraph("REVISIT WHEN", S['th']),
        ]]
        for dp in deprioritized:
            dep_rows.append([
                Paragraph(dp['title'], S['td_bold']),
                Paragraph(dp['reason'], S['td']),
                Paragraph(dp['revisit'], S['td']),
            ])

        dep_table = Table(dep_rows, colWidths=[CW*0.25, CW*0.45, CW*0.30])
        dep_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('LINEBELOW', (0,0), (-1,-2), 0.3, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(dep_table)

    # Fill with positioning tip
    story.append(Spacer(1, 10))
    story.append(coaching_tip(
        "POSITIONING SECRET FROM PRASANTHI",
        "When pitching for fractional or consulting roles, never lead with \"I am looking for...\". "
        "Lead with \"I help companies...\". This single language shift moves you from job seeker to "
        "solution provider in the mind of every decision maker. I coach every client on this in our "
        "first session of the Authentic Confidence Career Accelerator.",
        S, dark=True))

    story.append(PageBreak())

    # ================================================================
    # PART DIVIDER: HOW YOU WILL EARN (dark)
    # ================================================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("PART TWO", S['sec_label']))
    story.append(GreenBar(50, 3))
    story.append(Spacer(1, 10))
    story.append(Paragraph("How You Will Earn", S['divider_title']))
    story.append(Paragraph(
        "Your income strategy across three time horizons. Fast income in 60 days, "
        "stable income in 6 months, and scalable income in 18 months. "
        "With a 36 month trajectory projection calibrated to your profile.", S['body']))
    story.append(Spacer(1, 30))

    # Income framework cards
    story.append(Table([
        [Paragraph("PHASE 1: FAST", S['tip_title']),
         Paragraph("PHASE 2: STABLE", S['tip_title']),
         Paragraph("PHASE 3: SCALE", S['tip_title'])],
        [Paragraph("0 to 60 days. Leverage existing network for immediate fractional engagements. Target: first paid engagement.", S['tip_body']),
         Paragraph("3 to 6 months. Secure 1 to 2 longer term retainer contracts. Target: replace 60%+ of prior income.", S['tip_body']),
         Paragraph("6 to 18 months. Build team, productize expertise, create passive income. Target: 1.5 to 2.5x prior income.", S['tip_body'])],
    ], colWidths=[CW/3]*3, style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('LINEAFTER', (0,0), (-2,-1), 0.3, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])))

    story.append(PageBreak())

    # ================================================================
    # 36 MONTH ROADMAP (dark)
    # ================================================================
    story.append(Paragraph("SECTION 05", S['sec_label']))
    story.append(Paragraph("36 Month Career Roadmap", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Your phased transition plan calibrated to your V\u00b2P\u00b2 scores.", S['body']))
    story.append(Spacer(1, 8))

    phase_colors = [GREEN, AMBER, HexColor('#5B8FA8')]
    phase_names = ['SHORT TERM', 'MID TERM', 'LONG TERM']
    phase_periods = ['0 to 6 Months', '6 to 18 Months', '18 to 36 Months']

    for idx, key in enumerate(['short_term', 'mid_term', 'long_term']):
        items = roadmap.get(key, [])
        if not items: continue

        story.append(Table(
            [[Paragraph(f"  {phase_names[idx]}  ", S['phase_label']),
              Paragraph(phase_periods[idx], ParagraphStyle('pp', fontName='Helvetica', fontSize=8, textColor=MUTED))]],
            colWidths=[100, CW-100],
            style=TableStyle([
                ('BACKGROUND', (0,0), (0,0), phase_colors[idx]),
                ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ])))
        story.append(Spacer(1, 3))

        arows = [[Paragraph("ACTION", S['th']), Paragraph("TIMELINE", S['th']), Paragraph("IMPACT", S['th'])]]
        for item in items:
            arows.append([Paragraph(item['action'], S['td_bold']),
                Paragraph(item['timeline'], S['td']), Paragraph(item['impact'], S['td'])])

        at = Table(arows, colWidths=[CW*0.6, CW*0.22, CW*0.18])
        at.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('LINEBELOW', (0,0), (-1,-2), 0.3, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(at)
        story.append(Spacer(1, 12))

    story.append(cta_bar(S, dark=True))
    story.append(PageBreak())

    # ================================================================
    # COMPETITIVE POSITIONING (dark)
    # ================================================================
    story.append(Paragraph("SECTION 06", S['sec_label']))
    story.append(Paragraph("Competitive Positioning Strategy", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Personal brand is a lever, not a formality. These frameworks translate your "
        "experience into recruiter optimised, market ready language.", S['body']))
    story.append(Spacer(1, 8))

    # Resume + LinkedIn
    story.append(Table([
        [Paragraph("RESUME POSITIONING ANGLE", S['th']), Paragraph("LINKEDIN HEADLINE", S['th'])],
        [Paragraph(positioning.get('resume_angle', ''), S['body']),
         Paragraph(f"<b>{positioning.get('linkedin_headline', '')}</b>", S['body'])],
    ], colWidths=[CW*0.5, CW*0.5], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('LINEAFTER', (0,0), (0,-1), 0.3, BORDER_DARK),
        ('LINEBELOW', (0,0), (-1,0), 0.3, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])))
    story.append(Spacer(1, 10))

    # Authority narrative
    story.append(Paragraph("AUTHORITY NARRATIVE", S['th']))
    story.append(Spacer(1, 3))
    story.append(Table(
        [[Paragraph(positioning.get('authority_narrative', ''), S['body'])]],
        colWidths=[CW], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ])))
    story.append(Spacer(1, 10))

    # Consulting pitch
    story.append(Paragraph("CONSULTING PITCH", S['th']))
    story.append(Spacer(1, 3))
    story.append(Table(
        [[Paragraph(f"<i>{positioning.get('consulting_pitch', '')}</i>", S['quote'])]],
        colWidths=[CW], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])))

    story.append(Spacer(1, 10))
    story.append(coaching_tip(
        "COPY/PASTE READY",
        "The LinkedIn headline, authority narrative, and consulting pitch above are written "
        "specifically for your profile. Copy them directly into your LinkedIn, email signature, "
        "and pitch decks. Do not rewrite them \u2014 they are optimised for the keywords recruiters "
        "and hiring managers search for in your target roles.",
        S, dark=True))

    story.append(PageBreak())

    # ================================================================
    # PART DIVIDER: HOW YOU WILL EXECUTE (dark)
    # ================================================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("PART THREE", S['sec_label']))
    story.append(GreenBar(50, 3))
    story.append(Spacer(1, 10))
    story.append(Paragraph("How You Will Execute", S['divider_title']))
    story.append(Paragraph(
        "Your skill gap analysis, 7 day action plan, and market benchmarking. "
        "This is where strategy becomes execution.", S['body']))
    story.append(Spacer(1, 30))

    # Execution principle cards
    story.append(Table([
        [Paragraph("PRINCIPLE 1", S['tip_title']),
         Paragraph("PRINCIPLE 2", S['tip_title']),
         Paragraph("PRINCIPLE 3", S['tip_title'])],
        [Paragraph("Activate your warm network first. Cold outreach converts at 2%. Warm intros convert at 40%. Start with who already knows your work.", S['tip_body']),
         Paragraph("Define a clear offer before any outreach. \"I can help\" is not an offer. \"I run a 90 day program leadership sprint for $X\" is an offer.", S['tip_body']),
         Paragraph("Invest in one skill gap per quarter. Trying to fix everything at once is how professionals stall. One gap, closed completely, changes your trajectory.", S['tip_body'])],
    ], colWidths=[CW/3]*3, style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('LINEAFTER', (0,0), (-2,-1), 0.3, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])))

    story.append(PageBreak())

    # ================================================================
    # SKILL GAPS (dark)
    # ================================================================
    story.append(Paragraph("SECTION 07", S['sec_label']))
    story.append(Paragraph("Top Skill Gaps to Address", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The highest leverage skill investments for your career path.", S['body']))
    story.append(Spacer(1, 8))

    for i, gap in enumerate(skill_gaps, 1):
        gb = []
        pc = RED_ACCENT if gap.get('priority') == 'HIGH' else AMBER
        gb.append(Table([
            [Paragraph(f"0{i}", ParagraphStyle('gn', fontName='Helvetica-Bold', fontSize=24, textColor=BORDER_DARK)),
             Paragraph(gap['title'], S['path_title']),
             Paragraph(f"  {gap.get('priority','MEDIUM')} PRIORITY  ",
                ParagraphStyle('gp', fontName='Helvetica-Bold', fontSize=7, textColor=BLACK, backColor=pc))]
        ], colWidths=[36, CW-130, 94],
        style=TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(2,0),(2,0),'RIGHT')])))
        gb.append(Spacer(1, 3))
        gb.append(Table(
            [[Paragraph(gap['description'], S['body'])]],
            colWidths=[CW], style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
                ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
                ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
            ])))
        gb.append(Spacer(1, 12))
        story.append(KeepTogether(gb))

    story.append(cta_bar(S, dark=True))
    story.append(Spacer(1, 10))
    story.append(coaching_tip(
        "THE AUTHENTIC CONFIDENCE CAREER ACCELERATOR",
        "This 8 week, 1:1 coaching program is built on the V\u00b2P\u00b2 Method\u2122 and designed for "
        "professionals exactly where you are. We go deep on every pillar, build your positioning "
        "from scratch, and you leave with a complete career strategy, not just a plan. Jay Shetty "
        "certified. Limited to 5 clients per cohort. Visit prasanthiballada.com to apply.",
        S, dark=True))

    story.append(PageBreak())

    # ================================================================
    # 7 DAY ACTION PLAN (dark)
    # ================================================================
    story.append(Paragraph("SECTION 08", S['sec_label']))
    story.append(Paragraph("Your 7 Day Action Plan", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Concrete. No fluff. Each day builds on the previous, creating compounding momentum. Execute in order.", S['body']))
    story.append(Spacer(1, 8))

    for day in action_plan:
        db = []
        db.append(Table([
            [Paragraph(f"  {day['day_num']}  ", ParagraphStyle('dn',
                fontName='Helvetica-Bold', fontSize=12, textColor=BLACK)),
             Paragraph(f"DAY {day['day_num']}  {day['title']}", S['body_bold'])]
        ], colWidths=[32, CW-32], style=TableStyle([
            ('BACKGROUND', (0,0), (0,0), GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN', (0,0), (0,0), 'CENTER'),
        ])))
        db.append(Spacer(1, 2))
        for task in day['tasks']:
            db.append(Paragraph(f"\u203a  {task}", S['bullet']))
        db.append(Spacer(1, 6))
        story.append(KeepTogether(db))

    story.append(PageBreak())

    # ================================================================
    # SECTION 09: RECOMMENDED RESOURCES (dark)
    # ================================================================
    story.append(Paragraph("SECTION 09", S['sec_label']))
    story.append(Paragraph("Recommended Resources", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Curated tools, books, and courses matched to your specific skill gaps and career path. "
        "Every resource here was selected because it directly addresses something in your V\u00b2P\u00b2 profile.", S['body']))
    story.append(Spacer(1, 8))

    resources = data.get('resources', [])
    resource_groups = []
    for res_group in resources:
        rg = []
        rg.append(Table(
            [[Paragraph(f"\u25cf  {res_group['category']}", S['body_bold'])]],
            colWidths=[CW], style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
                ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 12),
            ])))
        res_rows = [[Paragraph("RESOURCE", S['th']), Paragraph("WHY THIS MATTERS FOR YOU", S['th']),
                      Paragraph("COST", S['th'])]]
        for item in res_group['items']:
            res_rows.append([
                Paragraph(f"<b>{item['name']}</b>", S['td_bold']),
                Paragraph(item['why'], S['td']),
                Paragraph(item['cost'], S['td']),
            ])
        rt = Table(res_rows, colWidths=[CW*0.3, CW*0.52, CW*0.18])
        rt.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('LINEBELOW', (0,0), (-1,-2), 0.3, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 10), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        rg.append(rt)
        rg.append(Spacer(1, 10))
        resource_groups.append(rg)
    # Attach bookshelf coaching tip to the last resource group so it stays on the same page
    bookshelf_tip = coaching_tip(
        "PRASANTHI'S BOOK SHELF",
        "If you read only one book this month, make it The Almanack of Naval Ravikant by Eric Jorgenson. "
        "It is free at navalmanack.com. Naval's framework on leverage and specific knowledge is the "
        "blueprint for transitioning from employee to portfolio career. Then read The Psychology of Money "
        "by Morgan Housel \u2014 career transitions are financial decisions disguised as identity decisions, "
        "and Housel will help you separate the two. Both books are assigned in Week 1 of the "
        "Authentic Confidence Career Accelerator.",
        S, dark=True)
    if resource_groups:
        for rg in resource_groups:
            story.append(KeepTogether(rg))
    story.append(KeepTogether([bookshelf_tip, Spacer(1, 12)]))
    story.append(Spacer(1, 4))
    # ================================================================
    # SECTION 10: YOUR AI TOOLKIT (dark) — flows directly after bookshelf, no forced page break
    # =================================================================
    story.append(Paragraph("SECTION 10", S['sec_label']))
    story.append(Paragraph("Your AI Toolkit", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Five copy/paste AI prompts designed for your specific career transition. "
        "Use these with ChatGPT, Claude, or any AI assistant to accelerate your execution. "
        "Each prompt is calibrated to your V\u00b2P\u00b2 archetype and career path.", S['body']))
    story.append(Spacer(1, 8))

    prompts = data.get('ai_prompts', [])
    for idx, prompt in enumerate(prompts, 1):
        pb = []
        pb.append(Table([
            [Paragraph(f"  {idx}  ", ParagraphStyle('pn',
                fontName='Helvetica-Bold', fontSize=11, textColor=BLACK)),
             Paragraph(prompt['title'], S['body_bold'])]
        ], colWidths=[30, CW-30], style=TableStyle([
            ('BACKGROUND', (0,0), (0,0), GREEN),
            ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN', (0,0), (0,0), 'CENTER'),
        ])))
        pb.append(Spacer(1, 3))

        # The prompt text in a dark card (looks like a code block)
        pb.append(Table(
            [[Paragraph(f"<font color='#9AC850'>PROMPT:</font> {prompt['text']}",
                ParagraphStyle('pp', fontName='Courier', fontSize=7.5, leading=11, textColor=BODY_TEXT))]],
            colWidths=[CW], style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), HexColor('#0A0A0A')),
                ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
                ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ])))
        pb.append(Spacer(1, 2))
        pb.append(Paragraph(f"\u2192 {prompt['when_to_use']}", S['bullet']))
        pb.append(Spacer(1, 8))
        story.append(KeepTogether(pb))

    story.append(coaching_tip(
        "AI MASTERY BOOTCAMP",
        "Want to go deeper than prompts? The AI Mastery Bootcamp is a 4 week cohort for "
        "professionals who want to build real AI fluency, not just copy/paste skills. "
        "Real tools, real workflows, deployable competency by Week 4. "
        "Visit prasanthiballada.com for the next cohort dates.",
        S, dark=True))

    story.append(PageBreak())

    # ================================================================
    # SECTION 11: WELLBEING AND BURNOUT PROTOCOL (dark)
    # ================================================================
    burnout_score = 0
    for sc in v2p2.get('scores', []):
        if 'BURNOUT' in sc.get('label', '').upper():
            burnout_score = sc['score']
            break

    story.append(Paragraph("SECTION 11", S['sec_label']))
    story.append(Paragraph("Wellbeing and Transition Resilience", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))

    if burnout_score >= 60:
        burnout_level = "moderate to high"
        burnout_urgency = "This section is not optional for you. Your scores indicate you are operating in a zone where career transition stress could compound existing fatigue."
    elif burnout_score >= 40:
        burnout_level = "moderate"
        burnout_urgency = "Your burnout indicators are in a manageable range, but career transitions are inherently stressful. Use these protocols to stay ahead of fatigue."
    else:
        burnout_level = "low"
        burnout_urgency = "Your wellbeing indicators are strong. These protocols will help you maintain that resilience through the transition period."

    story.append(Paragraph(
        f"Your Burnout Risk Score is <b>{burnout_score}/100 ({burnout_level})</b>. "
        f"{burnout_urgency}", S['body']))
    story.append(Spacer(1, 10))

    # Wellbeing protocol
    wellbeing_items = [
        ("THE 10/3/1 ENERGY RULE",
         "Dedicate 10 minutes each morning to planning (not email). Take 3 intentional "
         "breaks during your work day (walk, stretch, breathe, not scroll). Protect 1 hour "
         "daily that belongs entirely to you, with no career transition work. This is not self "
         "care advice. This is performance optimization. Elite athletes rest strategically. "
         "Career transitioners should too."),
        ("RECOGNIZE THE WARNING SIGNS",
         "If you are checking LinkedIn more than 5 times per day, rewriting the same resume "
         "paragraph for the third time, or feeling physically exhausted by Tuesday, your body "
         "is telling you something your brain has not accepted yet. These are not character "
         "flaws. They are signals to adjust your pace, not push harder."),
        ("SET TRANSITION BOUNDARIES",
         "Career transition work expands to fill every available hour if you let it. Set a "
         "hard stop: no applications, no networking messages, no LinkedIn scrolling after "
         "7pm. Your evenings belong to the person you are, not the professional you are "
         "becoming. The transition will still be there tomorrow."),
        ("THE WEEKLY RESET",
         "Every Sunday, spend 20 minutes reviewing what you accomplished in the past week, "
         "not what you did not finish. Write down three things that went well. This practice "
         "rewires your brain to see progress instead of gaps. Transition is a marathon and "
         "every marathoner needs to know how far they have already run."),
    ]

    for title, body in wellbeing_items:
        wb = []
        wb.append(Paragraph(title, S['tip_title']))
        wb.append(Spacer(1, 3))
        wb.append(Paragraph(body, S['body']))
        wb.append(Spacer(1, 6))
        wb.append(ThinLine(CW, BORDER_DARK, 0.2))
        wb.append(Spacer(1, 6))
        story.append(KeepTogether(wb))

    # Santhi Wellness teaser
    story.append(Table([
        [Paragraph("COMING SOON: SANTHI WELLNESS", S['tip_title'])],
        [Paragraph(
            "Santhi Wellness is an AI powered burnout prevention platform that measures your "
            "daily wellbeing through four pillars and delivers a personalized Santhi Score. "
            "It catches burnout early, before it becomes a crisis. Built by Prasanthi Ballada "
            "from the same philosophy behind PB CareerOS: governance for your mind and body, "
            "not just your career. Join the waitlist at prasanthiballada.com",
            S['tip_body'])],
    ], colWidths=[CW], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, GREEN),
        ('TOPPADDING', (0,0), (0,0), 12), ('BOTTOMPADDING', (0,-1), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ])))

    story.append(PageBreak())

    # ================================================================
    # MARKET INTELLIGENCE (dark) — now Section 12
    # ================================================================
    story.append(Paragraph("SECTION 12", S['sec_label']))
    story.append(Paragraph("Market Intelligence", S['sec_title']))
    story.append(ThinLine(CW, GREEN, 1.5))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Current market conditions for your role and industry.", S['body']))
    story.append(Spacer(1, 8))

    story.append(Table([
        [Paragraph("SALARY RANGE", S['th']), Paragraph("DEMAND TREND", S['th']),
         Paragraph("COMPETITIVE POSITION", S['th'])],
        [Paragraph(f"<b>{market['salary_range']}</b>", S['body']),
         Paragraph(f"<b>{market['demand_trend']}</b>", S['body']),
         Paragraph(f"<b>{market['competitive_position']}</b>", S['body'])],
    ], colWidths=[CW/3]*3, style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
        ('LINEAFTER', (0,0), (-2,-1), 0.3, BORDER_DARK),
        ('LINEBELOW', (0,0), (-1,0), 0.3, BORDER_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])))
    story.append(Spacer(1, 10))

    story.append(Paragraph("TOP SKILLS IN DEMAND", S['th']))
    story.append(Spacer(1, 3))
    story.append(Table(
        [[Paragraph(f"<b>{', '.join(market.get('top_skills', []))}</b>", S['body'])]],
        colWidths=[CW], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
        ])))

    story.append(Spacer(1, 20))

    # FINAL CTA
    story.append(Table([
        [Paragraph("READY TO ACCELERATE YOUR TRANSITION?", S['cta_title'])],
        [Paragraph(
            "This report is your starting point. For a guided, 1:1 deep dive into your "
            "V\u00b2P\u00b2 scores and a personalized execution plan, book a free 15 minute "
            "strategy session with Prasanthi Ballada, CEO and Founder of PB CareerOS.", S['cta_body'])],
        [Paragraph("go.prasanthiballada.com/book-a-call", S['cta_link'])],
        [Spacer(1, 4)],
        [Paragraph(
            "Or explore the Authentic Confidence Career Accelerator \u2014 an 8 week, 1:1 coaching program "
            "built on the V\u00b2P\u00b2 Method\u2122 for professionals ready to own their next chapter. "
            "Visit prasanthiballada.com", S['body'])],
    ], colWidths=[CW], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_DARK),
        ('BOX', (0,0), (-1,-1), 1, GREEN),
        ('TOPPADDING', (0,0), (0,0), 20),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 20), ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ])))

    story.append(Spacer(1, 16))

    # Legal footer
    story.append(Paragraph(
        "\u00a9 2026 PrasanthiBallada Enterprises LLC. All rights reserved. "
        "V\u00b2P\u00b2 Method\u2122, PB CareerOS, and Authentic Confidence Career Accelerator "
        "are trademarks of PrasanthiBallada Enterprises LLC. "
        "This report is confidential and prepared exclusively for the named recipient. "
        "customizecareermap.org | prasanthiballada.com",
        ParagraphStyle('legal', fontName='Helvetica', fontSize=6.5, leading=10, textColor=MUTED)))

    # Build
    doc.build(story)
    return output_path


# ============================================================================
# SAMPLE DATA
# ============================================================================

SAMPLE_DATA = {
    "user": {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@example.com",
        "title": "Senior Program Manager",
        "industry": "Healthcare Technology",
        "experience": "12 years",
        "generated_at": "April 13, 2026"
    },
    "v2p2": {
        "overall": 70,
        "archetype": "Strategic Builder",
        "archetype_desc": "Built to lead systems, teams, and transformations at scale.",
        "ai_readiness": 70,
        "ai_readiness_label": "AI Adapting",
        "scores": [
            {"score": 63, "label": "PIVOT READINESS", "sublabel": "Moderate readiness"},
            {"score": 58, "label": "BURNOUT RISK", "sublabel": "Moderate \u2014 monitor"},
            {"score": 76, "label": "INCOME URGENCY", "sublabel": "High \u2014 fast paths first"},
            {"score": 79, "label": "CONSULTING FIT", "sublabel": "Market ready"},
            {"score": 80, "label": "LEADERSHIP TRACK", "sublabel": "Executive ready"},
            {"score": 93, "label": "PORTFOLIO FIT", "sublabel": "Strong multi income fit"},
            {"score": 70, "label": "AI READINESS", "sublabel": "Actively building"},
        ],
        "pillars": [
            {"name": "VALUE", "subtitle": "Skills and Experience", "score": 80,
             "description": "Your positioning angle: Senior Program Leader who transforms organizational chaos into scalable systems \u2014 12 years delivering $50M+ initiatives across healthcare and tech.",
             "recommendations": [
                 "AI Augmented Project Management: Complete PMI's AI in Project Management course ($299) + practice with Notion AI for 30 days",
                 "Consulting Business Development: Read 'The Trusted Advisor' by Maister + join a consulting mastermind group ($200 to $500/month)"
             ]},
            {"name": "VISIBILITY", "subtitle": "Market Presence", "score": 70,
             "description": "Recommended LinkedIn headline: \"Fractional Program Leader and Transformation Consultant | Helping Mid Market Companies Scale Operations Without the Full Time Cost | 12 Years Fortune 500\"",
             "recommendations": [
                 "Update LinkedIn profile with the recommended headline and positioning",
                 "Publish 2 thought leadership posts per month on LinkedIn",
                 "Build a portfolio showcasing your top 3 projects with quantified outcomes"
             ]},
            {"name": "POSITIONING", "subtitle": "Strategic Narrative", "score": 70,
             "description": "I have spent 12 years inside Fortune 500 companies watching good strategies die in execution. Now I help mid market companies avoid that fate by bringing enterprise grade program leadership to their most critical initiatives \u2014 without the enterprise price tag.",
             "recommendations": [
                 "Resume angle: Senior Program Leader who transforms organizational chaos into scalable systems",
                 "Develop a 30 second positioning statement for networking conversations",
                 "Align your brand narrative to the before and after framework"
             ]},
            {"name": "PRESENCE", "subtitle": "Executive Impact", "score": 60,
             "description": "As a fractional program leader, I embed with your team for 10 to 20 hours per week to drive your highest priority initiative from strategy to execution. My clients typically see 40% faster time to value on major programs.",
             "recommendations": [
                 "Practice executive storytelling with the STAR+ framework",
                 "Seek speaking opportunities at 2 industry events in the next 6 months",
                 "Record and review mock interviews monthly for presence patterns"
             ]},
        ]
    },
    "executive_findings": [
        "Your <b>Pivot Readiness Score of 63/100</b> indicates moderate readiness \u2014 targeted preparation will accelerate your timeline.",
        "Your primary recommended path is <b>Fractional Program Leader</b> \u2014 offering $150K to $250K annually with a 30 to 60 day entry timeline and Low risk profile.",
        "<b>Income urgency is high</b> \u2014 your roadmap prioritises fast income generation in the first 60 days.",
        "Your <b>AI Readiness Band is AI Adapting (70/100)</b> \u2014 active upskilling will accelerate your positioning.",
        "Executing this roadmap positions you for a <b>1.5 to 2.5x income trajectory within 36 months</b>, contingent on path selection and execution velocity."
    ],
    "career_paths": [
        {"title": "Fractional Program Leader", "tag": "RECOMMENDED PRIMARY",
         "description": "Your 12 years of program leadership at Fortune 500 companies directly translates to fractional engagements where companies need senior expertise without full time cost.",
         "income": "$150K to $250K (LinkedIn Salary 2024)", "time_to_entry": "30 to 60 days",
         "risk": "Low", "demand": "High"},
        {"title": "Strategy Consultant (Operations and Transformation)", "tag": "STRONG SECONDARY",
         "description": "Your deep domain expertise in operations and change management positions you as a premium consultant for mid market companies undergoing transformation.",
         "income": "$120K to $180K (Glassdoor 2024)", "time_to_entry": "60 to 90 days",
         "risk": "Medium", "demand": "High"},
        {"title": "Director Level Corporate Role", "tag": "HIGH CEILING LONG GAME",
         "description": "Your combination of technical depth and leadership experience makes you a strong candidate for Director level roles in tech adjacent industries.",
         "income": "$130K to $160K (BLS 2024)", "time_to_entry": "3 to 6 months",
         "risk": "Low", "demand": "High"},
    ],
    "deprioritized_paths": [
        {"title": "Startup Cofounder (CTO/CPO)",
         "reason": "Your Burnout Risk score (58) and Income Urgency (76) make the 12 to 18 month runway of an unfunded startup a poor fit right now. Startup cofounding requires financial cushion you are not positioned to absorb today.",
         "revisit": "After 12 months of stable fractional income and reduced burnout risk. Ideal if you identify a cofounder with complementary skills and seed funding."},
        {"title": "Full Time Corporate VP Role",
         "reason": "Your Portfolio Fit score (93) is the highest in your profile, which means you are wired for multiple income streams, not a single employer. A full time VP role would underutilize your strongest dimension.",
         "revisit": "If a specific company offers equity, mission alignment, and a mandate that excites you enough to go all in. Otherwise, fractional gives you more leverage."},
        {"title": "Career Coach / Solopreneur",
         "reason": "While your Leadership Track (80) supports coaching, your Visibility score (70) needs to be higher before a coaching practice generates consistent inbound leads. Coaching without visibility means cold outreach, which has low conversion for new coaches.",
         "revisit": "After 6 months of consistent LinkedIn thought leadership and 2 to 3 speaking engagements. Build the audience first, then monetize the expertise."},
    ],
    "roadmap": {
        "short_term": [
            {"action": "Launch fractional consulting practice with 2 anchor clients", "timeline": "0 to 6 months", "impact": "High"},
            {"action": "Build LinkedIn content engine (2 posts/week minimum)", "timeline": "0 to 6 months", "impact": "High"},
            {"action": "Complete AI project management certification", "timeline": "0 to 6 months", "impact": "High"},
        ],
        "mid_term": [
            {"action": "Develop signature consulting framework and document methodology", "timeline": "6 to 18 months", "impact": "High"},
            {"action": "Launch group coaching program for 10 to 15 participants", "timeline": "6 to 18 months", "impact": "High"},
            {"action": "Hire first virtual assistant to handle admin and scheduling", "timeline": "6 to 18 months", "impact": "High"},
        ],
        "long_term": [
            {"action": "Write and publish a business book or comprehensive guide", "timeline": "18 to 36 months", "impact": "High"},
            {"action": "Secure 3 to 5 advisory board seats with equity compensation", "timeline": "18 to 36 months", "impact": "High"},
            {"action": "Launch premium mastermind or certification program", "timeline": "18 to 36 months", "impact": "High"},
        ]
    },
    "positioning": {
        "resume_angle": "Position yourself as a Senior Program Leader who transforms organizational chaos into scalable systems, highlighting your success delivering $50M+ initiatives and your 12 year track record.",
        "linkedin_headline": "Fractional Program Leader and Transformation Consultant | Helping Mid Market Companies Scale Operations Without the Full Time Cost | 12 Years Fortune 500",
        "authority_narrative": "As a Strategic Builder, Sarah consistently demonstrates the ability to lead complex systems and drive organizational change. Her tenure managing $50M+ initiatives across healthcare and technology showcases her mastery of both execution and strategic portfolio management.",
        "consulting_pitch": "As a Strategic Builder and Fractional Program Leader, I partner with mid market companies to drive their highest priority initiatives from strategy to execution. My 12 years of Fortune 500 program leadership ensures your critical projects are strategically aligned and flawlessly delivered. My clients typically see 40% faster time to value on major programs."
    },
    "skill_gaps": [
        {"title": "Public Visibility and Thought Leadership", "priority": "HIGH",
         "description": "Develop a consistent content strategy (LinkedIn articles, short form video) to share insights from your operations and transformation expertise. Focus on case studies demonstrating impact. Seek out speaking opportunities at industry conferences."},
        {"title": "Strategic Networking for Advisory and Board Roles", "priority": "MEDIUM",
         "description": "Actively seek out and engage with founders, VCs, and private equity firms who invest in healthcare technology companies. Attend industry events and join professional organizations."},
        {"title": "Advanced Financial Modeling for Consulting Engagements", "priority": "MEDIUM",
         "description": "Refine your skills in projecting ROI for transformation initiatives, structuring complex retainer agreements, and demonstrating the financial impact of your program leadership."},
    ],
    "action_plan": [
        {"day_num": 1, "title": "Archetype and Positioning Clarity", "tasks": [
            "Review your Strategic Builder archetype. Internalize how it aligns with your 12 years of experience.",
            "Update your LinkedIn headline to the recommended positioning.",
            "Draft a 2 to 3 sentence personal narrative for introductions and networking."]},
        {"day_num": 2, "title": "Fast Income Activation", "tasks": [
            "Identify 5 to 10 contacts who might need immediate program leadership support.",
            "Craft personalized outreach messages outlining your fractional offering.",
            "Review existing relationships for referral opportunities."]},
        {"day_num": 3, "title": "Portfolio and Case Study Development", "tasks": [
            "Document 3 to 5 key achievements with quantifiable impact.",
            "Translate these into concise case studies highlighting your approach.",
            "Begin compiling a services menu with packages and pricing."]},
        {"day_num": 4, "title": "LinkedIn Profile Optimization", "tasks": [
            "Update your About section to reflect your Strategic Builder identity.",
            "Publish your first LinkedIn post sharing program leadership insights.",
            "Engage with 5 to 10 relevant posts from industry leaders."]},
        {"day_num": 5, "title": "Targeted Outreach for Stable Income", "tasks": [
            "Research 3 to 5 mid market companies that need a Fractional Program Leader.",
            "Tailor your consulting pitch to each target company.",
            "Schedule 1 to 2 informational interviews or discovery calls."]},
        {"day_num": 6, "title": "Skill Gap Addressing", "tasks": [
            "Allocate 1 to 2 hours to research courses for your priority skill gap.",
            "Identify 1 to 2 industry events where you could present in the next 3 to 6 months.",
            "Begin outlining a thought leadership piece to enhance your positioning."]},
        {"day_num": 7, "title": "Strategic Planning and Self Care", "tasks": [
            "Review your progress and refine your 30/60/90 day plan.",
            "Schedule dedicated time for wellbeing and sustainable pace.",
            "Connect with a mentor or peer for accountability."]},
    ],
    "market": {
        "salary_range": "$150K to $250K",
        "demand_trend": "Growing (12% YoY)",
        "competitive_position": "Above Average (top 30%)",
        "top_skills": ["AI Augmented Project Management", "Consulting Business Development",
                       "Executive Presence and Speaking", "Change Management"]
    },
    "peer_comparison": [
        {"dimension": "Pivot Readiness", "user_score": 63, "median": 68, "assessment": "Below median \u2014 focus here"},
        {"dimension": "Consulting Fit", "user_score": 79, "median": 62, "assessment": "Above median"},
        {"dimension": "Leadership Track", "user_score": 80, "median": 71, "assessment": "Above median"},
        {"dimension": "AI Readiness", "user_score": 70, "median": 55, "assessment": "Above median"},
        {"dimension": "Portfolio Fit", "user_score": 93, "median": 67, "assessment": "Well above median"},
    ],
    "resources": [
        {"category": "BOOKS AND FRAMEWORKS (matched to your skill gaps)",
         "items": [
            {"name": "Thinking, Fast and Slow by Daniel Kahneman", "why": "Career transitions are full of cognitive traps \u2014 anchoring, loss aversion, sunk cost. Kahneman's framework helps you make better decisions under uncertainty and pressure.", "cost": "$16"},
            {"name": "The Almanack of Naval Ravikant by Eric Jorgenson", "why": "Naval's framework on specific knowledge and leverage is the blueprint for transitioning from employee to portfolio career. Required reading for anyone building fractional or consulting income.", "cost": "Free at navalmanack.com"},
            {"name": "The Psychology of Money by Morgan Housel", "why": "Career transitions are financial decisions disguised as identity decisions. Housel will help you separate the two and make clearer choices about income, risk, and runway.", "cost": "$15"},
         ]},
        {"category": "COURSES AND CERTIFICATIONS (matched to your career path)",
         "items": [
            {"name": "PMI AI in Project Management", "why": "Your AI Readiness is 70. This certification closes the gap and adds a credential to your LinkedIn.", "cost": "$299"},
            {"name": "Reforge Growth Series", "why": "Builds the strategic framework vocabulary that consulting clients expect from senior advisors.", "cost": "$1,995 / year"},
            {"name": "Toastmasters (local chapter)", "why": "Your Presence score (60) is your biggest leverage point. Weekly practice builds executive gravitas faster than any course.", "cost": "$50 / 6 months"},
         ]},
        {"category": "TOOLS AND TEMPLATES (use this week)",
         "items": [
            {"name": "Notion AI (free tier)", "why": "Build your consulting framework, track outreach, and organize case studies in one tool.", "cost": "Free"},
            {"name": "Calendly (free tier)", "why": "Professional scheduling for discovery calls. Removes friction from every \"let's chat\" conversation.", "cost": "Free"},
            {"name": "Loom (free tier)", "why": "Record 5 minute video pitches to send with cold outreach. Video outreach gets 3x response rates.", "cost": "Free"},
         ]},
    ],
    "ai_prompts": [
        {"title": "Resume Rewriter for Your Target Role",
         "text": "I am a [your current title] with [X] years of experience in [industry]. I am transitioning to [target role]. Here is my current resume: [paste resume]. Rewrite my experience bullets to emphasize outcomes and metrics relevant to [target role]. Use strong action verbs. Remove any language that sounds like a job description rather than an achievement.",
         "when_to_use": "Use on Day 1 before updating LinkedIn. Run it once per target role."},
        {"title": "LinkedIn Post Generator (Thought Leadership)",
         "text": "I am a [archetype] with expertise in [top 3 skills]. Write a LinkedIn post (150 to 200 words) sharing a contrarian insight about [industry topic]. Make it personal, use a specific example from corporate experience, and end with a question that invites comments. No hashtags. No emojis. Write like a human, not a marketer.",
         "when_to_use": "Use on Day 4 and twice weekly after that. Change the topic each time."},
        {"title": "Interview Prep (Behavioral Questions)",
         "text": "I am interviewing for [target role] at [company type]. My top 3 achievements are: [list them]. Generate 10 likely behavioral interview questions for this role. For each question, draft a STAR format answer using my specific achievements. Flag any questions where my experience might be thin and suggest how to bridge the gap.",
         "when_to_use": "Use 48 hours before any interview. Customize for each company."},
        {"title": "Networking Outreach Message",
         "text": "I am reaching out to [name], who is [their role] at [company]. I am a [your positioning statement]. Write a LinkedIn message (under 100 words) that references something specific about their work, explains why I am reaching out, and asks for a 15 minute conversation. Do not sound desperate. Do not flatter. Be direct and professional.",
         "when_to_use": "Use on Day 2 and Day 5. Personalize for each contact."},
        {"title": "Salary and Rate Research",
         "text": "I am a [title] with [X] years of experience in [industry], transitioning to [target role]. Research current market rates for this role in [location/remote]. Include: full time salary ranges from at least 3 sources, fractional/consulting hourly rates, retainer structures, and what factors command premium pricing. Cite your sources.",
         "when_to_use": "Use before any rate negotiation or proposal. Update quarterly."},
    ]
}

if __name__ == '__main__':
    out = '/mnt/user-data/outputs/PB-CareerOS-Pro-Report-V2.pdf'
    build_report(SAMPLE_DATA, out)
    print(f"Generated: {out}")
