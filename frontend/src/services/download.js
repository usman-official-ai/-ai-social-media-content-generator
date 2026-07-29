import { jsPDF } from "jspdf";

export function downloadTxt(text, filename = "content.txt") {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export function downloadPdf(text, filename = "content.pdf", title = "Generated Content") {
  const doc = new jsPDF({ unit: "pt", format: "a4" });
  const marginX = 48;
  let cursorY = 64;
  const pageHeight = doc.internal.pageSize.getHeight();
  const maxWidth = doc.internal.pageSize.getWidth() - marginX * 2;

  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.text(title, marginX, cursorY);
  cursorY += 28;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(11);

  const lines = doc.splitTextToSize(text, maxWidth);
  lines.forEach((line) => {
    if (cursorY > pageHeight - 48) {
      doc.addPage();
      cursorY = 64;
    }
    doc.text(line, marginX, cursorY);
    cursorY += 16;
  });

  doc.save(filename);
}

/** Flattens the generated-content object into one readable text block. */
export function formatContentAsText(content, businessName = "") {
  if (!content) return "";
  const lines = [];
  if (businessName) lines.push(`Business: ${businessName}`, "");
  lines.push("SHORT CAPTION", content.short_caption, "");
  lines.push("MEDIUM CAPTION", content.medium_caption, "");
  lines.push("LONG CAPTION", content.long_caption, "");
  if (content.hashtags?.length) {
    lines.push("HASHTAGS", content.hashtags.join(" "), "");
  }
  lines.push("CALL TO ACTION", content.cta, "");
  lines.push("AI IMAGE PROMPT", content.image_prompt, "");
  if (content.variations) {
    lines.push("VARIATIONS");
    lines.push(`A: ${content.variations.version_a}`);
    lines.push(`B: ${content.variations.version_b}`);
    lines.push(`C: ${content.variations.version_c}`);
  }
  return lines.join("\n");
}
