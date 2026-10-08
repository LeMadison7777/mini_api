# PowerShell script to download a small set of curated bike photos into static/img/
# This script does not run automatically; run it manually from project root.

$images = @(
    @{ name = 'vtt.jpg'; url = 'https://images.unsplash.com/photo-1519985176271-adb1088fa94c?w=1200&q=80&auto=format&fit=crop' },
    @{ name = 'electrique.jpg'; url = 'https://images.unsplash.com/photo-1520975911964-4834a2a9b9a6?w=1200&q=80&auto=format&fit=crop' },
    @{ name = 'route.jpg'; url = 'https://images.unsplash.com/photo-1509395176047-4a66953fd231?w=1200&q=80&auto=format&fit=crop' },
    @{ name = 'urbain.jpg'; url = 'https://images.unsplash.com/photo-1504198453319-5ce911bafcde?w=1200&q=80&auto=format&fit=crop' }
)

$dest = Join-Path -Path $PSScriptRoot -ChildPath '..\static\img'
if (-not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest | Out-Null }

foreach ($img in $images) {
    $out = Join-Path -Path $dest -ChildPath $img.name
    Write-Host "Downloading $($img.url) -> $out"
    try {
        Invoke-WebRequest -Uri $img.url -OutFile $out -UseBasicParsing
    } catch {
        Write-Warning "Failed to download $($img.url): $_"
    }
}

Write-Host "Done. Verify files in $dest"
