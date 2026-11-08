# setup_github.ps1 — transfer VPP_Article6_Project to the existing GitHub repo.
# Requires: Git for Windows (https://git-scm.com/download/win)
# Target repo: https://github.com/amirhassanli/Reserve-Deliverability-and-Throughput-Aging-in-Risk-Aware-Two-Stage-VPP-Bidding
# (already exists on GitHub with 1 commit = a bare README; we overwrite it with the full project.)

$ErrorActionPreference = "Stop"
$proj = "C:\Users\Mahboobian\Documents\VPP_Article6_Project"
Set-Location $proj

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git not found. Install Git for Windows first:" -ForegroundColor Yellow
    Write-Host "  winget install --id Git.Git -e --source winget" -ForegroundColor Cyan
    Write-Host "Then re-run this script."
    exit 1
}

if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

git config user.name  "Amir Hassanli"
git config user.email "amir.hassanli@example.com"   # <-- change to your email

git add .
git commit -m "Initial commit: full VPP Article 6 project (manuscript + code + data + results + reports + scripts)"

$remote = "https://github.com/amirhassanli/Reserve-Deliverability-and-Throughput-Aging-in-Risk-Aware-Two-Stage-VPP-Bidding.git"
git remote remove origin 2>$null
git remote add origin $remote

# The repo already has 1 commit (a bare README). We overwrite it cleanly.
git push -u origin main --force
Write-Host ""
Write-Host "Done. Open the repo:" -ForegroundColor Green
Write-Host "  https://github.com/amirhassanli/Reserve-Deliverability-and-Throughput-Aging-in-Risk-Aware-Two-Stage-VPP-Bidding" -ForegroundColor Cyan
