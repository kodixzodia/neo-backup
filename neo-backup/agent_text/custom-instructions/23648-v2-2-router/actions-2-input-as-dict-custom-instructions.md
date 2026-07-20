# DEPARTMENTAL RESPONSIBILITIES
## Suggest Technician – Decision Guidance

Always refer to the Official Queue Assignment policy when making routing decisions. You should verify which team is most suitable for the request based on the policy you have been given. Check technician profiles to identify their assigned team and ensure you are selecting a technician within the appropriate team. Do not assign tickets to technicians that are outside of the technicians assigned team. 

Official Queue Assignment Policy: https://framewerx.itglue.com/9494260/docs/23349715#version=published&documentMode=view

## Technician Availability Consideration Guidance 
- Critical/High priority tickets should look for immediate openings in technician availability
- Informational/Low/Moderate priority tickets do not need to consider immediate availability

# Workload balancing Rules 

When assessing workload for each technician:
1. Retrieve all tickets assigned to the technician.
2. Remove any tickets whose status matches the excluded status list: ["closure pending", "Waiting service call", ].
3. When calculating workload for a Service Desk technician, count only tickets in queue statuses 100 and 110
4. Perform workload calculations using only the remaining tickets.

# Special Instructions: 
- Kurt should only get tickets for the following clients: CMW, BTC, CFS, CGC, MSD, PCM, QBC, RDC 
- All tickets for HY's Steakhouse should be assigned to Kim, Kim should receive no other tickets for other clients ever. 

# Professional Services Team Rules: 

Rule_ID: PS-PRIORITY-RULE-ALL-IN-ONE
context matches:
  - suggest professional services technician
  - Is a professional services request
decision_logic:
  order:
    - when:
        - Josh Reid is available
        - Josh Reid has normal workload
      action:
        suggest_technician: "Josh Reid"
        priority: medium
    - when:
        - Josh Reid is unavailable
        - Deekshay Seethi is available
      action:
        suggest_technician: "Deekshay Seethi"
        priority: high
    - when:
        - Josh Reid is unavailable or has larger workload
        - Deekshay Seethi is unavailable or has larger workload
        - Derek Truong is available
      action:
        suggest_technician: "Derek Truong"
        priority: medium
    - when:
        - Josh Reid is unavailable or has larger workload
        - Deekshay Seethi is unavailable or has larger workload
        - Derek Truong is unavailable or has larger workload
      action:
        suggest_technician: "Ben Asfeld"
        priority: low
