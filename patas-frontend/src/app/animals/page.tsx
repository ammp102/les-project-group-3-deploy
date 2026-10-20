import type { Metadata } from "next";
import { headers } from "next/headers";
import Link from "next/link";
import { Suspense } from "react";

import { auth } from "@/lib/auth";
import { backendUrl } from "@/lib/backend";

export const metadata: Metadata = {
  title: "Animals | Patas",
};

type Animal = {
  id: string;
  species: string;
  name: string;
  owner_id: string;
  age_in_months: number | null;
  adoption_status: string;
};

function isAnimal(value: unknown): value is Animal {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const animal = value as Record<string, unknown>;
  return (
    typeof animal.id === "string" &&
    typeof animal.species === "string" &&
    typeof animal.name === "string" &&
    typeof animal.owner_id === "string" &&
    (animal.age_in_months === null || typeof animal.age_in_months === "number") &&
    typeof animal.adoption_status === "string"
  );
}

async function getAnimals(): Promise<Animal[]> {
  const response = await fetch(`${backendUrl()}/animals`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Unable to load animals: backend returned ${response.status}`);
  }

  const payload: unknown = await response.json();
  if (!Array.isArray(payload) || !payload.every(isAnimal)) {
    throw new Error("Unable to load animals: backend returned invalid data");
  }

  return payload;
}

async function AnimalList() {
  const animals = await getAnimals();

  if (animals.length === 0) {
    return <p>No animals are available yet.</p>;
  }

  return (
    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {animals.map((animal) => (
        <li
          key={animal.id}
          className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"
        >
          <p className="text-sm font-medium text-emerald-700">
            {animal.species} · {animal.adoption_status}
          </p>
          <h2 className="mt-2 text-xl font-semibold text-neutral-900">
            {animal.name}
          </h2>
          {animal.age_in_months !== null && (
            <p className="mt-1 text-sm text-neutral-600">
              {animal.age_in_months} months
            </p>
          )}
        </li>
      ))}
    </ul>
  );
}

// Visitors see the catalog too (AC5); only a logged-in user gets the button.
async function PublishLink() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    return (
      <p className="text-sm text-neutral-600">
        <Link href="/login" className="underline">
          Log in
        </Link>{" "}
        to publish an animal.
      </p>
    );
  }
  return (
    <Link
      href="/animals/new"
      className="self-start rounded bg-neutral-900 px-3 py-2 text-sm text-white"
    >
      Publish an animal
    </Link>
  );
}

export default function AnimalsPage() {
  return (
    <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-8 px-4 py-12">
      <header>
        <p className="text-sm font-medium uppercase tracking-wide text-emerald-700">
          Patas
        </p>
        <h1 className="mt-2 text-3xl font-semibold">Animals</h1>
        <p className="mt-2 text-neutral-600">
          Meet the animals waiting for care.
        </p>
      </header>
      <Suspense fallback={null}>
        <PublishLink />
      </Suspense>
      <Suspense fallback={<p>Loading animals…</p>}>
        <AnimalList />
      </Suspense>
    </main>
  );
}
