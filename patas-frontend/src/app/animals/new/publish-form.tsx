"use client";

import { useActionState } from "react";

import { publishAnimalAction, type PublishState } from "./actions";

const initialState: PublishState = { error: null };

export function PublishForm() {
  const [state, formAction, pending] = useActionState(
    publishAnimalAction,
    initialState,
  );

  return (
    <form action={formAction} className="flex flex-col gap-4">
      <label className="flex flex-col gap-1 text-sm">
        Name
        <input
          name="name"
          required
          className="rounded border border-neutral-400 px-3 py-2"
        />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Species
        <select
          name="species"
          defaultValue="dog"
          className="rounded border border-neutral-400 px-3 py-2"
        >
          <option value="dog">Dog</option>
          <option value="cat">Cat</option>
          <option value="other">Other</option>
        </select>
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Age in months (optional)
        <input
          name="age_in_months"
          type="number"
          min={0}
          step={1}
          className="rounded border border-neutral-400 px-3 py-2"
        />
      </label>
      {state.error && (
        <p role="alert" className="text-sm text-red-700">
          {state.error}
        </p>
      )}
      <button
        type="submit"
        disabled={pending}
        className="rounded bg-neutral-900 px-3 py-2 text-white disabled:opacity-50"
      >
        {pending ? "Publishing…" : "Publish"}
      </button>
    </form>
  );
}
