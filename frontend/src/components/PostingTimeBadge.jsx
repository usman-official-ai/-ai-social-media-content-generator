export default function PostingTimeBadge({ data }) {
  if (!data) return null;
  return (
    <div className="card p-5 flex items-start gap-4">
      <div className="font-display text-3xl text-amber leading-none pt-1">⏱</div>
      <div>
        <span className="eyebrow">Best Time To Post · {data.platform}</span>
        <p className="font-display text-xl mt-1">{data.best_time}</p>
        <p className="text-sm text-paper/60 mt-1">{data.note}</p>
      </div>
    </div>
  );
}
