import { useState } from "react";
import CopyButton from "./CopyButton";

export default function VariationsCard({ variations }) {
  const [active, setActive] = useState("version_a");
  if (!variations) return null;

  const tabs = [
    { key: "version_a", label: "Version A" },
    { key: "version_b", label: "Version B" },
    { key: "version_c", label: "Version C" },
  ];

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="eyebrow">Content Variations</span>
        <CopyButton text={variations[active]} />
      </div>
      <div className="flex gap-1 mb-4">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActive(tab.key)}
            className={`font-mono text-[11px] uppercase tracking-wide px-3 py-1.5 rounded transition-colors ${
              active === tab.key
                ? "bg-amber text-ink"
                : "text-paper/60 hover:text-paper border border-rule"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <p className="text-[15px] leading-relaxed text-paper/90 whitespace-pre-line">
        {variations[active]}
      </p>
    </div>
  );
}
