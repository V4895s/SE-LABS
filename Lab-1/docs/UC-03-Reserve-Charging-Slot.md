# Use-Case Specification – UC-03: Reserve Charging Slot

| Field | Detail |
|---|---|
| **Use Case ID / Name** | UC-03 – Reserve Charging Slot |
| **Primary Actor** | EV Driver |
| **Secondary Actor** | Payment Gateway |
| **Related FRs** | FR-001, FR-003 (also NFR-001, NFR-002) |
| **Trigger** | The driver selects a station and chooses *Reserve*. |
| **Includes** | UC-04 Validate Connector Compatibility; UC-05 Calculate Dynamic Rate; UC-06 Process Payment |
| **Extended by** | UC-09 Join Waitlist (at extension point *no slot available*) |

## Preconditions
1. The driver is registered and logged in.
2. The driver has an active vehicle profile with a connector type (CCS, CHAdeMO or Type 2).
3. The selected station is online and has at least one in-service charger.
4. The driver has a valid payment method on file.

## Postconditions
- **Success:** A 30-minute reservation is confirmed and the socket is locked for the window; the quoted rate is stored; the payment is pre-authorised; a confirmation with reservation ID/QR code is sent; the 10-minute no-show timer is scheduled.
- **Failure / abandoned:** No reservation is created, no payment is taken, and any temporary slot hold is released.

## Main Success Scenario
| Step | Actor | Action |
|---|---|---|
| 1 | Driver | Selects a station from the search results and chooses **Reserve**. |
| 2 | System | Retrieves the driver's active vehicle profile and connector type. |
| 3 | System | *«include» UC-04:* lists only sockets whose connector matches the vehicle and that are currently in service. |
| 4 | Driver | Selects a socket and a start time. |
| 5 | System | Verifies the 30-minute window is free and places a 3-minute temporary hold on the socket. |
| 6 | System | *«include» UC-05:* calculates the dynamic rate and displays price per kWh, estimated cost and the no-show penalty policy. |
| 7 | Driver | Reviews the details and confirms the reservation. |
| 8 | System | *«include» UC-06:* requests pre-authorisation of the estimated amount from the Payment Gateway. |
| 9 | Payment Gateway | Approves the pre-authorisation. |
| 10 | System | Converts the hold into a confirmed reservation, locks the socket and locks the quoted rate. |
| 11 | System | Sends the confirmation (reservation ID, QR code, navigation link) by app notification and e-mail/SMS, and starts the 10-minute no-show timer. **Use case ends.** |

## Alternate Flow
**A1 – Requested window not available** *(branches from Step 5)*
- A1.1 The system finds that the selected socket/time was taken by another driver, or no compatible socket is free in that window.
- A1.2 The system informs the driver and shows the nearest alternative start times and nearby stations with compatible sockets.
- A1.3a The driver picks an alternative; the use case resumes at **Step 4** (or **Step 3** if another station was chosen).
- A1.3b *Or* the driver selects **Join Waitlist** (*«extend» UC-09*) and is notified when a matching slot opens.
- A1.4 If the driver declines all options, no reservation is created and the use case ends (failure postcondition).

## Business Rules & Notes
- A socket can never hold two overlapping confirmed reservations (FR-001, NFR-001).
- The quoted rate is fixed once the reservation is confirmed (FR-003).
- If the driver does not plug in within 10 minutes of slot start, the socket is released and the penalty is applied (NFR-001).
