import type { Dispute, InvestigationResult } from "./types";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:4000";

export async function fetchDisputes(): Promise<Dispute[]> {
  const response = await fetch(`${apiUrl}/api/disputes`);

  if (!response.ok) {
    throw new Error("Failed to load disputes");
  }

  const body = (await response.json()) as { disputes: Dispute[] };
  return body.disputes;
}

export async function investigateDispute(dispute: Dispute, note: string): Promise<InvestigationResult> {
  const response = await fetch(`${apiUrl}/api/disputes/${dispute.id}/investigate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ...dispute,
      note
    })
  });

  const body = (await response.json()) as InvestigationResult;

  if (!response.ok) {
    return body;
  }

  return body;
}
