const RAZORPAY_SCRIPT_SRC = "https://checkout.razorpay.com/v1/checkout.js";

export const loadRazorpayScript = async (): Promise<boolean> => {
  if (typeof window === "undefined") {
    return false;
  }

  if ((window as Window & { Razorpay?: unknown }).Razorpay) {
    return true;
  }

  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = RAZORPAY_SCRIPT_SRC;
    script.async = true;
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
};

export type CheckoutPaymentMethod = "razorpay" | "cod";
