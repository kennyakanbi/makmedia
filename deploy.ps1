# ----------------------------------------
# Automatic Railway Deployment Script
# ----------------------------------------

# 1️⃣ Ensure npm global binaries are in PATH
$env:Path += ";$env:APPDATA\npm"

# 2️⃣ Check Railway CLI
try {
    railway --version
} catch {
    Write-Host "Railway CLI not found. Installing..."
    npm install -g @railway/cli
}

# 3️⃣ Get current folder name as project name
$projectFolder = Split-Path -Leaf (Get-Location)
Write-Host "Project folder detected as: $projectFolder"

# 4️⃣ Set required environment variables
# Replace DATABASE_URL with your PostgreSQL connection string
$databaseUrl = "postgresql://postgres:rFVlNsknTUoHNVaijioUhdQAUDFODzGP@postgres.railway.internal:5432/railway"
railway variables set DATABASE_URL $databaseUrl

# Generate a secure SECRET_KEY
$secretKey = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).Guid + (New-Guid).Guid))
railway variables set SECRET_KEY $secretKey

# 5️⃣ Deploy the current project folder
railway deploy

# 6️⃣ Print success message
Write-Host "`nDeployment triggered for $projectFolder. Check your Railway dashboard for logs."
