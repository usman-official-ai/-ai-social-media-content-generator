import { downloadTxt } from "../services/download";

export default function CalendarView({ calendar = [], days }) {
  if (!calendar.length) return null;

  function exportCalendar() {
    const text = calendar
      .map(
        (d) =>
          `Day ${d.day} — ${d.content_type}\n${d.topic}\n${d.caption_idea}\n`
      )
      .join("\n");
    downloadTxt(text, `content-calendar-${days}day.txt`);
  }

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-4">
        <span className="eyebrow">{days}-Day Content Calendar</span>
        <button className="btn-ghost font-mono text-[11px] uppercase" onClick={exportCalendar}>
          Export .TXT
        </button>
      </div>
      <div className="max-h-[420px] overflow-y-auto pr-1 space-y-2">
        {calendar.map((entry) => (
          <div
            key={entry.day}
            className="flex gap-4 border-b border-rule/60 pb-2 last:border-0"
          >
            <div className="font-mono text-amber text-sm w-14 shrink-0 pt-0.5">
              DAY {String(entry.day).padStart(2, "0")}
            </div>
            <div>
              <p className="text-xs font-mono uppercase tracking-wide text-teal">
                {entry.content_type}
              </p>
              <p className="text-sm font-medium text-paper/90 mt-0.5">{entry.topic}</p>
              <p className="text-sm text-paper/60 mt-0.5">{entry.caption_idea}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
