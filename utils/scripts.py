import pandas as pd
import re

def clean_string(text):
    # Elimina acentos y convierte a mayúsculas
    replacements = {
        'á': 'A', 'é': 'E', 'í': 'I', 'ó': 'O', 'ú': 'U',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'N', 'Ñ': 'N',
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    return text.upper()

def format_registro_1(row):
    try:        
        # excel:
        # TIPO	MODELO	EJERCICIO	CIF	NOMBRE DECLARANTE	TIPO DE SOPORTE C/T	TELEFONO PRESENTADOR	NOMBRE DEL PRESENTADOR	NUMERO DE JUSTIFICANTE DE LA DECLARACION	DECLARACION COMPLEMENTARIA O SUSTITUTIVA	NUMERO IDENTIFICATIVO DE LA DECLARACIÓN ANTERIOR	NUMERO TOTAL DE REGISTROS DE DECLARADOS	IMPORTE TOTAL	NATURALEZA DEL DECLARANTE
        # 2	182	2024	G83536565	AIPC PANDORA	T	914137768	HERNANDEZ SUELA, JUAN PEDRO	1820000000000	00	0000000000000	0000267	000000003135400	1

        # salida:
        # 11822024G83536565AIPC PANDORA                            T914137768HERNANDEZ SUELA, JUAN PEDRO             1820000000000  00000000000000000000020000000000040001                                                                                          

        tipo_registro = str(row['TIPO']).zfill(1)
        modelo = str(row['MODELO']).zfill(3)
        ejercicio = str(row['EJERCICIO']).zfill(4)
        cif = str(row['CIF']).strip()
        nombre_declarante = clean_string(str(row['NOMBRE DECLARANTE']).strip())[:40]
        tipo_soporte = str(row['TIPO DE SOPORTE C/T']).upper()
        telefono_presentador = str(row['TELEFONO PRESENTADOR']).strip()
        nombre_presentador = clean_string(str(row['NOMBRE DEL PRESENTADOR']).strip())
        numero_justificante = str(row['NUMERO DE JUSTIFICANTE DE LA DECLARACION']).strip()
        declaracion_complementaria = str(row['DECLARACION COMPLEMENTARIA O SUSTITUTIVA']).strip().zfill(2)
        numero_identificativo_anterior = str(row['NUMERO IDENTIFICATIVO DE LA DECLARACION ANTERIOR']).strip().zfill(14)
        numero_total_registros = str(row['NUMERO TOTAL DE REGISTROS DE DECLARADOS']).zfill(6)
        importe_total = str(row['IMPORTE TOTAL']).zfill(15)
        naturaleza_declarante = str(row['NATURALEZA DEL DECLARANTE']).upper()

        registro = (
            tipo_registro +  # 1
            modelo +  # 2-4
            ejercicio +  # 5-8
            cif +  # 9-17
            nombre_declarante.ljust(40) +  # 18-57
            tipo_soporte +  # 58
            telefono_presentador.ljust(9) +  # 59-67
            nombre_presentador.ljust(40) +  # 68-107
            numero_justificante + "  " +  # 108-120
            declaracion_complementaria +  # 121-122
            numero_identificativo_anterior +  # 123-135
            numero_total_registros +  # 136-141
            importe_total +  # 142-156
            naturaleza_declarante +  # 157
            ' ' * 90  # 158-250
        )

        return registro

    except Exception as e:
        return f"Error procesando fila: {row.to_dict()}" + f"Error específico: {str(e)}"


def format_registro_2(row):
    try:
        # Valores fijos
        tipo_registro = str(row['TIPO']).zfill(1)
        modelo = str(row['MODELO']).zfill(3)
        ejercicio = str(row['EJERCICIO']).zfill(4)
        cif = str(row['CIF']).strip()
        
        # Procesamiento de campos
        codigo = str(row['CODIGO']).zfill(2)

        dni = str(row['DNI/NIF']).strip() if codigo != '99' else '         '
        nombre = clean_string(str(row['NOMBRE']).strip())[:40]
        codigo = str(row['CODIGO']).zfill(2)
        
        # Manejo del importe
        importe_str = str(row['IMPORTE']).replace(',', '.')
        importe = str(int(float(importe_str) * 100)).zfill(11)
        
        # Manejo de recurrencia
        recurrente = '1' if str(row['RECURRENTE']).upper() == 'SI' else '2'
        
        # Campo CLAVE (posición 78)
        clave = 'A'  # Por defecto usamos A
        
        # Campo % DEDUCCIÓN (posiciones 79-83)
        porcentaje = row['%']
        porcentaje_entero = str(int(float(str(porcentaje)))).zfill(3)
        porcentaje_decimal = '00'
        
        # Campo NATURALEZA DEL DECLARADO (posición 105)
        naturaleza = str(row['F/J']).upper() # Para personas físicas
        
        # Construcción del registro
        registro = (
            tipo_registro +  # 1
            modelo +  # 2-4
            ejercicio +  # 5-8
            cif +  # 9-17
            dni.ljust(9) +  # 18-26
            ' ' * 9 +  # NIF representante legal (27-35)
            nombre.ljust(40) +  # 36-75
            codigo +  # 76-77
            clave +  # 78
            porcentaje_entero +  # 79-81
            porcentaje_decimal +  # 82-83
            '00' + importe +  # 84-96
            ' ' +  # Donativo en especie (97)
            '00' +  # Deducción Com. Autónoma (98-99)
            '00000' +  # % Deducción Com. Autónoma (100-104)
            naturaleza +  # 105
            ' ' +  # Revocación (106)
            '0000' +  # Ejercicio donación revocada (107-110)
            ' ' +  # Tipo de bien (111)
            ' ' * 20 +  # Identificación del bien (112-131)
            recurrente +  # Recurrencia donativos (132)
            ' ' * 118  # Resto de campos hasta 250
        )
        
        return registro
    except Exception as e:
        return f"Error procesando fila: {row.to_dict()}" + f"Error específico: {str(e)}"

def convert_excel_to_182(input_file, output_file):
    try:
        # Leer el archivo Excel especificando la codificación
        sheets = pd.read_excel(input_file, sheet_name=['DECLARADOS', 'CABECERA'])
        declarados_df = sheets['DECLARADOS']
        cabecera_df = sheets['CABECERA']

        registros = []

        # Tratar pestaña CABECERA
        if 'CABECERA' in sheets:
            try:
                # Ir a la pestaña CABECERA del excel y procesar la fila 1
                    registro = format_registro_1(cabecera_df.iloc[0])
                    registros.append(registro)
                    
                
            except Exception as e:
                return f"Error procesando la fila 1: {str(e)}"

        # Tratar pestaña DECLARADOS
        if 'DECLARADOS' in sheets:            
            # Procesar cada fila y generar registros
            for index, row in declarados_df.iterrows():
                try:
                    registro = format_registro_2(row)
                    registros.append(registro)
                except Exception as e:
                    return f"Error procesando la fila {index + 2}: {str(e)}"

        # Escribir al archivo de salida
        if registros:
            # Asegurese que el fichero es de texto y con el código de caracteres ISO-8859-1 / UTF8. Posiblemente el fichero de salida sea ISO-8859-1. Posición 2565

            with open(output_file, 'w', encoding='iso-8859-1') as f:
                for registro in registros:
                    f.write(registro + '\n')
            return f"Archivo {output_file} generado correctamente."
        else:
            return "No se generaron registros para escribir."
            
    except Exception as e:
        return f"Error general: {str(e)}"

# Uso del script
if __name__ == "__main__":
    input_file = "../../../../../LocalDesktop/script_mama/input3.xlsx"  # Ajusta el nombre de tu archivo Excel
    output_file = "../../../../../LocalDesktop/script_mama/fichero.182"
    
    convert_excel_to_182(input_file, output_file)