import fitz  # PyMuPDF
import math
import argparse # Módulo para manejar argumentos de línea de comandos

# --- Lógica de Imposición (Se mantiene igual) ---
def obtener_orden_imposicion(num_paginas_reales):
    """
    Calcula el orden de las páginas para la imposición de folleto (zine).
    Devuelve la lista de índices de página (base 0) y el número de rellenos.
    """
    n = num_paginas_reales
    N = math.ceil(n / 4) * 4 
    num_relleno = N - n
    
    indices_secuenciales = list(range(n)) + list(range(n, N))

    orden = []
    # Genera el orden de impresión (Última, Primera) y (Segunda, Penúltima)
    for i in range(N // 4):
        # Primer par (externo)
        indice_izq_a = N - 1 - 2 * i 
        indice_der_a = 0 + 2 * i      
        
        orden.append(indices_secuenciales[indice_izq_a])
        orden.append(indices_secuenciales[indice_der_a])
        
        # Segundo par (interno)
        indice_izq_b = 1 + 2 * i      
        indice_der_b = N - 2 - 2 * i  
        
        orden.append(indices_secuenciales[indice_izq_b])
        orden.append(indices_secuenciales[indice_der_b])
        
    return orden, num_relleno

# --- Lógica de Conversión (Se mantiene igual) ---
def crear_zine_imposicion_horizontal(input_pdf_path, output_pdf_path):
    """
    Convierte un PDF secuencial A5 a un PDF A4 apaisado en formato 'zine' (imposición).
    """

    try:
        doc_in = fitz.open(input_pdf_path)
        num_paginas_reales = len(doc_in)
        
        if num_paginas_reales == 0:
            print("El PDF está vacío.")
            return

        orden_paginas_indice_base_0, num_relleno = obtener_orden_imposicion(num_paginas_reales)
        print(f"📖 PDF de entrada: **{input_pdf_path}**")
        print(f"Número de páginas originales: {num_paginas_reales}. Relleno necesario: {num_relleno}.")
        
        doc_out = fitz.open()

        # Dimensiones A4 Apaisado (Horizontal) en puntos
        A4_LANDSCAPE_WIDTH = 842
        A4_LANDSCAPE_HEIGHT = 595
        A5_WIDTH_ON_A4 = A4_LANDSCAPE_WIDTH / 2
        A5_HEIGHT_ON_A4 = A4_LANDSCAPE_HEIGHT

        # 2. Iterar sobre el orden de imposición de dos en dos
        for i in range(0, len(orden_paginas_indice_base_0), 2):
            idx1 = orden_paginas_indice_base_0[i]
            idx2 = orden_paginas_indice_base_0[i + 1]
            
            new_page = doc_out.new_page(width=A4_LANDSCAPE_WIDTH, height=A4_LANDSCAPE_HEIGHT)
            
            # 3. Colocar la primera página (Izquierda)
            if idx1 < num_paginas_reales:
                rect_left = fitz.Rect(0, 0, A5_WIDTH_ON_A4, A5_HEIGHT_ON_A4)
                new_page.show_pdf_page(rect_left, doc_in, idx1)
                print(f"Hoja {doc_out.page_count}: Izquierda (Pág {idx1+1} de contenido)")
            else:
                print(f"Hoja {doc_out.page_count}: Izquierda (Pág en blanco)")

            # 4. Colocar la segunda página (Derecha)
            if idx2 < num_paginas_reales:
                rect_right = fitz.Rect(A5_WIDTH_ON_A4, 0, A4_LANDSCAPE_WIDTH, A5_HEIGHT_ON_A4)
                new_page.show_pdf_page(rect_right, doc_in, idx2)
                print(f"Hoja {doc_out.page_count}: Derecha (Pág {idx2+1} de contenido)")
            else:
                print(f"Hoja {doc_out.page_count}: Derecha (Pág en blanco)")

        # Guardar el documento de salida
        doc_out.save(output_pdf_path)
        doc_out.close()
        doc_in.close()
        
        print(f"\n✅ Conversión completada. Archivo listo para imprimir guardado en: **{output_pdf_path}**.")

    except FileNotFoundError:
        print(f"❌ Error: El archivo de entrada '{input_pdf_path}' no fue encontrado.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

# --- Nuevo Bloque de Argumentos ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convierte un PDF secuencial (A5) en un PDF A4 apaisado con imposición de zine (folleto).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Argumento obligatorio para el archivo de entrada
    parser.add_argument(
        "input_file",
        type=str,
        help="Ruta del archivo PDF de entrada (ej: mi_zine_a5_secuencial.pdf)"
    )
    
    # Argumento opcional para el archivo de salida
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="zine_listo_para_imprimir.pdf",
        help="Ruta del archivo PDF de salida (por defecto: zine_listo_para_imprimir.pdf)"
    )
    
    args = parser.parse_args()
    
    crear_zine_imposicion_horizontal(args.input_file, args.output)