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
    <g id="audit-thinking">
      <use href="#robot-base" />
      <circle cx="40" cy="36" r="2.5" fill="#1F3A5F" />
      <circle cx="64" cy="36" r="2.5" fill="#1F3A5F" />
      <line x1="46" y1="52" x2="54" y2="52" stroke="#1F3A5F" stroke-width="3" stroke-linecap="round"/>
      <path d="M 35 75 Q 25 80 25 95" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 65 75 Q 75 80 70 55" stroke="#1F3A5F" stroke-width="3" fill="none" stroke-linecap="round"/>
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

svg_content = f"""<svg width="757" height="75" viewBox="0 0 757 75" xmlns="http://www.w3.org/2000/svg" font-family="Carlito, sans-serif">
{audit_defs}
  <rect x="0" y="0" width="757" height="75" fill="transparent" stroke="none" />

  <!-- Arrows -->
  <g stroke="#E8742A" stroke-width="3" fill="none">
    <line x1="75" y1="37.5" x2="100" y2="37.5" />
    <polygon points="100,37.5 93,33 93,42" fill="#E8742A" stroke="none" />
    
    <line x1="190" y1="37.5" x2="215" y2="37.5" />
    <polygon points="215,37.5 208,33 208,42" fill="#E8742A" stroke="none" />
    
    <line x1="305" y1="37.5" x2="330" y2="37.5" />
    <polygon points="330,37.5 323,33 323,42" fill="#E8742A" stroke="none" />
    
    <!-- Split -->
    <path d="M 395 37.5 L 410 37.5 L 410 20 L 425 20" />
    <polygon points="425,20 418,15.5 418,24.5" fill="#E8742A" stroke="none" />
    <path d="M 410 37.5 L 410 55 L 425 55" />
    <polygon points="425,55 418,50.5 418,59.5" fill="#E8742A" stroke="none" />
    
    <!-- Rejoin -->
    <path d="M 545 20 L 560 20 L 560 37.5 L 575 37.5" />
    <path d="M 545 55 L 560 55 L 560 37.5" />
    <polygon points="575,37.5 568,33 568,42" fill="#E8742A" stroke="none" />
    
    <line x1="650" y1="37.5" x2="675" y2="37.5" />
    <polygon points="675,37.5 668,33 668,42" fill="#E8742A" stroke="none" />
  </g>

  <!-- N1: Question Bank -->
  <rect x="5" y="10" width="70" height="55" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <rect x="25" y="20" width="30" height="20" rx="3" fill="white" stroke="#1F3A5F" stroke-width="2"/>
  <path d="M 28 17 L 55 17" fill="none" stroke="#1F3A5F" stroke-width="2"/>
  <text x="40" y="55" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Question Bank</text>

  <!-- N2: Stage 1 -->
  <rect x="100" y="5" width="90" height="65" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <use href="#audit-thinking" transform="translate(132.5, 6) scale(0.25)" />
  <text x="145" y="42" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Stage 1:</text>
  <text x="145" y="53" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Initial answer</text>
  <text x="145" y="64" font-size="7.1" fill="#222222" text-anchor="middle" data-caption="1">no hints</text>

  <!-- N3: Stage 2 -->
  <rect x="215" y="5" width="90" height="65" rx="6" fill="#FDEFE5" stroke="#1F3A5F" stroke-width="3"/>
  <use href="#audit-mirror" transform="translate(247.5, 6) scale(0.25)" />
  <text x="260" y="42" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Stage 2:</text>
  <text x="260" y="53" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Self-review</text>
  <text x="260" y="64" font-size="7.1" fill="#222222" text-anchor="middle" data-caption="1">fixed prompt</text>

  <!-- N4: Final answer -->
  <rect x="330" y="10" width="65" height="55" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <text x="362.5" y="34" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Final</text>
  <text x="362.5" y="46" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">answer</text>

  <!-- N5: Grading split -->
  <rect x="425" y="5" width="120" height="30" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <text x="485" y="18" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Numeric / multiple choice:</text>
  <text x="485" y="28" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">auto-graded</text>
  
  <rect x="425" y="40" width="120" height="30" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <text x="485" y="53" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Open-ended:</text>
  <text x="485" y="63" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">manual grading</text>

  <!-- N6: Outcome bucket -->
  <rect x="575" y="10" width="75" height="55" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <circle cx="606" cy="24" r="4" fill="#1F3A5F"/>
  <circle cx="618" cy="24" r="4" fill="#1F3A5F"/>
  <circle cx="606" cy="36" r="4" fill="#1F3A5F"/>
  <circle cx="618" cy="36" r="4" fill="#1F3A5F"/>
  <text x="612.5" y="52" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Outcome</text>
  <text x="612.5" y="62" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">bucket</text>

  <!-- N7: Metrics -->
  <rect x="675" y="10" width="75" height="55" rx="6" fill="#F4F6F8" stroke="#1F3A5F" stroke-width="3"/>
  <rect x="700" y="32" width="6" height="10" fill="#1F3A5F"/>
  <rect x="710" y="24" width="6" height="18" fill="#1F3A5F"/>
  <rect x="720" y="16" width="6" height="26" fill="#1F3A5F"/>
  <text x="712.5" y="58" font-size="8.5" fill="#222222" text-anchor="middle" data-free="1">Metrics</text>

</svg>"""

with open('diagrams/fit/pipeline.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("pipeline.svg:", check_svg('diagrams/fit/pipeline.svg'))
