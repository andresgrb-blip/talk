#!/usr/bin/env python3
"""
Script per generare le icone PWA per Talkie
Crea icone di diverse dimensioni per Android/iOS
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
icons_dir = BASE_DIR / 'static' / 'icons'
icons_dir.mkdir(parents=True, exist_ok=True)

sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    img = Image.new('RGB', (size, size), color='#db2777')
    draw = ImageDraw.Draw(img)
    
    try:
        font_size = int(size * 0.4)
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', font_size)
    except:
        font = ImageFont.load_default()
    
    text = 'T'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2 - int(size * 0.05))
    
    draw.text(position, text, fill='white', font=font)
    
    output_path = icons_dir / f'icon-{size}x{size}.png'
    img.save(output_path, 'PNG')
    print(f'✓ Creata: {output_path}')

print(f'\n✓ Tutte le {len(sizes)} icone PWA sono state create in: {icons_dir}')
