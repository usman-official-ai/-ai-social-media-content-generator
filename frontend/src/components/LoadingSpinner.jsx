export default function LoadingSpinner({ label = "Generating…" }) {
  return (
    <div className="flex items-center gap-3 text-paper/70">
      <span className="relative flex h-4 w-4">
        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber/60" />
        <span className="relative inline-flex h-4 w-4 rounded-full bg-amber" />
      </span>
      <span className="font-mono text-xs tracking-wide uppercase">{label}</span>
    </div>
  );
}
