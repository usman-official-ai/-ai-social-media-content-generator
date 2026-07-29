import CopyButton from "./CopyButton";

export default function KeywordsCard({ keywords = [] }) {
  if (!keywords.length) return null;
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="eyebrow">SEO Keywords · {keywords.length}</span>
        <CopyButton text={keywords.join(", ")} />
      </div>
      <ul className="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-1.5">
        {keywords.map((kw) => (
          <li key={kw} className="text-sm text-paper/80 flex items-center gap-1.5">
            <span className="text-amber">·</span> {kw}
          </li>
        ))}
      </ul>
    </div>
  );
}
