import os
import requests

images = {
    'velo-vtt.jpg'#: 'https://source.unsplash.com/800x600/?mountain-bike',
    'velo5.jpg'#: 'https://source.unsplash.com/800x600/?electric-bike',
    'velo3.jpg'#: 'https://source.unsplash.com/800x600/?road-bike',
    'velo4.jpg'#: 'https://source.unsplash.com/800x600/?city-bike',
}

out_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'img')
os.makedirs(out_dir, exist_ok=True)

for name, url in images.items():
    path = os.path.join(out_dir, name)
    print('Downloading', url, '->', path)
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)
        print('Saved', path)
    except Exception as e:
        print('Failed to download', url, '->', e)

print('Done')
