-- ============================================================================
-- Patas - Plataforma Colaborativa de Proteção Animal
-- Baseline Database Schema, Full-Text Search (GIN) & Triggers (PostgreSQL 16)
-- ============================================================================

------------------------------------------------------------
-- SCHEMA CREATION
------------------------------------------------------------
DROP SCHEMA IF EXISTS patas CASCADE;
CREATE SCHEMA patas;
SET search_path TO patas;

------------------------------------------------------------
-- ENUMERATED TYPES
------------------------------------------------------------
CREATE TYPE verification_status AS ENUM (
    'pending',
    'verified',
    'rejected'
);

CREATE TYPE activity_level AS ENUM (
    'low',
    'moderate',
    'high'
);

CREATE TYPE housing_type AS ENUM (
    'apartment',
    'house_no_yard',
    'house_with_yard'
);

CREATE TYPE time_away AS ENUM (
    'few_hours',
    'half_day',
    'most_of_day'
);

CREATE TYPE species AS ENUM (
    'dog',
    'cat',
    'other'
);

CREATE TYPE adoption_status AS ENUM (
    'available',
    'reserved',
    'in_trial',
    'adopted',
    'unavailable'
);

CREATE TYPE animal_location AS ENUM (
    'at_shelter',
    'in_foster_home'
);

CREATE TYPE application_status AS ENUM (
    'submitted',
    'screening',
    'interview',
    'trial_period',
    'completed',
    'rejected',
    'withdrawn',
    'closed'
);

CREATE TYPE pledge_status AS ENUM (
    'pledged',
    'confirmed',
    'released'
);

------------------------------------------------------------
-- TABLES AND CONSTRAINTS
------------------------------------------------------------

-- 1. ASSOCIATIONS (Aggregate Root: Organization)
CREATE TABLE associations (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    verification_status verification_status NOT NULL DEFAULT 'pending',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT associations_pkey PRIMARY KEY (id),
    CONSTRAINT associations_name_not_blank_check CHECK (char_length(btrim(name)) > 0)
);

COMMENT ON TABLE associations IS
    'Animal protection organization that manages animals, applications, and wishlists.';
COMMENT ON COLUMN associations.name IS 'Public display name of the association.';
COMMENT ON COLUMN associations.verification_status IS
    'Platform Administrator verification before the association may publish animals.';

-- 2. USERS (Aggregate Root: Citizen)
CREATE TABLE users (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    email text UNIQUE NOT NULL,
    is_platform_admin boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_name_not_blank_check CHECK (char_length(btrim(name)) > 0),
    CONSTRAINT users_email_not_blank_check CHECK (char_length(btrim(email)) > 0),
    CONSTRAINT users_email_format_check CHECK (position('@' in email) > 1)
);

COMMENT ON TABLE users IS
    'Registered citizen. Visitor is unauthenticated and has no row.';
COMMENT ON COLUMN users.email IS
    'Unique login identity; case-insensitive lookups supported via idx_users_email_lower.';
COMMENT ON COLUMN users.is_platform_admin IS
    'Platform Administrator: verifies associations and moderates globally.';

-- 3. MATCHMAKER PROFILES (Lifestyle Questionnaire: 1-to-1 extension)
CREATE TABLE matchmaker_profiles (
    user_id uuid NOT NULL,
    activity activity_level NOT NULL,
    housing housing_type NOT NULL,
    time_away time_away NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT matchmaker_profiles_pkey PRIMARY KEY (user_id),
    CONSTRAINT matchmaker_profiles_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

COMMENT ON TABLE matchmaker_profiles IS
    'Optional lifestyle questionnaire used by the Matchmaker. updated_at tracks preference freshness.';

-- 4. VOLUNTEER PROFILES (Role profile: immutable preference tags)
CREATE TABLE volunteer_profiles (
    user_id uuid NOT NULL,
    preferences text[] NOT NULL DEFAULT ARRAY[]::text[],
    CONSTRAINT volunteer_profiles_pkey PRIMARY KEY (user_id),
    CONSTRAINT volunteer_profiles_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT volunteer_profiles_preferences_not_blank_check
        CHECK (
            NOT EXISTS (
                SELECT 1
                FROM unnest(preferences) AS preference
                WHERE char_length(btrim(preference)) = 0
            )
        )
);

COMMENT ON TABLE volunteer_profiles IS
    'Role: Citizen who offers time for walks, socialization, or operational shifts.';

-- 5. FOSTER PROFILES (Role profile: home conditions)
CREATE TABLE foster_profiles (
    user_id uuid NOT NULL,
    housing_conditions text NOT NULL,
    CONSTRAINT foster_profiles_pkey PRIMARY KEY (user_id),
    CONSTRAINT foster_profiles_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT foster_profiles_housing_conditions_not_blank_check
        CHECK (char_length(btrim(housing_conditions)) > 0)
);

COMMENT ON TABLE foster_profiles IS
    'Role: Citizen registered as a Foster Family for temporary housing.';

-- 6. ASSOCIATION MEMBERSHIPS (Staff Join Table)
CREATE TABLE association_memberships (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    association_id uuid NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT association_memberships_pkey PRIMARY KEY (id),
    CONSTRAINT association_memberships_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT association_memberships_association_id_fkey
        FOREIGN KEY (association_id) REFERENCES associations (id) ON DELETE RESTRICT,
    CONSTRAINT association_memberships_user_id_association_id_key
        UNIQUE (user_id, association_id)
);

COMMENT ON TABLE association_memberships IS
    'Links a User to an Association as Staff. created_at marks when membership began.';

-- 7. ANIMALS (Aggregate Root: Pet under shelter care)
CREATE TABLE animals (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    association_id uuid NOT NULL,
    name text NOT NULL,
    species species NOT NULL,
    description text,
    adoption_status adoption_status NOT NULL DEFAULT 'available',
    location animal_location NOT NULL DEFAULT 'at_shelter',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT animals_pkey PRIMARY KEY (id),
    CONSTRAINT animals_association_id_fkey
        FOREIGN KEY (association_id) REFERENCES associations (id) ON DELETE RESTRICT,
    CONSTRAINT animals_name_not_blank_check CHECK (char_length(btrim(name)) > 0)
);

COMMENT ON TABLE animals IS
    'Pet under the care of an Association. description provides free-form notes parsed for Matchmaker.';

-- 8. ADOPTION APPLICATIONS (Aggregate Root: Formal adoption process)
CREATE TABLE adoption_applications (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    applicant_id uuid NOT NULL,
    animal_id uuid NOT NULL,
    status application_status NOT NULL DEFAULT 'submitted',
    submitted_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT adoption_applications_pkey PRIMARY KEY (id),
    CONSTRAINT adoption_applications_applicant_id_fkey
        FOREIGN KEY (applicant_id) REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT adoption_applications_animal_id_fkey
        FOREIGN KEY (animal_id) REFERENCES animals (id) ON DELETE RESTRICT
);

COMMENT ON TABLE adoption_applications IS
    'Formal adoption process. Lifecycle active uniqueness enforced via partial index.';

-- 9. TRIAL PERIODS (Foster-to-Adopt window inside Application)
CREATE TABLE trial_periods (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    application_id uuid NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    fee_amount numeric(12, 2) NOT NULL DEFAULT 0,
    is_fee_paid boolean NOT NULL DEFAULT false,
    CONSTRAINT trial_periods_pkey PRIMARY KEY (id),
    CONSTRAINT trial_periods_application_id_fkey
        FOREIGN KEY (application_id) REFERENCES adoption_applications (id) ON DELETE CASCADE,
    CONSTRAINT trial_periods_application_id_key UNIQUE (application_id),
    CONSTRAINT trial_periods_dates_check CHECK (end_date >= start_date),
    CONSTRAINT trial_periods_fee_amount_non_negative_check CHECK (fee_amount >= 0)
);

COMMENT ON TABLE trial_periods IS
    'Foster-to-Adopt trial window. Timeframe is explicitly defined by start_date and end_date.';

-- 10. TRIAL CHECK-INS (Append-only Follow-up Log)
CREATE TABLE trial_check_ins (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    trial_period_id uuid NOT NULL,
    note text NOT NULL,
    logged_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT trial_check_ins_pkey PRIMARY KEY (id),
    CONSTRAINT trial_check_ins_trial_period_id_fkey
        FOREIGN KEY (trial_period_id) REFERENCES trial_periods (id) ON DELETE CASCADE,
    CONSTRAINT trial_check_ins_note_not_blank_check CHECK (char_length(btrim(note)) > 0)
);

COMMENT ON TABLE trial_check_ins IS
    'Append-only follow-up notes logged during a trial period (logged_at).';

-- 11. WISHLIST ITEMS (Aggregate Root: Material need)
CREATE TABLE wishlist_items (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    association_id uuid NOT NULL,
    item_name text NOT NULL,
    needed_quantity integer NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT wishlist_items_pkey PRIMARY KEY (id),
    CONSTRAINT wishlist_items_association_id_fkey
        FOREIGN KEY (association_id) REFERENCES associations (id) ON DELETE RESTRICT,
    CONSTRAINT wishlist_items_item_name_not_blank_check
        CHECK (char_length(btrim(item_name)) > 0),
    CONSTRAINT wishlist_items_needed_quantity_positive_check
        CHECK (needed_quantity > 0)
);

COMMENT ON TABLE wishlist_items IS
    'In-kind need published by an Association. updated_at reflects quantity updates upon receipts.';

-- 12. PLEDGES (Commitment to provide wishlist items)
CREATE TABLE pledges (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    wishlist_item_id uuid NOT NULL,
    user_id uuid NOT NULL,
    quantity integer NOT NULL,
    status pledge_status NOT NULL DEFAULT 'pledged',
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT pledges_pkey PRIMARY KEY (id),
    CONSTRAINT pledges_wishlist_item_id_fkey
        FOREIGN KEY (wishlist_item_id) REFERENCES wishlist_items (id) ON DELETE CASCADE,
    CONSTRAINT pledges_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT pledges_quantity_positive_check CHECK (quantity > 0)
);

COMMENT ON TABLE pledges IS
    'Citizen commitment to provide a quantity of an item. created_at tracks commitment timestamp.';

-- * ====================================================
-- * Index Creation
-- * ====================================================
-- Note: Foreign key indexes are managed automatically by the ORM/Alembic layer.

-- 1. Case-insensitive fast lookup for authentication
CREATE UNIQUE INDEX idx_users_email_lower
    ON users USING btree (lower(email));

-- 2. Domain Lifecycle Invariant: At most 1 ACTIVE application per applicant per animal
CREATE UNIQUE INDEX idx_adoption_applications_one_open_per_applicant_animal
    ON adoption_applications (applicant_id, animal_id)
    WHERE status NOT IN ('completed', 'rejected', 'withdrawn', 'closed');

-- * ====================================================
-- * Full Text Search Index Creation (GIN)
-- * ====================================================

ALTER TABLE animals
ADD COLUMN tsvectors TSVECTOR;

-- Optimized search trigger: recalculates tsvectors ONLY if name, species, or description changes.
-- Normal status/location/timestamp transitions do not trigger GIN re-indexing.
CREATE OR REPLACE FUNCTION animal_search_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.tsvectors = (
            setweight(to_tsvector('portuguese', COALESCE(NEW.name, '')), 'A') ||
            setweight(to_tsvector('portuguese', COALESCE(NEW.species::text, '')), 'B') ||
            setweight(to_tsvector('portuguese', COALESCE(NEW.description, '')), 'C')
        );
    ELSIF TG_OP = 'UPDATE' THEN
        IF (NEW.name <> OLD.name OR NEW.species <> OLD.species OR NEW.description IS DISTINCT FROM OLD.description) THEN
            NEW.tsvectors = (
                setweight(to_tsvector('portuguese', COALESCE(NEW.name, '')), 'A') ||
                setweight(to_tsvector('portuguese', COALESCE(NEW.species::text, '')), 'B') ||
                setweight(to_tsvector('portuguese', COALESCE(NEW.description, '')), 'C')
            );
        END IF;
    END IF;
    RETURN NEW;
END $$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_animal_search_update
BEFORE INSERT OR UPDATE ON animals
FOR EACH ROW
EXECUTE FUNCTION animal_search_update();

CREATE INDEX idx_animals_search ON animals USING GIN (tsvectors);

-- * ====================================================
-- * Triggers (Selective updated_at Maintenance)
-- * ====================================================

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_associations_set_updated_at
    BEFORE UPDATE ON associations
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_users_set_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_matchmaker_profiles_set_updated_at
    BEFORE UPDATE ON matchmaker_profiles
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_animals_set_updated_at
    BEFORE UPDATE ON animals
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_adoption_applications_set_updated_at
    BEFORE UPDATE ON adoption_applications
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trigger_wishlist_items_set_updated_at
    BEFORE UPDATE ON wishlist_items
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();
