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
    <g id="audit-mirror">
      <use href="#robot-base" />
      <circle cx="35" cy="38" r="2.5" fill="#1F3A5F" />
      <circle cx="59" cy="38" r="2.5" fill="#1F3A5F" />
      <line x1="46" y1="52" x2="54" y2="52" stroke="#1F3A5F" stroke-width="3" stroke-linecap="round"/>
      <path d="M 35 75 L 15 65" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 65 75 Q 75 80 75 95" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
      <line x1="15" y1="65" x2="5" y2="75" stroke="#1F3A5F" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="18" cy="55" rx="8" ry="12" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
      <path d="M 14 50 A 6 9 0 0 1 20 50" stroke="#1F3A5F" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.3"/>
    </g>
  </defs>"""

svg_content = f"""<svg width="376" height="92" viewBox="0 0 376 92" xmlns="http://www.w3.org/2000/svg" font-family="Carlito, sans-serif">
{audit_defs}
  <rect x="0" y="0" width="376" height="92" fill="transparent" stroke="none" />

  <!-- Bottom text -->
  <text x="188" y="88" font-size="8.5" fill="#1F3A5F" text-anchor="middle" data-free="1">Natural errors · Three domains · Correction + Damage Rate</text>

  <!-- Left Panel: Existing work -->
  <rect x="0" y="0" width="183" height="75" rx="6" fill="#F4F6F8" stroke="none" />
  <text x="91.5" y="14" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Existing work</text>
  
  <use href="#robot-base" transform="translate(76.5, 25) scale(0.3)" />

  <!-- Lines -->
  <g stroke="#1F3A5F" stroke-width="1.5" opacity="0.5" stroke-dasharray="2,2">
    <line x1="55" y1="36" x2="80" y2="40" />
    <line x1="55" y1="58" x2="80" y2="50" />
    <line x1="125" y1="36" x2="103" y2="40" />
    <line x1="125" y1="58" x2="103" y2="50" />
  </g>

  <!-- Ext tools (Wrench) -->
  <g stroke="#1F3A5F" stroke-width="1.5" fill="none">
    <circle cx="45" cy="30" r="3"/>
    <path d="M 43 32 L 37 38 L 40 41 L 46 35" />
  </g>
  <text x="32" y="30" font-size="7.1" fill="#222222" text-anchor="end" data-caption="1">External</text>
  <text x="32" y="40" font-size="7.1" fill="#222222" text-anchor="end" data-caption="1">tools</text>

  <!-- Hints (Lightbulb) -->
  <g stroke="#1F3A5F" stroke-width="1.5" fill="none">
    <path d="M 43 60 A 3 3 0 1 1 47 60 L 47 63 L 43 63 Z" />
    <line x1="45" y1="51" x2="45" y2="53" />
  </g>
  <text x="32" y="60" font-size="7.1" fill="#222222" text-anchor="end" data-caption="1">Hints</text>

  <!-- Error loc (Map pin) -->
  <g stroke="#1F3A5F" stroke-width="1.5" fill="none">
    <path d="M 135 30 Q 135 25 130 25 Q 125 25 125 30 Q 125 35 130 40 Q 135 35 135 30" />
    <circle cx="130" cy="30" r="1.5" />
  </g>
  <text x="139" y="30" font-size="7.1" fill="#222222" text-anchor="start" data-caption="1">Error</text>
  <text x="139" y="40" font-size="7.1" fill="#222222" text-anchor="start" data-caption="1">location</text>

  <!-- Reviewer (Small robot) -->
  <use href="#robot-base" transform="translate(120, 52) scale(0.18)" />
  <text x="139" y="55" font-size="7.1" fill="#222222" text-anchor="start" data-caption="1">Reviewer</text>
  <text x="139" y="65" font-size="7.1" fill="#222222" text-anchor="start" data-caption="1">model</text>


  <!-- Right Panel: ReasonAudit -->
  <rect x="193" y="0" width="183" height="75" rx="6" fill="#FDEFE5" stroke="none" />
  <text x="284.5" y="14" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">ReasonAudit</text>

  <use href="#audit-mirror" transform="translate(265, 20) scale(0.3)" />

  <!-- Lock & Label -->
  <rect x="235" y="60" width="10" height="8" rx="2" fill="white" stroke="#1F3A5F" stroke-width="1.5"/>
  <path d="M 237.5 60 V 56 A 2.5 2.5 0 0 1 242.5 56 V 60" fill="none" stroke="#1F3A5F" stroke-width="1.5"/>
  <text x="250" y="67" font-size="8.5" fill="#222222" text-anchor="start" data-free="1">Unaided self-review</text>

</svg>"""

with open('diagrams/fit/gap.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("gap.svg:", check_svg('diagrams/fit/gap.svg'))
