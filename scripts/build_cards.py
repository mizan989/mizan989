import os
import base64
import io
import re
from PIL import Image

PROJECTS = [
    {
        "id": "tracesearch",
        "name": "TraceSearch",
        "subtitle": "Autonomous AI Research Engine",
        "accent": "#2DD4BF",  # Teal / Emerald
        "type": "png",
        "src": "d:/PROJECTS/mizan989/assets/projects/tracesearch.png",
        "url": "https://github.com/mizan989/TraceSearch-AI_Researcher"
    },
    {
        "id": "novault",
        "name": "NoVAult",
        "subtitle": "Zero-Knowledge Security Vault",
        "accent": "#38BDF8",  # Cyber Blue
        "type": "png",
        "src": "d:/PROJECTS/mizan989/assets/projects/novault.png",
        "url": "https://github.com/mizan989/NoVAult-Password_Manager"
    },
    {
        "id": "loosenotion",
        "name": "LooseNotion",
        "subtitle": "Collaborative Workspace & Docs",
        "accent": "#A78BFA",  # Purple
        "type": "png",
        "src": "d:/PROJECTS/mizan989/assets/projects/loosenotion.png",
        "url": "https://github.com/mizan989/LooseNotion-Notion_Clone"
    },
    {
        "id": "cybersentinel",
        "name": "CyberSentinel",
        "subtitle": "Vulnerability Scanner & CVEs",
        "accent": "#F87171",  # Red / Coral
        "type": "png",
        "src": "d:/PROJECTS/mizan989/assets/projects/cybersentinel.png",
        "url": "https://github.com/mizan989/CyberSentinel-Vulnerability_Scanner"
    },
    {
        "id": "skylio",
        "name": "Skylio",
        "subtitle": "Minimalist Precision Weather",
        "accent": "#FBBF24",  # Amber / Sun
        "type": "svg",
        "src": "d:/PROJECTS/mizan989/assets/projects/skylio.svg",
        "url": "https://github.com/mizan989/Skylio-Weather_App"
    },
    {
        "id": "calcverse",
        "name": "CalcVerse",
        "subtitle": "Modern Scientific Calculator",
        "accent": "#34D399",  # Green
        "type": "svg",
        "src": "d:/PROJECTS/mizan989/assets/projects/calcverse.svg",
        "url": "https://github.com/mizan989/CalcVerse-Scientific_Calculator"
    },
    {
        "id": "storebox",
        "name": "Storebox",
        "subtitle": "Cinema-Grade Motion Platform",
        "accent": "#FB923C",  # Orange
        "type": "svg",
        "src": "d:/PROJECTS/mizan989/assets/projects/storebox.svg",
        "url": "https://github.com/mizan989/Storebox_clone"
    }
]

def get_base64_png(path, max_dim=96):
    im = Image.open(path).convert('RGBA')
    im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')

def get_clean_svg(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    vb_match = re.search(r'viewBox=["\']([^"\']+)["\']', content)
    vb = vb_match.group(1) if vb_match else "0 0 512 512"
    inner = re.sub(r'<\?xml[^>]*\?>', '', content)
    inner = re.sub(r'<!--.*?-->', '', inner, flags=re.DOTALL)
    inner = re.sub(r'<svg[^>]*>', '', inner)
    inner = re.sub(r'</svg>', '', inner).strip()
    return vb, inner

def generate_card(p):
    """
    Card dimensions: 260px x 74px
    With 4px transparent padding on all sides to guarantee clean wrapping gutters:
    Canvas size: 268px x 82px.
    """
    canvas_w = 268
    canvas_h = 82
    pad = 4
    card_w = canvas_w - (pad * 2)  # 260
    card_h = canvas_h - (pad * 2)  # 74
    
    logo_container_size = 46
    logo_size = 38
    logo_cx = pad + 14
    logo_cy = pad + (card_h - logo_container_size) // 2
    
    logo_x = logo_cx + (logo_container_size - logo_size) // 2
    logo_y = logo_cy + (logo_container_size - logo_size) // 2

    if p["type"] == "png":
        b64 = get_base64_png(p["src"], max_dim=96)
        logo_markup = f'<image x="{logo_x}" y="{logo_y}" width="{logo_size}" height="{logo_size}" href="{b64}" />'
    else:
        vb, inner = get_clean_svg(p["src"])
        logo_markup = f'<svg x="{logo_x}" y="{logo_y}" width="{logo_size}" height="{logo_size}" viewBox="{vb}">{inner}</svg>'

    accent = p["accent"]
    name = p["name"]
    sub = p["subtitle"]
    pid = p["id"]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" fill="none">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-{pid}" x1="{pad}" y1="{pad}" x2="{pad + card_w}" y2="{pad + card_h}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#161b22" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>

    <!-- Border Gradient with Subtle Brand Accent Highlight -->
    <linearGradient id="border-{pid}" x1="{pad}" y1="{pad}" x2="{pad + card_w}" y2="{pad + card_h}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.65" />
      <stop offset="35%" stop-color="#30363d" stop-opacity="0.85" />
      <stop offset="100%" stop-color="#21262d" stop-opacity="0.5" />
    </linearGradient>

    <!-- Top Glow -->
    <linearGradient id="topglow-{pid}" x1="{pad}" y1="{pad}" x2="{pad + card_w}" y2="{pad}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.35" />
      <stop offset="45%" stop-color="{accent}" stop-opacity="0.05" />
      <stop offset="100%" stop-color="{accent}" stop-opacity="0" />
    </linearGradient>

    <!-- Logo Ambient Backlight -->
    <radialGradient id="logoglow-{pid}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.2" />
      <stop offset="100%" stop-color="{accent}" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Card Base -->
  <rect x="{pad + 0.5}" y="{pad + 0.5}" width="{card_w - 1}" height="{card_h - 1}" rx="14" fill="url(#bg-{pid})" stroke="url(#border-{pid})" stroke-width="1" />

  <!-- Top Ambient Glow Line -->
  <rect x="{pad + 1}" y="{pad + 1}" width="{card_w - 2}" height="2.5" rx="1.25" fill="url(#topglow-{pid})" />

  <!-- Logo Backlight Glow -->
  <circle cx="{logo_cx + logo_container_size // 2}" cy="{logo_cy + logo_container_size // 2}" r="26" fill="url(#logoglow-{pid})" />

  <!-- Logo Container -->
  <rect x="{logo_cx}" y="{logo_cy}" width="{logo_container_size}" height="{logo_container_size}" rx="11" fill="#21262d" stroke="#30363d" stroke-width="1" />
  {logo_markup}

  <!-- Text Group -->
  <!-- Project Title -->
  <text x="{pad + 68}" y="{pad + 31}" fill="#F0F6FC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif" font-size="14.5" font-weight="600" letter-spacing="-0.2">{name}</text>

  <!-- Accent Status Dot -->
  <circle cx="{pad + 72}" cy="{pad + 47.5}" r="3" fill="{accent}" />

  <!-- Subtitle -->
  <text x="{pad + 80}" y="{pad + 51}" fill="#8B949E" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif" font-size="11" font-weight="400">{sub}</text>

  <!-- Top-Right Action Arrow Badge -->
  <g transform="translate({pad + card_w - 24}, {pad + 14})">
    <circle cx="5" cy="5" r="7.5" fill="#21262d" fill-opacity="0.8" stroke="#30363d" stroke-width="0.8" />
    <path d="M3.2 6.8L6.8 3.2M6.8 3.2H4.4M6.8 3.2V5.6" stroke="{accent}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
  </g>
</svg>'''
    return svg

def main():
    out_dir = "d:/PROJECTS/mizan989/assets/projects"
    os.makedirs(out_dir, exist_ok=True)
    
    for p in PROJECTS:
        svg_content = generate_card(p)
        svg_path = os.path.join(out_dir, f"card-{p['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated {svg_path} ({len(svg_content)} bytes)")

    # Build responsive preview HTML
    cards_html = "\n    ".join([
        f'<a href="{p["url"]}" target="_blank" rel="noopener noreferrer"><img src="card-{p["id"]}.svg" alt="{p["name"]}" width="268" height="82" /></a>'
        for p in PROJECTS
    ])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Featured Projects Preview</title>
<style>
  body {{
    background-color: #0d1117;
    color: #e6edf3;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 40px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .preview-wrapper {{
    max-width: 896px;
    width: 100%;
    margin: 0 auto;
  }}
  h2 {{
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 16px;
    text-align: center;
    color: #ffffff;
  }}
  .readme-sim {{
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 32px 16px;
    margin-bottom: 40px;
    box-sizing: border-box;
  }}
  /* Natural wrapping centered container replicating GitHub README div */
  .projects-center {{
    text-align: center;
  }}
  .projects-center a {{
    display: inline-block;
    text-decoration: none;
    vertical-align: middle;
    transition: transform 0.18s ease;
  }}
  .projects-center a:hover {{
    transform: translateY(-2px);
  }}
  .projects-center img {{
    display: inline-block;
    vertical-align: middle;
  }}
  .sim-note {{
    color: #8b949e;
    font-size: 13px;
    text-align: center;
    margin-bottom: 24px;
  }}
  /* Mobile simulation frame */
  .mobile-frame {{
    max-width: 375px;
    margin: 0 auto;
    border: 2px dashed #38bdf8;
    border-radius: 20px;
    padding: 24px 12px;
    background: #0d1117;
    box-sizing: border-box;
  }}
  .mobile-tag {{
    text-align: center;
    font-size: 12px;
    color: #38bdf8;
    font-weight: 600;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
</style>
</head>
<body>

<div class="preview-wrapper">
  <h2>Featured Projects — Desktop View (896px GitHub Content Area)</h2>
  <p class="sim-note">Natural flex wrapping without HTML tables. Zero horizontal scrollbar.</p>
  
  <div class="readme-sim">
    <div class="projects-center">
      <h3 style="margin-top:0; font-size:18px; color:#ffffff;">Featured Projects</h3>
      <br />
      {cards_html}
    </div>
  </div>

  <h2>Featured Projects — Mobile View (375px iPhone Viewport)</h2>
  <p class="sim-note">Notice how each 268px card centers effortlessly with 50px margins. ZERO horizontal scroll!</p>
  
  <div class="mobile-frame">
    <div class="mobile-tag">📱 Mobile 375px Width Test</div>
    <div class="projects-center">
      <h3 style="margin-top:0; font-size:18px; color:#ffffff;">Featured Projects</h3>
      <br />
      {cards_html}
    </div>
  </div>
</div>

</body>
</html>'''

    preview_path = "d:/PROJECTS/mizan989/assets/projects/preview.html"
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated preview: {preview_path}")

if __name__ == "__main__":
    main()
