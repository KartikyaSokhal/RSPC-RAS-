"""Build the gallery/contact sheet from actual captured screenshots; no synthetic UI images."""
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont
root = Path(__file__).resolve().parents[1]
folder = root / 'docs/design/screenshots'
manifest = json.loads((folder / 'manifest.json').read_text())
screens = manifest['screens']
font_path = '/System/Library/Fonts/Helvetica.ttc'
try: font = ImageFont.truetype(font_path, 14)
except OSError: font = ImageFont.load_default()
columns = 5; cell_width = 300; cell_height = 290
sheet = Image.new('RGB', (columns * cell_width, 100 + math.ceil(len(screens)/columns)*cell_height), '#e7eee3')
draw = ImageDraw.Draw(sheet)
draw.text((22,20), 'PREPAL / IMPLEMENTED PRODUCT REVIEW', fill='#203d36', font=font)
draw.text((22,48), 'Actual Chromium renders | Synthetic development content | Mocked AI | Full screenshots in GALLERY.md', fill='#203d36', font=font)
lines = ['# Prepal implemented interface gallery', '', 'Captured from the working React application and isolated Django demo on 19 October 2026. **Every lesson/quiz approval here is a synthetic fixture; AI is mocked. No live Gemini calls or editorial approval are claimed.** Error fixtures are individually labeled. Admin screenshots use only the isolated demo account.', '', 'Desktop viewport: 1440 × 1000. Mobile viewport: 390 × 844. Images capture the full rendered page, so heights vary. Source: [capture script](../../scripts/capture_gallery.mjs), [manifest](screenshots/manifest.json). Original [browser prototype](prototype.html) preceded application implementation.', '', '![All implemented screens](screenshots/contact-sheet.jpg)', '', 'Automated WCAG checks and desktop/mobile journey results are recorded in [verification](../evidence/MVP_IMPLEMENTATION_VERIFICATION.md). This is not a full accessibility certification or physical-device test.', '']
for index, screen in enumerate(screens):
    image = Image.open(folder / (screen['name']+'.png')).convert('RGB')
    image.thumbnail((280, 10000))
    # Overview crops show each screen's opening viewport; linked originals remain full height.
    cropped = image.crop((0,0,image.width,min(225,image.height)))
    x=(index%columns)*cell_width+10; y=100+(index//columns)*cell_height
    sheet.paste(cropped,(x+(280-image.width)//2,y))
    draw.text((x,y+230),screen['name'],fill='#203d36',font=font)
    draw.text((x,y+251),screen['variant'],fill='#52645b',font=font)
    lines.extend([f"## {index+1}. {screen['purpose']}", '', f"**{screen['variant']} · Implemented and browser rendered.** {screen['note']}.", '', f"![{screen['purpose']}](screenshots/{screen['name']}.png)", ''])
sheet.save(folder / 'contact-sheet.jpg', quality=90)
(root / 'docs/design/GALLERY.md').write_text('\n'.join(lines))
print(f'Gallery/contact sheet generated for {len(screens)} real screenshots')
