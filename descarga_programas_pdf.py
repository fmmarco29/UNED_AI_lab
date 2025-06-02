import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

# URL principal del Máster
base_url = "https://www.uned.es/universidad/inicio/estudios/masteres/master-universitario-en-investigacion-en-inteligencia-artificial.html?idContenido=8"

# Carpeta para guardar los PDFs
dest_folder = "pdfs"
os.makedirs(dest_folder, exist_ok=True)

# Constantes
codigo_titulacion = "310801"
curso = "2026"
base_pdf_url = "https://www.uned.es/universidad/pdf/GuiasAsignaturasMaster/PDFGuiaPublica"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

print("🔎 Buscando enlaces a las asignaturas...")

main_soup = get_soup(base_url)
asignatura_data = []

# Buscar enlaces con codAsignatura
for link in main_soup.find_all("a", href=True):
    href = link["href"]
    texto = link.get_text().strip()
    if "codAsignatura" in href:
        parsed = urlparse(href)
        query_params = parse_qs(parsed.query)
        codigo_asignatura = query_params.get("codAsignatura", [None])[0]
        if codigo_asignatura:
            asignatura_data.append({
                "codigo_asignatura": codigo_asignatura,
                "nombre": texto
            })

print(f"✅ Se encontraron {len(asignatura_data)} asignaturas.")

# Descargar PDFs para cada asignatura
for asignatura in asignatura_data:
    nombre = asignatura["nombre"]
    codigo_asignatura = asignatura["codigo_asignatura"]

    print(f"\n📚 Procesando asignatura: {nombre} (Código: {codigo_asignatura})")

    # Normalizar el nombre para evitar caracteres no válidos
    safe_nombre = nombre.replace("/", "-").replace("\\", "-")

    # Crear carpeta para la asignatura
    asignatura_folder = os.path.join(dest_folder, safe_nombre)
    os.makedirs(asignatura_folder, exist_ok=True)

    # Construir URL del PDF
    pdf_url = f"{base_pdf_url}?codigoAsignatura={codigo_asignatura}&curso={curso}&codigoTitulacion={codigo_titulacion}&language=es"
    pdf_name = f"{safe_nombre}.pdf"
    pdf_path = os.path.join(asignatura_folder, pdf_name)

    print(f"   ⇢ Descargando guía docente: {pdf_name}")
    try:
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()
        with open(pdf_path, "wb") as f:
            f.write(pdf_response.content)
        print(f"   ✅ Guardado en: {pdf_path}")
    except requests.HTTPError as e:
        print(f"   ⚠️ Error al descargar {pdf_url}: {e}")

print("\n✅ ¡Descarga de las guías docentes completada!")
