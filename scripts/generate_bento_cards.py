import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJECTS = [
    {
        "id": "tracesearch",
        "name": "TraceSearch",
        "category": "AI Research",
        "accent": (45, 212, 191),   # #2DD4BF Teal / Emerald
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/tracesearch.png",
        "url": "https://github.com/mizan989/TraceSearch-AI_Researcher"
    },
    {
        "id": "novault",
        "name": "NoVAult",
        "category": "Security Vault",
        "accent": (56, 189, 248),   # #38BDF8 Cyber Blue
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/novault.png",
        "url": "https://github.com/mizan989/NoVAult-Password_Manager"
    },
    {
        "id": "loosenotion",
        "name": "LooseNotion",
        "category": "Workspace",
        "accent": (167, 139, 250),  # #A78BFA Purple
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/loosenotion.png",
        "url": "https://github.com/mizan989/LooseNotion-Notion_Clone"
    },
    {
        "id": "cybersentinel",
        "name": "CyberSentinel",
        "category": "Scanner",
        "accent": (248, 113, 113),  # #F87171 Red / Coral
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/cybersentinel.png",
        "url": "https://github.com/mizan989/CyberSentinel-Vulnerability_Scanner"
    },
    {
        "id": "skylio",
        "name": "Skylio",
        "category": "Weather UI",
        "accent": (251, 191, 36),   # #FBBF24 Amber / Gold
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/skylio.png",
        "url": "https://github.com/mizan989/Skylio-Weather_App"
    },
    {
        "id": "calcverse",
        "name": "CalcVerse",
        "category": "Calculator",
        "accent": (52, 211, 153),   # #34D399 Green
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/calcverse.png",
        "url": "https://github.com/mizan989/CalcVerse-Scientific_Calculator"
    },
    {
        "id": "storebox",
        "name": "Storebox",
        "category": "Motion Platform",
        "accent": (251, 146, 60),   # #FB923C Orange
        "logo_path": "d:/PROJECTS/mizan989/assets/projects/storebox.png",
        "url": "https://github.com/mizan989/Storebox_clone"
    }
]

def create_bento_tile_png(p, target_w=144, target_h=140, scale=2):
    """
    Creates a Bento App Tile at 2x resolution.
    Target display size: 144px x 140px
    Internal canvas: 288px x 280px
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
    
    # Card surface fill: dark glass (#161b22)
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

    # 4. Logo Container & Logo
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

    # Load and place project logo
    logo_raw = Image.open(p["logo_path"]).convert('RGBA')
    logo_size = int(38 * scale)
    logo_raw = logo_raw.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    logo_px = icon_x + (icon_box_size - logo_size) // 2
    logo_py = icon_y + (icon_box_size - logo_size) // 2
    im.paste(logo_raw, (logo_px, logo_py), logo_raw)

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

def main():
    out_dir = "d:/PROJECTS/mizan989/assets/projects"
    os.makedirs(out_dir, exist_ok=True)
    
    for p in PROJECTS:
        tile_im = create_bento_tile_png(p, target_w=144, target_h=140, scale=2)
        tile_path = os.path.join(out_dir, f"tile-{p['id']}.png")
        tile_im.save(tile_path, "PNG", optimize=True)
        print(f"Generated {tile_path} ({os.path.getsize(tile_path)} bytes)")

if __name__ == "__main__":
    main()
