# Default Behaviour 
Triage this field after queue/category/type and before any other field. The predicted value for this AI Eligibility UDF is the single source of truth for all eligibility-dependent decisions in this triage run, including Status and escalation. Do not let Status or any other field make a separate, conflicting eligibility decision.

Set AI Eligibility = Eligible only when all are true: the predicted queue is in the 100–297 range; the request is a routine Level 1 task suitable for standard known steps or AI-assisted information gathering; it does not require project work, sales/TAM ownership, architecture/design decisions, billing decisions, security exceptions, approvals, or customer-specific judgment; and work can begin without human approval. Also set to Eligible if more information is required to make an AI Eligibility decision. 

Set AI Eligibility = Ineligible if any are true: 
- the predicted queue is 298 or higher
- request is complex, ambiguous beyond routine AI-assisted information gathering, sensitive because there is evidence or credible suspicion of compromise/harmful action, or needs human judgment beyond standard spam/phishing verification
- the request requires escalation per the NEO escalation triggers catalog (found in ITGlue)
- the request requires internal approval or custom analysis
- confidence is insufficient that AI handling is safe and appropriate.
- User is unable to work 
- User is unable to sign in to computer or VDI 
- Request states "URGENT" or "ASAP" 

Write exactly Eligible or Ineligible.

# Special Instructions

- Routine spam/phishing/email-security verification tickets are AI Eligible when the requester is asking whether a message is legitimate, reporting a suspicious/spam/phishing email, or asking for verification, and there is no evidence that credentials were submitted, a link or attachment was opened/executed, mailbox/account access was compromised, malicious rules or forwarding were created, data was accessed or exposed, funds/payment changes were made, malware executed, or any other harmful action occurred. Do not mark these Ineligible solely because the predicted queue/category/issue type is Security, Security Email, Phishing, or Email Breach/User Phished.
