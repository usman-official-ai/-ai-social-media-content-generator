export default function Tabs({ tabs, active, onChange }) {
  return (
    <div className="flex flex-wrap gap-1 border-b border-rule mb-6">
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={`font-mono text-xs uppercase tracking-wide px-4 py-2.5 -mb-px border-b-2 transition-colors ${
            active === tab.key
              ? "border-amber text-amber"
              : "border-transparent text-paper/50 hover:text-paper/80"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
