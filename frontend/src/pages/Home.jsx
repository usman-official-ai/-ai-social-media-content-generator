import { useState } from "react";
import BusinessForm from "../components/BusinessForm";
import Tabs from "../components/Tabs";
import ResultCard from "../components/ResultCard";
import HashtagList from "../components/HashtagList";
import VariationsCard from "../components/VariationsCard";
import DownloadBar from "../components/DownloadBar";
import PostingTimeBadge from "../components/PostingTimeBadge";
import KeywordsCard from "../components/KeywordsCard";
import CalendarView from "../components/CalendarView";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";
import {
  generateContent,
  generateHashtags,
  generateCalendar,
  generateKeywords,
  bestPostingTime,
} from "../services/api";
import { formatContentAsText } from "../services/download";

const EMPTY_INFO = {
  business_name: "",
  industry: "",
  target_audience: "",
  product_service: "",
  goal: "Awareness",
  platform: "Instagram",
  tone: "Friendly",
  language: "English",
  include_emojis: true,
};

const TABS = [
  { key: "content", label: "Content" },
  { key: "hashtags", label: "Hashtags" },
  { key: "calendar", label: "Calendar" },
  { key: "keywords", label: "SEO Keywords" },
  { key: "timing", label: "Best Time" },
];

const REQUIRED_FIELDS = ["business_name", "industry", "target_audience", "product_service"];

export default function Home() {
  const [info, setInfo] = useState(EMPTY_INFO);
  const [activeTab, setActiveTab] = useState("content");
  const [formErrors, setFormErrors] = useState({});
  const [calendarDays, setCalendarDays] = useState(7);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [content, setContent] = useState(null);
  const [hashtagData, setHashtagData] = useState(null);
  const [calendarData, setCalendarData] = useState(null);
  const [keywordsData, setKeywordsData] = useState(null);
  const [timingData, setTimingData] = useState(null);

  function validate() {
    const errs = {};
    REQUIRED_FIELDS.forEach((field) => {
      if (!info[field]?.trim()) errs[field] = "Required";
    });
    setFormErrors(errs);
    return Object.keys(errs).length === 0;
  }

  // ===== FIXED: Complete working runAction function =====
  async function runAction(action) {
    if (!validate()) {
      setError("Please fill in the required business details first.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      if (action === "content") {
        const result = await generateContent(info);
        console.log('Content Result:', result);
        if (result && result.success) {
          const contentData = result.data || result;
          if (contentData.call_to_action && !contentData.cta) {
            contentData.cta = contentData.call_to_action;
          }
          if (typeof contentData.hashtags === 'string') {
            contentData.hashtags = contentData.hashtags.split(',').map(t => t.trim());
          }
          setContent(contentData);
        } else {
          setContent(result);
        }
      } else if (action === "hashtags") {
        const result = await generateHashtags(info);
        console.log('Hashtags Result:', result);
        if (result && result.success) {
          setHashtagData(result.data);
        } else {
          setHashtagData(result);
        }
      } else if (action === "calendar") {
        const result = await generateCalendar(info, calendarDays);
        console.log('Calendar Result:', result);
        if (result && result.success) {
          setCalendarData(result.data);
        } else {
          setCalendarData(result);
        }
      } else if (action === "keywords") {
        const result = await generateKeywords(info);
        console.log('Keywords Result:', result);
        if (result && result.success) {
          setKeywordsData(result.data);
        } else {
          setKeywordsData(result);
        }
      } else if (action === "timing") {
        const result = await bestPostingTime(info.platform);
        console.log('Timing Result:', result);
        if (result && result.success) {
          setTimingData(result.data);
        } else {
          setTimingData(result);
        }
      }
    } catch (err) {
      console.error('Error in runAction:', err);
      setError(err.message || "An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  }

  const actionLabel = {
    content: "Generate Content",
    hashtags: "Generate Hashtags",
    calendar: `Generate ${calendarDays}-Day Calendar`,
    keywords: "Generate Keywords",
    timing: "Get Best Time",
  }[activeTab];

  return (
    <div className="min-h-screen">
      <header className="border-b border-rule">
        <div className="max-w-6xl mx-auto px-6 py-6 flex items-end justify-between flex-wrap gap-3">
          <div>
            <p className="eyebrow mb-1">AI-Powered · Multi-Platform · Bilingual</p>
            <h1 className="font-display text-3xl sm:text-4xl font-semibold tracking-tight">
              The Content Wire
            </h1>
          </div>
          <p className="text-sm text-paper/50 font-mono max-w-xs text-right hidden sm:block">
            Business details in. On-brand captions, hashtags &amp; a content calendar out.
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-[340px_1fr] gap-8">
        <aside className="card p-6 h-fit lg:sticky lg:top-6">
          <p className="eyebrow mb-4">Business Intake</p>
          <BusinessForm info={info} onChange={setInfo} errors={formErrors} />
        </aside>

        <section>
          <Tabs tabs={TABS} active={activeTab} onChange={setActiveTab} />

          <div className="flex items-center gap-4 mb-6 flex-wrap">
            {activeTab === "calendar" && (
              <div className="flex gap-1">
                {[7, 30].map((d) => (
                  <button
                    key={d}
                    onClick={() => setCalendarDays(d)}
                    className={`font-mono text-[11px] uppercase tracking-wide px-3 py-1.5 rounded border transition-colors ${
                      calendarDays === d
                        ? "bg-amber text-ink border-amber"
                        : "border-rule text-paper/60 hover:text-paper"
                    }`}
                  >
                    {d} Days
                  </button>
                ))}
              </div>
            )}

            <button className="btn-primary" onClick={() => runAction(activeTab)} disabled={loading}>
              {loading ? "Generating…" : actionLabel}
            </button>

            {loading && <LoadingSpinner />}
          </div>

          <ErrorBanner message={error} />

          <div className="space-y-5 mt-5">
            {/* CONTENT TAB */}
            {activeTab === "content" && content && (
              <>
                <div className="flex justify-end">
                  <DownloadBar
                    text={formatContentAsText(content, info.business_name)}
                    filenameBase={`${info.business_name || "content"}-${info.platform}`}
                    title={`${info.business_name} — ${info.platform} Content`}
                  />
                </div>
                <ResultCard eyebrow="Short Caption" copyText={content.short_caption}>
                  {content.short_caption}
                </ResultCard>
                <ResultCard eyebrow="Medium Caption" copyText={content.medium_caption}>
                  {content.medium_caption}
                </ResultCard>
                <ResultCard eyebrow="Long Caption" copyText={content.long_caption}>
                  {content.long_caption}
                </ResultCard>
                <HashtagList hashtags={content.hashtags} />
                <ResultCard eyebrow="Call To Action" copyText={content.call_to_action || content.cta}>
                  {content.call_to_action || content.cta}
                </ResultCard>
                <ResultCard eyebrow="AI Image Prompt" copyText={content.image_prompt}>
                  {content.image_prompt}
                </ResultCard>
                {content.variations && <VariationsCard variations={content.variations} />}
              </>
            )}

            {/* HASHTAGS TAB */}
            {activeTab === "hashtags" && hashtagData && (
              <HashtagList
                hashtags={hashtagData.hashtags || hashtagData.trending_hashtags}
                trending={hashtagData.trending_hashtags}
              />
            )}

            {/* CALENDAR TAB */}
            {activeTab === "calendar" && calendarData && (
              <CalendarView 
                calendar={calendarData.calendar || calendarData.daily_content_plan} 
                days={calendarDays} 
              />
            )}

            {/* SEO KEYWORDS TAB */}
            {activeTab === "keywords" && keywordsData && (
              <KeywordsCard keywords={keywordsData.keywords || keywordsData.seo_keywords} />
            )}

            {/* BEST TIME TAB */}
            {activeTab === "timing" && timingData && <PostingTimeBadge data={timingData} />}

            {/* EMPTY STATE */}
            {!loading &&
              !error &&
              ((activeTab === "content" && !content) ||
                (activeTab === "hashtags" && !hashtagData) ||
                (activeTab === "calendar" && !calendarData) ||
                (activeTab === "keywords" && !keywordsData) ||
                (activeTab === "timing" && !timingData)) && (
                <div className="border border-dashed border-rule rounded-md p-10 text-center">
                  <p className="text-paper/40 text-sm font-mono">
                    Fill in the business details and press "{actionLabel}" to see results here.
                  </p>
                </div>
              )}
          </div>
        </section>
      </main>

      <footer className="max-w-6xl mx-auto px-6 py-10 text-xs text-paper/30 font-mono">
        Built with FastAPI + Groq + React · The Content Wire
      </footer>
    </div>
  );
}