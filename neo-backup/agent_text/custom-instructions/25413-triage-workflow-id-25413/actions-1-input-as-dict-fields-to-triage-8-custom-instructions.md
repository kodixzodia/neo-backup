STANDARD TITLE FORMAT: [SERVICE DOMAIN] – [ISSUE SUMMARY]
  - Enforce the following standard by default on all triaged tickets

- Never remove urgency indicators from original ticket title. 
- Never remove the word "Termination" from ticket titles. 
- Add Urgency indicator to title only if an Urgency Indicator is explicitly stated in ticket description or original title.   

(override rule: ) Preserve the existing existing ticket title only if: 
  - queue_id matches "210", OR 
  - queue_name: "CS-Monitoring Alert", OR 
  - title_starts_with: "ITGlue Notification", OR
  - title_contain: "dark web", OR
  - title_contains: "New compromise found"
