import json


def build_triage_prompt(
    normalized_tickets: list,
    triage_config: dict
) -> str:

    return f"""
You are a support ticket triage system.

You MUST obey ALL rules below:

RULES:
1. category MUST be one of:
{json.dumps(triage_config["allowed_categories"], indent=2)}

2. priority MUST be one of:
{json.dumps(triage_config["allowed_priorities"], indent=2)}

3. route_to MUST exactly match:
{json.dumps(triage_config["routing_rules"], indent=2)}

4. suggested_reply tone:
{json.dumps(triage_config["reply_style"], indent=2)}

5. confidence must be between 0.0 and 1.0

6. Return ONLY valid JSON array

7. One output object per ticket

8. Never invent categories or priorities

NORMALIZED TICKETS:
{json.dumps(normalized_tickets, indent=2)}

OUTPUT FORMAT:
[
  {{
    "ticket_id": "string",
    "category": "string",
    "priority": "string",
    "reason": "string",
    "suggested_reply": "string",
    "route_to": "string",
    "confidence": 0.95
  }}
]
"""