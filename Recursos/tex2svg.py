#!/usr/bin/env python3
import os
import subprocess
import glob
import argparse
import shutil
from pathlib import Path
import sys
import platform


def find_tex_files(directory="."):
    """Busca todos los archivos .tex en el directorio especificado."""
    return glob.glob(os.path.join(directory, "*.tex"))


def compile_tex_to_pdf(tex_file):
    """Compila un archivo .tex a .pdf."""
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar {tex_file}: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def convert_pdf_to_svg_with_inkscape(pdf_file, inkscape_path=None):
    """Convierte un archivo .pdf a .svg usando Inkscape."""
    svg_file = pdf_file.replace(".pdf", ".svg")
    
    # Construir el comando de Inkscape
    if inkscape_path:
        cmd = [inkscape_path]
    else:
        cmd = ["inkscape"]
    
    # Detectar la versión de Inkscape para usar los parámetros correctos
    try:
        version_output = subprocess.run(
            cmd + ["--version"],
            capture_output=True,
            text=True
        ).stdout
        
        # Inkscape 1.0+ usa un formato de comando diferente
        if "Inkscape 1." in version_output or "Inkscape 2." in version_output:
            cmd += [
                pdf_file,
                "--export-filename=" + svg_file,
                "--export-plain-svg"
            ]
        else:  # Inkscape 0.9x y anteriores
            cmd += [
                "--file=" + pdf_file,
                "--export-plain-svg",
                "--export-filename=" + svg_file
            ]
    except Exception:
        # Si no podemos detectar la versión, intentamos con el formato más reciente
        cmd += [
            pdf_file,
            "--export-filename=" + svg_file,
            "--export-plain-svg"
        ]
        
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {pdf_file} a SVG con Inkscape: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def convert_pdf_to_svg_with_dvisvgm(pdf_file):
    """Convierte un archivo .pdf a .svg usando dvisvgm."""
    svg_file = pdf_file.replace(".pdf", ".svg")
    try:
        result = subprocess.run(
            ["pdf2svg", pdf_file, svg_file],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir {pdf_file} a SVG con pdf2svg: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def clean_auxiliary_files(base_name, keep_tex=True, keep_svg=True, keep_pdf=False):
    """Elimina archivos auxiliares generados por LaTeX."""
    extensions_to_remove = [
        ".aux", ".log", ".toc", ".lof", ".lot", ".out", 
        ".nav", ".snm", ".vrb", ".fls", ".fdb_latexmk", ".bbl", 
        ".blg", ".synctex.gz", ".idx", ".ilg", ".ind"
    ]
    
    if not keep_pdf:
        extensions_to_remove.append(".pdf")
    
    if not keep_tex:
        extensions_to_remove.append(".tex")
    
    if not keep_svg:
        extensions_to_remove.append(".svg")
    
    for ext in extensions_to_remove:
        file_to_remove = base_name + ext
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)
            print(f"Eliminado: {file_to_remove}")


def process_tex_files(directory=".", clean=True, keep_tex=True, keep_svg=True, keep_pdf=False, 
                     use_inkscape=True, inkscape_path=None):
    """Procesa todos los archivos .tex en el directorio."""
    tex_files = find_tex_files(directory)
    if not tex_files:
        print(f"No se encontraron archivos .tex en {directory}")
        return
    
    print(f"Encontrados {len(tex_files)} archivos .tex")
    
    for tex_file in tex_files:
        print(f"\nProcesando: {tex_file}")
        base_name = os.path.splitext(tex_file)[0]
        
        # Compilar a PDF
        if compile_tex_to_pdf(tex_file):
            print(f"Compilación a PDF exitosa: {base_name}.pdf")
            
            # Convertir PDF a SVG
            pdf_file = base_name + ".pdf"
            if os.path.exists(pdf_file):
                conversion_success = False
                
                if use_inkscape:
                    # Intentar con Inkscape primero
                    conversion_success = convert_pdf_to_svg_with_inkscape(pdf_file, inkscape_path)
                    if conversion_success:
                        print(f"Conversión a SVG exitosa con Inkscape: {base_name}.svg")
                    else:
                        print("Conversión con Inkscape fallida, intentando con pdf2svg...")
                
                # Si Inkscape falló o no se usa, intentar con pdf2svg
                if not conversion_success and not use_inkscape:
                    conversion_success = convert_pdf_to_svg_with_dvisvgm(pdf_file)
                    if conversion_success:
                        print(f"Conversión a SVG exitosa con pdf2svg: {base_name}.svg")
                    else:
                        print(f"Error al convertir a SVG: {pdf_file}")
                        
                if not conversion_success:
                    print(f"No se pudo convertir {pdf_file} a SVG con ninguna herramienta disponible.")
            else:
                print(f"Archivo PDF no encontrado: {pdf_file}")
        else:
            print(f"Error al compilar: {tex_file}")
        
        # Limpiar archivos auxiliares si se solicita
        if clean:
            clean_auxiliary_files(base_name, keep_tex, keep_svg, keep_pdf)
            print(f"Archivos auxiliares eliminados para: {base_name}")


def find_inkscape():
    """Intenta encontrar la ruta de instalación de Inkscape en el sistema."""
    system = platform.system()
    
    if system == "Windows":
        # Rutas comunes de instalación en Windows
        possible_paths = [
            r"C:\Program Files\Inkscape\inkscape.exe",
            r"C:\Program Files (x86)\Inkscape\inkscape.exe",
            # Añade más rutas comunes si es necesario
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
    return None


def check_dependencies(use_inkscape=True):
    """Verifica que las dependencias necesarias estén instaladas."""
    dependencies = ["pdflatex"]
    
    if not use_inkscape:
        dependencies.append("pdf2svg")
    
    missing = []
    
    # En Windows, no usamos 'which' sino 'where'
    check_command = "where" if platform.system() == "Windows" else "which"
    
    for cmd in dependencies:
        try:
            subprocess.run([check_command, cmd], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            missing.append(cmd)
    
    if use_inkscape:
        inkscape_path = find_inkscape()
        if inkscape_path:
            print(f"Inkscape encontrado en: {inkscape_path}")
        else:
            try:
                subprocess.run([check_command, "inkscape"], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                missing.append("inkscape")
    
    if missing:
        print("Faltan las siguientes dependencias:")
        for cmd in missing:
            print(f"  - {cmd}")
        print("\nPor favor, instálalas antes de continuar.")
        if "pdflatex" in missing:
            print("Para instalar LaTeX:")
            print("  - En Windows: Descarga e instala MiKTeX o TeX Live desde sus sitios web")
            print("  - En Ubuntu/Debian: sudo apt-get install texlive-base")
            print("  - En macOS: brew install --cask basictex")
        if "inkscape" in missing and use_inkscape:
            print("Para instalar Inkscape:")
            print("  - En Windows: Descarga desde https://inkscape.org/release/")
            print("  - En Ubuntu/Debian: sudo apt-get install inkscape")
            print("  - En macOS: brew install --cask inkscape")
        if "pdf2svg" in missing and not use_inkscape:
            print("Para instalar pdf2svg:")
            print("  - En Windows: Descarga desde http://www.cityinthesky.co.uk/opensource/pdf2svg/")
            print("  - En Ubuntu/Debian: sudo apt-get install pdf2svg")
            print("  - En macOS: brew install pdf2svg")
        return False, None
    
    return True, inkscape_path if use_inkscape else None


def main():
    parser = argparse.ArgumentParser(description="Convertir archivos LaTeX a SVG y limpiar archivos auxiliares")
    parser.add_argument("-d", "--directory", default=".", help="Directorio donde buscar archivos .tex")
    parser.add_argument("--no-clean", action="store_false", dest="clean", help="No eliminar archivos auxiliares")
    parser.add_argument("--remove-tex", action="store_false", dest="keep_tex", help="Eliminar también los archivos .tex originales")
    parser.add_argument("--remove-svg", action="store_false", dest="keep_svg", help="Eliminar también los archivos .svg generados")
    parser.add_argument("--keep-pdf", action="store_true", help="Mantener los archivos PDF intermedios")
    parser.add_argument("--no-inkscape", action="store_false", dest="use_inkscape", help="No usar Inkscape, usar pdf2svg en su lugar")
    parser.add_argument("--inkscape-path", help="Ruta al ejecutable de Inkscape (útil en Windows)")
    
    args = parser.parse_args()
    
    # Si el usuario proporcionó una ruta a Inkscape, la usamos
    inkscape_path = args.inkscape_path
    
    # Comprobamos dependencias
    deps_ok, auto_inkscape_path = check_dependencies(args.use_inkscape)
    
    # Si no se proporcionó una ruta a Inkscape pero la encontramos automáticamente, la usamos
    if not inkscape_path and auto_inkscape_path:
        inkscape_path = auto_inkscape_path
    
    if not deps_ok:
        return
    
    process_tex_files(
        directory=args.directory,
        clean=args.clean,
        keep_tex=args.keep_tex,
        keep_svg=args.keep_svg,
        keep_pdf=args.keep_pdf,
        use_inkscape=args.use_inkscape,
        inkscape_path=inkscape_path
    )
    
    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()