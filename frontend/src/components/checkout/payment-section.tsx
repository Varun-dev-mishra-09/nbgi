"use client";

import { useMemo, useState } from "react";

import { CheckoutPaymentMethod, loadRazorpayScript } from "@/lib/razorpay";

type PaymentSectionProps = {
  amount: number;
};

export function PaymentSection({ amount }: PaymentSectionProps) {
  const [method, setMethod] = useState<CheckoutPaymentMethod>("razorpay");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const formattedAmount = useMemo(() => `₹${(amount / 100).toFixed(2)}`, [amount]);

  const startPayment = async () => {
    setMessage(null);

    if (method === "cod") {
      setMessage("COD selected. Order will be confirmed with pay-on-delivery mode.");
      return;
    }

    setIsLoading(true);
    const loaded = await loadRazorpayScript();
    setIsLoading(false);

    if (!loaded) {
      setMessage("Unable to load Razorpay checkout. Please try again.");
      return;
    }

    setMessage("Razorpay script loaded. Proceed with order creation API call.");
  };

  return (
    <section className="rounded-lg border p-4">
      <h3 className="text-lg font-semibold">Payment Method</h3>
      <p className="mt-1 text-sm text-muted-foreground">Order total: {formattedAmount}</p>

      <div className="mt-4 space-y-3">
        <label className="flex items-center gap-2 text-sm">
          <input
            checked={method === "razorpay"}
            onChange={() => setMethod("razorpay")}
            type="radio"
            name="payment-method"
          />
          Razorpay (Test Mode)
        </label>

        <label className="flex items-center gap-2 text-sm">
          <input
            checked={method === "cod"}
            onChange={() => setMethod("cod")}
            type="radio"
            name="payment-method"
          />
          Cash on Delivery (COD)
        </label>
      </div>

      <button
        className="mt-4 rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        onClick={startPayment}
        disabled={isLoading}
        type="button"
      >
        {isLoading ? "Loading..." : "Continue"}
      </button>

      {message ? <p className="mt-3 text-sm">{message}</p> : null}
    </section>
  );
}
