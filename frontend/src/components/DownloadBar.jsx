import { downloadTxt, downloadPdf } from "../services/download";

export default function DownloadBar({ text, filenameBase = "content", title = "Generated Content" }) {
  if (!text) return null;

  return (
    <div className="flex items-center gap-2">
      <span className="label mb-0">Export</span>
      <button
        className="btn-ghost font-mono text-[11px] uppercase"
        onClick={() => downloadTxt(text, `${filenameBase}.txt`)}
      >
        .TXT
      </button>
      <button
        className="btn-ghost font-mono text-[11px] uppercase"
        onClick={() => downloadPdf(text, `${filenameBase}.pdf`, title)}
      >
        .PDF
      </button>
    </div>
  );
}
