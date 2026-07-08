Goal: Find Incident Tickets and associate them with the appropriate problem ticket. 

Detect newly created tickets that match an existing known issue/problem pattern for the same company, and associate the new incident ticket to the appropriate problem ticket.
For each ticket:

For each newly created ticket, first determine whether the new ticket is an Incident ticket.

Only continue if:
- Association is permitted only when the source ticket has ticketType = Incident and the destination ticket has ticketType = Problem.

Then search for an existing ticket where:
- ticketType = Problem
- the company matches the new Incident ticket
- the Problem ticket is open/active
- the Problem ticket describes the same issue or similar (if similar not not exact match, @𝘙𝘦𝘲𝘶𝘦𝘴𝘵 𝘛𝘦𝘤𝘩𝘯𝘪𝘤𝘪𝘢𝘯-𝘪𝘯-𝘵𝘩𝘦-𝘓𝘰𝘰𝘱 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭) 

A ticket is considered the same issue only when supported by evidence such as:
- same affected service/system
- same error message or failure condition
- same symptom pattern
- same issue context

Association rules:
- Never merge tickets
- Never convert ticket types
- Never close, suppress, or overwrite the new Incident ticket
- Associate the Incident ticket to one best-fit Problem ticket only
- Do not associate across different companies
- Do not associate if no clear Problem ticket match exists
- Do not associate if multiple possible Problem tickets exist and a single best match cannot be determined confidently

When a valid match is found:
- associate the Incident ticket to the matched Problem ticket
- add an internal note containing:
  - Incident ticket identified as ticketType = Incident
  - matched ticket identified as ticketType = Problem
  - matched Problem ticket ID
  - reason for association
  - key matching evidence

If the new ticket is not an Incident ticket, take no action. but explain why no match was found and whether or not a close match exists. (if a close match exists, @𝘙𝘦𝘲𝘶𝘦𝘴𝘵 𝘛𝘦𝘤𝘩𝘯𝘪𝘤𝘪𝘢𝘯-𝘪𝘯-𝘵𝘩𝘦-𝘓𝘰𝘰𝘱 𝘈𝘱𝘱𝘳𝘰𝘷𝘢𝘭) 
If no valid open Problem ticket exists for the same company and same issue, take no action.
