export type Dispute = {
  id: string;
  userId: string;
  amountCents: number;
  merchant: string;
  reason: string;
  trackingNumber?: string;
  note?: string;
  status: "new" | "investigating" | "approved" | "denied" | "error";
};

export type InvestigationResult =
  | {
      status: "approved";
      disputeId: string;
      refundId: string;
      reason: string;
    }
  | {
      status: "denied";
      disputeId: string;
      reason: string;
    }
  | {
      status: "error";
      message: string;
    };
