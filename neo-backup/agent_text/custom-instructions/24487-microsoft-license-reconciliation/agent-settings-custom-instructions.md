# Instructions 
1. For each connected M365 tenant, list users with id, displayName, userPrincipalName, accountEnabled, and assignedLicenses.
2. Keep only users where accountEnabled = false and assignedLicenses is not empty.
3. Exclude obvious non-person accounts by name/UPN patterns such as svc-, breakglass, emergency, admin, and test, unless the tenant explicitly wants those included.
4. For each remaining user, fetch licenseDetails and map the SKU IDs to friendly license names using the tenant’s /subscribedSkus list.
5. Before creating anything, check Autotask for an existing open ticket for the same user/UPN and the same issue. If one exists, skip creation and record the ticket number.
6. If no duplicate exists, create one Autotask ticket per user with:
        - Title: Disabled M365 user still has active license(s): <Display Name> (<UPN>)
        - Description: tenant name, UPN, disabled state, friendly license names, SKU part numbers, timestamp found, and any duplicate-check result
        - Company: the matching end-client Autotask company for that tenant
        - Use the tenant’s standard service-desk queue/status/priority 
7. After processing all tenants, send one internal summary with counts for created, skipped, duplicate hits, and errors. (send to Kodi) 
8. If company mapping is missing or ambiguous, do not guess; flag it for manual review.

# Action Flow: 
1. M365 scan — query users.
2. License enrichment — pull licenseDetails and tenant SKUs.
3. Deduplicate — search Autotask open tickets for the same user.
4. Create ticket — open one Autotask ticket per match.
5. Summarize — send one internal rollup.
