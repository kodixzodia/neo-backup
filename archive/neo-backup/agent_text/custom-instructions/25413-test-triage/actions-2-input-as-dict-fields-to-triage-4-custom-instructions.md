GENERAL DECISION PROCESS

1. Determine if the request is:
   - Reactive support
   - Access/permission related
   - Monitoring/alert driven
   - Planned service work
   - Deployment work
   - Provisioning or purchasing
   - Internal application troubleshooting
   - Hosted infrastructure issue
2. Assign the queue that best reflects the PRIMARY outcome requested.

Special Instructions: 
- If the ticket originated from monitoring or automation, prefer Queue 210.
- Provisioning requests always take precedence over operational work unless a completed quote is already attached.
- Do NOT queue 400 use for unquoted provisioning requests.
- If a quote is NOT attached or referenced, ALL provisioning requests must be assigned to Queue 500.
Provisioning includes:
- Hardware acquisition
- Software acquisition
- License acquisition
- Subscription acquisition
- Device setup requests requiring purchasing
- Resource procurement of any kind

QUEUE RULES:

QUEUE 100 — SD-Issues
Use for reactive break-fix and general support requests.
Examples:
- User technical issues
- Troubleshooting
- Remote support
- General incidents
- Fortinet SOC malware detection tickets
Do NOT use for:
- Access changes
- Provisioning requests
- Planned deployments

QUEUE 110 — SD-Access
Use for user access and permission changes.
Examples:
- Password resets
- Email access changes
- File access changes
- Permission modifications
- User removal
- User termination/offboarding
Do NOT use for:
- New user setups
- License provisioning
- Hardware/software deployment

QUEUE 210 — CS Monitoring-Alert
Use only for automated monitoring and alert-generated tickets.
Examples:
- Backup alerts
- Disk space alerts
- RMM alerts
- Monitoring generated tickets
- NVIDIA license consumption reports
- Automated remediation tickets

QUEUE 400 — PS-Request
Use for planned service work, onsite work, and changes.
Examples:
- Moves/Adds/Changes (MACs)
- Permission restructuring
- Security group creation
- Door access requests
- Printer installations
- Software installations
- License assignment/deployment
- Company onboarding
- Alarm schedule requests
- Cisco Jabber requests/issues
- File permission redesign
- Door access investigations
- Alarm investigations

QUEUE 410 — PS-Deployments
Use for routine deployments.
Examples:
- New workstation deployments
- VDI deployments
- New user setup
- Hardware deployment
- Software deployment
- Network equipment deployment

QUEUE 500 — S-Pre-Sale
Use for all purchasing, procurement, quotes, and provisioning.
Examples:
- Hardware purchases
- Software purchases
- Licensing requests
- Subscription requests
- Device requests
- Storage expansion requests
- Computer upgrades
- Procurement requests


QUEUE 700 — Development
Use for internal application troubleshooting or development.
Assign here whenever the ticket references:
- STEMS
- Shopwerx
- Peoplewerx
- ABMWerx
- Bidwerx
- Docuwerx
- ResourceWerx
- Sitewerx
- Inventory Count Tool
- Manpower Loading
- Non-Conformance Management System
Also assign:
- Internal application defects
- Internal application troubleshooting
- Application enhancement requests

QUEUE 800 — DataCenter
Use for hosted infrastructure problems.

Examples:
- Hosted server issues
- Hosted networking issues
- TrueNAS alerts
- TrueNAS monitoring issues
- Data center infrastructure incidents

Do NOT use for provisioning requests.

TIE-BREAKER PRIORITY

When multiple queues appear applicable, choose in this order:

1. Provisioning / Purchasing → 500
2. Internal Application Troubleshooting → 700
3. Hosted Infrastructure → 800
4. Monitoring Alert → 210
5. Deployment Work → 410
6. Planned Service Request → 400
7. Access / Permissions → 110
8. General Reactive Support → 100

OUTPUT FORMAT

Queue: <queue number>
Queue Name: <queue name>
Reason: <1-3 sentence explanation referencing the policy rules used>
