"""Stage 0: prior risk signals, WITHOUT AI (free and instant).

They never block on their own: they help prioritise (in production: which declarations go
through the agent) and contribute weakly to the risk score (decision.risk_score).
"""

from __future__ import annotations

from .config import Settings
from .db import fetchone
from .declarations import DeclarationDTO
from .refdata import RefData

# Galenic form names in the database (French) that imply a capsule shell.
CAPSULE_FORMS = ("gélule", "capsule")


def triage(settings: Settings, ref: RefData, decl: DeclarationDTO) -> dict:
    """Return {"signals": [...], "prior": 0-1}. The prior grows by 0.15 per signal."""
    signals: list[dict] = []
    galenic = (
        ref.galenic.get(str(decl.galenic_formulation_id), {}).get("name", "") if decl.galenic_formulation_id else ""
    )
    n_items = len(decl.items)
    n_inactive = sum(1 for it in decl.items if not (ref.get(it.uid).active if ref.get(it.uid) else it.active))
    # A capsule needs a shell: a single declared element, or no excipient at all, is suspicious.
    if galenic.lower().startswith(CAPSULE_FORMS) and n_items == 1:
        signals.append(
            {"code": "T-CAPSULE-ONE-ITEM", "detail": f"{galenic} declared with a single element (no shell?)"}
        )
    elif galenic.lower().startswith(CAPSULE_FORMS) and n_inactive == 0:
        signals.append({"code": "T-NO-EXCIPIENT", "detail": f"{galenic} without any declared non-active ingredient"})
    # A declared dose just below the max is a classic way to stay in article 15.
    for c in decl.computed_substances + [it for it in decl.items if it.kind == "substance"]:
        el = ref.get(c.uid)
        if el is None or c.quantity is None:
            continue
        mx = ref.max_for(el, decl.populations)
        if mx and 0.9 * mx <= c.quantity <= mx:
            signals.append(
                {
                    "code": "T-DOSE-AT-MAX",
                    "detail": f"{el.name} declared at {c.quantity:g} for a max of {mx:g} ({c.quantity / mx:.0%})",
                }
            )
    # Company history: other declarations blocked by an instructor for a label reason.
    if decl.company_id:
        row = fetchone(
            settings,
            """
            select count(distinct s.declaration_id) n from data_snapshot s join data_declaration d on d.id=s.declaration_id
            where d.company_id=%s and d.id<>%s and s.blocking_reasons && %s""",
            (
                decl.company_id,
                decl.declaration_id,
                # blocking reasons as stored in the database
                ["Incohérences entre le dossier et l'étiquetage", "Absence ou non conformité de l'étiquetage"],
            ),
        )
        if row and row["n"]:
            signals.append(
                {
                    "code": "T-COMPANY-HISTORY",
                    "detail": f"{row['n']} other declaration(s) of the company blocked for a label reason",
                }
            )
    prior = min(1.0, 0.15 * len(signals))
    return {"signals": signals, "prior": prior}
