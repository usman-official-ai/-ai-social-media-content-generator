export default function ErrorBanner({ message }) {
  if (!message) return null;
  return (
    <div className="border border-red-500/40 bg-red-500/10 text-red-300 text-sm rounded px-4 py-3">
      {message}
    </div>
  );
}
