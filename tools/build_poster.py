"""Build poster.html with embedded fonts and SVGs."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(ROOT)

def read(path):
    with open(os.path.join(PROJ, path), 'r', encoding='utf-8') as f:
        return f.read()

def read_b64(path):
    with open(os.path.join(ROOT, path), 'r') as f:
        return f.read().strip()

# Load fonts
font_regular = read_b64('carlito_regular_b64.txt')
font_bold = read_b64('carlito_bold_b64.txt')

# Load logo
logo_b64 = read_b64('logo_b64.txt')

# Load SVGs (strip XML declaration and outer whitespace)
def load_svg(name):
    content = read(f'diagrams/fit/{name}')
    # Strip any XML declaration
    if content.startswith('<?xml'):
        content = content[content.index('?>') + 2:].strip()
    return content

import base64
def load_image_b64(path):
    with open(os.path.join(PROJ, path), 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

pilot_img_b64 = load_image_b64('assets/web-page.png')

hero_svg = load_svg('hero.svg')
pipeline_svg = load_svg('pipeline.svg')
dataset_svg = load_svg('dataset.svg')
outcomes_svg = load_svg('outcomes.svg')
metrics_svg = load_svg('metrics.svg')
gap_svg = load_svg('gap.svg')

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ReasonAudit Poster</title>
<style>
@font-face {{
  font-family: 'Carlito';
  src: url(data:font/truetype;base64,{font_regular}) format('truetype');
  font-weight: normal;
  font-style: normal;
}}
@font-face {{
  font-family: 'Carlito';
  src: url(data:font/truetype;base64,{font_bold}) format('truetype');
  font-weight: bold;
  font-style: normal;
}}
@page {{
  size: 841mm 1189mm;
  margin: 0;
}}
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Carlito', sans-serif;
}}
html, body {{
  width: 841mm;
  height: 1189mm;
  overflow: hidden;
  background: white;
}}
.poster {{
  width: 841mm;
  height: 1189mm;
  padding: 30mm;
  display: flex;
  flex-direction: column;
  gap: 12mm;
}}
.row {{
  display: flex;
  gap: 12mm;
  flex-shrink: 0;
}}
.card {{
  border-radius: 12px;
  padding: 12mm;
  position: relative;
  overflow: clip;
  flex-shrink: 0;
}}
.card-gray {{ background: #F4F6F8; }}
.card-lnavy {{ background: #E8EDF3; }}
.card-header {{ background: #1F3A5F; }}
.card-hero {{ background: #FDEFE5; }}

.title-tab {{
  background: #1F3A5F;
  border-radius: 8px;
  height: 22mm;
  display: inline-flex;
  align-items: center;
  padding: 0 8mm;
  margin-bottom: 4mm;
  flex-shrink: 0;
}}
.title-tab span {{
  color: white;
  font-size: 52pt;
  font-weight: bold;
  line-height: 1;
  white-space: nowrap;
}}

.strip {{
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  padding: 2.5mm 4mm;
  margin-bottom: 2mm;
  gap: 4mm;
}}
.strip:last-child {{
  margin-bottom: 0;
}}
.strip .marker {{
  width: 14mm;
  min-width: 14mm;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.marker .dot {{
  width: 8mm;
  height: 8mm;
  border-radius: 50%;
  background: #E8742A;
}}
.marker .badge {{
  width: 10mm;
  height: 10mm;
  border-radius: 50%;
  background: #1F3A5F;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24pt;
  font-weight: bold;
}}
.strip .text {{
  flex: 1;
  font-size: 24pt;
  color: #222222;
  line-height: 1.25;
}}
.strip .text-ref {{
  font-size: 20pt;
}}

/* Header card specifics */
.header-inner {{
  display: flex;
  align-items: center;
  height: 100%;
  gap: 10mm;
  color: white;
}}
.header-logo {{
  width: 100mm;
  height: 100mm;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
}}
.header-logo img {{
  max-width: 90mm;
  max-height: 90mm;
  object-fit: contain;
}}
.header-center {{
  flex: 1;
}}
.header-title {{
  font-size: 80pt;
  font-weight: bold;
  line-height: 1.1;
  color: white;
}}
.header-authors {{
  font-size: 36pt;
  color: white;
  margin-top: 4mm;
  line-height: 1.2;
}}
.header-dept {{
  font-size: 28pt;
  color: rgba(255,255,255,0.85);
  margin-top: 2mm;
}}
.header-faculty {{
  display: flex;
  flex-direction: column;
  gap: 4mm;
  flex-shrink: 0;
  min-width: 150mm;
}}
.faculty-tile {{
  background: #E8EDF3;
  border-radius: 8px;
  padding: 3mm 5mm;
}}
.faculty-role {{
  font-size: 20pt;
  color: #E8742A;
  line-height: 1.2;
}}
.faculty-name {{
  font-size: 24pt;
  color: #1F3A5F;
  line-height: 1.2;
}}

/* Hero card */
.hero-inner {{
  display: flex;
  flex-direction: column;
  height: 100%;
}}
.hero-headline {{
  font-size: 56pt;
  font-weight: bold;
  color: #1F3A5F;
  line-height: 1.1;
  margin-bottom: 4mm;
  white-space: nowrap;
}}
.hero-diagram {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.hero-diagram svg {{
  width: 757mm;
  height: auto;
}}
.hero-caption {{
  font-size: 24pt;
  color: #6B7280;
  margin-top: 2mm;
  flex-shrink: 0;
}}

/* Card content layout */
.card-inner {{
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}}

/* Methodology specifics */
.method-diagram {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2mm;
  min-height: 0;
}}
.method-diagram svg {{
  width: 100%;
  height: 80mm;
}}
.method-controls {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-radius: 8px;
  padding: 3mm 5mm;
}}
.method-chip {{
  display: inline-block;
  border: 2px dashed #6B7280;
  border-radius: 8px;
  padding: 2mm 4mm;
  font-size: 24pt;
  color: #222222;
}}
.model-chips {{
  display: flex;
  align-items: center;
  gap: 3mm;
}}
.model-chip {{
  background: #F4F6F8;
  border-radius: 8px;
  padding: 2mm 4mm;
  font-size: 24pt;
  color: #222222;
}}
.model-label {{
  font-size: 24pt;
  color: #1F3A5F;
  font-weight: bold;
  margin-right: 3mm;
}}

/* Dataset card */
.dataset-diagram {{
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2mm;
}}
.dataset-diagram svg {{
  width: 246mm;
  height: 55mm;
}}

/* Outcomes card: diagram only */
.outcomes-diagram {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.outcomes-diagram svg {{
  width: 100%;
  height: 155mm;
  display: block;
  margin: 0 auto;
}}

/* Metrics card */
.metrics-diagram {{
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2mm;
}}
.metrics-diagram svg {{
  width: 223mm;
  height: 55mm;
}}
.strip .text-orange {{
  color: #E8742A;
  font-weight: bold;
}}

/* Gap card: diagram only */
.gap-diagram {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.gap-diagram svg {{
  width: 360mm;
  height: 85mm;
}}

/* Pilot system */
.pilot-inner {{
  display: flex;
  gap: 5mm;
  flex: 1;
  min-height: 0;
}}
.pilot-left {{
  flex: 1;
  display: flex;
  flex-direction: column;
}}
.pilot-right {{
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}}
.pilot-screenshot {{
  width: 100%;
  height: auto;
  max-height: 85mm;
  object-fit: contain;
  border: 3px solid #1F3A5F;
  border-radius: 8px;
  box-sizing: border-box;
}}
.pilot-caption {{
  font-size: 20pt;
  color: #6B7280;
  text-align: center;
  margin-top: 2mm;
}}

/* Status card */
.chevrons {{
  display: flex;
  gap: 2mm;
  margin-bottom: 2mm;
  flex-shrink: 0;
}}
.chevron {{
  flex: 1;
  height: 14mm;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24pt;
  font-weight: bold;
  color: white;
  background: #1F3A5F;
  clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%, 15% 50%);
  padding-left: 5mm;
}}
.chevron:first-child {{
  clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%);
  padding-left: 3mm;
}}
.chevron.active {{
  background: #E8742A;
}}
.status-descriptions {{
  display: flex;
  gap: 2mm;
  flex: 1;
}}
.status-col {{
  flex: 1;
  font-size: 24pt;
  color: #222222;
  line-height: 1.25;
  padding: 0 2mm;
}}

/* References */
.ref-inner {{
  background: white;
  border-radius: 8px;
  padding: 3mm;
  flex: 1;
  column-count: 2;
  column-gap: 4mm;
  font-size: 20pt;
  color: #222222;
  line-height: 1.25;
  overflow: hidden;
}}
.ref-inner p {{
  margin-bottom: 1.5mm;
  break-inside: avoid;
}}
</style>
</head>
<body>
<div class="poster">

  <!-- HEADER -->
  <div class="card card-header" data-card="header" style="width:781mm; height:150mm;">
    <div class="header-inner">
      <div class="header-logo">
        <img src="data:image/webp;base64,{logo_b64}" alt="UIU Logo">
      </div>
      <div class="header-center">
        <div class="header-title">ReasonAudit: Evaluating Error Awareness<br>and Self-Correction in Large Language Models</div>
        <div class="header-authors">Md. Assaduzzaman Nur &middot; Shahriar Yasin &middot; Shakib Ahmed &middot; Sadid Ahmed &middot; Rukan Mia</div>
        <div class="header-dept">Department of Computer Science and Engineering, United International University</div>
      </div>
      <div class="header-faculty">
        <div class="faculty-tile">
          <div class="faculty-role">Supervisor</div>
          <div class="faculty-name">Sadia Islam, Assistant Professor</div>
        </div>
        <div class="faculty-tile">
          <div class="faculty-role">Co-Supervisor</div>
          <div class="faculty-name">Mr. Nahid Hossain, Assistant Professor</div>
        </div>
        <div class="faculty-tile">
          <div class="faculty-role">Course Teacher</div>
          <div class="faculty-name">Dr. Riasat Azim, Associate Professor</div>
        </div>
      </div>
    </div>
  </div>

  <!-- HERO -->
  <div class="card card-hero" data-card="hero" style="width:781mm; height:180mm;">
    <div class="hero-inner">
      <div class="hero-headline">Can an LLM catch its own mistakes, or does second-guessing make things worse?</div>
      <div class="hero-diagram">{hero_svg}</div>
      <div class="hero-caption">We measure how often self-review fixes errors, and how often it ruins correct answers.</div>
    </div>
  </div>

  <!-- ROW A -->
  <div class="row">
    <!-- Motivation -->
    <div class="card card-gray" data-card="motivation" style="width:384.5mm; height:130mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Motivation</span></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">LLMs are used in coding, teaching, and research, often with little human checking.</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">They can give wrong answers with full confidence.</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Self-review is fragile: models may miss errors, keep bad answers, or change correct answers to wrong ones.</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">We need a precise measure of when self-correction helps and when it hurts.</div></div>
      </div>
    </div>
    <!-- Objectives -->
    <div class="card card-lnavy" data-card="objectives" style="width:384.5mm; height:130mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Objectives</span></div>
        <div class="strip"><div class="marker"><div class="badge">1</div></div><div class="text">Build a labeled reasoning dataset with verified answers and difficulty tags.</div></div>
        <div class="strip"><div class="marker"><div class="badge">2</div></div><div class="text">Measure Correction Rate, Damage Rate, and accuracy change after self-review.</div></div>
        <div class="strip"><div class="marker"><div class="badge">3</div></div><div class="text">Compare open-weight and proprietary models across reasoning types.</div></div>
        <div class="strip"><div class="marker"><div class="badge">4</div></div><div class="text">Link difficulty factors to self-correction success.</div></div>
      </div>
    </div>
  </div>

  <!-- ROW B: Methodology -->
  <div class="row">
    <div class="card card-gray" data-card="methodology" style="width:781mm; height:150mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Methodology</span></div>
        <div class="method-diagram">{pipeline_svg}</div>
        <div class="method-controls">
          <div class="method-chip">Controls: neutral review &middot; independent second attempt</div>
          <div class="model-chips">
            <div class="model-label">Models</div>
            <div class="model-chip">Claude Haiku 4.5</div>
            <div class="model-chip">GPT-6 Luna</div>
            <div class="model-chip">Gemini 3.8 Flash</div>
            <div class="model-chip">LLaMA 3 8B</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ROW C -->
  <div class="row">
    <!-- Dataset -->
    <div class="card card-lnavy" data-card="dataset" style="width:270mm; height:212mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Dataset</span></div>
        <div class="dataset-diagram">{dataset_svg}</div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Domains: Mathematics &middot; Formal Logic &middot; Commonsense</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Difficulty modifiers (yes/no tag per question): Ambiguity &middot; Missing information &middot; Contradiction &middot; Distracting information</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Built by: collecting questions from public datasets, then manual annotation and tagging. Each question keeps its source and a flag if modified.</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Scale: 20-question pilot, designed to scale to 2,000.</div></div>
      </div>
    </div>
    <!-- Outcome Buckets -->
    <div class="card card-gray" data-card="outcome-buckets" style="width:240mm; height:212mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Outcome Buckets</span></div>
        <div class="outcomes-diagram">{outcomes_svg}</div>
      </div>
    </div>
    <!-- Metrics -->
    <div class="card card-lnavy" data-card="metrics" style="width:247mm; height:212mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Metrics</span></div>
        <div class="metrics-diagram">{metrics_svg}</div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text"><span class="text-orange">Correction Rate</span> = WC / (WC + WW): share of wrong answers the model fixed</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text"><span class="text-orange">Damage Rate</span> = CW / (CC + CW): share of correct answers the model ruined</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Accuracy Change = Final Accuracy &minus; Initial Accuracy</div></div>
        <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Analysis: McNemar&#8217;s test, 95% confidence intervals, breakdown by domain and difficulty tag.</div></div>
      </div>
    </div>
  </div>

  <!-- ROW D -->
  <div class="row">
    <!-- Research Gap -->
    <div class="card card-gray" data-card="research-gap" style="width:384.5mm; height:135mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Research Gap</span></div>
        <div class="gap-diagram">{gap_svg}</div>
      </div>
    </div>
    <!-- Pilot System -->
    <div class="card card-lnavy" data-card="pilot-system" style="width:384.5mm; height:135mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Pilot System</span></div>
        <div class="pilot-inner">
          <div class="pilot-left">
            <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Two-stage pipeline in Google Sheets + Apps Script, with a web pilot tool.</div></div>
            <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Logs every prompt and raw response for traceability.</div></div>
            <div class="strip"><div class="marker"><div class="dot"></div></div><div class="text">Automatic retry on rate limits, CSV export.</div></div>
          </div>
          <div class="pilot-right">
            <img class="pilot-screenshot" src="data:image/png;base64,{pilot_img_b64}" alt="Pilot System Screenshot">
            <div class="pilot-caption">Illustrative pilot data.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ROW E -->
  <div class="row">
    <!-- Status -->
    <div class="card card-gray" data-card="status" style="width:384.5mm; height:100mm;">
      <div class="card-inner">
        <div class="title-tab"><span>Status and Next Steps</span></div>
        <div class="chevrons">
          <div class="chevron">Done</div>
          <div class="chevron active">In progress</div>
          <div class="chevron">Next</div>
        </div>
        <div class="status-descriptions">
          <div class="status-col">domain selection, literature review</div>
          <div class="status-col">architecture, pipeline design</div>
          <div class="status-col">dataset expansion, base paper validation, full model runs, statistical analysis</div>
        </div>
      </div>
    </div>
    <!-- References -->
    <div class="card card-lnavy" data-card="references" style="width:384.5mm; height:100mm;">
      <div class="card-inner">
        <div class="title-tab"><span>References</span></div>
        <div class="ref-inner">
          <p>1. Huang et al., Large Language Models Cannot Self-Correct Reasoning Yet, ICLR 2024</p>
          <p>2. Tyen et al., LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location, ACL Findings 2024</p>
          <p>3. Tsui, Self-Correction Bench, COLM 2026</p>
          <p>4. Madaan et al., Self-Refine, NeurIPS 2023</p>
          <p>5. Yuan et al., Hidden Error Awareness in Chain-of-Thought Reasoning, 2026</p>
          <p>6. Cobbe et al., Training Verifiers to Solve Math Word Problems, 2021</p>
        </div>
      </div>
    </div>
  </div>

</div>
</body>
</html>
'''

out_path = os.path.join(PROJ, 'poster.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written: {out_path} ({len(html)} bytes)")
