from urllib.parse import urlencode

from django.http import HttpResponse

from playwright.sync_api import sync_playwright

from api.utils.urls import get_base_url

base_url = f"{get_base_url()}lettre-officielle/"
params = {
    "letterName": "AccuseEnregistrement",
    "title": "accusé d’enregistrement de déclaration d’un complément alimentaire",
    "letterGenerationDate": "2024-06-24",
    "declarationDate": "2024-06-24",
    "caName": "L-Glutamine 2000",
    "caGalenicForm": "Gélule",
    "caCompany": "Musclor Sportive 2000",
    "caseNumber": "2024-5-1273",
    "transmissionEmail": "complement-alimentaire.dgal@agriculture.gouv.fr",
    "dgalDocumentUrl": "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
    "attestationUrl": "https://url-a-definir",  # TODO
    "moreLegalInfoUrl": "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}
url = f"{base_url}?{urlencode(params, doseq=True)}"

# TODO sécu: ajouter un token consommable pour empêcher n'importe qui de générer des courriers


def generate_pdf(request) -> HttpResponse:
    def run_playwright():
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            pdf_content = page.pdf(
                format="A4",
                margin={
                    "top": "2cm",
                    "bottom": "2cm",
                    "left": "2cm",
                    "right": "2cm",
                },
            )
            browser.close()
            return pdf_content

    pdf_content = run_playwright()

    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="lettre.pdf"'
    return response


# Données temporaires qu'on peut copier-coller pour tester les différentes lettres

params = {
    "letterName": "AccuseEnregistrement",
    "title": "accusé d’enregistrement de déclaration d’un complément alimentaire",
    "letterGenerationDate": "2024-06-24",
    "declarationDate": "2024-06-24",
    "caName": "L-Glutamine 2000",
    "caGalenicForm": "Gélule",
    "caCompany": "Nutrition Sportive Way",
    "caseNumber": "2024-5-1273",
    "transmissionEmail": "complement-alimentaire.dgal@agriculture.gouv.fr",
    "dgalDocumentUrl": "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
    "attestationUrl": "https://url-a-definir",  # TODO
    "moreLegalInfoUrl": "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}

params = {
    "letterName": "AttestationDeclarationArt15",
    "title": "attestation de déclaration d’un complément alimentaire",
    "letterGenerationDate": "2024-05-04",
    "name": "Johanna Galibert",
    "caName": "Ronce",
    "caGalenicForm": "Flacon",
    "caCompany": "Belar basa gemmothérapie",
    "declarationDate": "2024-05-04",
    "caseNumber": "2024-5-1273",
    "attestationUrl": "https://url-a-definir",  # TODO
    "moreLegalInfoUrl": "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}

params = {
    "letterName": "AttestationDeclarationArt16",
    "title": "attestation de déclaration d’un complément alimentaire",
    "letterGenerationDate": "2024-05-04",
    "name": "Johanna Galibert",
    "caName": "Ronce",
    "caGalenicForm": "Flacon",
    "caCompany": "Belar basa gemmothérapie",
    "declarationDate": "2024-05-04",
    "caseNumber": "2024-5-1273",
    "moreLegalInfoUrl": "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}

params = {
    "letterName": "Refus",
    "recipientName": "ARIIX EUROPE B.V",
    "recipientAddress": "President Kennedylaan 19\n2517 JK DEN HAAG",
    "letterGenerationDate": "2024-06-20",
    "caName": "RENEW",
    "caGalenicForm": "Poudre",
    "caCompany": "Kiwi Baies",
    "declarationDate": "2024-05-04",
    "caseNumber": "2024-5-1273",
    "telerecoursUrl": "https://citoyens.telerecours.fr/#/authentication",
}
