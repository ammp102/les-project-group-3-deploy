import type { Metadata } from "next";
import { Suspense } from "react";

export const metadata: Metadata = {
  title: "Animals | Patas",
};

type Animal = {
  id: string;
  species: string;
  name: string;
  owner_id: string;
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
    typeof animal.owner_id === "string"
  );
}

async function getAnimals(): Promise<Animal[]> {
  const backendUrl =
    process.env.BACKEND_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    "http://localhost:8000";
  const response = await fetch(`${backendUrl}/animals`, { cache: "no-store" });

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
            {animal.species}
          </p>
          <h2 className="mt-2 text-xl font-semibold text-neutral-900">
            {animal.name}
          </h2>
        </li>
      ))}
    </ul>
  );
}

export default function DashboardPage() {
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
      <Suspense fallback={<p>Loading animals…</p>}>
        <AnimalList />
      </Suspense>
    </main>
  );
}
