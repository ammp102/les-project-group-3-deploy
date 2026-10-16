// End-to-end check of the auth handoff: Better-Auth (Next.js) -> JWT -> FastAPI.
// Needs Postgres, FastAPI and `next dev` running. Usage: npm run smoke:auth
import assert from "node:assert/strict";

const NEXT = process.env.NEXT_URL ?? "http://localhost:3000";
const API = process.env.FASTAPI_URL ?? "http://localhost:8000";
const email = `smoke+${Date.now()}@example.com`;

// 1. Register through the Next.js API; the session arrives as a cookie.
const signUp = await fetch(`${NEXT}/api/auth/sign-up/email`, {
  method: "POST",
  headers: { "content-type": "application/json", origin: NEXT },
  body: JSON.stringify({
    name: "Smoke Test",
    email,
    password: "correct-horse-battery",
  }),
});
const signUpBody = await signUp.text();
assert.equal(signUp.status, 200, `sign-up failed: ${signUpBody}`);
const cookie = signUp.headers
  .getSetCookie()
  .map((c) => c.split(";")[0])
  .join("; ");

// 2. Exchange the session for a JWT.
const tokenResponse = await fetch(`${NEXT}/api/auth/token`, {
  headers: { cookie },
});
assert.equal(tokenResponse.status, 200, "token request failed");
const { token } = await tokenResponse.json();
assert.ok(token, "no token returned");

const me = (bearer) =>
  fetch(`${API}/me`, {
    headers: bearer ? { authorization: `Bearer ${bearer}` } : {},
  });

// 3. FastAPI refuses a request without a token.
assert.equal((await me()).status, 401, "request without token must be 401");

// 4. A valid token is accepted and the user is provisioned.
const first = await me(token);
const firstBody = await first.text();
assert.equal(first.status, 200, `valid token rejected: ${firstBody}`);
const user = JSON.parse(firstBody);
assert.equal(user.email, email);
assert.equal(user.name, "Smoke Test");
assert.equal(user.is_platform_admin, false);

// 5. A second call returns the same user (no duplicate).
const second = await (await me(token)).json();
assert.equal(second.id, user.id, "second call must return the same user");

// 6. A tampered token is refused.
const tampered = token.slice(0, -1) + (token.endsWith("A") ? "B" : "A");
assert.equal((await me(tampered)).status, 401, "tampered token must be 401");

console.log(`OK: ${email} registered, authenticated and provisioned as ${user.id}`);
