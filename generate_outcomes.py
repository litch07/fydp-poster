import os
import subprocess

def check_svg(filepath):
    result = subprocess.run(['python', 'tools/check_svg.py', filepath], capture_output=True, text=True)
    return result.stdout + result.stderr

audit_defs = """  <defs>
    <g id="robot-base">
      <line x1="50" y1="15" x2="50" y2="25" stroke="#1F3A5F" stroke-width="3" stroke-linecap="round"/>
      <circle cx="50" cy="15" r="4" fill="#E8742A" stroke="none"/>
      <rect x="25" y="25" width="50" height="40" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
      <circle cx="38" cy="38" r="6" fill="white" stroke="#1F3A5F" stroke-width="3"/>
      <circle cx="62" cy="38" r="6" fill="white" stroke="#1F3A5F" stroke-width="3"/>
      <rect x="35" y="65" width="30" height="35" rx="6" fill="#1F3A5F" stroke="none"/>
    </g>
    <g id="audit-happy">
      <use href="#robot-base" />
      <circle cx="38" cy="38" r="2.5" fill="#1F3A5F" />
      <circle cx="62" cy="38" r="2.5" fill="#1F3A5F" />
      <path d="M 44 50 Q 50 56 56 50" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 35 72 Q 20 60 20 45" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 65 72 Q 80 60 80 45" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>
    <g id="audit-worried">
      <use href="#robot-base" />
      <circle cx="39" cy="41" r="2.5" fill="#1F3A5F" />
      <circle cx="61" cy="41" r="2.5" fill="#1F3A5F" />
      <ellipse cx="50" cy="53" rx="3" ry="4" fill="#1F3A5F" stroke="none"/>
      <path d="M 35 75 Q 25 70 20 50" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 65 75 Q 75 70 80 50" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>
  </defs>"""

svg_content = f"""<svg width="216" height="150" viewBox="0 0 216 150" xmlns="http://www.w3.org/2000/svg" font-family="Carlito, sans-serif">
{audit_defs}
  <rect x="0" y="0" width="216" height="150" fill="transparent" stroke="none" />

  <!-- Headers -->
  <text x="85" y="18" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Final: Correct</text>
  <text x="176" y="18" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Final: Wrong</text>

  <text x="40" y="48" font-size="8.5" fill="#222222" text-anchor="end" data-free="1">Initial:</text>
  <text x="40" y="58" font-size="8.5" fill="#222222" text-anchor="end" data-free="1">Correct</text>

  <text x="40" y="118" font-size="8.5" fill="#222222" text-anchor="end" data-free="1">Initial:</text>
  <text x="40" y="128" font-size="8.5" fill="#222222" text-anchor="end" data-free="1">Wrong</text>

  <!-- CC Cell -->
  <rect x="45" y="25" width="80" height="55" rx="6" fill="#E3F1EA" stroke="none"/>
  <text x="50" y="45" font-size="16" font-weight="bold" fill="#1F3A5F" data-free="1">CC</text>
  <text x="50" y="60" font-size="8.5" fill="#222222" data-free="1">Correct-</text>
  <text x="50" y="72" font-size="8.5" fill="#222222" data-free="1">to-Correct</text>
  <use href="#audit-happy" transform="translate(90, 28) scale(0.3)" />

  <!-- CW Cell -->
  <rect x="136" y="25" width="80" height="55" rx="6" fill="#F7E3E2" stroke="none"/>
  <text x="141" y="45" font-size="16" font-weight="bold" fill="#1F3A5F" data-free="1">CW</text>
  <text x="141" y="60" font-size="8.5" fill="#222222" data-free="1">Correct-</text>
  <text x="141" y="72" font-size="8.5" fill="#222222" data-free="1">to-Wrong</text>
  <use href="#audit-worried" transform="translate(181, 28) scale(0.3)" />
  <g stroke="#E8742A" stroke-width="1.5" fill="none">
    <path d="M 190 62 Q 196 55 202 62" />
    <polygon points="202,62 199,59 205,59" fill="#E8742A" stroke="none"/>
  </g>
  <text x="196" y="72" font-size="7.1" fill="#E8742A" text-anchor="middle" data-caption="1">Damage</text>

  <!-- WC Cell -->
  <rect x="45" y="95" width="80" height="55" rx="6" fill="#E3F1EA" stroke="none"/>
  <text x="50" y="115" font-size="16" font-weight="bold" fill="#1F3A5F" data-free="1">WC</text>
  <text x="50" y="130" font-size="8.5" fill="#222222" data-free="1">Wrong-</text>
  <text x="50" y="142" font-size="8.5" fill="#222222" data-free="1">to-Correct</text>
  <use href="#audit-happy" transform="translate(90, 98) scale(0.3)" />
  <g stroke="#E8742A" stroke-width="1.5" fill="none">
    <path d="M 99 132 Q 105 125 111 132" />
    <polygon points="111,132 108,129 114,129" fill="#E8742A" stroke="none"/>
  </g>
  <text x="105" y="142" font-size="7.1" fill="#E8742A" text-anchor="middle" data-caption="1">Correction</text>

  <!-- WW Cell -->
  <rect x="136" y="95" width="80" height="55" rx="6" fill="#F7E3E2" stroke="none"/>
  <text x="141" y="115" font-size="16" font-weight="bold" fill="#1F3A5F" data-free="1">WW</text>
  <text x="141" y="130" font-size="8.5" fill="#222222" data-free="1">Wrong-</text>
  <text x="141" y="142" font-size="8.5" fill="#222222" data-free="1">to-Wrong</text>
  <use href="#audit-worried" transform="translate(181, 98) scale(0.3)" />

</svg>"""

with open('diagrams/fit/outcomes.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("outcomes.svg:", check_svg('diagrams/fit/outcomes.svg'))
