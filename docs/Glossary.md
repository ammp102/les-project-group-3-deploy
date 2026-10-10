# Domain Glossary (Ubiquitous Language)

This document defines the core terminology for the **Patas** platform. Its purpose is to establish a Ubiquitous Language to be shared across the development team, domain experts, and stakeholders, ensuring that code and communication use the exact same vocabulary.

## 1. Actors & Roles
*   **Visitor:** An unauthenticated user browsing the public catalog, viewing animal profiles, or taking the Matchmaker quiz.
*   **Citizen:** A registered, authenticated user.
*   **Volunteer:** A Citizen who has signed up to offer their time for walks, socialization, or operational shifts at an Association.
*   **Foster Family:** A Citizen who has registered their home availability and physical conditions to provide temporary housing for animals.
*   **Association Staff:** A user linked to a specific Association, responsible for managing its animals, applications, rosters, and wishlists.
*   **Platform Administrator:** A super-user who manages the platform globally, verifying new Associations and moderating content.

## 2. Core Entities & Concepts
*   **Association:** An animal protection organization or shelter that registers on the platform to manage its animals, operations, and adoption processes.
*   **Animal:** A pet (e.g., dog, cat) under the care of an Association, registered in the system with its profile, needs, and medical history.
*   **Adoption Application (Application):** The formal process and documentation submitted by a Citizen to adopt a specific Animal.
*   **Adoption Tracker:** The system module that provides real-time, transparent tracking of an Application's status (timeline) to the Citizen.
*   **Matchmaker:** The optional compatibility system that suggests Animals to Visitors/Citizens based on a lifestyle and routine questionnaire.
*   **Foster-to-Adopt (Trial Period):** An optional phase within the Adoption Application where the Citizen takes the Animal home for a short, agreed-upon period to ensure adaptation before finalizing the legal adoption.
*   **Temporary Fostering:** The act of a Foster Family temporarily housing an Animal (independent of an adoption process).
*   **Operational Roster:** A schedule of shifts managed by an Association for core facility tasks (e.g., feeding, cleaning) that Volunteers can sign up for.
*   **Walk / Socialization Session:** Specific time slots available for Volunteers to spend time with Animals to improve their well-being.
*   **Wishlist:** A reverse marketplace list published by an Association detailing specific in-kind items (goods) they currently need.
*   **Pledge:** A commitment made by a Citizen to provide a specific quantity of an item from an Association's Wishlist. The item remains "pledged" until the Association confirms its physical receipt.

## 3. Animal Lifecycle & States
*   **Adoption Status:** The state dimension representing the animal's progress towards a permanent home.
    *   *Available:* Ready to receive new Adoption Applications.
    *   *Reserved:* An application is progressing favorably; other applications are put on hold.
    *   *In Trial:* Currently in a Foster-to-Adopt trial period.
    *   *Adopted:* The adoption process is finalized.
    *   *Unavailable:* Not ready for adoption (e.g., undergoing medical treatment, behavioral issues).
*   **Location:** The physical whereabouts of the animal (independent of adoption status).
    *   *At Shelter:* Physically located at the Association's facilities.
    *   *In Foster Home:* Physically located at a temporary Foster Family's residence.

## 4. Application Status (States)
*   **Submitted:** Application received by the Association; awaiting review.
*   **Screening:** Association Staff is actively reviewing the application details.
*   **Interview/Contact:** Association Staff is in direct communication with the applicant.
*   **Trial Period:** The Animal is currently with the applicant for a Foster-to-Adopt trial.
*   **Completed:** The adoption is finalized and successful.
*   **Rejected:** The application was declined by the Association.
*   **Withdrawn:** The application was canceled by the Citizen.
*   **Closed:** The application was closed because the Animal was adopted by someone else.
