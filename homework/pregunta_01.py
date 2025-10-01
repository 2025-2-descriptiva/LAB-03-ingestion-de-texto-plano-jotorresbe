"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import re

#print(bloques)
def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    with open('files/input/clusters_report.txt') as f:
        lineas = f.read()

    # Separando .txt por salto de linea
    linea = lineas.split('\n')

    # Tomo el header en un solo string 
    header_text = '\n'.join(linea[:2])
    # En una lista agrego cada elemento por separado 
    # Dividiendo mi string por cada 2 espacios o más
    # Elimino espacios adelante y atrás de str
    header_text = re.split(r'\s{2,}', header_text.strip())

    # Lista donde almacenaré los headers
    header_final = []


    # Recorro mi lista de header previa y busco si tienen "de"
    # para agregarles "palabras clave" que está en la última posición
    # Si no, agregamos el item sin cambios
    for elemento in range(len(header_text)):
        if "de" in header_text[elemento]:
            header_final.append(header_text[elemento]+" "+header_text[-1])
        else:
            header_final.append(header_text[elemento])

    # Estandarizo a minúsculas, borro espacios en blanco iniciales
    # Reemplazo espacios en blanco entre las palabras con '_' 
    # Si el item no tiene espacios en blanco al inicio o al final
    header_final = [x.lower().lstrip().replace(' ', '_') for x in header_final if x.strip()]

    # Retorno 2 últimos items (ya que los dos últimos son 'palabras clave')
    header_final = header_final[:-2]

    # Regex donde busco salto de linea \n
    # cero o más espacios en blanco \s*
    # \d+ una o más cifras
    # \s+ uno o más espacios en blanco (como separador entre #)
    # \d+ para procesar el 2do número 
    # \d+ uno o más espacios en blanco
    # [\d,]+ uno o mas caracteres que sean digitos o comas: 1,23
    # \s? cero o un espacio antes de %
    # %: pues el porcentaje

    # La idea global es verificar si mi linea empieza tipo:
    # \n con tab tal vez y sigue con: 
    # numero <espacio> numero2 <espacio> numero_con_coma <espacio opcional>%
    bloques = re.split(r"(?=\n\s*\d+\s+\d+\s+[\d,]+\s?%)", lineas)

    patron = re.compile(r"^(\d+)\s+(\d+)\s+([\d,]+\s?%)\s+(.*)$")
    
    datos = []
    # Divido cada linea para asignarla en su regex correspondiente
    # Al final a cada grupo lo agrego a mi lista limpia
    for bloque in bloques:
        # Quitar saltos de línea internos y espacios múltiples
        linea = " ".join(bloque.split()) 
        match = patron.match(linea)
        if match:
            rank = int(match.group(1))
            count = int(match.group(2))
            percentage = match.group(3)
            keywords = match.group(4)
            datos.append([rank, count, percentage, keywords])
        else:
            continue
    # Creo el df para limpiar los %, reemplazar las comas por puntos
    # Y quitar los puntos finales donde hay   
    df_final = pd.DataFrame(datos, columns=header_final)
    df_final['porcentaje_de_palabras_clave']=df_final['porcentaje_de_palabras_clave'].str.strip("%").str.replace(",",'.').astype(float)
    df_final['principales_palabras_clave'] = df_final['principales_palabras_clave'].str.strip('.')

    return df_final

print(pregunta_01())
