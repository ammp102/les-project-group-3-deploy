# Definition of Done

> **Document:** Team-wide Definition of Done (DoD)
> **Context:** MESW, Software Engineering Laboratory (2026/27)
> **Product:** Patas, Collaborative Animal Welfare Platform

A user story is **done** when every item below is satisfied and the evidence is linked in the pull request (see `.github/pull_request_template.md`). Once a story is done it is **not reopened or re-reviewed**: the evidence is the proof.

If an item is not met, the story is not done. There is no partial credit and no "done except for...". If an item cannot apply to a story, the PR must say which item and why, and the reviewer must agree.

---

## Before (entry gate)

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 1 | The story has **testable acceptance criteria**, written as concrete examples. | Criteria listed in the story or PR. |
| 2 | Any **business logic** (triage rules, validations, flows) was **agreed with the team before implementation** . | Link to the agreed decision (doc, ADR or recorded message). |

## Automatic

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 3 | **Automatic tests were written**, that validate the functionality, the types and quantity are up to the programmer. | CI run. |
| 4 | **Linters and static analysis pass with no warnings**, and no rule is suppressed without a written technical justification . | CI run. |
| 5 | **CI is fully green**: specification tests and linters . | CI run link. |

## Human

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 6 | Every **design decision** introduced has a justification of the concrete problem it solves . | Justification in the PR or documentation. |
| 7 | Major **structural decisions** (patterns adopted, aggregate design, API contracts, entity models) are documented. | Link to the documentation. |
| 8 | **A teammate other than the author tested manually the full functionality** of the story. A line-by-line code review is **not** required. This is to assure that all team members know what features are being done. | Approval recorded in the PR or ADR. |

## Delivery

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 9 | The branch has an **incremental commit history**. No single massive commit . | Commit log. |
| 10 | The story **runs on the `iter-N` tag** with **real data and real persistence**. | Short demo steps that someone else can follow. |

---

## Notes

* **What review means here.** Review is about decisions and behavior (business rules, domain logic, architecture), not about reading every line. Review does not replace understanding, any team member may be asked to defend the code in person.
* **Changing this document.** The DoD is a team agreement. Any change needs the whole team's agreement, and the change itself goes through a PR.
