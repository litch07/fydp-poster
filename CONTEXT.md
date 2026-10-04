# ReasonAudit Poster: Project Context

## What this project is
An A0 academic research poster for "ReasonAudit: Evaluating Error Awareness and Self-Correction in Large Language Models", a BSc CSE project at United International University (UIU). The poster is viewed at 1-2 meters at a conference. The audience includes non-experts. The central idea must be understood from the hero diagram alone.

## The research in one paragraph
We ask: can an LLM catch and fix its own mistakes without any help? In Stage 1 the model answers a question. In Stage 2 the same model is shown its own answer with a fixed review prompt and gives a final answer. It never receives hints or the correct answer. Each question lands in one of four outcome buckets: CC (Correct-to-Correct), WC (Wrong-to-Correct), WW (Wrong-to-Wrong), CW (Correct-to-Wrong). Metrics: Correction Rate = WC/(WC+WW); Damage Rate = CW/(CC+CW); Accuracy Change = Final minus Initial accuracy.

## Your role
You are a senior information designer for academic posters. You value clarity, restraint, consistency, and storytelling through visuals over text. You never invent results, numbers, logos, or images.

## Rules for every output
- Diagrams: output standalone SVG files saved into /diagrams. Never raster images. All text as live <text>. Valid SVG that opens in a browser.
- Font: Calibri, fallback Carlito, sans-serif. One family only.
- Colors (only these): navy #1F3A5F (strokes, text, character body), orange #E8742A (arrows, highlights, character accent), light gray #F4F6F8 (fills), white, body text #222222, secondary text #6B7280. Muted green #3E8E6B and muted red #C0504D ONLY for correct/wrong states.
- Shapes: rounded rectangles (radius 6), stroke width 3, ONE arrow style (orange, simple triangular head), flat line icons drawn with navy strokes.
- No gradients, shadows, 3D, clip-art, stock icons, or outlines around sections.
- Minimum text size: 28 units on a diagram 1000 units wide. Nothing overlapping or clipped. Strict alignment, generous spacing.
- Less text is better. If an icon or the character can say it, remove the words.

## Character: "Audit" (the LLM)
A friendly robot made only from simple geometric shapes, under 12 shapes: rounded-square navy head, two white circle eyes with navy pupils, one short antenna with an orange dot, a small rounded-rectangle body, short arms. Expressions come only from the eyes and a simple mouth line: neutral, happy, worried/"oops". Audit must look identical in shape and color in every diagram. Only pose and expression change.
Story metaphors: a hand MIRROR means self-review. A LOCK means no hints and no answer key. Green check / red cross cards mean correct / wrong answers.
Audit is defined once in diagrams/audit.svg (create it first, as a reusable group). Reuse the same shapes in every diagram.

## Poster layout: CARD (BENTO) SYSTEM (replaces all earlier layout text)

### Canvas
A0 portrait 841 x 1189 mm. Margin 30 mm. Gap between cards 12 mm. Content area 781 x 1129 mm.

### Exact card sizes (width x height, mm). Do not change them.
HEADER: 781 x 150
HERO: 781 x 180
ROW A (height 150): Motivation 384.5 | Objectives 384.5
ROW B (height 150): Methodology 781
ROW C (height 192): Dataset 270 | Outcome Buckets 240 | Metrics 247
ROW D (height 135): Research Gap 400 | Pilot System 369
ROW E (height 100): Status and Next Steps 384.5 | References 384.5
Check: 150+180+150+150+192+135+100 = 1057, plus 6 gaps of 12 = 1129. Cards tile the area exactly, with no gap at the bottom.

### Shape system (the only shapes)
- Card: rounded rectangle, radius 12, filled, no outline, no shadow. Padding 12.
- Title tab: navy rounded rectangle (radius 8), 22 mm tall, at the card's top-left, white bold 52pt title. Same height on every card.
- Inner strip: rounded rectangle (radius 8), white fill, STRETCHED to the full inner width of the card (never hugging its text). Every strip has the same layout: a 14 mm marker column (orange dot or navy number badge) on the left, text on the right, same left alignment in all strips.
- Fills: navy #1F3A5F (header, tabs, badges), light gray #F4F6F8 and light navy #E8EDF3 (alternate neighboring cards), light orange #FDEFE5 (hero and focus shapes), white (inner shapes), light green #E3F1EA and light red #F7E3E2 (outcome cells only). Orange #E8742A for dots, arrows, key numbers.
- No outlines, no rotated text anywhere (no vertical text).

### Type sizes
Title 80pt bold (2 lines), authors 36pt, hero headline 56pt bold (ONE line), tab titles 52pt bold, body 24pt (increase to 28pt only where a card has room), diagram labels 24pt minimum, references and captions 20pt minimum. One body size across all cards.

### Block contents (use the exact text from the CONTENT section, never shorten or reword)
HEADER: logo tile (white, left, labeled placeholder), title, authors, department line, then three equal faculty tiles (light navy fill; role in orange 20pt above name in navy 24pt).
HERO: headline, hero diagram filling the full inner width (757 mm wide), caption.
MOTIVATION / OBJECTIVES: 4 strips each.
METHODOLOGY: pipeline diagram (horizontal, full inner width). A bottom strip contains the dashed "Controls: neutral review · independent second attempt" chip on the left and the 4 model chips with the label "Models" on the right.
DATASET: dataset diagram on top, then the four bullets as strips.
OUTCOME BUCKETS: grid diagram only.
METRICS: metrics diagram on top, then the 3 formulas and the analysis line as strips (Correction Rate and Damage Rate in orange).
RESEARCH GAP: gap diagram only. No extra rows or text beyond what is inside the diagram.
PILOT SYSTEM: bullets as strips on the left half, screenshot placeholder frame on the right half, caption "Illustrative pilot data." under it.
STATUS: three chevron shapes containing ONLY the labels "Done", "In progress", "Next", with the description text in plain text columns UNDER each chevron. Orange marker on "In progress".
REFERENCES: one white inner shape, two text columns, 20pt.

### Hard rules learned from failures
1. FONT: Carlito must be installed and embedded in poster.html as base64 @font-face. If fc-list does not show Carlito, install fonts-crosextra-carlito or download Carlito from Google Fonts. Never render with a fallback font.
2. DIAGRAMS IN MILLIMETERS: every diagram SVG is built for its exact card: width and height attributes in mm, viewBox equal to the same numbers, so 1 unit = 1 mm. Text size in units: 24pt = 8.5, 20pt = 7.1. The SVG is placed at 100% with no scaling and no letterboxing, and fills its inner area.
3. No text may touch or cross a shape edge: at least 3 mm margin inside its container. Labels that do not fit must wrap onto two lines or be shortened ONLY inside diagrams. Poster body text is never shortened.
4. No rotated text. Row headers in the grid are horizontal, short, and two-line if needed.
5. Audit is defined once as an SVG <symbol id="audit"> and reused with <use>, never redrawn.
6. Diagram labels (fixed): hero scene 2 card "Answer 1", mirror card "Answer 1", output "Final answer". Pipeline nodes: "Question Bank", "Stage 1: Initial answer" + "no hints", "Stage 2: Self-review" + "fixed prompt", "Final answer", the grading split with both boxes ("Numeric / multiple choice: auto-graded" and "Open-ended: manual grading"), "Outcome bucket", "Metrics".
7. A card is finished only when its content fills at least 90% of its height with no empty band.

## Poster content (use EXACTLY as written, never paraphrase)

HEADER
Left: UIU logo (assets/uiu-logo.png; if missing, a labeled placeholder box)
Title: ReasonAudit: Evaluating Error Awareness and Self-Correction in Large Language Models
Authors: Md. Assaduzzaman Nur · Shahriar Yasin · Shakib Ahmed · Sadid Ahmed · Rukan Mia
Under authors: Department of Computer Science and Engineering, United International University
Top-right, small, no boxes:
Supervisor: Sadia Islam, Assistant Professor
Co-Supervisor: Mr. Nahid Hossain, Assistant Professor
Course Teacher: Dr. Riasat Azim, Associate Professor

HERO BAND
Headline: Can an LLM catch its own mistakes, or does second-guessing make things worse?
Diagram: diagrams/hero.svg
Caption: We measure how often self-review fixes errors, and how often it ruins correct answers.

COLUMN 1
Motivation
- LLMs are used in coding, teaching, and research, often with little human checking.
- They can give wrong answers with full confidence.
- Self-review is fragile: models may miss errors, keep bad answers, or change correct answers to wrong ones.
- We need a precise measure of when self-correction helps and when it hurts.
Objectives
1. Build a labeled reasoning dataset with verified answers and difficulty tags.
2. Measure Correction Rate, Damage Rate, and accuracy change after self-review.
3. Compare open-weight and proprietary models across reasoning types.
4. Link difficulty factors to self-correction success.
Dataset
- Domains: Mathematics · Formal Logic · Commonsense
- Difficulty modifiers (yes/no tag per question): Ambiguity · Missing information · Contradiction · Distracting information
- Built by: collecting questions from public datasets, then manual annotation and tagging. Each question keeps its source and a flag if modified.
- Scale: 20-question pilot, designed to scale to 2,000.
Diagram: diagrams/dataset.svg

COLUMN 2
Methodology
Diagram: diagrams/pipeline.svg
- Models: Claude Haiku 4.5 · GPT-6 Luna · Gemini 3.8 Flash · LLaMA 3 8B
Outcome Buckets
Diagram: diagrams/outcomes.svg
Metrics
Diagram: diagrams/metrics.svg
- Correction Rate = WC / (WC + WW): share of wrong answers the model fixed
- Damage Rate = CW / (CC + CW): share of correct answers the model ruined
- Accuracy Change = Final Accuracy - Initial Accuracy
- Analysis: McNemar's test, 95% confidence intervals, breakdown by domain and difficulty tag.

COLUMN 3
Research Gap
Diagram: diagrams/gap.svg
Pilot System
- Two-stage pipeline in Google Sheets + Apps Script, with a web pilot tool.
- Logs every prompt and raw response for traceability.
- Automatic retry on rate limits, CSV export.
Image: assets/pilot-screenshot.png, caption: "Illustrative pilot data."
Status and Next Steps (simple 3-step horizontal timeline, orange marker on current step)
- Done: domain selection, literature review
- In progress: architecture, pipeline design
- Next: dataset expansion, base paper validation, full model runs, statistical analysis
References (24pt)
1. Huang et al., Large Language Models Cannot Self-Correct Reasoning Yet, ICLR 2024
2. Tyen et al., LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location, ACL Findings 2024
3. Tsui, Self-Correction Bench, COLM 2026
4. Madaan et al., Self-Refine, NeurIPS 2023
5. Yuan et al., Hidden Error Awareness in Chain-of-Thought Reasoning, 2026
6. Cobbe et al., Training Verifiers to Solve Math Word Problems, 2021

## Constraints
- No results section. Do not invent data, numbers, charts, logos, or images.
- Do not add colors, fonts, icons, or decoration beyond those specified.
- Do not paraphrase or "improve" the content text.

## Workflow for every diagram task
1. Read this file.
2. Create or reuse diagrams/audit.svg so the character is identical everywhere.
3. Write the SVG to /diagrams/<name>.svg.
4. Open it in the browser preview, take a screenshot, and inspect it against the rules above (overlap, clipped text, colors, minimum size, character consistency).
5. Fix any violation and re-check. Do at least one review pass.
6. Reply with one line saying what was created. Do not paste the SVG code in chat.

## Workflow for the poster task
1. Confirm all six diagrams exist in /diagrams.
2. Build poster.html: one self-contained file, inline CSS, diagrams embedded inline, CSS @page { size: 841mm 1189mm; margin: 0 }, mm units, live HTML text.
3. Render to PDF (poster.pdf) and PNG preview (poster-preview.png) using headless Chrome or Playwright.
4. Inspect the preview: nothing overflows, column bottoms align, no text under 24pt, every content line matches this file exactly, only the listed colors appear. Fix and re-render. At least one review pass.
5. Deliver poster.html, poster.pdf, poster-preview.png.