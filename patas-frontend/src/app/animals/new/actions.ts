"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { auth } from "@/lib/auth";
import { backendUrl } from "@/lib/backend";

export type PublishState = { error: string | null };

export async function publishAnimalAction(
  _previous: PublishState,
  form: FormData,
): Promise<PublishState> {
  // Re-checked here, not only on the page: a Server Action is a public endpoint.
  const requestHeaders = await headers();
  const session = await auth.api.getSession({ headers: requestHeaders });
  if (!session) {
    redirect("/login");
  }
  const { token } = await auth.api.getToken({ headers: requestHeaders });

  const age = String(form.get("age_in_months") ?? "").trim();
  const response = await fetch(`${backendUrl()}/animals`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: String(form.get("name") ?? ""),
      species: String(form.get("species") ?? ""),
      age_in_months: age === "" ? null : Number(age),
    }),
  });

  if (response.status === 422) {
    // The domain's rule errors are a string; FastAPI's type errors are a list.
    const { detail } = (await response.json()) as { detail: unknown };
    return { error: typeof detail === "string" ? detail : "Invalid animal data" };
  }
  if (!response.ok) {
    return { error: `Publishing failed (backend returned ${response.status})` };
  }
  redirect("/animals");
}
