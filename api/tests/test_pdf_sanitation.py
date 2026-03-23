import io

from django.core.exceptions import ValidationError
from django.test import TestCase

import pikepdf

from api.serializers import sanitize_pdf


def make_malicious_pdf_bytes():
    """Génère un PDF minimal avec JavaScript embarqué."""
    pdf = pikepdf.Pdf.new()
    page = pikepdf.Dictionary(
        Type=pikepdf.Name("/Page"),
        MediaBox=[0, 0, 612, 792],
    )
    pdf.make_indirect(page)
    pdf.pages.append(pikepdf.Page(page))

    pdf.Root["/OpenAction"] = pikepdf.Dictionary(
        S=pikepdf.Name("/JavaScript"),
        JS=pikepdf.String("app.alert('XSS');"),
    )
    pdf.Root["/Names"] = pikepdf.Dictionary(
        JavaScript=pikepdf.Dictionary(
            Names=pikepdf.Array(
                [
                    pikepdf.String("alert"),
                    pikepdf.Dictionary(
                        S=pikepdf.Name("/JavaScript"),
                        JS=pikepdf.String("app.alert('XSS');"),
                    ),
                ]
            )
        )
    )

    buf = io.BytesIO()
    pdf.save(buf)
    return buf.getvalue()


class SanitizePDFTest(TestCase):
    def test_clean_pdf_passes_validation(self):
        clean_pdf = pikepdf.Pdf.new()
        page = pikepdf.Dictionary(
            Type=pikepdf.Name("/Page"),
            MediaBox=[0, 0, 612, 792],
        )
        clean_pdf.make_indirect(page)
        clean_pdf.pages.append(pikepdf.Page(page))
        buf = io.BytesIO()
        clean_pdf.save(buf)

        file = io.BytesIO(buf.getvalue())
        sanitized = sanitize_pdf(file)

        # Doit toujours être un PDF valide
        with pikepdf.open(io.BytesIO(sanitized)) as pdf:
            self.assertEqual(len(pdf.pages), 1)

    def test_removes_open_action(self):
        pdf_bytes = make_malicious_pdf_bytes()
        file = io.BytesIO(pdf_bytes)

        sanitized = sanitize_pdf(file)

        with pikepdf.open(io.BytesIO(sanitized)) as pdf:
            self.assertNotIn("/OpenAction", pdf.Root)

    def test_removes_javascript_from_names(self):
        pdf_bytes = make_malicious_pdf_bytes()
        file = io.BytesIO(pdf_bytes)

        sanitized = sanitize_pdf(file)

        with pikepdf.open(io.BytesIO(sanitized)) as pdf:
            names = pdf.Root.get("/Names")
            if names is not None:
                self.assertNotIn("/JavaScript", names)

    def test_invalid_pdf_raises_validation_error(self):
        file = io.BytesIO(b"not a pdf at all")
        with self.assertRaises(ValidationError):
            sanitize_pdf(file)
