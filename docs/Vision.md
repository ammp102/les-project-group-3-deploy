# Product Vision & Strategic Ideas Repository: Patas

| Metadata | Detail |
| :--- | :--- |
| **Project** | Patas — Collaborative Animal Welfare Platform |
| **Context** | Web Project / Software Engineering (Agile Process in 4 Sprints) |
| **Date** | October 2026 |
| **Status** | Consolidated Vision & Open Ideas Repository |

---

## 1. Product Vision Statement

> **For** animal lovers looking to adopt, foster or care for animals, and for animal protection associations struggling with administrative overload,  
> **Patas** is a collaborative web platform that centralizes and simplifies the entire animal care and adoption cycle.  
> **Unlike** manual processes relying on spreadsheets, chaotic group chats and scattered applications that leave adopters in the dark,  
> **Our product** combines an open exploration route with smart lifestyle matching, full transparency through a real-time *Adoption Tracker*, and a guided *Foster-to-Adopt* model — complemented by community volunteering and a solidarity wishlist of goods. By doing so, we maximize compatibility between families and animals, drastically reduce the risk of returns, and relieve associations of heavy manual workloads.

**Our main priority is giving these animals love and a better life.**

### Core Options

* **Adopt:** people look for the animal that best fits their home and family and adopt it; a temporary stay (*Foster-to-Adopt*) is possible before finalizing the decision, to ensure the fit is right.
* **Foster:** someone volunteers to provide housing and care for one or multiple animals for a period of time.
* **Care:** users volunteer to walk animals, feed them, clean them or take them to the vet.

---

## 2. Identified Real Pains (The Problem Space)

### On the Associations' and Shelters' Side
1. **Communication Chaos and Loss of History:** Applications and questions arrive simultaneously via WhatsApp, Instagram, email and isolated forms, causing data loss and duplicated effort.
2. **Reliance on Manual Spreadsheets:** Tracking of animal status (available, in foster care, adopted) and of volunteer schedules is done in shared Excel files with fragile access.
3. **Overload from Incompatible Screening:** Receiving applicants whose living conditions clash with the animal's needs, increasing the time spent on rejections.
4. **Disorganized Donation Collection:** Difficulty communicating the exact material needs of the moment (e.g., renal food, blankets in winter, milk replacer for litters).

### On the Citizens' and Adopters' Side
1. **The Application "Black Hole":** Submitting long forms without knowing whether they were received, are under review, or whether the animal has already been adopted.
2. **Adoptions Driven by Looks vs. Returns:** Choices made solely on appearance or a photo, without assessing routine or temperament, leading to painful returns.
3. **Fear of Immediate Commitment:** Willingness to adopt held back by fear that the animal won't adapt to the home, the children or other existing pets.
4. **Wanting to Help Without Being Able to Adopt:** People who want to help (walking dogs, playing with cats, donating food) but don't know where or how to offer themselves in a practical, low-bureaucracy way.

---

## 3. Actors & Roles

| Role | Description | Main Capabilities |
| :--- | :--- | :--- |
| **Visitor** | Unauthenticated user | Browse the catalog, view animal profiles and wishlists, take the Matchmaker quiz. |
| **Citizen (Registered User)** | Authenticated person | Submit and track adoption applications, request a Foster-to-Adopt period, pledge wishlist items. |
| **Volunteer** | Registered citizen with a volunteer profile | Sign up for walk/socialization slots and operational shifts (feeding, cleaning, vet transport). |
| **Foster Family** | Registered citizen with a fostering profile | Register fostering availability and conditions. |
| **Association Staff** | Member of a specific association | Manage that association's animals, applications, rosters, wishlist and payment settings. |
| **Platform Administrator** | Patas operator | Register and verify associations, moderate content. |

---

## 4. Platform Model: Multiple Associations

* Patas is a **multi-association platform**: each association has its own space (animals, applications, volunteers, wishlist), and the public catalog aggregates animals from all verified associations.
* Each association's data is isolated: staff only see and manage their own association's records.
* New associations go through a **registration and verification** process by the Platform Administrator before publishing animals.
* **Single-association deployment:** the platform must remain deployable for a single association (e.g., an instance dedicated to one shelter) without structural changes.

---

## 5. Strategic Pillars & Ideas Repository

```
                                          ┌────────────────────────┐
                                          │     PATAS PLATFORM     │
                                          └───────────┬────────────┘
                                                      │
       ┌──────────────────┬──────────────────┬────────┴─────────┬──────────────────┐
       ▼                  ▼                  ▼                  ▼                  ▼
 [ 1. ADOPTION ]   [ 2. FOSTERING ]  [ 3. VOLUNTEERING ] [ 4. SOLIDARITY ]  [ 5. BACK-OFFICE ]
 • Dual Discovery  • Foster-to-Adopt • Walks             • Goods Wishlist   • Application Kanban
 • Real-Time       • Parametric      • Socialization     • Pledges &        • Animal Management
   Tracker           Foster Engine   • Operational Roster  Direct Delivery  • Volunteer Hub
```

---

### Pillar 1: Discovery & Responsible Adoption

* **Path 1 — Open Universal Catalog:**
  * Fast, unobstructed browsing of all registered animals across associations.
  * Clear filters: species, size, age, location, association, compatibility (children, other dogs, cats).
  * Rich animal profile: photos, temperament, story and required routine.

* **Path 2 — Optional Compatibility Algorithm ("Matchmaker"):**
  * Short lifestyle questionnaire: average time away from home, physical activity level, housing type and previous experience.
  * The system highlights animals with the highest behavioral affinity, explaining why (without blocking access to the remaining animals).
  * **The algorithm's design is intentionally left open at this stage** and will be detailed later. Envisioned direction: a swipe-based discovery experience ("Tinder-style") in which the user's choices refine future suggestions.

* **Adoption Tracker (End-to-End Transparency):**
  * Visual timeline for the applicant, in the style of parcel tracking (see the application state machine in [Section 6](#6-state-models)).
  * Notifications at every stage change, delivered **by email and in-app** (notification center within the platform), removing uncertainty and follow-up messages to the association.
  * The applicant always knows the outcome, including rejections and when the animal has been adopted by someone else.

---

### Pillar 2: Flexible Temporary Fostering (Foster Care & Foster-to-Adopt)

* **Foster-to-Adopt (Optional Trial Period):**
  * An **optional stage** of the adoption application: the adopter may request a short trial period (e.g., 7 to 15 days) before finalizing the legal adoption.
  * **The adopter requests it; the association approves or declines it** for each application.
  * The association may set a **trial-period fee**, paid online through the platform (**Stripe, in test mode**, given the academic context of the project).
  * During the trial, the association follows up on the adaptation through the platform (check-ins, notes, trial end date), minimizing returns after definitive adoption.

* **Parametric Temporary Fostering Engine (Foster Families):**
  * Volunteer families register their availability with flexible parameters:
    * Capacity: accepted species, maximum size, number of simultaneous animals.
    * Physical conditions: house with garden, fenced yard, apartment with safety netting, available play space.
    * Time window: one-off fostering (weekend, other caregivers' holidays) or ongoing.
  * Associations can search foster families whose parameters match an animal's needs.

---

### Pillar 3: Dynamic Volunteering and Socialization

* **Walking and Well-Being Sessions:**
  * Sign-up for time slots to walk dogs that spend the day in kennels, or for enrichment/socialization sessions with cats.
  * Sign-up **requires a simple registered account** (name, contact, acceptance of the volunteering terms), so that slots and responsibility can be managed.
  * Slot management per animal/shift, ensuring every animal gets its walk without overcrowding the facilities.

* **Operational Roster:**
  * Shifts for core facility tasks: feeding, cleaning enclosures, logistical support and transport to veterinary appointments.
  * Open to any registered volunteer, under the same simple-account requirement as walks.

---

### Pillar 4: Solidarity Wishlist and In-Kind Donations

* **Reverse Marketplace of Needs:**
  * The association publishes specific items currently needed, with the quantity required (e.g., *"10kg of gastrointestinal dry food"*, *"Fleece blankets for winter"*, *"Wet food for senior cats"*).
* **Pledges with Confirmation:**
  * The donor pledges a quantity of an item, which is shown as "pledged" to avoid duplicate purchases.
  * The association confirms receipt, and only then is the outstanding need updated. Pledges not fulfilled can be released by the association.
* **Donations Without Payment Intermediation:**
  * The user buys the items independently wherever they prefer and arranges the drop-off point/time or postal shipping. Wishlist donations do not go through the platform's payment system.

---

### Pillar 5: Association Management Cockpit (Back-Office)

* **Application Kanban Board:**
  * Column view by application state to move applications, add private screening notes and trigger automatic updates to the adopter.
* **Integrated Animal Management:**
  * Animal registration and editing, with the state model described in [Section 6](#6-state-models).
* **Volunteer and Roster Hub:**
  * Global view of attendance and active sign-ups per day and shift.
* **Foster-to-Adopt Settings:**
  * Approve/decline trial requests, define the trial fee and view payment status.

---

## 6. State Models

> **Proposal — pending team validation.** The original vision mixed temporary fostering and the adoption trial in a single animal state. The proposal below separates them.
>
> **Alternatives and trade-offs (animal model):**
>
> | Option | Cohesion | Coupling | Testability | Maintainability |
> | :--- | :--- | :--- | :--- | :--- |
> | **A. Single state machine** (original: `Available → In Process → In Foster/Trial → Adopted`) | Low — one state mixes "where the animal is" with "how far its adoption has gone" | Fostering and adoption rules depend on each other | Fewer states, but cannot express "fostered and still available" | Every new location or process step multiplies the number of states |
> | **B. Two independent dimensions** (adoption status + location, proposed below) | High — each dimension has a single responsibility | Fostering and adoption evolve independently | Each state machine can be tested in isolation; combinations need a few extra tests | New locations do not affect the adoption flow |
>
> Both options are compatible with the **State** pattern required by `AGENTS.md`; option B implies two state objects in the `Animal` aggregate instead of one.

### 6.1 Animal

**Adoption status:**

```
                ┌──────────────────────────────────────────┐
                ▼                                          │ (application rejected/withdrawn,
  Available ──► Reserved ──► In Trial (Foster-to-Adopt) ──► Adopted
      ▲            │                │                       │
      │            └────────────────┴── return ─────────────┘ (return → Available)
      │
  Unavailable (e.g., medical treatment)            Deceased (terminal)
```

* `Available`: can receive applications.
* `Reserved`: an application has been accepted for this animal; other applications are put on hold.
* `In Trial`: Foster-to-Adopt period in progress.
* `Adopted`: adoption completed. A later return moves the animal back to `Available`.
* `Unavailable`: temporarily not adoptable (medical, behavioral).

**Location** (independent of adoption status): `At Shelter` | `In Foster Home`. A fostered animal (temporary foster care) can remain `Available` for adoption.

### 6.2 Adoption Application

```
Submitted ──► Screening ──► Interview/Contact ──► [Trial Period] ──► Completed
    │             │                │                    │
    └─────────────┴────────────────┴────────────────────┴──► Rejected | Withdrawn | Closed (animal adopted by another applicant)
```

* `Trial Period` is optional (requested by the adopter, approved by the association, may require payment of the trial fee).
* Every transition triggers an email and in-app notification to the applicant.

---

## 7. Suggested Prioritization for the Agile Process (MVP vs. Evolution)

To ensure success within a 4-Sprint schedule (8 weeks of development), the broad vision is split into operational layers:

| Feature / Idea | MVP Priority (Sprints 1 to 4) | Next Increment / Future |
| :--- | :---: | :---: |
| **Authentication, Roles & Association Registration** | Essential (Sprint 1) | Advanced association verification |
| **Public Catalog with Filters** | Essential (Sprint 1) | — |
| **Back-Office: Animal & Status Management** | Essential (Sprint 1-2) | — |
| **Application Flow with Adoption Tracker (email + in-app)** | Essential (Sprint 2-3) | — |
| **Compatibility Algorithm / Quiz** | Differentiating Value (Sprint 3) | Swipe-based ("Tinder-style") discovery |
| **Foster-to-Adopt (optional trial + Stripe test payment)** | Differentiating Value (Sprint 4) | Extension to Multiple Foster Homes |
| **Walk Scheduling (registered volunteers)** | Optional (If Sprint 4 has slack) | Points Gamification |
| **Wishlist with Pledges & Confirmation** | Optional (Sprint 4 / Extension) | Integration with Local Stores |
| **Parametric Foster Family Engine** | Essential (Sprint to be defined) | — |
| **Operational Roster (registered volunteers)** | Essential (Sprint to be defined) | — |
| **Volunteer & Roster Hub (Back-Office)** | Essential (Sprint to be defined) | — |

---

## 8. Out of Scope (MVP)

* Real (non-test) payment processing; Stripe is used in test mode only.
* Online monetary donations; the wishlist handles in-kind donations only.
* Detailed design of the Matchmaker algorithm (deferred, see Pillar 1).
* Native mobile applications.
* Legal adoption contracts and veterinary record management.

---

## 9. Non-Functional Requirements & Constraints

* **Data protection (GDPR):** applications contain personal and housing data; access is restricted to the applicant and the staff of the association concerned.
* **Data isolation:** each association only accesses its own data (see Section 4).
* **Responsive web:** usable on mobile browsers.
* **Accessibility:** follow basic web accessibility guidelines.
* **Notifications:** email and in-app.
* **Payments:** Stripe in test mode; no real card data is processed.

---

## 10. Impact and Success Metrics

> The original metrics (zero unanswered applications, reduced return rates, volunteer growth) depend on real-world usage over long periods and cannot be measured within the project's timeframe. The metrics below can be verified during development and usability testing.

1. **Follow-Up Transparency:** 100% of application state changes generate a notification to the applicant; average time to first state change is visible to the association.
2. **Application Effort:** an applicant can find an animal and submit an application in a limited number of steps, validated in usability tests.
3. **Task Success:** association staff can complete core tasks (register an animal, move an application, approve a trial) in usability tests without assistance.
4. **Decision Quality (long term):** reduced return rates through the combination of the *Matchmaker* and the *Foster-to-Adopt* period — tracked by recording returns in the platform.
5. **Community Engagement (long term):** number of registered volunteers and fulfilled walk/socialization slots per association.
