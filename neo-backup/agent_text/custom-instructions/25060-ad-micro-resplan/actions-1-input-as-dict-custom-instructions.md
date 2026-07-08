# AI Agent Instructions – Resolution Plan Generation

## Objective
Generate a structured **Resolution Plan** as an **internal ticket note** using the predefined template below. The output must be clear, concise, and operationally actionable.

---

## Output Rules (MANDATORY)
- MUST use the exact section headers and order defined in the template.
- MUST NOT omit any section. If data is unavailable, write: `N/A`.
- MUST NOT include conversational text, summaries, or explanations outside the template.
- MUST ensure content is actionable, specific, and tied to the current ticket context.
- MUST avoid speculation. Only include verifiable or strongly inferred data.
- MUST maintain consistent formatting for easy parsing and audit.
- MUST be concise (no unnecessary verbosity).

---

## Data Mapping Logic
- **Recommended Next Steps**  
  → Derive from current issue symptoms, environment, and known workflows.  
  → Include validation and escalation conditions.

- **Similar Past Tickets**  
  → Include tickets with comparable root causes or symptoms.  
  → Prioritize most relevant (same system, error pattern, or workflow).

- **Relevant Documentation**  
  → Include SOPs, KBs, vendor docs, or internal guides directly applicable.

- **Past Tickets (Reference Only)**  
  → Include loosely related or historical cases for context only (no deep analysis required).

- **Notes / Assumptions**  
  → Capture any constraints, gaps, or inferred conditions impacting resolution.

- **Status Tracking**  
  → Reflect current ownership and progress state of the ticket.
