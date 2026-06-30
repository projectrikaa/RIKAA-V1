"""Blueprint Module 3.12 — Decision Risks Module.

Uses Hermes for semantic understanding of decision risks.
Owns the Blueprint boundary: JSON deserialization, validation, and structured output.
"""

import json

from models.chat import DecisionRisksResult, PlanningContext
from prompts.decision_risks_prompt import get_decision_risks_system_prompt
from services.ollama_service import send_messages_to_ollama

_EXPECTED_KEYS = {"risk_list", "probability_assessment", "impact_assessment", "mitigation_options", "residual_risks"}


def identify_decision_risks(context: PlanningContext) -> DecisionRisksResult:
    """Identify decision risks by instructing Hermes.

    Consumes all previous PlanningContext fields to construct the analysis.
    Hermes owns semantic reasoning and returns JSON.
    This module owns deserialization, validation, and Blueprint boundaries.
    """
    p = context.purpose
    pr = context.problem
    t = context.target_outcome
    s = context.success_criteria
    sc = context.scope
    a = context.anti_goals
    c = context.constraints
    asm = context.assumptions
    ev = context.evidence
    oq = context.open_questions
    vs = context.validation_strategy
    user_message = (
        f"Primary Purpose: {p.primary_purpose}\n"
        f"Secondary Purpose: {p.secondary_purpose}\n"
        f"Expected Value: {p.expected_value}\n"
        "\n"
        "Problem:\n"
        f"Problem Statement: {pr.problem_statement}\n"
        f"Root Cause: {pr.root_cause}\n"
        f"Impact: {pr.impact}\n"
        f"Stakeholders Affected: {pr.stakeholders_affected}\n"
        "\n"
        "Target Outcome:\n"
        f"Target Outcome Statement: {t.target_outcome_statement}\n"
        f"Desired Future State: {t.desired_future_state}\n"
        f"Expected Business Outcome: {t.expected_business_outcome}\n"
        f"Expected User Outcome: {t.expected_user_outcome}\n"
        f"Outcome Boundaries: {t.outcome_boundaries}\n"
        "\n"
        "Success Criteria:\n"
        f"Success Criteria: {s.success_criteria}\n"
        f"Acceptance Rules: {s.acceptance_rules}\n"
        f"Measurement Rules: {s.measurement_rules}\n"
        "\n"
        "Scope:\n"
        f"Scope Statement: {sc.scope_statement}\n"
        f"In-Scope Items: {sc.in_scope_items}\n"
        f"Out-of-Scope Items: {sc.out_of_scope_items}\n"
        f"Scope Boundary: {sc.scope_boundary}\n"
        "\n"
        "Anti-Goals:\n"
        f"Anti-Goals: {a.anti_goals}\n"
        f"Non-Targeted Objectives: {a.non_targeted_objectives}\n"
        f"Optimization Exclusions: {a.optimization_exclusions}\n"
        "\n"
        "Constraints:\n"
        f"Constraint List: {c.constraint_list}\n"
        f"Constraint Categories: {c.constraint_categories}\n"
        f"Constraint Boundaries: {c.constraint_boundaries}\n"
        "\n"
        "Assumptions:\n"
        f"Assumption List: {asm.assumption_list}\n"
        f"Confidence Rating: {asm.confidence_rating}\n"
        f"Validation Priority: {asm.validation_priority}\n"
        f"Review Conditions: {asm.review_conditions}\n"
        "\n"
        "Evidence:\n"
        f"Evidence List: {ev.evidence_list}\n"
        f"Evidence Classification: {ev.evidence_classification}\n"
        f"Source References: {ev.source_references}\n"
        f"Evidence Coverage: {ev.evidence_coverage}\n"
        "\n"
        "Open Questions:\n"
        f"Open Question List: {oq.open_question_list}\n"
        f"Question Priority: {oq.question_priority}\n"
        f"Required Action: {oq.required_action}\n"
        f"Target Resolution Point: {oq.target_resolution_point}\n"
        "\n"
        "Validation Strategy:\n"
        f"Validation Plan: {vs.validation_plan}\n"
        f"Validation Method: {vs.validation_method}\n"
        f"Validation Checklist: {vs.validation_checklist}\n"
        f"Validation Schedule: {vs.validation_schedule}\n"
        f"Acceptance Decision: {vs.acceptance_decision}\n"
        "\n"
        "Based on all the above, identify the decision risks."
    )
    messages = [
        {"role": "system", "content": get_decision_risks_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    raw_response = send_messages_to_ollama(messages)

    return _parse_decision_risks_json(raw_response)


def _normalize_missing(value) -> str:
    """Normalize missing/null/empty values to 'Not Specified'.

    Rules:
      None        → "Not Specified"
      ""          → "Not Specified"
      "None"      → "Not Specified"
      "null"      → "Not Specified"
      whitespace  → "Not Specified"
    Otherwise returns the original value unchanged.
    """
    if value is None:
        return "Not Specified"
    s = str(value).strip()
    if s in ("", "None", "null"):
        return "Not Specified"
    return value


def _parse_decision_risks_json(raw: str) -> DecisionRisksResult:
    """Deserialize Hermes JSON response into a DecisionRisksResult.

    If JSON is invalid or fields are missing, missing fields default
    to 'Not Specified'. No inference is performed.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return DecisionRisksResult()

    # Extract only known fields, ignore any extras Hermes might return
    return DecisionRisksResult(
        risk_list=_normalize_missing(data.get("risk_list", "Not Specified")),
        probability_assessment=_normalize_missing(data.get("probability_assessment", "Not Specified")),
        impact_assessment=_normalize_missing(data.get("impact_assessment", "Not Specified")),
        mitigation_options=_normalize_missing(data.get("mitigation_options", "Not Specified")),
        residual_risks=_normalize_missing(data.get("residual_risks", "Not Specified")),
    )