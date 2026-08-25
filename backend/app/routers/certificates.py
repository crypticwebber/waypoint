import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/me", response_model=list[schemas.CertificateOut], summary="List my certificates")
def my_certificates(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    certs = db.query(models.Certificate).filter(models.Certificate.user_id == current_user.id).all()
    return [
        schemas.CertificateOut(
            id=c.id, course_id=c.course_id, course_title=c.course.title,
            issued_at=c.issued_at, certificate_code=c.certificate_code,
        ) for c in certs
    ]


def _draw_certificate_pdf(learner_name: str, course_title: str, issued_at, code: str) -> bytes:
    buffer = io.BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    ink = HexColor("#12181B")
    paper = HexColor("#F6F4EE")
    amber = HexColor("#E8A33D")
    teal = HexColor("#2E7D6B")

    c.setFillColor(paper)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    margin = 14 * mm
    c.setStrokeColor(ink)
    c.setLineWidth(1.4)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=0, stroke=1)
    c.setStrokeColor(amber)
    c.setLineWidth(0.6)
    c.rect(margin + 4, margin + 4, width - 2 * margin - 8, height - 2 * margin - 8, fill=0, stroke=1)

    # signature "route line": a dotted waypoint path across the top, echoing
    # the product's visual signature on the certificate itself.
    y_line = height - margin - 22 * mm
    c.setDash(1, 6)
    c.setStrokeColor(teal)
    c.setLineWidth(1.5)
    c.line(margin + 20 * mm, y_line, width - margin - 20 * mm, y_line)
    c.setDash()
    for i, x_frac in enumerate([0.0, 0.33, 0.66, 1.0]):
        x = margin + 20 * mm + x_frac * (width - 2 * margin - 40 * mm)
        c.setFillColor(amber if i % 2 == 0 else teal)
        c.circle(x, y_line, 2.6 * mm, fill=1, stroke=0)

    c.setFillColor(ink)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - margin - 12 * mm, "WAYPOINT")
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - margin - 42 * mm, "Certificate of Completion")

    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2, height / 2 + 14 * mm, "This certifies that")

    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(teal)
    c.drawCentredString(width / 2, height / 2, learner_name)

    c.setFillColor(ink)
    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2, height / 2 - 14 * mm, "has successfully completed")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height / 2 - 28 * mm, course_title)

    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, margin + 18 * mm, f"Issued {issued_at.strftime('%d %B %Y')}")
    c.drawCentredString(width / 2, margin + 12 * mm, f"Certificate code: {code}")

    c.showPage()
    c.save()
    return buffer.getvalue()


@router.get(
    "/{certificate_id}/pdf",
    summary="Download a certificate as a styled PDF",
    response_class=StreamingResponse,
)
def download_certificate_pdf(certificate_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cert = db.query(models.Certificate).filter(models.Certificate.id == certificate_id).first()
    if not cert or cert.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Certificate not found")

    pdf_bytes = _draw_certificate_pdf(current_user.full_name, cert.course.title, cert.issued_at, cert.certificate_code)
    filename = f"waypoint-certificate-{cert.certificate_code}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
