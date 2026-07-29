import CopyButton from "./CopyButton";

export default function ResultCard({ eyebrow, children, copyText }) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="eyebrow">{eyebrow}</span>
        {copyText ? <CopyButton text={copyText} /> : null}
      </div>
      <div className="text-[15px] leading-relaxed text-paper/90 whitespace-pre-line">
        {children}
      </div>
    </div>
  );
}
