import { useEffect, useMemo, useState } from "react";
import { fetchDisputes, investigateDispute } from "./api";
import type { Dispute, InvestigationResult } from "./types";

function formatMoney(amountCents: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amountCents / 100);
}

function getResultMessage(result: InvestigationResult): string {
  if (result.status === "approved") {
    return `${result.reason} (${result.refundId})`;
  }

  if (result.status === "denied") {
    return result.reason;
  }

  return result.message;
}

export function App() {
  const [disputes, setDisputes] = useState<Dispute[]>([]);
  const [selectedId, setSelectedId] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [investigating, setInvestigating] = useState(false);
  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState("");

  useEffect(() => {
    fetchDisputes()
      .then((items) => {
        setDisputes(items);
        setSelectedId(items[0]?.id ?? "");
      })
      .catch((loadError: unknown) => {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Failed to load disputes",
        );
      })
      .finally(() => setLoading(false));
  }, []);

  const selectedDispute = useMemo(
    () => disputes.find((dispute) => dispute.id === selectedId),
    [disputes, selectedId],
  );

  async function handleInvestigate() {
    if (!selectedDispute) {
      return;
    }

    setError(null);
    setResult(null);
    setInvestigating(true);

    try {
      const nextResult = await investigateDispute(selectedDispute, note);
      setResult(nextResult);
    } catch (investigationError) {
      setError(
        investigationError instanceof Error
          ? investigationError.message
          : "Investigation failed",
      );
    } finally {
      setInvestigating(false);
    }
  }

  return (
    <main className="shell">
      <section className="header">
        <div>
          <p className="eyebrow">ChargeShield AI</p>
          <h1>Dispute Investigation</h1>
        </div>
      </section>

      <section className="layout">
        <aside className="panel list-panel">
          <div className="panel-header">
            <h2>Disputes</h2>
          </div>

          {loading ? (
            <p className="muted">Loading disputes...</p>
          ) : (
            <div className="dispute-list">
              {disputes.map((dispute) => (
                <button
                  className={
                    dispute.id === selectedId
                      ? "dispute-row active"
                      : "dispute-row"
                  }
                  key={dispute.id}
                  onClick={() => {
                    setSelectedId(dispute.id);
                    setNote("");
                    setResult(null);
                    setError(null);
                  }}
                >
                  <span>{dispute.merchant}</span>
                  <small>{formatMoney(dispute.amountCents)}</small>
                </button>
              ))}
            </div>
          )}
        </aside>

        <section className="panel detail-panel">
          {selectedDispute ? (
            <>
              <div className="panel-header split">
                <div>
                  <h2>{selectedDispute.merchant}</h2>
                  <p className="muted">{selectedDispute.id}</p>
                </div>
                <span className="status">{selectedDispute.status}</span>
              </div>

              <dl className="details">
                <div>
                  <dt>User</dt>
                  <dd>{selectedDispute.userId}</dd>
                </div>
                <div>
                  <dt>Amount</dt>
                  <dd>{formatMoney(selectedDispute.amountCents)}</dd>
                </div>
                <div>
                  <dt>Tracking</dt>
                  <dd>{selectedDispute.trackingNumber ?? "None"}</dd>
                </div>
              </dl>

              <div className="claim">
                <h3>Claim</h3>
                <p>{selectedDispute.reason}</p>
              </div>

              <label className="note-field">
                <span>Note</span>
                <textarea
                  value={note}
                  onChange={(event) => setNote(event.target.value)}
                  placeholder="Add investigation context or a customer note..."
                  rows={4}
                />
              </label>

              <button className="primary-button" onClick={handleInvestigate}>
                Investigate
              </button>

              {result ? (
                <div
                  className={
                    result.status === "error" ? "result error" : "result"
                  }
                >
                  <strong>{result.status.toUpperCase()}</strong>
                  <p>{getResultMessage(result)}</p>
                </div>
              ) : null}

              {error ? (
                <div className="result error">
                  <strong>ERROR</strong>
                  <p>{error}</p>
                </div>
              ) : null}
            </>
          ) : (
            <p className="muted">Select a dispute.</p>
          )}
        </section>
      </section>
    </main>
  );
}
