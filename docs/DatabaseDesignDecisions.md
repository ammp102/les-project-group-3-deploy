# Architecture Decision Record: Database Design & Baseline Schema

> **Documento:** Registo de Decisões de Arquitetura e Modelação Relacional  
> **Contexto:** MESW — Laboratório de Engenharia de Software (2026/27)  
> **Produto:** Patas — Plataforma Colaborativa de Proteção Animal  
> **Ficheiro Relacionado:** [`database/create.sql`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/database/create.sql)

---

## 1. Contexto e Motivação

O projeto Patas iniciou a definição do seu modelo de domínio em [`docs/DomainModel.md`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/docs/DomainModel.md) e das máquinas de estados de ciclo de vida em [`docs/StateMachines.md`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/docs/StateMachines.md). 
Para suportar o desenvolvimento da API backend (FastAPI / SQLAlchemy / Alembic) e manter conformidade com as diretrizes de governança em [`AGENTS.md`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/AGENTS.md), foi necessário consolidar, otimizar e auditar criticamente o esquema inicial da base de dados relacional (PostgreSQL 16).

Este documento formaliza as decisões arquiteturais tomadas colaborativamente pela equipa nesta sessão.

---

## 2. Decisões Arquiteturais

### Decisão 1: Reposicionamento e Consolidação dos Scripts SQL
* **Decisão:** A pasta `database/` foi movida para fora do backend, passando a residir na raiz do repositório (`/database`), e os scripts anteriormente fragmentados (`schema.sql`, `indexes.sql`, `triggers.sql`) foram unificados num único ficheiro canónico e auto-suficiente: [`database/create.sql`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/database/create.sql).
* **Justificação:**
  * Desacopla a especificação relacional pura da implementação do framework de backend.
  * Adota o padrão de referência académica (LBAW/FEUP), permitindo criar o esquema completo de ponta a ponta numa única execução sequencial.
  * Isola todas as tabelas e tipos no schema dedicado `patas` (`DROP SCHEMA IF EXISTS patas CASCADE; CREATE SCHEMA patas; SET search_path TO patas;`), garantindo *namespacing* limpo e compatibilidade futura com o Alembic (`version_table_schema = 'patas'`).

---

### Decisão 2: Política Estrita de Timestamps (`created_at` e `updated_at`)
* **Decisão:** Limitar a presença de `created_at` e `updated_at` exclusivamente a entidades que possuem valor funcional real de ciclo de vida ou auditoria.
* **Mapeamento:**
  * **Mantêm `created_at` e `updated_at`:**
    * `associations`: Criação e atualizações de dados institucionais / verificação.
    * `users`: Registo de conta e atualização de perfil.
    * `animals`: Entrada no abrigo e transições de estado / adoção.
    * `wishlist_items`: Criação da necessidade e atualização de quantidades pendentes.
  * **Casos Especiais:**
    * `adoption_applications`: Usa `submitted_at` (linguagem ubíqua de domínio para o momento de submissão) e `updated_at` para transições na máquina de estados.
    * `matchmaker_profiles`: Mantém apenas `updated_at` para aferir a "frescura" das preferências no cálculo de afinidade.
    * `pledges`: Mantém apenas `created_at` (data do compromisso de doação).
    * `association_memberships`: Mantém apenas `created_at` (registo estático de adesão ao staff; não tem atributos editáveis).
    * `trial_check_ins`: Mantém apenas `logged_at` (tabela de notas *append-only* imutável).
  * **Sem Timestamps:**
    * `trial_periods`: As datas são expressas explicitamente por `start_date` e `end_date`.
    * `volunteer_profiles` e `foster_profiles`: Perfis acessórios 1:1 acoplados ao ciclo de vida do `User`.
* **Impacto:** Redução de **11 triggers** para apenas **6 triggers** `BEFORE UPDATE`, eliminando processamento desnecessário no SGBD.

---

### Decisão 3: Estratégia de Índices e Otimização HOT (Heap-Only Tuples)
* **Decisão:** Remover índices em colunas mutáveis e delegar índices de chaves estrangeiras ao ORM / Alembic.
* **Justificação Técnica:**
  * **Preservação de HOT Updates:** No PostgreSQL, atualizar uma coluna indexada força a reescrita do índice e impede *Heap-Only Tuples*. Ao eliminar índices em colunas como `adoption_status`, `location`, `status` e `pledge_status`, **as transições de estado dos animais e candidaturas produzem HOT updates com zero escritas em índices secundários**.
  * **Omissão de FK Indexes Manuais:** O Alembic / SQLAlchemy gerará índices relacionais em chaves estrangeiras durante a geração de modelos, evitando duplicações no script baseline.
  * **Unicidade Case-Insensitive:** Mantido o índice funcional `idx_users_email_lower` (`UNIQUE ON users (lower(email))`) para suportar autenticação rápida e blindar a regra de negócio contra duplicados por maiúsculas/minúsculas.

---

### Decisão 4: Regra de Unicidade em Candidaturas de Adoção
* **Decisão:** Implementação de um **Índice Parcial Único** em `adoption_applications`:
  ```sql
  CREATE UNIQUE INDEX idx_adoption_applications_one_open_per_applicant_animal
      ON adoption_applications (applicant_id, animal_id)
      WHERE status NOT IN ('completed', 'rejected', 'withdrawn', 'closed');
  ```
* **Trade-off Analisado:**
  * Uma restrição de tabela `UNIQUE (applicant_id, animal_id)` impediria para sempre um cidadão de submeter uma nova candidatura para o mesmo animal, mesmo após rejeição ou desistência passada.
  * O índice parcial cumpre a invariante de domínio: **no máximo 1 candidatura ativa em simultâneo**, permitindo novas tentativas caso o processo anterior tenha terminado.

---

### Decisão 5: Full-Text Search (GIN) e Suporte ao Matchmaker
* **Decisão:** Adicionar a coluna `description text` a `animals` e criar um índice `GIN` para pesquisa textual vetorial em português.
* **Implementação:**
  * Coluna `tsvectors` indexada com pesos: Nome (A), Espécie (B) e Descrição (C).
  * **Trigger Otimizado contra Write Amplification:**
    ```sql
    IF (NEW.name <> OLD.name OR NEW.species <> OLD.species OR NEW.description IS DISTINCT FROM OLD.description) THEN
        NEW.tsvectors = ...;
    END IF;
    ```
    Atualizações operacionais em `adoption_status`, `location` ou `updated_at` **não recalculam `tsvectors` nem tocam no índice GIN**.
* **Alinhamento com o Matchmaker:**
  * A coluna livre `description` acolhe notas comportamentais do abrigo sem exigir dezenas de colunas esparsas e rígidas na base de dados.
  * Uma camada aplicacional de serviço no backend (*Write-Time Parser* / NLP) processará esse texto para alimentar os algoritmos de afinidade do *Matchmaker*.

---

### Decisão 6: Governança de Membros e Tipos de Dados
* **Membros de Staff (`association_memberships`):** Mantida como relação pura N:M sem coluna de cargo (`role`). Todos os membros de uma associação partilham dos mesmos privilégios para o âmbito do MVP.
* **Tipos Enumerados (`ENUM`):** Preservados como tipos nativos PostgreSQL (`CREATE TYPE ... AS ENUM`) para garantir integridade forte ao nível do catálogo de dados do motor relacional.

---

## 3. Estado Atual dos Ficheiros

* Script mestre executável: [`database/create.sql`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/database/create.sql)
* Documento conceitual de domínio: [`docs/DomainModel.md`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/docs/DomainModel.md)
* Ciclo de vida e máquinas de estados: [`docs/StateMachines.md`](file:///c:/Users/joaop/Desktop/MESW/LES/LES-C/docs/StateMachines.md)
