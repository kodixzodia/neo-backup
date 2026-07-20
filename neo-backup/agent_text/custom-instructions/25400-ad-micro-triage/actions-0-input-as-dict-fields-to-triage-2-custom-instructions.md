Enforce the following standard by default on all tickets: [SERVICE DOMAIN] – [ISSUE SUMMARY]

(override rule: ) Preserve the existing existing ticket title only if: 
  - queue_id matches "210", OR 
  - queue_name: "CS-Monitoring Alert", OR 
  - title_starts_with: "ITGlue Notification", OR
  - title_contain: "dark web", OR
  - title_contains: "New compromise found"
