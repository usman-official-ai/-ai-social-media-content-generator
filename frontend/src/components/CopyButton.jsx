import { useState } from "react";

export default function CopyButton({ text, label = "Copy" }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text || "");
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      // Clipboard API can fail in insecure contexts; fail silently, button just won't confirm.
    }
  }

  return (
    <button
      type="button"
      onClick={handleCopy}
      className="btn-ghost font-mono text-[11px] tracking-wide uppercase"
    >
      {copied ? "Copied ✓" : label}
    </button>
  );
}
