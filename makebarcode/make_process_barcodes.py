#!/usr/bin/env python3

#----------------------------------------------------------------------
"""
Create barcodes from processes and embed in a PDF with tasks
"""

class ProcessBarcode(canvas.Canvas):

    from reportlab.graphics.barcode import createBarcodeDrawing

    # TODO Read in csv
    csvfile = '/home/oney/Schweizer Insektenzucht/Zucht/standardanweisung/ablauf.xlsx'
    sheetname = 'tenebrio_prozesse'
    def get_processes(csvfile):
        # from pandas import read_csv as read
        # import pandas as pd
        from pandas import read_excel as read

        data = read(csvfile, sheetname=sheetname)
        data.dropna(0, 'all', inplace=True)

        return data

    
    processes = get_processes(csvfile)

    # Reshape
    def shape_processes(processes, process_col, step_col):
        todo_list = {process: processes[step_col][processes[process_col] == process].tolist()
                     for process in processes[process_col].unique()}
        return todo_list

    processes_shp = shape_processes(processes, 'Prozess', 'Schritt')

    # TODO create start and end barcodes
    start_format='START %s'
    end_format='ENDE %s'
    encoder='Code128'

    # filter processes
    # make rows
    barcodes = {}
    for i, process in processes.iterkeys():
        barcodes[process] = createBarcodeDrawing(encoder,
                             **dict(value=start_format.format(process),
                                    # height=(label_height - height) * 0.92,
                                    # width=label_width
                             )
        )

        pass
    
    barcodes = make_start_and_end_barcodes(csvfile)

    # TODO put on pdf
    def get_processes(csvfile):
        pass
    # TODO list process steps
    def list_processes(csvfile):
        pass
    # TODO make page a color or give a watermark
    def get_processes(csvfile):
        pass








































    def draw_labels(self, codes, encoder, label_height, label_width,
                    no_labels_x, no_labels_y, x_gap, x_offset, y_gap,
                    y_offset, show_text=1):

        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph
        from reportlab.graphics import barcode


        if show_text==0:
            height = 0
        else:
            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            style = getSampleStyleSheet()
            # center text and wrap if necessary
            style['Normal'].alignment = 1


        for i, code in enumerate(codes):
            if i % no_labels_x == 0:
                x = x_offset

            y = y_offset + i / no_labels_x * label_height + i / no_labels_x * y_gap

            if show_text!=0:
                p = Paragraph(code, style=style["Normal"])
                width, height = p.wrapOn(self, label_width, label_height * 0.3)
                # self.drawCentredString(x + label_width / 2, y + label_height - height, code)
                p.drawOn(self, x, y + label_height - height)

            encoded = barcode.createBarcodeDrawing(encoder,
                                                   **dict(value=code,
                                                          height=(label_height - height) * 0.92,
                                                          width=label_width))
            # import pdb; pdb.set_trace() 
            encoded.drawOn(self, x, y)
            x = x + label_width + x_gap


# if __name__ == '__main__':
def main():

    import argparse
    import importlib

    parser = argparse.ArgumentParser()
    parser.add_argument('-c',  '--codes',         default='0001')
    parser.add_argument('-f',  '--filename',      default='barcodes')
    parser.add_argument('-r',  '--recipe',        default='avery_3475')
    parser.add_argument('-e',  '--encoder',       default='Code128', help='Encoder to be used. E.g. QR')
    parser.add_argument('-s',  '--show_text',     default=1,         type=int)
    parser.add_argument('-le', '--list-encoders', default=False,     dest='le', action='store_true')
    parser.add_argument('-lr', '--list-recipes',  default=False,     dest='lr', action='store_true')
    args = parser.parse_args()

    if args.le:
        import sys
        from reportlab.graphics import barcode
        print('\nAccepted encoders are:\n')
        sys.stdout.write('\t' + '\n\t'.join(barcode.getCodeNames()) + '\n\n')
        sys.exit(0)

    if args.lr:
        import sys
        from makebarcode.recipe_database import DATABASE as DB
        print('\nDescribed recipes are:\n')
        import sys
        sys.stdout.write('\t' + '\n\t'.join(DB.keys()) + '\n\n')
        sys.stdout.write('\n\tWould you like to contribute metrics for a certain label paper?\n\tPlease do so at:\n\thttps://github.com/oneyb/reportlab-barcode-recipes')
        sys.exit(0)


    # import pdb; pdb.set_trace() 

    # Reportlab imports
    from reportlab.graphics import barcode
    from reportlab.lib import pagesizes

    # import recipes
    from makebarcode.recipe_database import DATABASE as DB

    # Set important variables
    if args.encoder not in barcode.getCodeNames():
        import sys
        print('\nStopping here.\nAccepted encoders are:\n')
        sys.stdout.write('\t' + '\n\t'.join(barcode.getCodeNames()) + '\n\n')
        raise NameError, "{0} not an accepted barcode encoder".format(args.barcode)


    recipe = DB.get(args.recipe)
    pagesize = getattr(pagesizes, recipe.pop('pagesize') if recipe.get('pagesize') is not None else 'A4')

    import re
    found_script = re.search('[\[\]*./_-]', args.codes)
    if found_script is not None:
        try:
            codes = eval(args.codes)
        except NameError:
                locals().update(recipe)
                codes = eval(args.codes)
    else:
        from warnings import warn
        warn("The ID to be encoded is not python code. Assuming it's a unique string.", Warning)
        codes = [args.codes
                 for x in range(recipe.get('no_labels_y') *
                                recipe.get('no_labels_x'))]

    # import pdb; pdb.set_trace

    # make the pdf
    pdf = BarcodeCanvas(args.filename
                        ,pagesize = pagesize
                        ,bottomup = 0
    )
     
    pdf.draw_labels(codes, args.encoder, show_text=args.show_text, **recipe)
    pdf.showPage()
    pdf.save()

if __name__ == '__main__':
    main()

