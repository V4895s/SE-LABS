# EV Charging Station Reservation System
**PES University – Dept. of CSE | SE Lab 1: Requirements Engineering & UML Use-Case Modelling**
**Problem Statement #21 – Smart Cities, Transport & Logistics**

A navigation and reservation portal that lets EV drivers find compatible charging sockets (CCS, CHAdeMO, Type 2), reserve guaranteed time slots, and see dynamic power rates.

**Actors:** EV Driver (primary), Station Operator (primary), Payment Gateway (secondary / external system)

## Repository contents
| Deliverable | File |
|---|---|
| Requirements table (5 FR + 2 NFR) | [docs/requirements.md](docs/requirements.md) |
| UML use-case diagram | [diagrams/use-case-diagram.svg](diagrams/use-case-diagram.svg) (PlantUML source: `use-case-diagram.puml`) |
| Use-case flow specification (1 page) | [docs/UC-03-Reserve-Charging-Slot.md](docs/UC-03-Reserve-Charging-Slot.md) |

## Use-case diagram
![Use-case diagram](diagrams/use-case-diagram.svg)

## Assumptions
- A reservation window is fixed at 30 minutes (per the sample FR).
- Rates are quoted at booking time and locked for that reservation.
- The 10-minute no-show grace period and the cancellation/penalty amounts are operator-configurable defaults.
