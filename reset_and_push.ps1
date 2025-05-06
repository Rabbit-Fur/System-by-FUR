
# PowerShell-Skript: Bereinigt Projekt, entpackt Patch, committed & pusht via Git
$repoRoot = Get-Location
$patchZip = "$repoRoot\GGWbyFUR_final_clean.zip"

Write-Host "🔄 Lösche alte Dateien (außer .git)..."
Get-ChildItem -Path $repoRoot -Force |
    Where-Object { $_.Name -ne ".git" -and $_.Name -ne "GGWbyFUR_final_clean.zip" } |
    Remove-Item -Force -Recurse

Write-Host "📦 Entpacke Patch-ZIP..."
Expand-Archive -Path $patchZip -DestinationPath $repoRoot -Force

$nestedPath = Join-Path $repoRoot "GGWbyFUR"
if (Test-Path $nestedPath) {
    Write-Host "📁 Verschiebe Inhalte aus GGWbyFUR/ nach Root..."
    Get-ChildItem -Path $nestedPath -Force | Move-Item -Destination $repoRoot
    Remove-Item -Recurse -Force $nestedPath
}

Write-Host "💾 Git Add, Commit & Push"
git add -A
git commit -m "chore: wipe repo and apply final clean patch"
git push

Write-Host "✅ Erfolgreich gepusht!"
