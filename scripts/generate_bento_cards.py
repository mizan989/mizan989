import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "projects")

PROJECTS = [
    {
        "id": "tracesearch",
        "name": "TraceSearch",
        "category": "AI Research",
        "accent": (45, 212, 191),   # #2DD4BF Teal / Emerald
        "logo_path": os.path.join(ASSETS_DIR, "tracesearch.png"),
        "url": "https://github.com/mizan989/TraceSearch-AI_Researcher"
    },
    {
        "id": "novault",
        "name": "NoVAult",
        "category": "Security Vault",
        "accent": (56, 189, 248),   # #38BDF8 Cyber Blue
        "logo_path": os.path.join(ASSETS_DIR, "novault.png"),
        "url": "https://github.com/mizan989/NoVAult-Password_Manager"
    },
    {
        "id": "loosenotion",
        "name": "LooseNotion",
        "category": "Workspace",
        "accent": (167, 139, 250),  # #A78BFA Purple
        "logo_path": os.path.join(ASSETS_DIR, "loosenotion.png"),
        "url": "https://github.com/mizan989/LooseNotion-Notion_Clone"
    },
    {
        "id": "cybersentinel",
        "name": "CyberSentinel",
        "category": "Scanner",
        "accent": (248, 113, 113),  # #F87171 Red / Coral
        "logo_path": os.path.join(ASSETS_DIR, "cybersentinel.png"),
        "url": "https://github.com/mizan989/CyberSentinel-Vulnerability_Scanner"
    },
    {
        "id": "skylio",
        "name": "Skylio",
        "category": "Weather App",
        "accent": (251, 191, 36),   # #FBBF24 Amber / Gold
        "logo_path": os.path.join(ASSETS_DIR, "skylio.png"),
        "url": "https://github.com/mizan989/Skylio-Weather_App"
    },
    {
        "id": "calcverse",
        "name": "CalcVerse",
        "category": "Calculator",
        "accent": (52, 211, 153),   # #34D399 Green
        "logo_path": os.path.join(ASSETS_DIR, "calcverse.png"),
        "url": "https://github.com/mizan989/CalcVerse-Scientific_Calculator"
    },
    {
        "id": "storebox",
        "name": "Storebox",
        "category": "Digital Marketing",
        "accent": (251, 146, 60),   # #FB923C Orange
        "logo_path": os.path.join(ASSETS_DIR, "storebox.png"),
        "url": "https://github.com/mizan989/Storebox_clone"
    }
]

def get_cropped_logo(logo_path):
    """
    Loads logo image and crops to its non-transparent bounding box
    to ensure all logos have identical framing and zero stray margins.
    """
    raw = Image.open(logo_path).convert('RGBA')
    bbox = raw.getbbox()
    if bbox:
        raw = raw.crop(bbox)
    return raw

def create_bento_tile_png(p, target_w=144, target_h=140, scale=2):
    """
    Creates a Bento App Tile at 2x Retina resolution (288px x 280px).
    Target display size: 144px x 140px.
    All logos are equalized to the exact same size inside the container.
    """
    w = target_w * scale
    h = target_h * scale
    accent = p["accent"]
    
    # Base transparent canvas
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    # 1. Subtle Ambient Glow behind logo
    glow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_cx, glow_cy = w // 2, int(48 * scale)
    glow_r = int(38 * scale)
    glow_draw.ellipse(
        (glow_cx - glow_r, glow_cy - glow_r, glow_cx + glow_r, glow_cy + glow_r),
        fill=(accent[0], accent[1], accent[2], 42)
    )
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=16 * scale))
    im = Image.alpha_composite(im, glow_layer)
    draw = ImageDraw.Draw(im)

    # 2. Card Background: #161b22 with rounded corners
    card_margin = 2 * scale
    card_rect = (card_margin, card_margin, w - card_margin, h - card_margin)
    card_radius = int(16 * scale)
    
    draw.rounded_rectangle(
        card_rect,
        radius=card_radius,
        fill=(22, 27, 34, 250),
        outline=(48, 54, 61, 230),
        width=int(1.5 * scale)
    )

    # 3. Top Accent Glow Bar
    top_glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    top_draw = ImageDraw.Draw(top_glow)
    top_draw.rounded_rectangle(
        (card_margin + int(12 * scale), card_margin, w - card_margin - int(12 * scale), card_margin + int(2.5 * scale)),
        radius=int(1.5 * scale),
        fill=(accent[0], accent[1], accent[2], 190)
    )
    top_glow = top_glow.filter(ImageFilter.GaussianBlur(radius=1.5 * scale))
    im = Image.alpha_composite(im, top_glow)
    draw = ImageDraw.Draw(im)

    # 4. Logo Container & Logo (Unified exact size for all logos)
    icon_box_size = int(50 * scale)
    icon_x = (w - icon_box_size) // 2
    icon_y = int(20 * scale)
    
    # Icon container background (#21262d)
    draw.rounded_rectangle(
        (icon_x, icon_y, icon_x + icon_box_size, icon_y + icon_box_size),
        radius=int(12 * scale),
        fill=(33, 38, 45, 255),
        outline=(48, 54, 61, 220),
        width=int(1.2 * scale)
    )

    # Load, crop, and place project logo with identical dimensions
    logo_raw = get_cropped_logo(p["logo_path"])
    logo_size = int(38 * scale)
    logo_resized = logo_raw.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    logo_px = icon_x + (icon_box_size - logo_size) // 2
    logo_py = icon_y + (icon_box_size - logo_size) // 2
    im.paste(logo_resized, (logo_px, logo_py), logo_resized)

    # 5. Project Name Typography
    font_title = ImageFont.truetype("segoeuib.ttf", int(14.5 * scale))
    name = p["name"]
    bbox = font_title.getbbox(name)
    title_w = bbox[2] - bbox[0]
    title_x = (w - title_w) // 2
    title_y = int(79 * scale)
    draw.text((title_x, title_y), name, fill=(240, 246, 252, 255), font=font_title)

    # 6. Category Pill Badge
    font_cat = ImageFont.truetype("segoeui.ttf", int(10.5 * scale))
    cat = p["category"]
    cat_bbox = font_cat.getbbox(cat)
    cat_text_w = cat_bbox[2] - cat_bbox[0]
    pill_w = cat_text_w + int(14 * scale)
    pill_h = int(18 * scale)
    pill_x = (w - pill_w) // 2
    pill_y = int(104 * scale)
    
    # Pill background
    draw.rounded_rectangle(
        (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
        radius=int(9 * scale),
        fill=(33, 38, 45, 220),
        outline=(48, 54, 61, 160),
        width=int(0.8 * scale)
    )
    
    # Pill text in accent color
    draw.text((pill_x + int(7 * scale), pill_y + int(2.5 * scale)), cat, fill=(accent[0], accent[1], accent[2], 255), font=font_cat)

    return im

def create_bento_tile_svg(p, target_w=144, target_h=140):
    """
    Creates a responsive, dark-glass Bento App Tile SVG (144px x 140px).
    Matches the exact layout, geometry, typography, and logo proportions as the Retina PNG.
    """
    w = target_w
    h = target_h
    accent_rgb = p["accent"]
    accent_hex = f"#{accent_rgb[0]:02x}{accent_rgb[1]:02x}{accent_rgb[2]:02x}"
    pid = p["id"]
    name = p["name"]
    category = p["category"]

    # Prepare base64 PNG of cropped logo at 2x resolution (76x76) for crisp rendering
    logo_raw = get_cropped_logo(p["logo_path"])
    logo_size_px = 76
    logo_im = logo_raw.resize((logo_size_px, logo_size_px), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    logo_im.save(buf, format='PNG', optimize=True)
    b64_logo = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"

    # Calculate pill width dynamically based on font metrics
    try:
        font_cat = ImageFont.truetype("segoeui.ttf", 21)
        cb = font_cat.getbbox(category)
        pill_w = (cb[2] - cb[0]) / 2 + 14
    except Exception:
        pill_w = len(category) * 6.5 + 16
    pill_h = 18
    pill_x = (w - pill_w) / 2
    pill_y = 104

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  <defs>
    <radialGradient id="glow-{pid}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent_hex}" stop-opacity="0.32" />
      <stop offset="100%" stop-color="{accent_hex}" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="topglow-{pid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_hex}" stop-opacity="0" />
      <stop offset="20%" stop-color="{accent_hex}" stop-opacity="0.8" />
      <stop offset="80%" stop-color="{accent_hex}" stop-opacity="0.8" />
      <stop offset="100%" stop-color="{accent_hex}" stop-opacity="0" />
    </linearGradient>
  </defs>

  <!-- Ambient Glow Behind Logo -->
  <circle cx="72" cy="48" r="38" fill="url(#glow-{pid})" />

  <!-- Card Background Surface (#161b22) -->
  <rect x="2" y="2" width="140" height="136" rx="16" fill="#161b22" stroke="#30363d" stroke-width="1.5" />

  <!-- Top Accent Bar -->
  <rect x="14" y="2" width="116" height="2.5" rx="1.25" fill="url(#topglow-{pid})" />

  <!-- Logo Container (#21262d) -->
  <rect x="47" y="20" width="50" height="50" rx="12" fill="#21262d" stroke="#30363d" stroke-width="1.2" />

  <!-- Project Logo (Uniform 38x38 Size) -->
  <image x="53" y="26" width="38" height="38" href="{b64_logo}" />

  <!-- Project Name -->
  <text x="72" y="93.5" fill="#F0F6FC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="14.5" font-weight="700" letter-spacing="-0.2" text-anchor="middle">{name}</text>

  <!-- Category Pill Badge -->
  <rect x="{pill_x:.1f}" y="{pill_y}" width="{pill_w:.1f}" height="{pill_h}" rx="9" fill="#21262d" fill-opacity="0.85" stroke="#30363d" stroke-width="0.8" />
  <text x="72" y="{pill_y + 12.5}" fill="{accent_hex}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="10.5" font-weight="500" text-anchor="middle">{category}</text>
</svg>'''
    return svg

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    print("Generating Bento App Tiles (both 2x Retina PNG and Vector SVG)...")
    for p in PROJECTS:
        pid = p["id"]
        
        # 1. Generate 2x Retina PNG (288x280 displayed at 144x140)
        tile_im = create_bento_tile_png(p, target_w=144, target_h=140, scale=2)
        tile_png_path = os.path.join(ASSETS_DIR, f"tile-{pid}.png")
        tile_im.save(tile_png_path, "PNG", optimize=True)
        print(f"Generated PNG: {tile_png_path} ({os.path.getsize(tile_png_path)} bytes)")

        # 2. Generate Bento Tile SVG (144x140)
        svg_content = create_bento_tile_svg(p, target_w=144, target_h=140)
        tile_svg_path = os.path.join(ASSETS_DIR, f"tile-{pid}.svg")
        with open(tile_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated SVG: {tile_svg_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    main()
