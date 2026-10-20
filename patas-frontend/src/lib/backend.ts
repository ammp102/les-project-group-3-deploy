// Server-side only: the browser never calls FastAPI directly (ADR 0005).
export function backendUrl(): string {
  return (
    process.env.BACKEND_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    "http://localhost:8000"
  );
}
