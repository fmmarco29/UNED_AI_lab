import os
import requests

# Datos de las asignaturas: nombre y código
asignaturas = [
    ("01_AprendizajeProfundo", "31101061"),
    ("02_ProcesamientoLenguajeNatural", "31101170"),
    ("03_FundamentosIA", "31101199"),
    ("04_MetodosAprendizajeAutomatico", "31101220"),
    ("05_MetodosProbabilistasIA", "31101235"),
    ("06_MetodosSimbolicosIA", "31101248"),
    ("07_MetodosBioinspiradosIA", "31101251"),
    ("08_MetodosHibridosIA", "31101264"),
    ("09_VisionArtificial", "31101277"),
    ("10_MineriaDatos", "31101280"),
    ("11_DescubrimientoInformacionTextos", "31101293"),
    ("12_AplicacionesIA_DesarrolloHumano", "31108041"),
    ("13_IA_EnIngenieria", "31108022"),
    ("14_TecnicasIA_EnIngenieria", "31108023"),
    ("15_ComplementosFormacion_IA_Ensenanza", "31108024"),
    ("16_MetodologiaInvestigacionSI", "31108025"),
    ("17_TFM_InvestigacionIA", "31108026")
]

# URL base para las guías docentes
base_url = "https://www.uned.es/universidad/pdf/GuiasAsignaturasMaster/PDFGuiaPublica"

# Carpeta principal del proyecto
root_folder = "UNED_Master_AI"
os.makedirs(root_folder, exist_ok=True)

# Subcarpetas por asignatura
subfolders = ["notebooks", "scripts", "data", "docs", "results"]

# Archivos adicionales en la carpeta principal
with open(os.path.join(root_folder, "README.md"), "w", encoding="utf-8") as f:
    f.write("# UNED Máster IA - Repositorio completo\n\nRepositorio con materiales, estructura de carpetas y guías docentes de las asignaturas.\n")

with open(os.path.join(root_folder, "LICENSE"), "w", encoding="utf-8") as f:
    f.write("MIT License\n\n(c) 2025 Tu Nombre\n")

with open(os.path.join(root_folder, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("numpy\npandas\nscikit-learn\nrequests\nbeautifulsoup4\n")

with open(os.path.join(root_folder, ".gitignore"), "w", encoding="utf-8") as f:
    f.write("__pycache__/\n*.pyc\n.env\n.DS_Store\n")

# Iterar sobre las asignaturas
for nombre_asignatura, codigo_asignatura in asignaturas:
    # Crear carpeta de la asignatura
    asignatura_path = os.path.join(root_folder, nombre_asignatura)
    os.makedirs(asignatura_path, exist_ok=True)

    # Crear subcarpetas dentro de la asignatura
    for sub in subfolders:
        os.makedirs(os.path.join(asignatura_path, sub), exist_ok=True)

    # Crear README.md para la asignatura
    with open(os.path.join(asignatura_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {nombre_asignatura}\n\nMateriales, ejemplos de código y guía docente para la asignatura **{nombre_asignatura}**.\n")

    # Descargar guía PDF y guardarla en la raíz de la carpeta de la asignatura
    params = {
        "codigoAsignatura": codigo_asignatura,
        "codigoTitulacion": "310801",
        "curso": "2026",
        "language": "es"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        pdf_path = os.path.join(asignatura_path, f"{nombre_asignatura}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"Guía descargada para {nombre_asignatura}")
    except requests.HTTPError as e:
        print(f"Error al descargar la guía para {nombre_asignatura}: {e}")

print("\nEstructura de carpetas y descarga de guías finalizada.")
