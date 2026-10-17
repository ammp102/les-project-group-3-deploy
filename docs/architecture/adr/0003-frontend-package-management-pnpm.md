# ADR 0003: Frontend Package Management with pnpm

## Status
Accepted

## Context
Our backend infrastructure leverages Astral `uv` for deterministic, sub-second dependency resolution. The Next.js frontend initially utilized standard `npm`. During Docker container builds and Continuous Integration (CI) pipeline runs, `npm ci` proved inefficient as it repeatedly downloads and extracts tarballs, bloating build minutes. Furthermore, `npm` utilizes a flat `node_modules` directory structure, which introduces the risk of "phantom dependencies" (where code can inadvertently import transient dependencies not explicitly declared in `package.json`).

## Decision
We migrated the frontend package manager from `npm` to `pnpm`.
1. **Content-Addressable Store:** Packages are cached globally and hard-linked into `node_modules`, resulting in near-instantaneous installations after the first cache.
2. **Strict Dependency Resolution:** `pnpm` enforces a non-flat `node_modules` topology. If a package is not in `package.json`, Next.js/TypeScript will immediately throw an error, ensuring environment parity.
3. **CI/CD Integration:** We integrated `pnpm/action-setup` in our GitHub Actions pipeline to cache the virtual store across CI runs.
4. **Security Policy Enforcement:** We leverage `pnpm-workspace.yaml` to explicitly whitelist necessary build scripts (e.g., `unrs-resolver`), adhering to secure supply chain practices.

## Consequences
* **Positive:** Frontend CI steps and multi-stage Docker builds are drastically faster; zero risk of phantom dependencies; aligns frontend tooling philosophy with the backend (`uv`).
* **Negative:** Required explicit `pnpm approve-builds` configuration to authorize required sub-dependency post-install scripts.
