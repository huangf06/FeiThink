Set-Location E:\GitStack
Write-Host "Pulling latest changes from GitHub..."
git pull origin main --rebase
Write-Host "Pushing your changes..."
git push origin main
Write-Host ""
Write-Host "Done! Wait 1-2 minutes then visit: https://huangf06.github.io/GitStack/"
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
