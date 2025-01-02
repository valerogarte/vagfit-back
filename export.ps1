# Define la ruta de los archivos que quieres leer
$archivos = @(
    "./src/ejercicios/models.py", 
    "./src/ejercicios/serializers.py", 
    "./src/ejercicios/views.py", 
    "./src/entrenamiento/models.py", 
    "./src/entrenamiento/serializers.py", 
    "./src/entrenamiento/views.py", 
    "./src/rutinas/models.py", 
    "./src/rutinas/serializers.py", 
    "./src/rutinas/views.py",
    "./src/vagfit/urls.py"
    "./src/vagfit/utils.py"
    )

# Define el archivo de salida
$archivoSalida = "./chatgpt.txt"

# Inicializa el archivo de salida
Clear-Content -Path $archivoSalida

# Lee y concatena el contenido
foreach ($archivo in $archivos) {
    $titulo = "// " + [System.IO.Path]::GetFileName($archivo) # Obtén el nombre del archivo como título
    Add-Content -Path $archivoSalida -Value $titulo
    Add-Content -Path $archivoSalida -Value (Get-Content -Path $archivo) # Añade el contenido del archivo
    Add-Content -Path $archivoSalida -Value "" # Línea en blanco entre archivos
}

Write-Output "Archivos concatenados en $archivoSalida"
