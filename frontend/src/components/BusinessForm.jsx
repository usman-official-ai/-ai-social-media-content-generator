const PLATFORMS = ["Instagram", "Facebook", "LinkedIn", "Twitter (X)"];
const GOALS = ["Awareness", "Sales", "Engagement"];
const TONES = ["Professional", "Friendly", "Funny", "Luxury", "Promotional", "Educational"];
const LANGUAGES = ["English", "Urdu"];

function Field({ label, children }) {
  return (
    <div>
      <label className="label">{label}</label>
      {children}
    </div>
  );
}

export default function BusinessForm({ info, onChange, errors = {} }) {
  function set(field, value) {
    onChange({ ...info, [field]: value });
  }

  return (
    <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
      <Field label="Business Name">
        <input
          className="input-field"
          placeholder="e.g. Bright Smile Dental"
          value={info.business_name}
          onChange={(e) => set("business_name", e.target.value)}
        />
        {errors.business_name && <p className="text-xs text-red-400 mt-1">{errors.business_name}</p>}
      </Field>

      <Field label="Industry">
        <input
          className="input-field"
          placeholder="e.g. Healthcare / Dental Clinic"
          value={info.industry}
          onChange={(e) => set("industry", e.target.value)}
        />
        {errors.industry && <p className="text-xs text-red-400 mt-1">{errors.industry}</p>}
      </Field>

      <Field label="Target Audience">
        <input
          className="input-field"
          placeholder="e.g. Families in Lahore, ages 25-45"
          value={info.target_audience}
          onChange={(e) => set("target_audience", e.target.value)}
        />
        {errors.target_audience && <p className="text-xs text-red-400 mt-1">{errors.target_audience}</p>}
      </Field>

      <Field label="Product / Service">
        <textarea
          className="input-field min-h-[72px] resize-none"
          placeholder="e.g. Teeth whitening & general dentistry"
          value={info.product_service}
          onChange={(e) => set("product_service", e.target.value)}
        />
        {errors.product_service && <p className="text-xs text-red-400 mt-1">{errors.product_service}</p>}
      </Field>

      <div className="grid grid-cols-2 gap-3">
        <Field label="Goal">
          <select className="input-field" value={info.goal} onChange={(e) => set("goal", e.target.value)}>
            {GOALS.map((g) => (
              <option key={g}>{g}</option>
            ))}
          </select>
        </Field>
        <Field label="Platform">
          <select className="input-field" value={info.platform} onChange={(e) => set("platform", e.target.value)}>
            {PLATFORMS.map((p) => (
              <option key={p}>{p}</option>
            ))}
          </select>
        </Field>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Field label="Tone">
          <select className="input-field" value={info.tone} onChange={(e) => set("tone", e.target.value)}>
            {TONES.map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </Field>
        <Field label="Language">
          <select className="input-field" value={info.language} onChange={(e) => set("language", e.target.value)}>
            {LANGUAGES.map((l) => (
              <option key={l}>{l}</option>
            ))}
          </select>
        </Field>
      </div>

      <label className="flex items-center gap-2.5 cursor-pointer select-none pt-1">
        <input
          type="checkbox"
          checked={info.include_emojis}
          onChange={(e) => set("include_emojis", e.target.checked)}
          className="h-4 w-4 rounded border-rule bg-ink accent-amber"
        />
        <span className="text-sm text-paper/80">Include emojis</span>
      </label>
    </form>
  );
}
