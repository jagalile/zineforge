import fitz  # PyMuPDF
import math
import argparse 

# --- Lógica de Imposición ---
def obtener_orden_imposicion(num_paginas_reales, fill_position):
    """
    Calcula el orden de las páginas para la imposición de folleto (zine), 
    controlando dónde se insertan las páginas en blanco de relleno.
    """
    n = num_paginas_reales
    N = math.ceil(n / 4) * 4 
    num_relleno = N - n
    
    indices_relleno = list(range(n, N)) 
    
    if num_relleno > 0:
        if fill_position == 'before_last':
            contenido_inicio = list(range(n - 1)) 
            ultima_pagina = [n - 1] 
            indices_secuenciales = contenido_inicio + indices_relleno + ultima_pagina
            
        elif fill_position == 'end':
            indices_secuenciales = list(range(n)) + indices_relleno
            
        else:
            raise ValueError("Valor de fill_position no válido. Use 'end' o 'before_last'.")
    else:
        indices_secuenciales = list(range(n))

    orden = []
    for i in range(N // 4):
        indice_izq_a = N - 1 - 2 * i 
        indice_der_a = 0 + 2 * i      
        orden.append(indices_secuenciales[indice_izq_a])
        orden.append(indices_secuenciales[indice_der_a])
        
        indice_izq_b = 1 + 2 * i      
        indice_der_b = N - 2 - 2 * i  
        orden.append(indices_secuenciales[indice_izq_b])
        orden.append(indices_secuenciales[indice_der_b])
        
    return orden, num_relleno

# --- Lógica de Conversión Actualizada ---
def crear_zine_imposicion_horizontal(input_pdf_path, output_pdf_path, fill_position):
    """
    Convierte un PDF secuencial A5 a un PDF A4 apaisado en formato 'zine' (imposición),
    añadiendo páginas en blanco si es necesario y una guía de doblado en la primera hoja.
    """

    try:
        doc_in = fitz.open(input_pdf_path)
        num_paginas_reales = len(doc_in)
        
        if num_paginas_reales == 0:
            print("El PDF está vacío.")
            return

        orden_paginas_indice_base_0, num_relleno = obtener_orden_imposicion(num_paginas_reales, fill_position)
        print(f"📖 PDF de entrada: **{input_pdf_path}**")
        print(f"Posición de relleno: **{fill_position}**")
        print(f"Páginas originales: {num_paginas_reales}. Relleno necesario: {num_relleno}.")
        
        doc_out = fitz.open()

        A4_LANDSCAPE_WIDTH = 842
        A4_LANDSCAPE_HEIGHT = 595
        A5_WIDTH_ON_A4 = A4_LANDSCAPE_WIDTH / 2
        
        # 2. Iterar y colocar en el nuevo A4 apaisado
        for i in range(0, len(orden_paginas_indice_base_0), 2):
            idx1 = orden_paginas_indice_base_0[i]
            idx2 = orden_paginas_indice_base_0[i + 1]
            
            new_page = doc_out.new_page(width=A4_LANDSCAPE_WIDTH, height=A4_LANDSCAPE_HEIGHT)
            
            # Colocar la página de la izquierda (idx1)
            if idx1 < num_paginas_reales:
                rect_left = fitz.Rect(0, 0, A5_WIDTH_ON_A4, A4_LANDSCAPE_HEIGHT)
                new_page.show_pdf_page(rect_left, doc_in, idx1)
                print(f"Hoja {doc_out.page_count}: Izquierda (Pág {idx1+1})")
            else:
                print(f"Hoja {doc_out.page_count}: Izquierda (Pág en blanco)")

            # Colocar la página de la derecha (idx2)
            if idx2 < num_paginas_reales:
                rect_right = fitz.Rect(A5_WIDTH_ON_A4, 0, A4_LANDSCAPE_WIDTH, A4_LANDSCAPE_HEIGHT)
                new_page.show_pdf_page(rect_right, doc_in, idx2)
                print(f"Hoja {doc_out.page_count}: Derecha (Pág {idx2+1})")
            else:
                print(f"Hoja {doc_out.page_count}: Derecha (Pág en blanco)")

            # --- AÑADIR LÍNEA GUÍA DE DOBLADO SOLO EN LA PRIMERA PÁGINA DE SALIDA ---
            if doc_out.page_count == 1: # Esto es la primera página A4 generada
                center_x = A4_LANDSCAPE_WIDTH / 2
                start_point = fitz.Point(center_x, 0) # Desde arriba
                end_point = fitz.Point(center_x, A4_LANDSCAPE_HEIGHT) # Hasta abajo
                
                new_page.draw_line(
                    start_point, 
                    end_point, 
                    color=(0, 0, 0), # Negro
                    width=0.5,       # Fina
                    dashes=[1, 2]    # Línea discontinua (guía)
                )
                print(f"  --> Añadida línea guía de doblado en la Hoja {doc_out.page_count}.")


        # Guardar el documento de salida
        doc_out.save(output_pdf_path)
        doc_out.close()
        doc_in.close()
        
        print(f"\n✅ Conversión completada. Archivo listo para imprimir guardado en: **{output_pdf_path}**.")

    except FileNotFoundError:
        print(f"❌ Error: El archivo de entrada '{input_pdf_path}' no fue encontrado.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

# --- Bloque de Argumentos (Sin cambios) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convierte un PDF secuencial (A5) en un PDF A4 apaisado con imposición de zine (folleto).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Ruta del archivo PDF de entrada (ej: mi_zine_a5_secuencial.pdf)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="zine_listo_para_imprimir.pdf",
        help="Ruta del archivo PDF de salida (por defecto: zine_listo_para_imprimir.pdf)"
    )
    
    parser.add_argument(
        "-f", "--fill-position",
        type=str,
        default="end",
        choices=["end", "before_last"],
        help="Define dónde se insertan las páginas en blanco:\n"
             "  end: Al final del documento original (1, 2, ..., última, BLANCO)\n"
             "  before_last: Justo antes de la última página (1, 2, ..., BLANCO, última)\n"
             "(Por defecto: end)"
    )
    
    args = parser.parse_args()
    
    crear_zine_imposicion_horizontal(args.input_file, args.output, args.fill_position)