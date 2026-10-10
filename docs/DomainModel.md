# Conceptual Domain Model

This document outlines the core aggregates, entities, and relationships for the Patas platform, adhering strictly to Object-Oriented principles.

## Core UML Domain Model

```mermaid
classDiagram

    class User {
        <<AggregateRoot>>
        +UUID id
        +String name
        +String email
        +updateMatchmakerProfile()
    }

    class MatchmakerProfile {
        <<Entity>>
        +ActivityLevel activity
        +HousingType housing
        +TimeAway timeAway
    }

    class Role {
        <<Interface>>
    }

    class VolunteerProfile {
        +List preferences
    }

    class FosterProfile {
        +HousingConditions conditions
    }

    class Association {
        <<AggregateRoot>>
        +UUID id
        +String name
        +VerificationStatus status
    }

    class Animal {
        <<AggregateRoot>>
        +UUID id
        +String name
        +Species species
        +AdoptionStatus adoptionStatus
        +Location location
    }

    class AdoptionApplication {
        <<AggregateRoot>>
        +UUID id
        +ApplicationStatus status
        +Date submittedAt
        +approveTrial()
        +completeAdoption()
    }

    class TrialPeriod {
        <<Entity>>
        +Date startDate
        +Date endDate
        +Decimal feeAmount
        +Boolean isFeePaid
        +logCheckIn(note)
    }

    class WishlistItem {
        <<AggregateRoot>>
        +UUID id
        +String itemName
        +int neededQuantity
    }

    class Pledge {
        <<Entity>>
        +int quantity
        +PledgeStatus status
        +confirmReceipt()
    }

    User "1" *-- "0..1" MatchmakerProfile : has
    User "1" *-- "*" Role : acts_as
    Role <|-- VolunteerProfile
    Role <|-- FosterProfile

    Association "1" *-- "*" Animal : manages
    Association "1" *-- "*" WishlistItem : lists
    
    User "1" --> "*" AdoptionApplication : submits
    Animal "1" <-- "*" AdoptionApplication : targets
    
    AdoptionApplication "1" *-- "0..1" TrialPeriod : includes
    
    User "1" --> "*" Pledge : makes
    WishlistItem "1" *-- "*" Pledge : receives
```

## Modeling Decisions & Rationale

1. **Composition over Inheritance for Roles:** 
   A `User` *has* a collection of `Role` objects (like `VolunteerProfile` or `FosterProfile`). This allows a single person to dynamically gain or lose capabilities (e.g., becoming a volunteer for a while, then stopping) without changing their underlying base class.
2. **Matchmaker Profile as an Entity:** 
   The `MatchmakerProfile` is stored as an editable entity tied to the `User`, allowing citizens to update their lifestyle conditions over time to get better animal recommendations.
3. **Trial Period as a Separate Entity:** 
   The `TrialPeriod` is a distinct entity within the `AdoptionApplication` aggregate. Because it is optional, making it a separate object prevents the `AdoptionApplication` from being cluttered with null fields (like `trialStartDate`, `trialFee`) for standard adoptions. It also encapsulates its own specific logic (like logging check-ins and tracking fee payments).
