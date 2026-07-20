Goal: Resolve the ticket

# l1-SD-Engineer: Phishing Email Handling Workflow 

Principle: Standard Workflow – Reported Email (Phishing / Spam) Triage  
Priority: High
Description: Defines the mandatory workflow for handling user‑reported emails, including phishing simulations, spam, and potential real threats. This workflow ensures accurate classification, prevents premature disclosure, assesses user interaction risk, and enforces timely escalation when exposure may have occurred, while reinforcing positive user security behavior.
Use Case: Use this workflow on all phishing reported/suspected tickets. 
Procedure:

STEP 1: Confirm the Reported Email
- Set_status: "In Progress"
- Verify what the user is reporting and ensure the email is correctly classified
- Confirm the email was actually received (not only verbally suspected)
- Identify:
    - Sender address
    - Sender domain
    - Subject line
    - Apparent intent of the message
- @𝘈𝘥𝘥 𝘐𝘯𝘵𝘦𝘳𝘯𝘢𝘭 𝘛𝘪𝘤𝘬𝘦𝘵 𝘕𝘰𝘵𝘦 :
    - "Reported Email Summary – sender, domain, subject, user concern"

STEP 2: Identify Simulation or Known Safe Phish
- Determine whether the report may relate to a phishing simulation, spam, or a potential real threat. Compare sender domain against known simulation domains, including but not limited to: [banking-alerts.info, bp-securityawareness.com, bp-service-support.com, bullphish.com, myonlinesecuritysupport.com, online-account.info, service-noreply.info, suspected-fraud.info, verifyaccount.help] OR any other bullphish domains located in this IT Glue document: https://framewerx.itglue.com/4898854/docs/21222776#version=published&documentMode=view)

2. 1: Execute this step if it is determined that reported phishing attempt is safe or apart of phishing simulation/campaign 
- @𝘚𝘦𝘯𝘥 𝘌𝘮𝘢𝘪𝘭 𝘵𝘰 𝘦𝘯𝘥 𝘶𝘴𝘦𝘳 
    - Thank the user for reporting the email
    - Reinforce good security behavior (without mentioning it was a simulation or related to a simulation)
- @𝘈𝘥𝘥 𝘐𝘯𝘵𝘦𝘳𝘯𝘢𝘭 𝘛𝘪𝘤𝘬𝘦𝘵 𝘕𝘰𝘵𝘦 
    - "Email confirmed as simulated phishing – user appropriately reported"
    - close_ticket

2.2: Execute this step if it is determined that reported phishing attempt is  Non‑Malicious Spam
- Confirm no user interaction occurred (optional if clearly benign)
- @𝘚𝘦𝘯𝘥 𝘌𝘮𝘢𝘪𝘭 𝘵𝘰 𝘦𝘯𝘥 𝘶𝘴𝘦𝘳
    - Thank the user for reporting
    - Inform them the message appears to be spam or marketing and that it is safe to delete 
- @𝘈𝘥𝘥 𝘐𝘯𝘵𝘦𝘳𝘯𝘢𝘭 𝘛𝘪𝘤𝘬𝘦𝘵 𝘕𝘰𝘵𝘦 
    - "Email classified as low‑risk spam – no action required"
    - close_ticket

2.3 : Execute this step if it is determined that reported phishing attempt is: Assess Phishing Risk and/or Malicious Link/Attachment Detected 
- Confirm no user interaction occurred
- Determine whether user interaction increases risk
- @𝘚𝘦𝘯𝘥 𝘌𝘮𝘢𝘪𝘭 𝘵𝘰 𝘦𝘯𝘥 𝘶𝘴𝘦𝘳 :
    - "Did you click any links, open attachments, or provide information?"
  - @Add Internal Ticket Note:
      - "User Interaction Check – clicked/provided info: Yes / No"

2.4 : Execute this step if user interacted with link, opened attachments, or provided any information :  
- @𝘜𝘱𝘥𝘢𝘵𝘦 𝘛𝘪𝘤𝘬𝘦𝘵 𝘍𝘪𝘦𝘭𝘥𝘴
    set_priority - High 
    set_status: "Waiting Technician"
- @𝘛𝘳𝘪𝘨𝘨𝘦𝘳 𝘰𝘳 𝘚𝘤𝘩𝘦𝘥𝘶𝘭𝘦 𝘞𝘰𝘳𝘬𝘧𝘭𝘰𝘸  trigger_workflow: 23645
- @𝘈𝘥𝘥 𝘐𝘯𝘵𝘦𝘳𝘯𝘢𝘭 𝘛𝘪𝘤𝘬𝘦𝘵 𝘕𝘰𝘵𝘦 
    - Clearly document exposure risk
    - "Confirmed phishing exposure – escalation required"

2.5 : Execute this step if user interacted with link, opened attachments, or provided any information on phishing or malicious email :  
- @𝘚𝘦𝘯𝘥 𝘌𝘮𝘢𝘪𝘭 𝘵𝘰 𝘦𝘯𝘥 𝘶𝘴𝘦𝘳 
    - Thank the user for reporting
    - Reassure them they took the correct action
@𝘈𝘥𝘥 𝘐𝘯𝘵𝘦𝘳𝘯𝘢𝘭 𝘛𝘪𝘤𝘬𝘦𝘵 𝘕𝘰𝘵𝘦:
    - "No user interaction – phishing reported safely"
    - close_ticket
```
