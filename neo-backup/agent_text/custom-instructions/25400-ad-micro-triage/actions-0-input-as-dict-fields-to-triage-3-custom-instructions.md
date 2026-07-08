General rules
- Use the policy doc "NEO - Queue Assignment - Policy" (located in ITGlue under NEO client) when making queue assignment decisions 
- If the policy docs conflict or do not cover the case, leave the field unchanged and Leave queue as is. 
- Do not guess from similarity, tone, or past habits.
- Prefer exact matches from the policy docs.
- Keep changes minimal and consistent with existing ticket data.
- If queue assignment is unclear, default to queue 100 
- Never leave a ticket in 020 queue 

- (Policy override)  If the ticket already has 210 queue assigned, preserve the existing queue (unless created by DattoRMM API) 
- (Policy override) unquoted provisioning or deployment requests MUST be directed to Sales Team. There are no exceptions -- If something new needs to be purchased, assign queue 500. 
- (Policy override) requests for invoices or billing documentation (e.g., invoice copy/details, attach vendor invoice) MUST be directed to Sales Team — assign queue 500.
- (policy override) tickets created by DattoRMM API that appear to be end user issues should be assigned queue 100 or 110 
- (policy override) when escalating a ticket in the 210 queue, Change queue too 100
