import streamlit as st
import streamlit.components.v1 as components
import requests
import math

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vivek-Kavach · AI Content Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

WEBHOOK_URL = "https://hriday.datachef.in/webhook-test/41ff8937-9d4f-4128-b786-52ab925f1062"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600&display=swap');

:root {
  --cream:       #FAF8F4;
  --paper:       #F3F0EA;
  --warm-grey:   #E8E4DC;
  --muted:       #9B9589;
  --ink:         #2A2520;
  --ink-light:   #4A4540;
  --ink-muted:   #6B6560;
  --accent:      #C84B31;
  --accent-soft: #F5E0DA;
  --safe:        #2A7A4F;
  --safe-soft:   #D4EDE1;
  --warn:        #B85C00;
  --warn-soft:   #FDECD4;
  --border:      rgba(42,37,32,0.09);
  --shadow-sm:   0 2px 10px rgba(42,37,32,0.06);
  --shadow-md:   0 6px 28px rgba(42,37,32,0.10);
  --r:           14px;
  --r-sm:        8px;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background: var(--cream);
  color: var(--ink);
}
.stApp { background: var(--cream) !important; }

[data-testid="stSidebar"] { background: var(--paper) !important; border-right: 1px solid var(--border); }

#MainMenu, footer, header { visibility: hidden; }

.stTextArea textarea {
  background: #fff !important;
  border: 1.5px solid var(--warm-grey) !important;
  border-radius: var(--r) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  color: var(--ink) !important;
  padding: 14px 18px !important;
  box-shadow: var(--shadow-sm) !important;
  transition: border-color .2s, box-shadow .2s !important;
}
.stTextArea textarea:focus {
  border-color: var(--ink) !important;
  box-shadow: 0 0 0 3px rgba(42,37,32,0.08) !important;
}

div[data-baseweb="select"] > div {
  background: #fff !important;
  border: 1.5px solid var(--warm-grey) !important;
  border-radius: var(--r-sm) !important;
}

.stButton > button {
  background: var(--ink) !important;
  color: #FAF8F4 !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  padding: 12px 28px !important;
  transition: all .2s !important;
  box-shadow: var(--shadow-sm) !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: #3D3530 !important;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md) !important;
}

.stSpinner > div { border-top-color: var(--ink) !important; }

.vk-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 22px 24px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 16px;
  animation: fadeUp .4s ease both;
  overflow: visible;
}

.vk-label {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 12px;
}

.vk-verdict {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 11px 22px;
  border-radius: 100px;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  width: 100%;
  justify-content: center;
}
.vk-verdict.approved { background: var(--safe-soft); color: var(--safe); border: 1.5px solid rgba(42,122,79,.2); }
.vk-verdict.blocked  { background: var(--accent-soft); color: var(--accent); border: 1.5px solid rgba(200,75,49,.2); }

@keyframes pulse {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:.5; transform:scale(0.75); }
}
.pulse-dot {
  width: 9px; height: 9px; border-radius: 50%;
  animation: pulse 1.8s ease-in-out infinite;
  flex-shrink: 0;
}
.pulse-dot.safe  { background: var(--safe); }
.pulse-dot.block { background: var(--accent); }

.score-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 9px 0;
  border-bottom: 1px solid var(--warm-grey);
  font-size: 13.5px;
  color: var(--ink-light);
}
.score-row:last-child { border-bottom: none; }
.score-row .pts  { font-weight: 700; color: var(--accent); }
.score-row .safe { font-weight: 600; color: var(--safe); }

.vk-viol {
  display: flex;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--warm-grey);
  animation: fadeUp .35s ease both;
  align-items: flex-start;
}
.vk-viol:last-child { border-bottom: none; }
.vk-deduct {
  min-width: 50px; max-width: 50px;
  text-align: center;
  background: var(--accent-soft);
  color: var(--accent);
  border-radius: 6px;
  padding: 5px 0;
  font-weight: 700;
  font-size: 12px;
  line-height: 1.3;
  flex-shrink: 0;
}
.vk-flag-name   { font-weight: 600; color: var(--ink); font-size: 14px; margin-bottom: 3px; }
.vk-flag-detail { font-size: 13px; color: var(--ink-muted); line-height: 1.55; }

.vk-meta {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--paper); border: 1px solid var(--border);
  border-radius: 100px; padding: 5px 14px;
  font-size: 12.5px; color: var(--ink-muted); font-weight: 500;
}
.vk-meta b { color: var(--ink); font-weight: 600; }

.gen-card {
  background: linear-gradient(135deg, #FFFFFF 0%, #F8F6F1 100%);
  border: 1px solid var(--border);
  border-radius: var(--r);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  margin-bottom: 16px;
  animation: fadeUp .45s ease both;
}
.gen-card-header {
  background: var(--ink);
  padding: 12px 22px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.gen-card-header .gtitle {
  font-size: 10.5px; font-weight: 700; letter-spacing: 1.4px;
  text-transform: uppercase; color: rgba(255,255,255,0.55);
}
.gen-card-header .gbadge {
  margin-left: auto;
  background: rgba(255,255,255,0.12);
  border-radius: 100px; padding: 3px 12px;
  font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.8);
}
.gen-card-body {
  padding: 22px 24px;
  font-size: 15.5px;
  line-height: 1.85;
  color: var(--ink);
  font-family: 'DM Sans', sans-serif;
}
.gen-card-footer {
  background: var(--paper);
  border-top: 1px solid var(--border);
  padding: 10px 24px;
  font-size: 11.5px; color: var(--muted);
  display: flex; align-items: center; gap: 8px;
}

.vk-fix {
  background: var(--safe-soft);
  border-left: 3px solid var(--safe);
  border-radius: 0 var(--r-sm) var(--r-sm) 0;
  padding: 14px 18px; font-size: 14px;
  color: var(--ink-light); line-height: 1.7;
}
.vk-warn-fix {
  background: var(--accent-soft);
  border-left: 3px solid var(--accent);
  border-radius: 0 var(--r-sm) var(--r-sm) 0;
  padding: 14px 18px; font-size: 14px;
  color: var(--ink-light); line-height: 1.7;
}

.vk-hero {
  padding: 8px 0 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.vk-hero h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 2rem; color: var(--ink); margin: 0; line-height: 1.15;
}
.vk-hero p { color: var(--ink-muted); font-size: 14.5px; margin: 7px 0 0; }

.vk-empty {
  text-align: center; padding: 64px 20px; color: var(--muted);
  animation: fadeUp .5s ease both;
}
.vk-empty .ico { font-size: 2.8rem; margin-bottom: 14px; }
.vk-empty h3 {
  font-family: 'DM Serif Display', serif;
  font-size: 1.35rem; color: var(--ink-light); margin: 0 0 8px;
}
.vk-empty p { font-size: 14px; max-width: 360px; margin: 0 auto; line-height: 1.7; }

.about-hero {
  background: linear-gradient(120deg, #F3F0EA 0%, #FAF8F4 100%);
  border: 1px solid var(--border); border-radius: var(--r);
  padding: 38px 44px; margin-bottom: 24px; animation: fadeUp .5s ease both;
}
.about-hero h1 {
  font-family: 'DM Serif Display', serif; font-size: 2.4rem;
  color: var(--ink); margin: 0 0 10px;
}
.about-hero p { font-size: 15.5px; color: var(--ink-muted); max-width: 540px; line-height: 1.7; margin: 0; }

.feature-card {
  background: #fff; border: 1px solid var(--border); border-radius: var(--r);
  padding: 22px; height: 100%; box-shadow: var(--shadow-sm);
  transition: box-shadow .2s, transform .2s; animation: fadeUp .45s ease both;
}
.feature-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.feature-card .ico { font-size: 1.7rem; margin-bottom: 10px; }
.feature-card h3 {
  font-family: 'DM Serif Display', serif; font-size: 1.05rem;
  color: var(--ink); margin: 0 0 7px;
}
.feature-card p { font-size: 13px; color: var(--ink-muted); line-height: 1.6; margin: 0; }

.stack-pill {
  display: inline-block; background: var(--paper); border: 1px solid var(--border);
  border-radius: 100px; padding: 4px 12px; font-size: 12.5px;
  font-weight: 500; color: var(--ink-light); margin: 3px;
}

hr { border-color: var(--border) !important; margin: 20px 0 !important; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ── Gauge rendered via components.html ────────────────────────────────────────
def gauge_html(score: int) -> str:
    pct = max(0, min(100, score)) / 100
    cx, cy, r = 155, 130, 100

    if score >= 80:
        color, zone = "#2A7A4F", "Safe to Publish"
    elif score >= 50:
        color, zone = "#B85C00", "Needs Review"
    else:
        color, zone = "#C84B31", "Blocked — Do Not Publish"

    sweep_deg = 180 * pct
    angle_rad = math.radians(180 - sweep_deg)
    ex = cx + r * math.cos(angle_rad)
    ey = cy - r * math.sin(angle_rad)
    large = 1 if sweep_deg > 180 else 0

    ticks = ""
    for val in [0, 25, 50, 75, 100]:
        a  = math.radians(180 - 180 * val / 100)
        x1 = cx + (r - 9)  * math.cos(a)
        y1 = cy - (r - 9)  * math.sin(a)
        x2 = cx + (r + 4)  * math.cos(a)
        y2 = cy - (r + 4)  * math.sin(a)
        lx = cx + (r + 20) * math.cos(a)
        ly = cy - (r + 20) * math.sin(a)
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#D4CFC4" stroke-width="1.5"/>'
        ticks += f'<text x="{lx:.1f}" y="{ly+4:.1f}" font-size="10" fill="#9B9589" text-anchor="middle" font-family="DM Sans,sans-serif">{val}</text>'

    arc  = f'<path id="arc" d="M {cx-r},{cy} A {r},{r} 0 {large},1 {ex:.2f},{ey:.2f}" fill="none" stroke="{color}" stroke-width="15" stroke-linecap="round" filter="url(#glow)"/>' if pct > 0 else ""
    dot  = f'<circle id="dot" cx="{ex:.2f}" cy="{ey:.2f}" r="8" fill="{color}" stroke="white" stroke-width="3"/>' if pct > 0 else f'<circle id="dot" cx="{cx-r}" cy="{cy}" r="8" fill="#D4CFC4" stroke="white" stroke-width="3"/>'

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; display:flex; justify-content:center; overflow:hidden; font-family:'DM Sans',sans-serif; }}
  @keyframes drawArc {{
    from {{ stroke-dashoffset:700; }}
    to   {{ stroke-dashoffset:0; }}
  }}
  @keyframes pop {{
    from {{ opacity:0; transform:scale(.8); }}
    to   {{ opacity:1; transform:scale(1); }}
  }}
  #arc {{ stroke-dasharray:700; animation:drawArc 1.1s cubic-bezier(.4,0,.2,1) both .15s; }}
  #dot {{ animation:pop .4s ease both 1.1s; opacity:0; animation-fill-mode:both; }}
  #score-g {{ animation:pop .5s ease both 1s; opacity:0; animation-fill-mode:both; }}
  #zone-t  {{ animation:pop .5s ease both 1.25s; opacity:0; animation-fill-mode:both; }}
</style>
</head>
<body>
<svg width="310" height="188" viewBox="0 0 310 188" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background track -->
  <path d="M {cx-r},{cy} A {r},{r} 0 0,1 {cx+r},{cy}"
        fill="none" stroke="#E8E4DC" stroke-width="15" stroke-linecap="round"/>

  <!-- Ticks -->
  {ticks}

  <!-- Active arc -->
  {arc}

  <!-- Needle dot -->
  {dot}

  <!-- Score number -->
  <g id="score-g">
    <text x="{cx}" y="{cy+8}" font-size="44" fill="{color}" text-anchor="middle"
          font-family="DM Serif Display,serif">{score}</text>
    <text x="{cx}" y="{cy+28}" font-size="11" fill="#9B9589" text-anchor="middle"
          font-family="DM Sans,sans-serif" letter-spacing="2">/ 100</text>
  </g>

  <!-- Zone label -->
  <text id="zone-t" x="{cx}" y="{cy+52}" font-size="12" fill="{color}" text-anchor="middle"
        font-family="DM Sans,sans-serif" font-weight="700" letter-spacing="0.4">{zone}</text>
</svg>
</body>
</html>"""


# ── Webhook helper ────────────────────────────────────────────────────────────
def call_workflow(prompt, department, content_type):
    try:
        resp = requests.post(
            WEBHOOK_URL,
            json={"user_prompt": prompt, "department": department, "content_type": content_type},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        st.error("⏱ Timed out. Make sure n8n is in test/listening mode.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot reach n8n. Is your GCP instance running?")
    except Exception as e:
        st.error(f"Error: {e}")
    return None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:4px 0 22px;'>
      <div style='font-family:"DM Serif Display",serif;font-size:1.35rem;color:#2A2520;'>🛡️ Vivek-Kavach</div>
      <div style='font-size:11.5px;color:#9B9589;margin-top:3px;'>AI Content Governance</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Nav", ["⚡  Compliance Check", "📖  About"], label_visibility="collapsed")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:12px;color:#9B9589;line-height:1.85;'>
      <b style='color:#4A4540;display:block;margin-bottom:6px;'>Score thresholds</b>
      🟢 &nbsp;80 – 100 → Approved<br>
      🟡 &nbsp;50 – 79  → Review<br>
      🔴 &nbsp;0  – 49  → Blocked
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — COMPLIANCE CHECK
# ═══════════════════════════════════════════════════════════════════════════════
if "⚡" in page:

    st.markdown("""
    <div class='vk-hero'>
      <h1>Content Compliance Auditor</h1>
      <p>Describe the content you need. The pipeline will generate it, then audit it against Acme Corp policies.</p>
    </div>
    """, unsafe_allow_html=True)

    col_in, col_cfg = st.columns([3, 1], gap="medium")
    with col_in:
        user_prompt = st.text_area(
            "prompt",
            placeholder="e.g. Write a social media post for our Lemon Zest Soda launch targeting Gen Z…",
            height=148,
            label_visibility="collapsed",
        )
    with col_cfg:
        department   = st.selectbox("Department",   ["Sales","Marketing","HR","Legal","Finance","Product"])
        content_type = st.selectbox("Content Type", ["Social Media Post","Email Campaign","Blog Article","Ad Copy","Internal Memo","Press Release"])
        run_btn      = st.button("🔍 Run Audit")

    st.markdown("<hr/>", unsafe_allow_html=True)

    if run_btn:
        if not user_prompt.strip():
            st.warning("Please enter a prompt to audit.")
            st.stop()

        with st.spinner("Running: Retriever → Architect → Referee…"):
            data = call_workflow(user_prompt.strip(), department, content_type)

        if not data:
            st.stop()

        score      = int(data.get("compliance_score", data.get("score", 0)))
        compliant  = bool(data.get("compliant", score >= 80))
        final_post = data.get("final_post", data.get("final_content", "")).strip()
        fix        = data.get("recommendation", data.get("actionable_fix", "")).strip()
        meta       = data.get("meta", {})
        dept_out   = meta.get("department", department)
        type_out   = meta.get("type", content_type)
        query_out  = meta.get("query", user_prompt[:80])
        raw_expl   = data.get("score_explanation", "")

        # Parse violations from score_explanation lines
        violations = []
        for line in raw_expl.splitlines():
            line = line.strip()
            if line.startswith("-") and "pts:" in line:
                try:
                    pts_part, rest = line[1:].split("pts:", 1)
                    pts = abs(int(pts_part.strip()))
                    rest = rest.strip()
                    if "(" in rest and rest.endswith(")"):
                        flag   = rest[:rest.rfind("(")].strip()
                        detail = rest[rest.rfind("(")+1:-1].strip()
                    else:
                        flag, detail = rest, ""
                    violations.append({"flag": flag, "detail": detail, "pts": pts})
                except Exception:
                    pass

        # ── META BAR ─────────────────────────────────────────────────────────
        q_display = query_out[:65] + ("…" if len(query_out) > 65 else "")
        st.markdown(f"""
        <div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px;animation:fadeUp .3s ease both;'>
          <span class='vk-meta'>🏢 &nbsp;<b>{dept_out}</b></span>
          <span class='vk-meta'>📄 &nbsp;<b>{type_out}</b></span>
          <span class='vk-meta'>💬 &nbsp;<b>{q_display}</b></span>
        </div>
        """, unsafe_allow_html=True)

        # ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────
        left, right = st.columns([5, 6], gap="large")

        with left:
            # 1) Verdict
            dot   = "safe" if compliant else "block"
            badge = "approved" if compliant else "blocked"
            icon  = "✓" if compliant else "✕"
            label = "Your content is safe to publish." if compliant else "Content is blocked — violations found."
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:.04s;'>
              <div class='vk-label'>Compliance Verdict</div>
              <div class='vk-verdict {badge}'>
                <span class='pulse-dot {dot}'></span>
                {icon}&nbsp;&nbsp;{label}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # 3) Score breakdown
            st.markdown("""<div class='vk-card' style='animation-delay:.08s;'>
              <div class='vk-label'>Score Breakdown</div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class='score-row'>
              <span>Base score</span>
              <span style='font-weight:600;color:#2A2520;'>100</span>
            </div>""", unsafe_allow_html=True)

            if violations:
                for v in violations:
                    st.markdown(f"""
                    <div class='score-row'>
                      <span style='font-size:13px;'>{v['flag']}</span>
                      <span class='pts'>−{v['pts']}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='score-row'>
                  <span class='safe' style='font-size:13px;'>✓ No violations found</span>
                  <span class='safe'>−0</span>
                </div>""", unsafe_allow_html=True)

            score_color = "#2A7A4F" if compliant else "#C84B31"
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;
                        margin-top:14px;padding-top:14px;border-top:2px solid #E8E4DC;
                        font-weight:700;font-size:15px;'>
              <span style='color:#2A2520;'>Final Score</span>
              <span style='font-family:"DM Serif Display",serif;font-size:1.6rem;color:{score_color};'>{score}</span>
            </div>
            </div>""", unsafe_allow_html=True)

            # 4) Explanation
            clean_exp = "\n".join(
                l for l in raw_expl.splitlines()
                if not l.strip().startswith("-") and l.strip()
            ).strip()
            if clean_exp:
                st.markdown(f"""
                <div class='vk-card' style='animation-delay:.12s;'>
                  <div class='vk-label'>Why this score?</div>
                  <div style='font-size:13.5px;color:#4A4540;line-height:1.75;'>{clean_exp}</div>
                </div>""", unsafe_allow_html=True)

        with right:
            # 2) Gauge — uses components.html so SVG renders correctly
            st.markdown("""
            <div style='background:#fff;border:1px solid rgba(42,37,32,.09);border-radius:14px;
                        padding:16px 8px 8px;box-shadow:0 2px 10px rgba(42,37,32,.06);
                        margin-bottom:16px;animation:fadeUp .4s ease both .06s;'>
              <div style='font-size:10.5px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;
                          color:#9B9589;margin-bottom:0;padding:0 16px;'>Compliance Score</div>
            """, unsafe_allow_html=True)
            components.html(gauge_html(score), height=196, scrolling=False)
            st.markdown("</div>", unsafe_allow_html=True)

            # Generated content — styled card
            if final_post:
                post_html = final_post.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                post_html = post_html.replace("\n\n", "<br><br>").replace("\n", "<br>")
                st.markdown(f"""
                <div class='gen-card' style='animation-delay:.16s;'>
                  <div class='gen-card-header'>
                    <span class='gtitle'>Generated Content</span>
                    <span class='gbadge'>{dept_out.upper()} &middot; {type_out}</span>
                  </div>
                  <div class='gen-card-body'>{post_html}</div>
                  <div class='gen-card-footer'>
                    ✨ &nbsp;Generated by GPT-4o Architect &middot; Vivek-Kavach pipeline
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # ── FULL-WIDTH: Violations + Fix ──────────────────────────────────────
        if violations:
            count = len(violations)
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:.2s;'>
              <div class='vk-label'>🚩 Violated Texts &amp; Flags Raised ({count} violation{"s" if count > 1 else ""})</div>
            """, unsafe_allow_html=True)
            for v in violations:
                detail = v['detail'] if v['detail'] else "Policy violation detected in submitted content."
                st.markdown(f"""
                <div class='vk-viol'>
                  <div class='vk-deduct'>−{v['pts']}<br>pts</div>
                  <div>
                    <div class='vk-flag-name'>{v['flag']}</div>
                    <div class='vk-flag-detail'>{detail}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if fix and fix.lower() not in ("no fixes needed.", "no fixes needed", ""):
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:.25s;'>
              <div class='vk-label'>🔧 Actionable Fix</div>
              <div class='vk-warn-fix'>{fix}</div>
            </div>""", unsafe_allow_html=True)
        elif compliant:
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:.25s;'>
              <div class='vk-label'>🔧 Recommendation</div>
              <div class='vk-fix'>✓ Content is fully compliant. No edits required — safe to publish.</div>
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class='vk-empty'>
          <div class='ico'>🛡️</div>
          <h3>Awaiting content</h3>
          <p>Enter your content prompt, pick a department and content type, then hit <strong>Run Audit</strong>.</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class='about-hero'>
      <h1>Vivek-Kavach</h1>
      <p>Enterprise AI content governance middleware — audit, score, and block
         non-compliant AI-generated content before it reaches a customer.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    features = [
        ("🔍", "Policy Retrieval",      "Pinecone vector store holds brand guidelines and legal rules. Every audit starts with a fresh policy fetch."),
        ("🤖", "Content Generation",    "GPT-4o Architect generates content, fully aware of department context and content type constraints."),
        ("⚖️", "Compliance Refereeing", "Strict GPT-4o Referee runs a 10-point checklist, deducting points for every policy violation found."),
        ("📊", "Visual Scoring",        "Animated gauge with colour-coded zones — green, amber, red — for instant intuition on compliance status."),
        ("🚩", "Flag & Explain",        "Every violation surfaces with exact policy reference, deducted points, and the flagged text snippet."),
        ("🔧", "Actionable Fixes",      "Every blocked report includes concrete, step-by-step remediation so writers can fix and resubmit fast."),
    ]
    for i, (ico, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card' style='animation-delay:{0.05*i:.2f}s;'>
              <div class='ico'>{ico}</div>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    pa, pb = st.columns([3, 2], gap="large")

    with pa:
        st.markdown("<div class='vk-card'><div class='vk-label'>n8n Workflow Pipeline</div>", unsafe_allow_html=True)
        steps = [
            ("Webhook",           "Receives prompt, department, content type from this UI"),
            ("Retriever (Gemini)","Calls Pinecone assistant to fetch relevant policies"),
            ("Parser 1",          "Strips AI fluff, extracts structured policy context"),
            ("Architect (GPT-4o)","Generates policy-aware content for the request"),
            ("Code Parser 2",     "Parses generated content into clean JSON"),
            ("Referee (GPT-4o)",  "Runs 10-point compliance audit and scores it"),
            ("Compliance Router", "Routes to Approved or Blocked webhook response"),
        ]
        for i, (name, desc) in enumerate(steps):
            border = "border-bottom:1px solid #E8E4DC;" if i < len(steps)-1 else ""
            st.markdown(f"""
            <div style='display:flex;gap:14px;align-items:flex-start;padding:11px 0;{border}'>
              <div style='min-width:26px;height:26px;background:#F3F0EA;border:1px solid #E8E4DC;
                          border-radius:50%;display:flex;align-items:center;justify-content:center;
                          font-size:11px;font-weight:700;color:#6B6560;flex-shrink:0;'>{i+1}</div>
              <div>
                <div style='font-weight:600;font-size:13.5px;color:#2A2520;'>{name}</div>
                <div style='font-size:12.5px;color:#6B6560;margin-top:2px;'>{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with pb:
        st.markdown("<div class='vk-card'><div class='vk-label'>Tech Stack</div>", unsafe_allow_html=True)
        stacks = {
            "Orchestration": ["n8n (self-hosted)", "GCP VM", "Docker"],
            "AI Models":     ["GPT-4o (OpenAI)", "Gemini 1.5 Flash"],
            "Vector DB":     ["Pinecone", "vivek-kavach assistant"],
            "Frontend":      ["Streamlit", "DM Serif Display", "CSS"],
        }
        for cat, items in stacks.items():
            st.markdown(f"<div style='font-size:11px;font-weight:700;color:#9B9589;letter-spacing:.9px;text-transform:uppercase;margin:16px 0 6px;'>{cat}</div>", unsafe_allow_html=True)
            pills = "".join(f"<span class='stack-pill'>{it}</span>" for it in items)
            st.markdown(pills, unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("<div class='vk-label'>Scoring Deductions</div>", unsafe_allow_html=True)
        rules = [
            ("Unverified health/product claim", "−20"),
            ("Unauthorized pricing promise",    "−25"),
            ("PII / sensitive data exposure",   "−30"),
            ("EU AI Act / DPDP violation",      "−25"),
            ("Copyright / trademark risk",      "−20"),
            ("Aggressive / fear-based language","−15"),
            ("Superlatives without proof",      "−10"),
        ]
        for rule, pts in rules:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:8px 0;
                        border-bottom:1px solid #E8E4DC;font-size:12.5px;color:#4A4540;'>
              <span>{rule}</span>
              <span style='font-weight:700;color:#C84B31;'>{pts}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;color:#9B9589;font-size:12px;padding:22px 0;
                border-top:1px solid rgba(42,37,32,.09);margin-top:8px;'>
      Built for the <b style='color:#4A4540;'>Enterprise AI Governance Hackathon</b>
      &nbsp;·&nbsp; n8n · Pinecone · GPT-4o · Gemini
    </div>
    """, unsafe_allow_html=True)
