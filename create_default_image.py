from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
profile_pics_dir = BASE_DIR / 'media' / 'profile_pics'
profile_pics_dir.mkdir(parents=True, exist_ok=True)

img = Image.new('RGB', (400, 400), color='#ec4899')

draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 150)
except:
    font = ImageFont.load_default()

text = "?"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
position = ((400 - text_width) // 2, (400 - text_height) // 2 - 20)

draw.text(position, text, fill='white', font=font)

output_path = profile_pics_dir / 'default.jpg'
img.save(output_path, 'JPEG', quality=95)

print(f'Immagine default creata: {output_path}')
