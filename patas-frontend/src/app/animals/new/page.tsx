import type { Metadata } from "next";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { Suspense } from "react";

import { auth } from "@/lib/auth";

import { PublishForm } from "./publish-form";

export const metadata: Metadata = {
  title: "Publish an animal | Patas",
};

async function RequireSession({ children }: { children: React.ReactNode }) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) {
    redirect("/login");
  }
  return children;
}

export default function NewAnimalPage() {
  return (
    <main className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center gap-6 px-4 py-16">
      <h1 className="text-2xl font-semibold">Publish an animal</h1>
      <Suspense fallback={<p>Loading…</p>}>
        <RequireSession>
          <PublishForm />
        </RequireSession>
      </Suspense>
    </main>
  );
}
