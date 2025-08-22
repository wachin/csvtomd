#!/usr/bin/env python3

"""
csvtomd - Convert CSV files to Markdown tables

Este script convierte archivos CSV en tablas Markdown sin dependencias externas.
"""

import argparse
import csv
import sys

DEFAULT_PADDING = 2

def check_negative(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('"%s" debe ser un número entero' % value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError('"%s" no puede ser un valor negativo' % value)
    return ivalue

def pad_to(unpadded, target_len):
    """
    Rellena una cadena hasta la longitud objetivo, o devuelve la cadena original
    si es más larga que la longitud objetivo.
    """
    under = target_len - len(unpadded)
    if under <= 0:
        return unpadded
    return unpadded + (' ' * under)

def normalize_cols(table):
    """
    Rellena filas cortas para que coincidan con la fila más larga
    """
    longest_row_len = max([len(row) for row in table])
    for row in table:
        while len(row) < longest_row_len:
            row.append('')
    return table

def pad_cells(table):
    """Rellena cada celda al tamaño de la celda más grande en su columna."""
    col_sizes = [max(map(len, col)) for col in zip(*table)]
    for row in table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = pad_to(cell, col_sizes[cell_num])
    return table

def horiz_div(col_widths, horiz, vert, padding):
    """
    Crea los divisores horizontales para una tabla con anchos de columna dados.
    """
    horizs = [horiz * w for w in col_widths]
    div = ''.join([padding * ' ', vert, padding * ' '])
    return '|' + div.join(horizs) + '|'

def add_dividers(row, divider, padding):
    """Añade divisores y relleno a una fila de celdas y devuelve una cadena."""
    div = ''.join([padding * ' ', divider, padding * ' '])
    return '|' + div.join(row) + '|'

def md_table(table, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convierte un array 2D de elementos en una tabla Markdown.
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)

def csv_to_table(file, delimiter=','):
    return list(csv.reader(file, delimiter=delimiter))

def main():
    parser = argparse.ArgumentParser(
        description='Lee uno o más archivos CSV y muestra su contenido en forma de tablas Markdown.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Ejemplos:
  python3 csvtomd.py archivo.csv
  python3 csvtomd.py -p 1 archivo.csv
  python3 csvtomd.py -d ";" archivo.csv
  cat archivo.csv | python3 csvtomd.py'''
    )
    
    parser.add_argument('files', metavar='archivo_csv', type=str, nargs='*',
                        default=['-'],
                        help="Uno o más archivos CSV a convertir. Usa - para entrada estándar.")
    parser.add_argument('-p', '--padding', type=check_negative,
                        default=DEFAULT_PADDING,
                        help="Número de espacios entre celdas y divisores. Por defecto: %(default)s")
    parser.add_argument('-d', '--delimiter', default=',',
                        help='Delimitador CSV. Por defecto: "%(default)s"')

    args = parser.parse_args()

    if '-' in args.files and len(args.files) > 1:
        print('Error: La entrada estándar (-) solo puede usarse sola.', file=sys.stderr)
        sys.exit(1)
    
    for filename in args.files:
        if filename == '-':
            # Leer desde entrada estándar
            table = csv_to_table(sys.stdin, args.delimiter)
        else:
            # Leer desde archivo
            try:
                with open(filename, 'r', newline='', encoding='utf-8') as f:
                    table = csv_to_table(f, args.delimiter)
            except FileNotFoundError:
                print(f'Error: Archivo no encontrado: {filename}', file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f'Error al leer {filename}: {e}', file=sys.stderr)
                sys.exit(1)
        
        # Generar y mostrar tabla Markdown
        try:
            result = md_table(table, padding=args.padding)

            # Imprime en pantalla
            print(result)

            # Además, guarda en archivo .md
            if filename != '-':
                outname = filename.rsplit('.', 1)[0] + ".md"
                with open(outname, "w", encoding="utf-8") as out:
                    out.write(result + "\n")
        except Exception as e:
            print(f'Error al convertir la tabla: {e}', file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
