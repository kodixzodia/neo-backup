Set "AI Eligibility" UDF = Eligible only when all of the following are true:
- The ticket belongs to queues in range 100 - 297
- It is a routine Level 1 task that can be handled using standard known steps
- It does not require project work, sales assistance, TAM ownership, architecture/design decisions, billing, decisions, security exceptions, approvals, or customer-specific judgment
- It does not require human coordination before work can begin

Set "AI Eligibility" UDF = Ineligible if any of the following are true:
- The ticket belongs to queues 298 and higher 
- The request is complex, ambiguous, sensitive, or needs human judgment
- The request requires escalation as identified in our escalation catalog found in IT Glue (under the "NEO" client, called "NEO - Escalation Triggers - Catalog")
- The request requires internal approval, or custom analysis
- You are not confident the ticket is safe and appropriate for AI handling

If the ticket is Eligible , write "Eligible" to the "AI Eligibility" UDF
If the ticket is Ineligible, write "Ineligible" to the AI Eligibility UDF
