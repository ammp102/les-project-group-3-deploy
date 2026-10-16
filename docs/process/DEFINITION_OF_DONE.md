# Definition of Done

> **Document:** Team-wide Definition of Done (DoD)
> **Context:** MESW, Software Engineering Laboratory (2026/27)
> **Product:** Patas, Collaborative Animal Welfare Platform
> **Derived from:** `AGENTS.md` §1 to §6

A user story is **done** when every item below is satisfied and the evidence is linked in the pull request (see `.github/pull_request_template.md`). Once a story is done it is **not reopened or re-reviewed**: the evidence is the proof.

If an item is not met, the story is not done. There is no partial credit and no "done except for...". If an item cannot apply to a story, the PR must say which item and why, and the reviewer must agree.

---

## Before (entry gate)

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 1 | The story has **testable acceptance criteria**, written as concrete examples. | Criteria listed in the story or PR. |
| 2 | Any **business logic** (triage rules, validations, flows) was **agreed with the team before implementation** (`AGENTS.md` §6). | Link to the agreed decision (doc, ADR or recorded message). |

## Automatic

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 3 | Each acceptance criterion has a **specification test that can fail on a real regression**, and at least one test runs as a **vertical slice from user entry to persistence**. No vanity tests, no tests that only mock the implementation (`AGENTS.md` §3). | Test names mapped to criteria in the PR. |
| 4 | **Linters and static analysis pass with no warnings**, and no rule is suppressed without a written technical justification (`AGENTS.md` §4). | CI run. |
| 5 | **CI is fully green**: specification tests and linters (`AGENTS.md` §4). | CI run link. |

## Human

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 6 | Every **design pattern** introduced has a one-line justification of the concrete problem it solves. No speculative patterns (`AGENTS.md` §2). | Justification in the PR. |
| 7 | Every **structural decision** (patterns adopted, aggregate design, API contracts, entity models) is documented as an ADR or technical note (`AGENTS.md` §6). | Link to the ADR or note. |
| 8 | **A teammate other than the author approved the business, logic and architecture decisions** of the story. A line-by-line code review is **not** required. | Approval recorded in the PR or ADR. |
| 9 | The author **can explain how the feature works and why it was designed that way**. The reviewer asked **at least one "why" question** and got a satisfactory answer (`AGENTS.md` §1, "The Room Wins"). | Question and answer noted in the PR. |
| 10 | Any AI hallucination, wrong proposal or failure that needed human correction is **flagged for the iteration's `CLAIM.md`** (`AGENTS.md` §1). Write "none" if there was none. | Entry in `CLAIM.md`, or "none" in the PR. |

## Delivery

| # | Criterion | Evidence |
| :-- | :-- | :-- |
| 11 | The branch has an **incremental commit history**. No single massive commit (`AGENTS.md` §5.2, "Friday Dumps"). | Commit log. |
| 12 | The story **runs on the `iter-N` tag** with **real data and real persistence**. No static mockups (`AGENTS.md` §5.1 and §5.4). | Short demo steps that someone else can follow. |

---

## Notes

* **What review means here.** Review is about decisions and behavior (business rules, domain logic, architecture), not about reading every line. The safety net for code correctness is item 3. Review does not replace understanding: item 9 exists because any team member may be asked to defend the code in person.
* **Changing this document.** The DoD is a team agreement. Any change needs the whole team's agreement, and the change itself goes through a PR.
