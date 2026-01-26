import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

media_folders = [
    'media',
    'media/profile_pics',
    'media/cover_photos',
    'media/post_images',
]

for folder in media_folders:
    folder_path = BASE_DIR / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    print(f'Created: {folder_path}')

print('\nCartelle media create con successo!')
print('IMPORTANTE: Aggiungi un\'immagine default in media/profile_pics/default.jpg')
