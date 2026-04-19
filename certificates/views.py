import os
from io import BytesIO
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from .models import Certificate, CustomCertificate
from payments.models import Enrollment


# ── palette ────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor('#0F2557')
BLUE   = colors.HexColor('#1E3A8A')
ACCENT = colors.HexColor('#3B82F6')
GOLD   = colors.HexColor('#C9A84C')
GOLD2  = colors.HexColor('#F0D080')
LIGHT  = colors.HexColor('#EFF6FF')
GRAY   = colors.HexColor('#6B7280')
DARK   = colors.HexColor('#1E293B')
WHITE  = colors.white

PAGE_W, PAGE_H = landscape(A4)   # 841.89 x 595.28 pt


def _logo_path():
    for name in ['vignan_logo_final.png', 'Vignan_Techsolutions_Logo_4K.png', 'logo.png']:
        p = os.path.join(settings.BASE_DIR, 'static', 'images', name)
        if os.path.exists(p):
            return p
    return None


def _msme_path():
    p = os.path.join(settings.BASE_DIR, 'static', 'images', 'msme-certificate.png')
    return p if os.path.exists(p) else None


def _draw_corporate_background(c, doc):
    """Draw the full corporate background on every page."""
    w, h = PAGE_W, PAGE_H

    # Deep navy base
    c.setFillColor(colors.HexColor('#0A1628'))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Subtle diagonal gradient bands
    for i, alpha in enumerate([0.04, 0.03, 0.025, 0.02]):
        c.setFillColorRGB(0.12, 0.23, 0.55, alpha=alpha)
        c.rect(0, h * (0.25 * i), w, h * 0.3, fill=1, stroke=0)

    # Gold outer border — thick
    c.setStrokeColor(GOLD)
    c.setLineWidth(3.5)
    c.rect(18, 18, w - 36, h - 36, fill=0, stroke=1)

    # Gold inner border — thin
    c.setStrokeColor(GOLD2)
    c.setLineWidth(0.8)
    c.rect(26, 26, w - 52, h - 52, fill=0, stroke=1)

    # Navy inner fill panel
    c.setFillColor(colors.HexColor('#0D1E3D'))
    c.rect(27, 27, w - 54, h - 54, fill=1, stroke=0)

    # Top accent bar
    c.setFillColor(BLUE)
    c.rect(27, h - 100, w - 54, 73, fill=1, stroke=0)

    # Gold line under top bar
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(27, h - 100, w - 27, h - 100)

    # Bottom accent bar
    c.setFillColor(BLUE)
    c.rect(27, 27, w - 54, 58, fill=1, stroke=0)

    # Gold line above bottom bar
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(27, 85, w - 27, 85)

    # Decorative corner diamonds — top-left
    for offset in [30, 38]:
        c.setFillColor(GOLD)
        c.saveState()
        c.translate(offset + 10, h - offset - 10)
        c.rotate(45)
        size = 5 if offset == 30 else 3
        c.rect(-size/2, -size/2, size, size, fill=1, stroke=0)
        c.restoreState()

    # Decorative corner diamonds — top-right
    for offset in [30, 38]:
        c.setFillColor(GOLD)
        c.saveState()
        c.translate(w - offset - 10, h - offset - 10)
        c.rotate(45)
        size = 5 if offset == 30 else 3
        c.rect(-size/2, -size/2, size, size, fill=1, stroke=0)
        c.restoreState()

    # Decorative corner diamonds — bottom-left
    for offset in [30, 38]:
        c.setFillColor(GOLD)
        c.saveState()
        c.translate(offset + 10, offset + 10)
        c.rotate(45)
        size = 5 if offset == 30 else 3
        c.rect(-size/2, -size/2, size, size, fill=1, stroke=0)
        c.restoreState()

    # Decorative corner diamonds — bottom-right
    for offset in [30, 38]:
        c.setFillColor(GOLD)
        c.saveState()
        c.translate(w - offset - 10, offset + 10)
        c.rotate(45)
        size = 5 if offset == 30 else 3
        c.rect(-size/2, -size/2, size, size, fill=1, stroke=0)
        c.restoreState()

    # Watermark text
    c.saveState()
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.setFillAlpha(0.07)
    c.setFont('Helvetica-Bold', 72)
    c.translate(w / 2, h / 2)
    c.rotate(30)
    c.drawCentredString(0, 0, 'VIGNAN TECHSOLUTIONS')
    c.restoreState()


def _draw_seal(c, cx, cy, r, logo_path):
    """Draw the circular Vignan TechSolutions seal."""
    import math
    # Outer filled circle
    c.setFillColor(colors.HexColor('#EEF3FA'))
    c.setStrokeColor(colors.HexColor('#1A3A6B'))
    c.setLineWidth(2.8)
    c.circle(cx, cy, r, fill=1, stroke=1)
    # Middle ring
    c.setStrokeColor(colors.HexColor('#2E5FA3'))
    c.setLineWidth(1.2)
    c.circle(cx, cy, r - 8, fill=0, stroke=1)
    # Inner ring
    c.setStrokeColor(colors.HexColor('#2E5FA3'))
    c.setLineWidth(0.6)
    c.circle(cx, cy, r - 11, fill=0, stroke=1)
    # Logo in center
    if logo_path:
        try:
            lw, lh = 38, 19
            c.drawImage(logo_path, cx - lw/2, cy - 4,
                        width=lw, height=lh,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    # Arc text TOP: "VIGNAN · TECHSOLUTIONS"
    top_text = 'VIGNAN  *  TECHSOLUTIONS'
    arc_r = r - 5
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica-Bold', 5.2)
    n = len(top_text)
    total_angle = 150  # degrees spanning top arc
    start_angle = 90 + total_angle / 2
    step = total_angle / max(n - 1, 1)
    for i, ch in enumerate(top_text):
        angle_deg = start_angle - i * step
        angle_rad = math.radians(angle_deg)
        tx = cx + arc_r * math.cos(angle_rad)
        ty = cy + arc_r * math.sin(angle_rad)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(angle_deg - 90)
        c.drawCentredString(0, 0, ch)
        c.restoreState()
    # Arc text BOTTOM: "KALABURAGI"
    bot_text = 'KALABURAGI'
    total_angle_b = 100
    start_angle_b = -90 + total_angle_b / 2
    step_b = total_angle_b / max(len(bot_text) - 1, 1)
    for i, ch in enumerate(bot_text):
        angle_deg = start_angle_b - i * step_b
        angle_rad = math.radians(angle_deg)
        tx = cx + arc_r * math.cos(angle_rad)
        ty = cy + arc_r * math.sin(angle_rad)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(angle_deg + 90)
        c.drawCentredString(0, 0, ch)
        c.restoreState()
    # Stars at left & right of seal
    c.setFont('Helvetica-Bold', 6)
    c.drawCentredString(cx - arc_r + 3, cy - 2, '★')
    c.drawCentredString(cx + arc_r - 3, cy - 2, '★')


def _draw_signature(c, x, y, w_sig):
    """Draw a handwriting-style signature using bezier curves."""
    c.saveState()
    c.setStrokeColor(colors.HexColor('#1A1A1A'))
    c.setLineWidth(0.9)
    c.setLineCap(1)
    # S-curve stroke 1
    p = c.beginPath()
    p.moveTo(x, y)
    p.curveTo(x+8, y+10, x+18, y+14, x+28, y+8)
    p.curveTo(x+36, y+3, x+42, y+12, x+50, y+10)
    c.drawPath(p, stroke=1, fill=0)
    # S-curve stroke 2
    p2 = c.beginPath()
    p2.moveTo(x+10, y-4)
    p2.curveTo(x+20, y+6, x+34, y+2, x+44, y-2)
    p2.curveTo(x+52, y-5, x+60, y+4, x+70, y+2)
    c.drawPath(p2, stroke=1, fill=0)
    # Underline flourish
    p3 = c.beginPath()
    p3.moveTo(x, y-8)
    p3.curveTo(x+20, y-6, x+50, y-10, x+w_sig, y-7)
    c.drawPath(p3, stroke=1, fill=0)
    c.restoreState()


def generate_custom_certificate_pdf(cert: CustomCertificate) -> BytesIO:
    buffer = BytesIO()
    c = pdfcanvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = PAGE_W, PAGE_H   # 841.89 x 595.28 pt

    # ── 1. BACKGROUND ─────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#F0F4FA'))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # ── 2. BORDERS ────────────────────────────────────────────────────────
    # Outermost thick navy
    c.setStrokeColor(colors.HexColor('#1A3A6B'))
    c.setLineWidth(7)
    c.rect(10, 10, w - 20, h - 20, fill=0, stroke=1)
    # Second navy line
    c.setLineWidth(1.8)
    c.rect(18, 18, w - 36, h - 36, fill=0, stroke=1)
    # Inner thin blue
    c.setStrokeColor(colors.HexColor('#3A6DB5'))
    c.setLineWidth(0.8)
    c.rect(23, 23, w - 46, h - 46, fill=0, stroke=1)

    # ── 3. LOGO centered top ──────────────────────────────────────────────
    logo_path = _logo_path()
    LOGO_W, LOGO_H = 210, 68
    logo_x = w / 2 - LOGO_W / 2
    logo_y = h - 32 - LOGO_H
    if logo_path:
        try:
            c.drawImage(logo_path, logo_x, logo_y,
                        width=LOGO_W, height=LOGO_H,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            # fallback text
            c.setFillColor(colors.HexColor('#1A3A6B'))
            c.setFont('Helvetica-Bold', 26)
            c.drawCentredString(w/2, logo_y + 24, 'ViGNAN TECHSOLUTIONS')

    # ── 4. SUBTITLE ───────────────────────────────────────────────────────
    sub_y = logo_y - 13
    c.setFillColor(colors.HexColor('#3A3A3A'))
    c.setFont('Helvetica', 10)
    c.drawCentredString(w/2, sub_y,
        '(Software Development  |  AI & ML  |  Web  Technologies)')
    c.setFont('Helvetica', 9.5)
    c.setFillColor(colors.HexColor('#444444'))
    c.drawCentredString(w/2, sub_y - 14, 'Kalaburagi')

    # ── 5. THIN RULE ──────────────────────────────────────────────────────
    rule_y = sub_y - 26
    c.setStrokeColor(colors.HexColor('#9AAFC8'))
    c.setLineWidth(0.7)
    c.line(36, rule_y, w - 36, rule_y)

    # ── 6. "CERTIFICATE" with flanking lines ──────────────────────────────
    cert_y = rule_y - 19
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(w/2, cert_y, 'CERTIFICATE')
    # flanking lines
    c.setStrokeColor(colors.HexColor('#1A3A6B'))
    c.setLineWidth(1.4)
    flank_gap = 58
    c.line(36, cert_y + 7,  w/2 - flank_gap, cert_y + 7)
    c.line(w/2 + flank_gap, cert_y + 7, w - 36, cert_y + 7)

    # ── 7. BLUE GRADIENT BANNER ───────────────────────────────────────────
    ban_h  = 36
    ban_y  = cert_y - 13 - ban_h
    ban_x  = 23
    ban_w  = w - 46
    # left half darker, right half lighter — simulates gradient
    steps  = 60
    for i in range(steps):
        t  = i / steps
        r_ = int(26  + t * (58  - 26))   # #1A → #3A
        g_ = int(58  + t * (109 - 58))
        b_ = int(107 + t * (180 - 107))
        c.setFillColorRGB(r_/255, g_/255, b_/255)
        c.rect(ban_x + i * ban_w/steps, ban_y,
               ban_w/steps + 0.5, ban_h, fill=1, stroke=0)
    # Banner label
    type_map = {
        'completion':    'PROJECT COMPLETION',
        'internship':    'INTERNSHIP',
        'participation': 'PARTICIPATION',
        'excellence':    'EXCELLENCE',
        'appreciation':  'APPRECIATION',
        'training':      'TRAINING',
    }
    banner_text = type_map.get(cert.cert_type, cert.cert_type.upper())
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(w/2, ban_y + 10, banner_text)

    # ── 8. BODY TEXT ──────────────────────────────────────────────────────
    y = ban_y - 20

    # "This is to certify that"
    c.setFillColor(colors.HexColor('#2A2A2A'))
    c.setFont('Helvetica', 11)
    c.drawCentredString(w/2, y, 'This is to certify that')
    y -= 22

    # [STUDENT NAME] — large bold navy
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica-Bold', 24)
    c.drawCentredString(w/2, y, cert.recipient_name)
    y -= 18

    # "has successfully completed the project titled"
    action_map = {
        'completion':    'has successfully completed the project titled',
        'internship':    'has successfully completed the internship program titled',
        'participation': 'has actively participated in',
        'excellence':    'has demonstrated excellence in',
        'appreciation':  'is hereby appreciated for outstanding contribution in',
        'training':      'has successfully completed the training program titled',
    }
    c.setFillColor(colors.HexColor('#2A2A2A'))
    c.setFont('Helvetica', 10.5)
    c.drawCentredString(w/2, y, action_map.get(cert.cert_type,
                                               'has successfully completed'))
    y -= 18

    # “PROJECT TITLE” with flanking lines
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica-Bold', 13.5)
    title_str = f'\u201c{cert.program_name}\u201d'
    c.drawCentredString(w/2, y, title_str)
    title_hw = min(c.stringWidth(title_str, 'Helvetica-Bold', 13.5) / 2 + 14, 230)
    c.setStrokeColor(colors.HexColor('#9AAFC8'))
    c.setLineWidth(0.8)
    c.line(36,      y + 5, w/2 - title_hw, y + 5)
    c.line(w/2 + title_hw, y + 5, w - 36, y + 5)
    y -= 16

    # "at Vignan Tech Solutions, Kalaburagi, during the period"
    # mixed bold/normal inline
    c.setFont('Helvetica', 10.5)
    c.setFillColor(colors.HexColor('#2A2A2A'))
    pre   = 'at '
    bold  = 'Vignan Tech Solutions'
    post  = ', Kalaburagi, during the period'
    pre_w  = c.stringWidth(pre,  'Helvetica',      10.5)
    bold_w = c.stringWidth(bold, 'Helvetica-Bold', 10.5)
    post_w = c.stringWidth(post, 'Helvetica',      10.5)
    total_w = pre_w + bold_w + post_w
    sx = w/2 - total_w/2
    c.drawString(sx,           y, pre)
    c.setFont('Helvetica-Bold', 10.5)
    c.drawString(sx + pre_w,   y, bold)
    c.setFont('Helvetica', 10.5)
    c.drawString(sx + pre_w + bold_w, y, post)
    y -= 16

    # [ START DATE ]  to  [ END DATE ]
    if cert.start_date and cert.end_date:
        date_str = (f'[ {cert.start_date.strftime("%d %B %Y")} ]'
                    f'   to   '
                    f'[ {cert.end_date.strftime("%d %B %Y")} ]')
    elif cert.start_date:
        date_str = f'[ {cert.start_date.strftime("%d %B %Y")} ]'
    else:
        date_str = f'[ {cert.issued_date.strftime("%d %B %Y")} ]'
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica-Bold', 11.5)
    c.drawCentredString(w/2, y, date_str)
    y -= 16

    # Description lines — mixed bold inline
    domain_text = cert.project_domain or \
        'Artificial Intelligence / Machine Learning / Data Science / Web Development / Python'

    # Line 1: "During this tenure, the candidate demonstrated strong **technical proficiency, commitment,** and"
    c.setFont('Helvetica', 9.8)
    c.setFillColor(colors.HexColor('#2A2A2A'))
    seg1a = 'During this tenure, the candidate demonstrated strong '
    seg1b = 'technical proficiency, commitment,'
    seg1c = ' and'
    w1a = c.stringWidth(seg1a, 'Helvetica',      9.8)
    w1b = c.stringWidth(seg1b, 'Helvetica-Bold', 9.8)
    w1c = c.stringWidth(seg1c, 'Helvetica',      9.8)
    tot1 = w1a + w1b + w1c
    sx1  = w/2 - tot1/2
    c.drawString(sx1,            y, seg1a)
    c.setFont('Helvetica-Bold', 9.8)
    c.drawString(sx1 + w1a,      y, seg1b)
    c.setFont('Helvetica', 9.8)
    c.drawString(sx1 + w1a+w1b,  y, seg1c)
    y -= 13

    # Line 2: "problem-solving skills while working in the domain of:"
    c.drawCentredString(w/2, y,
        'problem-solving skills while working in the domain of:')
    y -= 13

    # Line 3: domain
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica', 9.2)
    c.drawCentredString(w/2, y, f'[ {domain_text} ]')
    y -= 4   # small gap before bottom section

    # ── 9. BOTTOM SECTION ─────────────────────────────────────────────────
    # We place everything relative to a fixed bottom baseline
    BASE_Y   = 95   # top of bottom block
    SEAL_CX  = 76
    SEAL_CY  = 58
    SEAL_R   = 44

    # Seal
    _draw_seal(c, SEAL_CX, SEAL_CY, SEAL_R, logo_path)

    # Closing paragraph — left-aligned starting after seal
    txt_x  = SEAL_CX + SEAL_R + 14
    txt_y  = BASE_Y
    c.setFillColor(colors.HexColor('#2A2A2A'))
    c.setFont('Helvetica', 9)
    close_lines = [
        'The project has been successfully completed as per organizational standards.',
        "We appreciate the candidate\u2019s sincere efforts and wish them success in their future",
        'academic and professional endeavors.',
    ]
    for line in close_lines:
        c.drawString(txt_x, txt_y, line)
        txt_y -= 12

    # Cert ID & Date of Issue
    footer_y = txt_y - 6
    c.setFont('Helvetica', 9)
    c.setFillColor(colors.HexColor('#2A2A2A'))
    c.drawString(txt_x, footer_y,
        f'Certificate ID:  {cert.cert_number}')
    c.drawString(txt_x + 280, footer_y,
        f'Date of Issue:  {cert.issued_date.strftime("%d/%m/%Y")}')

    # ── 10. SIGNATORY (right side) ────────────────────────────────────────
    SIG_CX   = w - 110   # center-x of signature block
    SIG_W    = 130
    sig_top  = BASE_Y + 14

    # Handwriting signature
    _draw_signature(c, SIG_CX - SIG_W/2 + 10, sig_top - 10, SIG_W - 20)

    # Signature line
    c.setStrokeColor(colors.HexColor('#2A2A2A'))
    c.setLineWidth(0.8)
    c.line(SIG_CX - SIG_W/2, sig_top - 18, SIG_CX + SIG_W/2, sig_top - 18)

    # Name bold
    c.setFillColor(colors.HexColor('#1A3A6B'))
    c.setFont('Helvetica-Bold', 10.5)
    c.drawCentredString(SIG_CX, sig_top - 30, cert.signatory_name)

    # Title & Org
    c.setFillColor(colors.HexColor('#333333'))
    c.setFont('Helvetica', 9)
    c.drawCentredString(SIG_CX, sig_top - 42, cert.signatory_title)
    c.drawCentredString(SIG_CX, sig_top - 53, cert.signatory_org)

    # Extra note (very bottom center)
    if cert.extra_note:
        c.setFillColor(colors.HexColor('#666666'))
        c.setFont('Helvetica-Oblique', 8)
        c.drawCentredString(w/2, 14, cert.extra_note)

    c.save()
    buffer.seek(0)
    return buffer


def generate_certificate_pdf(certificate):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=36, textColor=colors.HexColor('#1E3A8A'),
                                  alignment=TA_CENTER, spaceAfter=10)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, textColor=colors.HexColor('#3B82F6'),
                                     alignment=TA_CENTER, spaceAfter=6)
    name_style = ParagraphStyle('Name', parent=styles['Normal'], fontSize=28, textColor=colors.HexColor('#1E3A8A'),
                                 alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=10)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=13, textColor=colors.HexColor('#374151'),
                                 alignment=TA_CENTER, spaceAfter=6)
    cert_id_style = ParagraphStyle('CertID', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#6B7280'),
                                    alignment=TA_CENTER)

    enrollment = certificate.enrollment
    item_name = enrollment.course.title if enrollment.course else enrollment.internship.title
    item_type = 'Course' if enrollment.course else 'Internship'
    student_name = certificate.student.get_full_name()
    cert_id = f"CERT-{str(certificate.certificate_id)[:8].upper()}"
    issued_date = certificate.issued_date.strftime('%B %d, %Y')

    story = [
        Spacer(1, 0.3*inch),
        Paragraph("VIGNAN TECHSOLUTIONS", title_style),
        Paragraph("MSME Registered Technology Company", subtitle_style),
        Spacer(1, 0.2*inch),
        Paragraph("CERTIFICATE OF COMPLETION", ParagraphStyle('CertTitle', parent=styles['Normal'],
                   fontSize=20, textColor=colors.HexColor('#374151'), alignment=TA_CENTER,
                   fontName='Helvetica-Bold', spaceAfter=10)),
        Paragraph("This is to certify that", body_style),
        Spacer(1, 0.1*inch),
        Paragraph(student_name, name_style),
        Spacer(1, 0.1*inch),
        Paragraph(f"has successfully completed the {item_type}", body_style),
        Paragraph(f"<b>{item_name}</b>", ParagraphStyle('ItemName', parent=styles['Normal'],
                   fontSize=18, textColor=colors.HexColor('#1E3A8A'), alignment=TA_CENTER,
                   fontName='Helvetica-Bold', spaceAfter=10)),
        Spacer(1, 0.2*inch),
        Paragraph(f"Date of Issue: {issued_date}", body_style),
        Spacer(1, 0.3*inch),
        Paragraph(f"Certificate ID: {cert_id}", cert_id_style),
        Paragraph("Verify at: vignantechsolutions.com/certificates/verify/", cert_id_style),
    ]

    doc.build(story)
    buffer.seek(0)
    return buffer


@login_required
def download_certificate(request, cert_id):
    certificate = get_object_or_404(Certificate, certificate_id=cert_id, student=request.user, is_valid=True)
    buffer = generate_certificate_pdf(certificate)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate-{str(cert_id)[:8]}.pdf"'
    return response


def verify_certificate(request, cert_id=None):
    certificate = None
    if request.method == 'POST':
        cert_id = request.POST.get('cert_id', '').strip()
    if cert_id:
        try:
            certificate = Certificate.objects.select_related('student', 'enrollment__course', 'enrollment__internship').get(
                certificate_id=cert_id, is_valid=True
            )
        except Certificate.DoesNotExist:
            certificate = 'invalid'
    return render(request, 'certificates/verify.html', {'certificate': certificate, 'cert_id': cert_id})


def download_custom_certificate(request, pk):
    """Admin-only: download a custom certificate PDF."""
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    cert = get_object_or_404(CustomCertificate, pk=pk)
    buffer = generate_custom_certificate_pdf(cert)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cert.cert_number}.pdf"'
    return response
