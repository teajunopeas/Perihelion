#!/usr/bin/env python3
import os
import subprocess
import glob
import argparse
import shutil
from pathlib import Path
import sys
import platform


# --- Funciones de Búsqueda y Compilación/Conversión ---

def find_tex_files(directory="."):
    """Busca todos los archivos .tex en el directorio especificado."""
    return glob.glob(os.path.join(directory, "*.tex"))


def find_executable(name):
    """Encuentra la ruta de un ejecutable en el sistema."""
    path = shutil.which(name)
    if path:
        return path

    if platform.system() == "Windows":
        # Búsqueda adicional específica para Windows si shutil.which falla
        common_paths_windows = {
            "inkscape": [
                r"C:\Program Files\Inkscape\bin\inkscape.exe",
                r"C:\Program Files\Inkscape\inkscape.exe",
                r"C:\Program Files (x86)\Inkscape\inkscape.exe",
            ],
            "pdflatex": [  # Asumiendo MiKTeX o TeX Live en rutas comunes
                r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
                r"C:\texlive\2023\bin\win32\pdflatex.exe",  # Ejemplo, ajustar año
                r"C:\texlive\2024\bin\win32\pdflatex.exe",
            ],
            "latex": [
                r"C:\Program Files\MiKTeX\miktex\bin\x64\latex.exe",
                r"C:\texlive\2023\bin\win32\latex.exe",
                r"C:\texlive\2024\bin\win32\latex.exe",
            ],
            "dvi2svg": [  # dvisvgm es más común y a menudo se llama así
                r"C:\Program Files\MiKTeX\miktex\bin\x64\dvisvgm.exe",
                r"C:\texlive\2023\bin\win32\dvisvgm.exe",
                r"C:\texlive\2024\bin\win32\dvisvgm.exe",
            ]
        }
        if name in common_paths_windows:
            for p in common_paths_windows[name]:
                if os.path.exists(p):
                    return p
    return None


def compile_tex_to_pdf(tex_file, pdflatex_exe="pdflatex"):
    """Compila un archivo .tex a .pdf usando pdflatex."""
    print(f"Compilando {tex_file} a PDF con {pdflatex_exe}...")
    try:
        result = subprocess.run(
            [pdflatex_exe, "-interaction=nonstopmode", tex_file],
            capture_output=True, text=True, check=True,
            cwd=os.path.dirname(tex_file) or '.'
        )
        print(f"Compilación a PDF exitosa: {os.path.splitext(tex_file)[0]}.pdf")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar {tex_file} a PDF: {e}")
        print(f"Salida de {os.path.basename(pdflatex_exe)}:\n{e.stdout}")
        print(f"Error de {os.path.basename(pdflatex_exe)}:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: El comando '{pdflatex_exe}' no se encontró.")
        return False


def compile_tex_to_dvi(tex_file, latex_exe="latex"):
    """Compila un archivo .tex a .dvi usando latex."""
    print(f"Compilando {tex_file} a DVI con {latex_exe}...")
    try:
        result = subprocess.run(
            [latex_exe, "-interaction=nonstopmode", tex_file],
            capture_output=True, text=True, check=True,
            cwd=os.path.dirname(tex_file) or '.'
        )
        # Latex puede requerir múltiples pasadas para referencias cruzadas, etc.
        # Para simplificar, aquí solo hacemos una pasada.
        # Considerar ejecutarlo 2-3 veces si es necesario para documentos complejos.
        print(f"Compilación a DVI exitosa: {os.path.splitext(tex_file)[0]}.dvi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar {tex_file} a DVI: {e}")
        print(f"Salida de {os.path.basename(latex_exe)}:\n{e.stdout}")
        print(f"Error de {os.path.basename(latex_exe)}:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: El comando '{latex_exe}' no se encontró.")
        return False


def convert_pdf_to_svg_with_inkscape(pdf_file, inkscape_exe="inkscape"):
    """Convierte un archivo .pdf a .svg usando Inkscape con optimizaciones para tamaño."""
    svg_file = pdf_file.replace(".pdf", ".svg")
    print(f"Convirtiendo {pdf_file} a SVG con Inkscape ({inkscape_exe})...")

    # Opciones optimizadas para reducir tamaño del SVG
    cmd_args = [
        pdf_file,
        f"--export-filename={svg_file}",
        "--export-plain-svg",  # SVG básico sin metadatos extras
        "--export-area-drawing",  # Ajustar al área de dibujo exacta
        "--vacuum-defs"  # Eliminar definiciones no utilizadas
    ]

    try:
        result = subprocess.run(
            [inkscape_exe] + cmd_args,
            capture_output=True, text=True, check=True
        )
        print(f"Conversión a SVG exitosa con Inkscape: {svg_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {pdf_file} a SVG con Inkscape: {e}")
        print(f"Comando intentado: {inkscape_exe} {' '.join(cmd_args)}")
        print(f"Salida de Inkscape:\n{e.stdout}")
        print(f"Error de Inkscape:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: El comando '{inkscape_exe}' no se encontró.")
        return False


def convert_pdf_to_svg_with_pdf2svg(pdf_file, pdf2svg_exe="pdf2svg"):
    """Convierte un archivo .pdf a .svg usando pdf2svg."""
    svg_file = pdf_file.replace(".pdf", ".svg")
    print(f"Convirtiendo {pdf_file} a SVG con pdf2svg ({pdf2svg_exe})...")
    try:
        result = subprocess.run(
            [pdf2svg_exe, pdf_file, svg_file],
            capture_output=True, text=True, check=True
        )
        print(f"Conversión a SVG exitosa con pdf2svg: {svg_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {pdf_file} a SVG con pdf2svg: {e}")
        print(f"Salida de pdf2svg:\n{e.stdout}")
        print(f"Error de pdf2svg:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: El comando '{pdf2svg_exe}' no se encontró.")
        return False


def convert_dvi_to_svg(dvi_file, dvi2svg_exe="dvisvgm"):
    """Convierte un archivo .dvi a .svg usando dvisvgm (comúnmente llamado dvi2svg o dvisvgm)."""
    # dvisvgm usualmente genera el svg con el mismo nombre base.
    # dvisvgm input.dvi -o output.svg
    svg_file = dvi_file.replace(".dvi", ".svg")
    print(f"Convirtiendo {dvi_file} a SVG con {dvi2svg_exe}...")
    try:
        # Opciones comunes: --no-fonts (embebido de paths), --exact (bounding box)
        # La opción -o es para el archivo de salida
        cmd = [dvi2svg_exe, dvi_file, "-o", svg_file, "--exact"]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, check=True,
            cwd=os.path.dirname(dvi_file) or '.'
        )
        print(f"Conversión DVI a SVG exitosa: {svg_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {dvi_file} a SVG con {dvi2svg_exe}: {e}")
        print(f"Comando: {' '.join(cmd)}")
        print(f"Salida de {os.path.basename(dvi2svg_exe)}:\n{e.stdout}")
        print(f"Error de {os.path.basename(dvi2svg_exe)}:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: El comando '{dvi2svg_exe}' no se encontró. (A menudo se llama 'dvisvgm').")
        return False


# --- Limpieza ---
def clean_auxiliary_files(base_name, keep_tex=True, delete_intermediate_pdf=False, delete_intermediate_dvi=False):
    """Elimina archivos auxiliares y opcionalmente intermedios."""
    print(f"Limpiando archivos para: {base_name}")
    extensions_to_remove = [
        ".aux", ".log", ".toc", ".lof", ".lot", ".out",
        ".nav", ".snm", ".vrb", ".fls", ".fdb_latexmk", ".bbl",
        ".blg", ".synctex.gz", ".idx", ".ilg", ".ind"
    ]

    if delete_intermediate_pdf:
        extensions_to_remove.append(".pdf")
    if delete_intermediate_dvi:
        extensions_to_remove.append(".dvi")

    for ext in extensions_to_remove:
        file_to_remove = base_name + ext
        if os.path.exists(file_to_remove):
            try:
                os.remove(file_to_remove)
                print(f"  - Eliminado: {os.path.basename(file_to_remove)}")
            except OSError as e:
                print(f"  - Error al eliminar {os.path.basename(file_to_remove)}: {e}")

    if not keep_tex:
        tex_file = base_name + ".tex"
        if os.path.exists(tex_file):
            try:
                os.remove(tex_file)
                print(f"  - Eliminado: {os.path.basename(tex_file)} (según --remove-tex)")
            except OSError as e:
                print(f"  - Error al eliminar {os.path.basename(tex_file)}: {e}")


# --- Lógica Principal de Procesamiento ---
def process_tex_files(directory=".", target='svg', clean_enabled=True, keep_tex=True,
                      keep_pdf_intermediate=False, keep_dvi_intermediate=False,  # Nuevo para DVI
                      force_overwrite=False,
                      workflow_info=None):  # Contendrá la info del flujo decidido
    """Procesa todos los archivos .tex en el directorio según el flujo y objetivo."""
    tex_files = find_tex_files(directory)
    if not tex_files:
        print(f"No se encontraron archivos .tex en '{os.path.abspath(directory)}'")
        return

    print(f"Encontrados {len(tex_files)} archivos .tex en '{os.path.abspath(directory)}'")
    processed_count = 0
    skipped_count = 0
    error_count = 0

    if not workflow_info or workflow_info['name'] == "NONE":
        print("Error: No se pudo determinar un flujo de trabajo válido debido a dependencias faltantes.")
        return

    print(f"Usando flujo de trabajo: {workflow_info['name']}")

    for tex_file in tex_files:
        base_name = os.path.splitext(tex_file)[0]
        pdf_file = base_name + ".pdf"
        dvi_file = base_name + ".dvi"  # Nuevo
        svg_file = base_name + ".svg"
        print(f"\n--- Procesando: {os.path.basename(tex_file)} ---")

        target_file_path = ""
        if target == 'svg':
            target_file_path = svg_file
        elif target == 'pdf':
            target_file_path = pdf_file

        if os.path.exists(target_file_path) and not force_overwrite:
            print(
                f"Objetivo '{target}' ({os.path.basename(target_file_path)}) ya existe y no se usó --force. Omitiendo.")
            skipped_count += 1
            continue

        # --- INICIO DEL FLUJO DE TRABAJO ---
        pdf_generated = False
        dvi_generated = False
        conversion_ok = (target != 'svg')  # Si el target no es SVG, la "conversión" es trivialmente OK

        # --- Flujo: PDFLATEX -> PDF -> [PDF_Converter] -> SVG ---
        if workflow_info['name'] == "PDFLATEX_INKSCAPE" or \
                workflow_info['name'] == "PDFLATEX_PDF2SVG" or \
                workflow_info['name'] == "PDFLATEX_ONLY":

            if not compile_tex_to_pdf(tex_file, pdflatex_exe=workflow_info['pdflatex_exe']):
                print(f"Fallo en la compilación a PDF. Omitiendo.")
                error_count += 1
                continue
            pdf_generated = os.path.exists(pdf_file)
            if not pdf_generated:
                print(f"No se encontró {os.path.basename(pdf_file)} tras la compilación. Omitiendo.")
                error_count += 1
                continue

            if target == 'svg':
                if workflow_info['name'] == "PDFLATEX_INKSCAPE":
                    conversion_ok = convert_pdf_to_svg_with_inkscape(pdf_file,
                                                                     inkscape_exe=workflow_info['pdf_converter_exe'])
                elif workflow_info['name'] == "PDFLATEX_PDF2SVG":
                    conversion_ok = convert_pdf_to_svg_with_pdf2svg(pdf_file,
                                                                    pdf2svg_exe=workflow_info['pdf_converter_exe'])

                if not conversion_ok:
                    print(f"Fallo en la conversión PDF a SVG. Omitiendo generación de SVG para este archivo.")
                    error_count += 1
                    # No continuar a limpieza de SVG si falló
                elif not os.path.exists(svg_file):
                    print(f"Aunque la conversión PDF-SVG pareció exitosa, no se encontró {os.path.basename(svg_file)}.")
                    error_count += 1
                    conversion_ok = False


        # --- Flujo Alternativo: LATEX -> DVI -> DVI2SVG -> SVG ---
        elif workflow_info['name'] == "LATEX_DVI2SVG":
            if target == 'pdf':
                print(
                    f"Error: El flujo LATEX->DVI no puede generar PDF directamente. Omita {tex_file} para target=pdf.")
                error_count += 1
                continue  # No podemos hacer PDF con este flujo

            if not compile_tex_to_dvi(tex_file, latex_exe=workflow_info['latex_exe']):
                print(f"Fallo en la compilación a DVI. Omitiendo.")
                error_count += 1
                continue
            dvi_generated = os.path.exists(dvi_file)
            if not dvi_generated:
                print(f"No se encontró {os.path.basename(dvi_file)} tras la compilación. Omitiendo.")
                error_count += 1
                continue

            if target == 'svg':  # Siempre será SVG para este flujo por ahora
                conversion_ok = convert_dvi_to_svg(dvi_file, dvi2svg_exe=workflow_info['dvi_converter_exe'])
                if not conversion_ok:
                    print(f"Fallo en la conversión DVI a SVG. Omitiendo generación de SVG para este archivo.")
                    error_count += 1
                elif not os.path.exists(svg_file):
                    print(f"Aunque la conversión DVI-SVG pareció exitosa, no se encontró {os.path.basename(svg_file)}.")
                    error_count += 1
                    conversion_ok = False
        else:
            print(f"Flujo de trabajo desconocido o no viable: {workflow_info['name']}. Omitiendo {tex_file}.")
            error_count += 1
            continue
        # --- FIN DEL FLUJO DE TRABAJO ---

        # --- Limpieza ---
        if clean_enabled:
            # El PDF se borra si fue intermedio para SVG Y no se pide mantenerlo
            del_pdf = (target == 'svg' and pdf_generated and not keep_pdf_intermediate)
            # El DVI se borra si fue intermedio para SVG Y no se pide mantenerlo
            del_dvi = (target == 'svg' and dvi_generated and not keep_dvi_intermediate)

            clean_auxiliary_files(
                base_name,
                keep_tex=keep_tex,
                delete_intermediate_pdf=del_pdf,
                delete_intermediate_dvi=del_dvi
            )
        else:
            print("Limpieza de archivos auxiliares desactivada (--no-clean).")

        if (target == 'pdf' and pdf_generated) or (target == 'svg' and conversion_ok and os.path.exists(svg_file)):
            processed_count += 1
        # error_count ya se incrementó si hubo fallos

    print("\n--- Resumen del Proceso ---")
    print(f"Archivos .tex encontrados: {len(tex_files)}")
    print(f"Archivos procesados exitosamente al formato '{target.upper()}': {processed_count}")
    print(f"Archivos omitidos (ya existían o no aplicables): {skipped_count}")
    print(f"Archivos con errores: {error_count}")


def check_dependencies(target='svg', use_inkscape_preference=True, inkscape_path_arg=None, forced_workflow=None):
    """
    Verifies dependencies and determines the viable workflow.
    Can force a specific workflow through the forced_workflow parameter.

    Args:
        target: Output format ('svg' or 'pdf')
        use_inkscape_preference: Whether to prefer Inkscape over pdf2svg
        inkscape_path_arg: Optional explicit path to Inkscape executable
        forced_workflow: Force a specific workflow ('pdflatex-inkscape', 'pdflatex-pdf2svg', 'latex-dvisvgm')

    Returns:
        Dictionary with workflow name and executable paths
    """
    print("Comprobando dependencias...")
    missing = []
    workflow = {"name": "NONE"}  # Por defecto, ningún flujo es viable

    # Handle forced workflow if specified
    if forced_workflow and forced_workflow != 'auto':
        print(f"Forzando flujo de trabajo: {forced_workflow}")

        if forced_workflow == 'pdflatex-inkscape':
            # Force pdflatex -> PDF -> Inkscape -> SVG workflow
            pdflatex_exe = find_executable("pdflatex")
            inkscape_exe = inkscape_path_arg or find_executable("inkscape")

            if pdflatex_exe and inkscape_exe:
                workflow = {
                    "name": "PDFLATEX_INKSCAPE",
                    "pdflatex_exe": pdflatex_exe,
                    "pdf_converter_exe": inkscape_exe
                }
                print(f"  [OK] pdflatex encontrado en: {pdflatex_exe}")
                print(f"  [OK] inkscape encontrado en: {inkscape_exe}")
                print(f"  Flujo forzado viable: pdflatex -> PDF -> Inkscape -> SVG")
                return workflow
            else:
                if not pdflatex_exe:
                    print(f"  [FALLO] pdflatex no encontrado. Requerido para flujo '{forced_workflow}'")
                if not inkscape_exe:
                    print(f"  [FALLO] inkscape no encontrado. Requerido para flujo '{forced_workflow}'")

        elif forced_workflow == 'pdflatex-pdf2svg':
            # Force pdflatex -> PDF -> pdf2svg -> SVG workflow
            pdflatex_exe = find_executable("pdflatex")
            pdf2svg_exe = find_executable("pdf2svg")

            if pdflatex_exe and pdf2svg_exe:
                workflow = {
                    "name": "PDFLATEX_PDF2SVG",
                    "pdflatex_exe": pdflatex_exe,
                    "pdf_converter_exe": pdf2svg_exe
                }
                print(f"  [OK] pdflatex encontrado en: {pdflatex_exe}")
                print(f"  [OK] pdf2svg encontrado en: {pdf2svg_exe}")
                print(f"  Flujo forzado viable: pdflatex -> PDF -> pdf2svg -> SVG")
                return workflow
            else:
                if not pdflatex_exe:
                    print(f"  [FALLO] pdflatex no encontrado. Requerido para flujo '{forced_workflow}'")
                if not pdf2svg_exe:
                    print(f"  [FALLO] pdf2svg no encontrado. Requerido para flujo '{forced_workflow}'")

        elif forced_workflow == 'latex-dvisvgm':
            # Force latex -> DVI -> dvisvgm -> SVG workflow
            latex_exe = find_executable("latex")
            dvisvgm_exe = find_executable("dvisvgm")

            if latex_exe and dvisvgm_exe:
                workflow = {
                    "name": "LATEX_DVI2SVG",
                    "latex_exe": latex_exe,
                    "dvi_converter_exe": dvisvgm_exe
                }
                print(f"  [OK] latex encontrado en: {latex_exe}")
                print(f"  [OK] dvisvgm encontrado en: {dvisvgm_exe}")
                print(f"  Flujo forzado viable: latex -> DVI -> dvisvgm -> SVG")
                return workflow
            else:
                if not latex_exe:
                    print(f"  [FALLO] latex no encontrado. Requerido para flujo '{forced_workflow}'")
                if not dvisvgm_exe:
                    print(f"  [FALLO] dvisvgm no encontrado. Requerido para flujo '{forced_workflow}'")

        print(f"Flujo forzado '{forced_workflow}' no disponible con las dependencias actuales.")
        print("Volviendo a detección automática de flujo de trabajo...")

    # --- Original automatic workflow detection logic starts here ---
    # --- Intentar flujo primario (basado en pdflatex) ---
    print("Intentando flujo primario: pdflatex -> PDF -> [PDF_Converter] -> SVG (o PDF)")
    pdflatex_exe = find_executable("pdflatex")
    if pdflatex_exe:
        print(f"  [OK] pdflatex encontrado en: {pdflatex_exe}")
        workflow['pdflatex_exe'] = pdflatex_exe

        if target == 'pdf':
            workflow['name'] = "PDFLATEX_ONLY"
            print("  Flujo viable: pdflatex -> PDF")
            return workflow  # Si solo queremos PDF y pdflatex está, es suficiente

        elif target == 'svg':
            pdf_converter_exe = None
            converter_name_for_primary_path = ""  # Para mensajes de error

            if use_inkscape_preference:
                converter_name_for_primary_path = "Inkscape"
                if inkscape_path_arg and os.path.exists(inkscape_path_arg):
                    pdf_converter_exe = inkscape_path_arg
                    print(f"  [OK] Inkscape (ruta especificada): {pdf_converter_exe}")
                else:
                    pdf_converter_exe = find_executable("inkscape")
                    if pdf_converter_exe:
                        print(f"  [OK] Inkscape (PATH): {pdf_converter_exe}")

                if pdf_converter_exe:
                    workflow['name'] = "PDFLATEX_INKSCAPE"
                    workflow['pdf_converter_exe'] = pdf_converter_exe
                    print("  Flujo viable: pdflatex -> PDF -> Inkscape -> SVG")
                    return workflow  # Ruta primaria para SVG con Inkscape encontrada
                else:
                    print(
                        f"  [AVISO] {converter_name_for_primary_path} no encontrado (ni en PATH ni en ruta especificada).")

            # Si no se prefiere Inkscape, o si Inkscape (siendo preferido) no se encontró
            # Intentar con pdf2svg
            if not pdf_converter_exe:  # Solo si Inkscape no fue encontrado o no era la preferencia
                converter_name_for_primary_path = "pdf2svg"  # Actualizar para mensajes
                pdf_converter_exe = find_executable("pdf2svg")
                if pdf_converter_exe:
                    print(f"  [OK] pdf2svg (PATH): {pdf_converter_exe}")
                    workflow['name'] = "PDFLATEX_PDF2SVG"
                    workflow['pdf_converter_exe'] = pdf_converter_exe
                    print("  Flujo viable: pdflatex -> PDF -> pdf2svg -> SVG")
                    return workflow  # Ruta primaria para SVG con pdf2svg encontrada
                else:
                    print(f"  [AVISO] {converter_name_for_primary_path} no encontrado.")

            # Si llegamos aquí, pdflatex fue encontrado pero ninguno de sus convertidores SVG.
            if use_inkscape_preference:
                missing.append("Inkscape (para ruta pdflatex -> SVG)")
            else:
                missing.append("pdf2svg (para ruta pdflatex -> SVG)")
    else:
        print("  [FALLO] pdflatex no encontrado.")
        missing.append("pdflatex")

    # --- Si el flujo primario (pdflatex) no es viable para el target SVG, ---
    # --- intentar flujo alternativo (latex -> dvi -> dvisvgm) SOLO si target es SVG ---
    if target == 'svg':  # Solo tiene sentido el fallback DVI para SVG
        print("Flujo primario para SVG no viable. Intentando flujo alternativo: latex -> DVI -> dvisvgm...")
        latex_exe = find_executable("latex")
        dvi2svg_exe = find_executable("dvisvgm")  # dvisvgm es el nombre común

        if latex_exe and dvi2svg_exe:
            print(f"  [OK] latex encontrado en: {latex_exe}")
            print(f"  [OK] dvisvgm encontrado en: {dvi2svg_exe}")
            workflow['name'] = "LATEX_DVI2SVG"
            workflow['latex_exe'] = latex_exe
            workflow['dvi_converter_exe'] = dvi2svg_exe
            missing = [m for m in missing if not ("Inkscape" in m or "pdf2svg" in m)]
            if "pdflatex" in missing and workflow['name'] == "LATEX_DVI2SVG":
                missing.remove("pdflatex")

            print("  Flujo alternativo viable: latex -> DVI -> dvisvgm -> SVG")
            return workflow  # Flujo de respaldo encontrado
        else:
            if not latex_exe:
                print("  [FALLO] latex no encontrado para flujo alternativo.")
                missing.append("latex (para ruta alternativa DVI->SVG)")
            if not dvi2svg_exe:
                print("  [FALLO] dvisvgm (o dvi2svg) no encontrado para flujo alternativo.")
                missing.append("dvisvgm (para ruta alternativa DVI->SVG)")

    # Si ningún flujo fue viable
    final_missing = list(set(missing))  # Eliminar duplicados para el mensaje final

    if not final_missing and workflow['name'] != "NONE":
        print(
            f"Advertencia: Se alcanzó el final de check_dependencies sin errores 'missing' pero workflow es {workflow['name']}")
    elif final_missing:
        workflow['name'] = "NONE"
        print("\nError: No se pudo establecer un flujo de trabajo completo para el objetivo deseado.")
        print("Dependencias críticas faltantes o no encontradas:")
        for item in final_missing:
            print(f"  - {item}")
        print("\nPor favor, instálalas y asegúrate de que estén en el PATH del sistema,")
        print("o proporciona la ruta explícita si es necesario (ej. --inkscape-path).")
    elif workflow['name'] == "NONE" and not final_missing:
        print(
            "\nError: No se pudo establecer un flujo de trabajo completo para el objetivo deseado (caso no cubierto por mensajes de error específicos).")

    return workflow


def main():
    parser = argparse.ArgumentParser(
        description="Convierte archivos LaTeX (.tex) al formato objetivo (SVG o PDF) y limpia archivos auxiliares. También permite convertir directamente archivos .pdf o .dvi a .svg.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d", "--directory", default=".",
        help="Directorio donde buscar archivos .tex, .pdf o .dvi (por defecto: directorio actual)."
    )
    parser.add_argument(
        "--target", choices=['svg', 'pdf'], default='svg',
        help="Formato de salida final deseado:\n"
             "  svg: Convierte a SVG. Intentará (pdflatex->pdf->svg_converter) o (latex->dvi->dvisvgm) (predeterminado).\n"
             "  pdf: Convierte solo tex -> pdf (usando pdflatex)."
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Forzar la regeneración del archivo objetivo aunque ya exista."
    )
    parser.add_argument(
        "--from-intermediate", nargs="?", const=True, default=None,
        help="Convierte directamente uno o todos los archivos .pdf/.dvi a .svg (no requiere .tex). Si no se especifica archivo, procesa todos los .pdf y .dvi del directorio."
    )

    # Nuevo argumento para forzar un flujo de trabajo específico
    parser.add_argument(
        "--workflow", choices=['auto', 'pdflatex-inkscape', 'pdflatex-pdf2svg', 'latex-dvisvgm'],
        default='auto',
        help="Forzar un flujo de trabajo específico:\n"
             "  auto: Detección automática (predeterminado)\n"
             "  pdflatex-inkscape: Forzar conversión pdflatex -> PDF -> Inkscape -> SVG\n"
             "  pdflatex-pdf2svg: Forzar conversión pdflatex -> PDF -> pdf2svg -> SVG\n"
             "  latex-dvisvgm: Forzar conversión latex -> DVI -> dvisvgm -> SVG"
    )

    clean_group = parser.add_argument_group('Opciones de Limpieza')
    clean_group.add_argument(
        "--no-clean", action="store_false", dest="clean", default=True,
        help="No eliminar archivos auxiliares (.log, .aux, etc.) ni intermedios."
    )
    clean_group.add_argument(
        "--keep-pdf", action="store_true", dest="keep_pdf_intermediate", default=False,
        help="Si target=svg y se usa ruta PDF, mantener el .pdf intermedio."
    )
    clean_group.add_argument(
        "--keep-dvi", action="store_true", dest="keep_dvi_intermediate", default=False,
        help="Si target=svg y se usa ruta DVI, mantener el .dvi intermedio."
    )
    clean_group.add_argument(
        "--remove-tex", action="store_false", dest="keep_tex", default=True,
        help="Eliminar los archivos .tex originales después del procesamiento (¡Usar con cuidado!)."
    )

    conversion_group = parser.add_argument_group(
        'Opciones de Conversión PDF->SVG (si se usa ruta pdflatex y target=svg)'
    )
    converter_choice = conversion_group.add_mutually_exclusive_group()
    converter_choice.add_argument(
        "--use-inkscape", action="store_true", dest="use_inkscape", default=True,
        help="Preferir Inkscape para la conversión PDF a SVG (predeterminado si pdflatex viable)."
    )
    converter_choice.add_argument(
        "--use-pdf2svg", action="store_false", dest="use_inkscape",
        help="Preferir pdf2svg para la conversión PDF a SVG en lugar de Inkscape."
    )
    conversion_group.add_argument(
        "--inkscape-path", default=None,
        help="Ruta explícita al ejecutable de Inkscape."
    )
    args = parser.parse_args()

    # --- NUEVO: Si se usa --from-intermediate, convertir uno o todos los archivos intermedios ---
    if args.from_intermediate is not None:
        # Si se pasa un archivo concreto: --from-intermediate archivo.pdf
        if isinstance(args.from_intermediate, str):
            files_to_convert = [os.path.join(args.directory, args.from_intermediate)]
        else:
            # Si solo se pasa --from-intermediate, buscar todos los .pdf y .dvi
            files_to_convert = sorted(glob.glob(os.path.join(args.directory, "*.pdf")))
            files_to_convert += sorted(glob.glob(os.path.join(args.directory, "*.dvi")))

        if not files_to_convert:
            print(f"No se encontraron archivos .pdf ni .dvi en '{os.path.abspath(args.directory)}'")
            sys.exit(1)

        total = len(files_to_convert)
        ok_count = 0
        for input_file in files_to_convert:
            if not os.path.isfile(input_file):
                print(f"Error: El archivo '{input_file}' no existe.")
                continue
            ext = os.path.splitext(input_file)[1].lower()
            output_svg = os.path.splitext(input_file)[0] + ".svg"
            if os.path.exists(output_svg) and not args.force:
                print(f"El archivo de salida '{output_svg}' ya existe. Usa --force para sobrescribir.")
                continue
            if ext == ".pdf":
                inkscape_exe = find_executable("inkscape")
                pdf2svg_exe = find_executable("pdf2svg")
                if inkscape_exe:
                    print(f"Convirtiendo {input_file} a SVG con Inkscape...")
                    ok = convert_pdf_to_svg_with_inkscape(input_file, inkscape_exe=inkscape_exe)
                elif pdf2svg_exe:
                    print(f"Convirtiendo {input_file} a SVG con pdf2svg...")
                    ok = convert_pdf_to_svg_with_pdf2svg(input_file, pdf2svg_exe=pdf2svg_exe)
                else:
                    print("No se encontró ni Inkscape ni pdf2svg en el sistema.")
                    continue
                if ok and os.path.exists(output_svg):
                    print(f"¡Conversión exitosa! SVG guardado en: {output_svg}")
                    ok_count += 1
                else:
                    print(f"No se pudo completar la conversión de {input_file} a SVG.")
            elif ext == ".dvi":
                dvisvgm_exe = find_executable("dvisvgm")
                if dvisvgm_exe:
                    print(f"Convirtiendo {input_file} a SVG con dvisvgm...")
                    ok = convert_dvi_to_svg(input_file, dvi2svg_exe=dvisvgm_exe)
                else:
                    print("No se encontró dvisvgm en el sistema.")
                    continue
                if ok and os.path.exists(output_svg):
                    print(f"¡Conversión exitosa! SVG guardado en: {output_svg}")
                    ok_count += 1
                else:
                    print(f"No se pudo completar la conversión de {input_file} a SVG.")
            else:
                print(f"El archivo '{input_file}' debe ser .pdf o .dvi para conversión directa a SVG.")
        print(f"\nResumen: {ok_count} de {total} archivos intermedios convertidos correctamente a SVG.")
        return

    # --- Comprobación de dependencias y determinación del flujo ---
    workflow_info = check_dependencies(
        target=args.target,
        use_inkscape_preference=args.use_inkscape,
        inkscape_path_arg=args.inkscape_path,
        forced_workflow=args.workflow  # Nuevo parámetro para forzar el flujo
    )

    if workflow_info['name'] == "NONE":
        print("Saliendo debido a dependencias faltantes para el flujo de trabajo requerido.")
        sys.exit(1)

    # --- Mostrar configuración ---
    print("\n--- Configuración del Proceso ---")
    print(f"Directorio de trabajo: {os.path.abspath(args.directory)}")
    print(f"Objetivo final (--target): {args.target.upper()}")
    print(f"Flujo de trabajo: {workflow_info['name']}")
    # Mostrar si el flujo fue forzado o detectado automáticamente
    if args.workflow != 'auto':
        print(f"  (Flujo forzado mediante --workflow={args.workflow})")

    if 'pdflatex_exe' in workflow_info: print(f"  pdflatex: {workflow_info['pdflatex_exe']}")
    if 'latex_exe' in workflow_info: print(f"  latex: {workflow_info['latex_exe']}")
    if 'pdf_converter_exe' in workflow_info: print(f"  Convertidor PDF->SVG: {workflow_info['pdf_converter_exe']}")
    if 'dvi_converter_exe' in workflow_info: print(f"  Convertidor DVI->SVG: {workflow_info['dvi_converter_exe']}")

    print(f"Forzar sobreescritura (--force): {'Sí' if args.force else 'No'}")
    print(f"Limpiar archivos (--no-clean): {'Sí' if args.clean else 'No'}")
    if args.clean:
        if args.target == 'svg':
            if "PDFLATEX" in workflow_info['name']:
                print(f"  - Mantener PDF intermedio (--keep-pdf): {'Sí' if args.keep_pdf_intermediate else 'No'}")
            if "LATEX_DVI2SVG" in workflow_info['name']:
                print(f"  - Mantener DVI intermedio (--keep-dvi): {'Sí' if args.keep_dvi_intermediate else 'No'}")
        print(f"  - Eliminar .TEX original (--remove-tex): {'Sí' if not args.keep_tex else 'No'}")

    # --- Ejecutar procesamiento ---
    process_tex_files(
        directory=args.directory,
        target=args.target,
        clean_enabled=args.clean,
        keep_tex=args.keep_tex,
        keep_pdf_intermediate=args.keep_pdf_intermediate,
        keep_dvi_intermediate=args.keep_dvi_intermediate,
        force_overwrite=args.force,
        workflow_info=workflow_info
    )


if __name__ == "__main__":
    main()