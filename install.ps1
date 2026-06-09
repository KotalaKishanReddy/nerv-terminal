# NERV Terminal - Windows Installer (PowerShell / CMD)
# Run in PowerShell:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
#   irm https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/install.ps1 | iex

param([switch]$Update)

$RED    = "`e[38;2;210;25;25m"
$AMBER  = "`e[38;2;255;170;0m"
$GREEN  = "`e[38;2;0;210;90m"
$DIM    = "`e[38;2;75;65;55m"
$RESET  = "`e[0m"

function ok($msg)   { Write-Host "$GREEN  [ OK ] $msg$RESET" }
function warn($msg) { Write-Host "$AMBER  [  *  ] $msg$RESET" }
function err($msg)  { Write-Host "$RED  [ ERR ] $msg$RESET"; exit 1 }

Write-Host ""
Write-Host "$RED  NN   NN EEEEEEE RRRRRR  VV     VV$RESET"
Write-Host "$RED  NNN  NN EE      RR   RR VV     VV$RESET"
Write-Host "$RED  NN N NN EEEEE   RRRRRR   VV   VV $RESET"
Write-Host "$RED  NN  NNN EE      RR  RR    VV VV  $RESET"
Write-Host "$RED  NN   NN EEEEEEE RR   RR    VVV   $RESET"
Write-Host "$DIM  GEHIRN ADVANCED RESEARCH - INSTALLER v2.0$RESET"
Write-Host ""

# --- Python check ---
warn "Checking Python..."
$pycmd = $null
foreach ($try in @('python','python3','py')) {
    if (Get-Command $try -ErrorAction SilentlyContinue) {
        $pycmd = $try; break
    }
}
if (-not $pycmd) {
    err "Python 3.8+ not found. Install from https://python.org and re-run."
}
$pyver = & $pycmd -c "import sys; print(sys.version_info.minor)" 2>$null
if ([int]$pyver -lt 8) { err "Python 3.8+ required. Found 3.$pyver" }
ok "Python 3.$pyver found"

# --- Install dir ---
$InstallDir = "$env:APPDATA\nerv-terminal"
warn "Installing to $InstallDir ..."

$gitExists = Get-Command git -ErrorAction SilentlyContinue
if ($gitExists) {
    if (Test-Path "$InstallDir\.git") {
        warn "Repo exists - pulling latest..."
        git -C $InstallDir pull --ff-only --quiet
        ok "Updated to latest"
    } else {
        git clone --depth 1 --quiet https://github.com/KotalaKishanReddy/nerv-terminal.git $InstallDir
        ok "Cloned repo"
    }
} else {
    warn "git not found - downloading files directly..."
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    $raw = "https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main"
    foreach ($f in @('nerv.py','run.py','requirements.txt')) {
        Invoke-WebRequest -Uri "$raw/$f" -OutFile "$InstallDir\$f" -UseBasicParsing
    }
    ok "Downloaded files"
}

# --- Venv setup ---
$venv = "$InstallDir\.venv"
warn "Creating isolated venv at $venv ..."
& $pycmd -m venv $venv
$py = "$venv\Scripts\python.exe"
if (-not (Test-Path $py)) { err "venv creation failed" }
warn "Installing Python deps (blessed, pycryptodome)..."
& $py -m pip install --quiet --upgrade pip
& $py -m pip install --quiet --upgrade blessed pycryptodome
ok "Dependencies installed"

# --- Write launcher batch file ---
$BinDir  = "$env:APPDATA\nerv-terminal\bin"
New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
$Launcher = "$BinDir\nerv.bat"
@"
@echo off
""$py"" ""$InstallDir\run.py"" %*
"@ | Set-Content -Path $Launcher -Encoding UTF8
ok "Launcher written: $Launcher"

# --- Add to user PATH if not present ---
$userPath = [Environment]::GetEnvironmentVariable('PATH','User')
if ($userPath -notlike "*$BinDir*") {
    [Environment]::SetEnvironmentVariable('PATH', "$BinDir;$userPath", 'User')
    ok "Added $BinDir to your user PATH"
    warn "Restart your terminal for PATH to take effect"
} else {
    ok "$BinDir already in PATH"
}

Write-Host ""
ok "NERV Terminal installed!"
Write-Host "$DIM  Restart your terminal, then run:  nerv$RESET"
Write-Host "$DIM  Updates are automatic on every launch.$RESET"
Write-Host ""
