"""Stage 6: automatic BLOCK / PASS decision and the reasoned message to the declarant.

Business constraint: nobody reviews the outputs. The pipeline therefore only blocks on a
BLOCKING finding that is proven (quote found in the label, or confirmed by the agent) and above
the confidence threshold, on a MAJOR finding of the policy confirmed with proof by the agent,
or on an accumulation of serious findings (noisy-OR risk score). Uncertain findings never block.

Thresholds and the policy live in config.Settings and were calibrated on the gold set
(eval/policy.py: highest recall under a precision constraint).
"""

from __future__ import annotations

from .config import Settings
from .schemas import Decision, Finding, Severity

# Weight of each severity in the noisy-OR risk score.
WEIGHTS = {Severity.BLOCKING: 0.9, Severity.MAJOR: 0.45, Severity.MINOR: 0.08, Severity.INFO: 0.02}
# French wording of the fraud types. Not used by the pipeline yet (meant for a summary line in the message).
FRAUD_FR = {
    "fake_label": "étiquette non conforme ou ne correspondant pas au produit",
    "undeclared_ingredients": "ingrédients non déclarés",
    "article_bypass": "composition relevant d'une autre procédure que l'article 15",
    "dose_underdeclared": "quantités sous-déclarées",
    "label_noncompliance": "mentions d'étiquetage non conformes",
}


def risk_score(findings: list[Finding], prior: float = 0.0) -> float:
    """Noisy-OR of the findings: 1 - prod(1 - weight x confidence), starting from the triage prior.

    It ranks declarations by risk and can block on its own above Settings.block_risk_score.
    """
    p = 1.0 - 0.1 * prior
    for f in findings:
        if f.verified == "refuted":
            continue
        # A finding the agent could not establish weighs little: we never block on what is uncertain
        w = WEIGHTS[f.severity] * (0.3 if f.verified == "uncertain" else 1.0)
        p *= 1.0 - w * f.confidence
    return round(1.0 - p, 4)


def is_blocking(f: Finding, settings: Settings) -> bool:
    """Can this single finding block the declaration on its own?"""
    if f.verified in ("refuted", "uncertain"):
        return False
    if f.severity == Severity.BLOCKING:
        return f.confidence >= settings.block_confidence and (f.grounded or f.verified == "confirmed")
    # A MAJOR finding blocks when it is established twice: the rule detected it AND the agent
    # confirmed it by going back to the label, with high confidence. Only the codes of the policy
    # (calibrated on the gold set) qualify.
    if f.severity == Severity.MAJOR and f.verified == "confirmed":
        return f.confidence >= settings.confirmed_major_confidence and f.code.startswith(
            settings.confirmed_major_codes
        )
    return False


def build_message(decl_name: str, blocking: list[Finding], others: list[Finding]) -> str:
    """Message to the declarant (in French), with the reasons and quotes from the label.

    It states that the check is automated: an automated individual administrative decision must
    say so (to be validated with the legal team).
    """
    lines = [
        f"Votre déclaration « {decl_name} » n'a pas pu être validée automatiquement : un contrôle de cohérence "
        "entre l'étiquetage fourni et la composition déclarée a relevé les points suivants.",
        "",
    ]
    for f in blocking + others:
        lines.append(f"- {f.title}. {f.detail}")
        for e in f.evidence[:2]:
            if e.quote:
                lines.append(f"  Extrait de l'étiquette (page {e.page + 1}) : « {e.quote[:200]} »")
    lines += [
        "",
        "Merci de corriger votre déclaration et/ou votre étiquetage, puis de la soumettre à nouveau.",
        "Ce contrôle est réalisé par un traitement automatisé ; vous pouvez demander les règles qu'il applique.",
    ]
    return "\n".join(lines)


def decide(findings: list[Finding], settings: Settings, decl_name: str, facts: dict, prior: float = 0.0) -> Decision:
    """Final decision. Pure function of the findings and the settings, so a new policy can be
    replayed on saved findings without any model call (`cli reeval --redecide`)."""
    risk = risk_score(findings, prior)
    blocking = [f for f in findings if is_blocking(f, settings)]
    block = bool(blocking) or risk >= settings.block_risk_score
    # Other serious findings, listed in the message after the blocking ones (most severe first).
    others = [
        f
        for f in findings
        if f not in blocking
        and f.verified != "refuted"
        and f.severity in (Severity.BLOCKING, Severity.MAJOR)
        and f.confidence >= 0.6
    ]
    others.sort(key=lambda f: -WEIGHTS[f.severity] * f.confidence)
    reason_codes = sorted({f.code for f in blocking} | ({f.code for f in others[:5]} if block else set()))
    return Decision(
        decision="BLOCK" if block else "PASS",
        risk_score=risk,
        blocking_findings=[f.id for f in blocking],
        reason_codes=reason_codes,
        message_to_declarant=build_message(decl_name, blocking, others[:6]) if block else "",
        counterfactual_article=facts.get("counterfactual_article"),
        declared_article=facts.get("declared_article"),
    )
