# BikeRental (mini_api)

This project is a Flask backend with a React frontend (Vite).

Quick start (development):

1. Activate Python venv and install requirements (if not done):

```powershell
# BikeRental (mini_api)

This project is a Flask backend with a React frontend (Vite).

Quick start (development):

1. Activate Python venv and install requirements (if not done):

```powershell
# BikeRental (mini_api)

This project is a Flask backend with a React frontend (Vite).

Quick start (development)

1. Activate Python venv and install requirements (if not done):

```powershell
cd "C:\Users\Le MADISON\OneDrive\Desktop\mini_api"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

1. Start the backend (Flask):

```powershell
cd "C:\Users\Le MADISON\OneDrive\Desktop\mini_api"
.\.venv\Scripts\python.exe app.py
```

1. Start the frontend dev server (optional):

```powershell
cd "C:\Users\Le MADISON\OneDrive\Desktop\mini_api\frontend"
npm install
npm run dev
# open http://localhost:3000
```

Production (serve built frontend via Flask)

1. Build the frontend:

```powershell
cd "C:\Users\Le MADISON\OneDrive\Desktop\mini_api\frontend"
npm run build
```

1. Start Flask. The app will serve the production build under `/app/` (for example: [http://127.0.0.1:5000/app/](http://127.0.0.1:5000/app/)).

Notes

- API endpoints:

- `GET /api/bikes`
- `POST /api/register`
- `POST /api/login`
- `POST /api/reservations` (requires authenticated session)
- `GET /api/my_reservations` (requires authenticated session)
- `GET /api/me`

- Admin account (created during DB init): username `admin`, password `admin`.

If you want a public URL for sharing (ngrok or similar), tell me and I'll guide you through it.

Fetch real bike photos (optional)

To replace placeholder images with real photos, two helper scripts are provided in the `scripts/` folder:

- `scripts/download_images.ps1` — PowerShell script that downloads a small set of curated bike photos into `static/img/`.
- `scripts/apply_local_images.py` — Python script that updates existing `BikeType.image_url` records in the database to point to the downloaded local images (e.g. `/static/img/vtt.jpg`).

Usage (Windows PowerShell):

```powershell
cd "C:\Users\Le MADISON\OneDrive\Desktop\mini_api"
# run the downloader (will create static/img/ and save files)
.\scripts\download_images.ps1

# then update DB entries to use local images
.\.venv\Scripts\python.exe scripts\apply_local_images.py
```

Notes on images

- The script downloads images from Unsplash (free to use with attribution). If you prefer other sources, open `scripts/download_images.ps1` and replace the URLs.
- After running `apply_local_images.py`, the API will return local image URLs such as `/static/img/vtt.jpg` which are served by Flask.

Credits and license

Images come from Unsplash or other public sources; attribute as needed when publishing.
