# CLAIM: Iteration 0

Group 3, Patas. Vertical prototype: publish an animal and see it in the catalog.
Every link below points at the tag `iter-0`, so nothing needs hunting.

## Links

| Item | Link |
| :-- | :-- |
| Tag | [iter-0](https://github.com/MESW-LES-2627/les-project-group-3/tree/iter-0) |
| Compare with the last tag | First iteration, there is no earlier tag. [Whole history, root commit to `iter-0`](https://github.com/MESW-LES-2627/les-project-group-3/compare/d351ee989d0994d681ae3ee7a82112b6d49183b1...iter-0) |
| Production | TODO: production URL |
| Staging | TODO: staging URL, or "none" and why |
| Pipeline | TODO: URL of the green CI run on the tagged commit. Workflow: [ci.yml](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/.github/workflows/ci.yml) |
| MVP | [MVP Vision](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/product/MVPVision.md) |
| Vision | [Vision](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/product/Vision.md) |
| Stories in this increment | [Acceptance criteria AC1 to AC5](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/integrations/vertical-prototype/VerticalPrototypeSpec.md#22-acceptance-criteria-dod-1) |
| How to run the tests | [Running tests and checks](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/README.md#running-tests-and-checks) |
| Retrospective | [Retrospective](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/iterations/0/CLAIM.md#retrospective) |
| AI log | [AI log](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/iterations/0/CLAIM.md#ai-log) |

## What runs on this tag

The slice of [the vertical prototype spec](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/integrations/vertical-prototype/VerticalPrototypeSpec.md):
a person registers and logs in, publishes an animal, and the animal appears in the
public catalog, read from PostgreSQL with the publisher recorded as owner.

| Story | Criterion |
| :-- | :-- |
| AC1 | A logged-in user publishes a valid animal; it is in `GET /animals` with that user as owner and status `available`. |
| AC2 | A request without a valid JWT is rejected with 401 and nothing is stored. |
| AC3 | An invalid animal (blank name, negative age) is rejected by the domain and nothing is stored. |
| AC4 | The first authenticated call creates the user's row; a second call does not duplicate it. |
| AC5 | The catalog is public: a visitor without login sees the published animals. |

Demo steps someone else can follow: [README, publish an animal and see it in the catalog](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/README.md#demo-publish-an-animal-and-see-it-in-the-catalog).

## Team artefacts

| Artefact | Link |
| :-- | :-- |
| Architecture Decision Records 0001 to 0006 | [adr/](https://github.com/MESW-LES-2627/les-project-group-3/tree/iter-0/docs/architecture/adr) |
| Definition of Done | [DEFINITION_OF_DONE.md](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/process/DEFINITION_OF_DONE.md) |
| Pull request template | [pull_request_template.md](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/.github/pull_request_template.md) |
| Engineering rules and AI guidelines | [AGENTS.md](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/AGENTS.md) |
| Domain Model | [DomainModel.md](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/domain/DomainModel.md) |
| State Machines | [StateMachines.md](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/domain/StateMachines.md) |
| Glossary | [Glossary.md](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/domain/Glossary.md) |

## Known gaps

* The domain documents and `database/create.sql` still describe the full Vision
  (associations, fostering). The MVP changes are listed in
  [MVP Vision §13](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/docs/product/MVPVision.md#13-impact-on-existing-documents).

## Retrospective

TODO: the team writes this section.

## AI log

Failures of the AI agent that needed human intervention (AGENTS.md §1).

| Date | Who | What the AI got wrong | How it was caught | Fix |
| :-- | :-- | :-- | :-- | :-- |
| 2026-10-17 | frutastontas | Assumed that an invalid enum value sent through asyncpg surfaces as SQLAlchemy `DataError`. It surfaces as the generic `DBAPIError`. | Running the test; it failed. | Test now expects `DBAPIError` and matches the reason ([`test_animals_migration.py`](https://github.com/MESW-LES-2627/les-project-group-3/blob/iter-0/patas-backend/tests/test_animals_migration.py), commit `29336ed`). |
| TODO | TODO | TODO: entries from the other members | | |
