import CopyButton from "./CopyButton";

export default function HashtagList({ hashtags = [], trending = [] }) {
  const trendingSet = new Set(trending.map((t) => t.toLowerCase()));

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="eyebrow">Hashtags · {hashtags.length}</span>
        <CopyButton text={hashtags.join(" ")} />
      </div>
      <div className="flex flex-wrap gap-2">
        {hashtags.map((tag) => {
          const isTrending = trendingSet.has(tag.toLowerCase());
          return (
            <span
              key={tag}
              className={`font-mono text-xs px-2.5 py-1 rounded-full border ${
                isTrending
                  ? "border-amber text-amber bg-amber/10"
                  : "border-rule text-paper/80"
              }`}
              title={isTrending ? "Trending" : undefined}
            >
              {tag}
              {isTrending ? " ↑" : ""}
            </span>
          );
        })}
      </div>
    </div>
  );
}
