Only escalate ticket if UDF 'AI Eligibility'  is determined to be 'Ineligible'
 OR 
Ticket matches one of the following criteria rules:  

```
TRIGGER_ID_017  
Match if: involves physical access cards for SSL.
Keywords: "access card", "badge", "fob", "door access", "card reader", "SSL access".
```
```
TRIGGER_ID_018  
Match if: Cisco Unity Connection emails.
Keywords: "Cisco Unity", "Unity Connection", "voicemail to email", "voicemail email".
```
```
TRIGGER_ID_004  
Match if: Evidence of Physically damaged hardware.
Keywords: "won't power", "broken",  "physical damage".
```
```
TRIGGER_ID_005  
Match if: Admin rights are required.
Keywords: "admin", "administrator", "elevated", "UAC", "run as admin", "install requires admin".
```
```
TRIGGER_ID_006  
Match if: onsite work required.
Keywords: "onsite", "on-site", "in person", "cannot be remote".
```
```
TRIGGER_ID_007  
Match if: Confirmed security breaches.
Keywords: "malware" "ransomware", "account compromised", "unauthorized"
Exceptions: Suspected phishing emails, reported phishing/malicious emails by end user 
```
```
TRIGGER_ID_008  
Match if: issue involves Multifactor Authentication (MFA).
Keywords: "MFA", "2FA", "authenticator", "conditional access"
```
```
TRIGGER_ID_009  
Match if: Fortinet malware detected.
Keywords: "Fortinet", "FortiEDR", "FortiClient", "malware detected", "Fortinet alert"
Exceptions:  SOCaas weekly summary reports
```
```
TRIGGER_ID_010  
Match if: NEO agent issue or feature request.
Keywords: "NEO", "agent bug", "dispatch agent", "feature request"
```
```
TRIGGER_ID_012  
Match if: is involving an Internal application. 
Keywords: "ABMWerx", "Bidwerx", "Docuwerx", "Inventory Count Tool", "Manpower Loading", "Non-conformance Management System", "Peoplewerx", "ResourceWerx", "Shopwerx","Sitewerx", "Stems"
```
```
TRIGGER_ID_013  
Match if: Ticket is queued for technician follow-up.
```
```
TRIGGER_ID_014  
Match if: Technician-in-the-loop approval was denied
```
```
TRIGGER_ID_015  
Match if: ThreatLocker application request.
Keywords: "ThreatLocker", "application request", "allow app", "permit"
```
```
TRIGGER_ID_016 
Match if: TrueNAS ticket.
Keywords: "TrueNAS", "NAS", "storage", "share on TrueNAS"
```
```
TRIGGER_ID_019  
Match if: client-wide outage.
Keywords: "everyone", "all users", "site-wide", "company-wide", "widespread outage".
```
```
TRIGGER_ID_020  
Match if: steps become unsafe / risk of damage or irreversible action
```
```
TRIGGER_ID_021  
Match if: Ticket is URGENT 
Keywords: "urgent", "ASAP", "P1", "security incident"
```
```
TRIGGER_ID_022  
Match if: potential compliance or configuration risk.
Keywords: "compliance", "audit", "non-compliant", "policy violation", "configuration risk".
```
```
TRIGGER_ID_023  
Match if: purchase request / quote request / invoice request.
Keywords: "purchase request", "quote", "pricing", "procurement", "buy", "order".
```
```
TRIGGER_ID_024  
Match if: Framewerx Datacenter systems issues (Nimble, ESXi, vCenter).
Keywords: "Nimble", "ESXi", "datacenter".
Exceptions: user VDI log in issues; Omnissa/VDI visibility issues (e.g., "server not visible", "VDI not listed"). 
```
```
TRIGGER_ID_0025  
Match if: Issue involves permissions, roles, or access control
Keywords: "permissions", "access denied", "role", "RBAC", "conditional access", "not authorized", "insufficient privileges"
```
```
TRIGGER_ID_0026  
Match if: Is a ticket regarding the offboarding of a client organization
Keywords
```
```
TRIGGER_ID_027  
Match if: New Computer or VDI set-up 
Keywords: "New Computer", "New VDI", "New User Computer", "Set-up"
```
```
TRIGGER_ID_028  
Match if: New Computer or VDI set-up 
Keywords: "New Computer", "New VDI", "New User Computer", "Set-up"
```
```
TRIGGER_ID_028 
Match If: request is not related to End user troubleshooting, IT related inquiries/issues , MSP related inquiries/issues
```
```
TRIGGER_ID_029
priority: high
Match if: is an unquoted provisioning request OR is a request implying purchase 
Key Phrases: "provision", "request quote", "send quote"
Additional Context: this trigger should include any provisioning request for both hardware & software requests. 
```
TRIGGER_ID_030
Match if: User is requesting a phone call, callback, or direct human contact.
Keywords: "can someone call me", "Call back", "please call", "I need to speak to someone"
```
