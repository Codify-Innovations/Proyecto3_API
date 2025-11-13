Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "    Iniciando AutoCut IA Backend...  " -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1️⃣ Activa el entorno virtual
$venvPath = "E:\Proyecto3\Proyecto3_API\AutoCut IA\.venv\Scripts\Activate.ps1"
Write-Host " Activando entorno virtual..."
& $venvPath

# 2️⃣ Define el ejecutable del entorno virtual
$pythonPath = "E:\Proyecto3\Proyecto3_API\AutoCut IA\.venv\Scripts\python.exe"
Write-Host "`n Ejecutando con intérprete: $pythonPath"

# 3️⃣ Corre el servidor FastAPI usando el python correcto
& $pythonPath -m uvicorn app.main:app --host 127.0.0.1 --port 8000
