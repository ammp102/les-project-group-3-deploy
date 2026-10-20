// Demo data through the real application: registers 3 demo users with Better-Auth,
// exchanges each session for a JWT and publishes Diogo's sample animals through
// POST /animals. Safe to re-run: existing users sign in, existing animals are skipped.
// Needs the stack running. Usage: pnpm seed:demo
import assert from "node:assert/strict";

const NEXT = process.env.NEXT_URL ?? "http://localhost:3000";
const API = process.env.FASTAPI_URL ?? "http://localhost:8000";
// Local demo only: never use these accounts outside a development database.
const PASSWORD = "demo-password-123";

const OWNERS = [
  {
    name: "Ana Demo",
    email: "ana.demo@example.com",
    animals: [
      { name: "Milo", species: "cat", age_in_months: 18 },
      { name: "Luna", species: "dog", age_in_months: 30 },
    ],
  },
  {
    name: "Bruno Demo",
    email: "bruno.demo@example.com",
    animals: [
      { name: "Pipoca", species: "other", age_in_months: 8 },
      { name: "Nina", species: "cat", age_in_months: null },
    ],
  },
  {
    name: "Carla Demo",
    email: "carla.demo@example.com",
    animals: [
      { name: "Bobby", species: "dog", age_in_months: 60 },
      { name: "Cenoura", species: "other", age_in_months: 12 },
    ],
  },
];

async function tokenFor(owner) {
  const post = async (path, body) => {
    for (let attempt = 1; ; attempt++) {
      const response = await fetch(`${NEXT}/api/auth/${path}`, {
        method: "POST",
        headers: { "content-type": "application/json", origin: NEXT },
        body: JSON.stringify(body),
      });
      if (response.status !== 429 || attempt === 5) {
        return response;
      }
      // Better-Auth allows 3 sign-in/sign-up requests per 10 s per IP in production.
      const seconds = Number(response.headers.get("x-retry-after") ?? 10);
      console.log(`rate limited by Better-Auth, waiting ${seconds}s`);
      await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
    }
  };
  let response = await post("sign-in/email", { email: owner.email, password: PASSWORD });
  if (!response.ok) {
    response = await post("sign-up/email", {
      name: owner.name,
      email: owner.email,
      password: PASSWORD,
    });
  }
  assert.ok(response.ok, `could not sign in ${owner.email}: ${await response.text()}`);
  const cookie = response.headers
    .getSetCookie()
    .map((c) => c.split(";")[0])
    .join("; ");
  const { token } = await (
    await fetch(`${NEXT}/api/auth/token`, { headers: { cookie } })
  ).json();
  return token;
}

const catalog = await (await fetch(`${API}/animals`)).json();
for (const owner of OWNERS) {
  const token = await tokenFor(owner);
  const authorization = `Bearer ${token}`;
  const me = await (await fetch(`${API}/me`, { headers: { authorization } })).json();
  for (const animal of owner.animals) {
    if (catalog.some((a) => a.owner_id === me.id && a.name === animal.name)) {
      console.log(`skip ${animal.name} (already published by ${owner.email})`);
      continue;
    }
    const response = await fetch(`${API}/animals`, {
      method: "POST",
      headers: { authorization, "content-type": "application/json" },
      body: JSON.stringify(animal),
    });
    assert.equal(response.status, 201, `publish ${animal.name} failed: ${await response.text()}`);
    console.log(`published ${animal.name} for ${owner.email}`);
  }
}
console.log(`Demo users log in with password "${PASSWORD}".`);
