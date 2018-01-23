#!/usr/bin/env python3

#----------------------------------------------------------------------
"""
Create barcodes from processes and embed in a PDF with tasks
"""

class ProcessBarcode(canvas.Canvas):
    """

    #+begin_src ditaa :cmdline -E :file /home/oney/Schweizer Insektenzucht/Zucht/server/prozess_blatt.png
    +---------------------------------------------------------+
    |                         Kopzfzeile                      |
    |  Prozess werden dokumentiert durchs Scannen vom ersten  |
    |  Barcode. Dann werden die Prozessschritte gemacht.      |
    |  Folgend wird der finale barcode gescannt.       _\__/_ |
    |  Revision 1, Ensectable AG, Brian J. Oney        \-  -/ |
    |                                                   \`´/  |
    +---------------------------------------------------------+
    +---------------------------------------------------------+
    |     Prozess A                            Prozess A      |
    |      START                                  ENDE        |
    |    +---------+     +--------------+     +---------+     |
    |    |         |     | 1. Schritt   |     |         |     |
    |    | Barcode |     | 2. Scan Box  |     | Barcode |     |
    |    |         |     | 3. Schritt   |     |         |     |
    |    +---------+     +--------------+     +---------+     |
    +---------------------------------------------------------+
    +---------------------------------------------------------+
    |     Prozess B                            Prozess B      |
    |       START                                 ENDE        |
    |    +---------+     +--------------+     +---------+     |
    |    |         |     | 1. Schritt   |     |         |     |
    |    | Barcode |     | 2. Schritt   |     | Barcode |     |
    |    |         |     | 3. Schritt   |     |         |     |
    |    +---------+     +--------------+     +---------+     |
    +---------------------------------------------------------+
    #+end_src
    """

    from reportlab.graphics.barcode import createBarcodeDrawing
    from pandas import DataFrame
    # from pandas import read_csv as read
    # import pandas as pd
    from pandas import read_excel as read
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.lib import pagesizes

    pagesize = pagesizes.A4

    # TODO Read in csv
    csvfile = '/home/oney/Schweizer Insektenzucht/Zucht/standardanweisung/ablauf.xlsx'
    sheet_name = 'tenebrio_prozesse'
    def read_processes(csvfile, sheet_name=None):

        data = read(csvfile, sheet_name=sheet_name)
        data.dropna(0, 'all', inplace=True)

        return data

    
    processes_df = read_processes(csvfile, sheet_name)

    # Reshape
    def filter_processes(processes, process_col, steps_col, queries=None):
        if queries is not None:
            assert type(queries) is type(dict())
            assert type(processes) is type(DataFrame())
            assert all(type(x) is type(list()) for x in queries.values())
            assert all(x in processes.columns.tolist() for x in queries.keys())
            for key in queries.keys():
                # import pdb; pdb.set_trace() 
                processes.where(processes[key].isin(queries[key]), inplace=True)

        # processes = processes_df.to_dict()
        lists = {process: processes[steps_col][processes[process_col] == process].tolist()
                 for process in processes[process_col].unique()
        }
        assert all(type(x) is type(list()) for x in lists.values())
        return lists

    processes = filter_processes(processes_df, 'Prozess', 'Schritt',
                                 queries=dict(Wichtigkeit=['Lebensmittel']))

    # TODO create start and end barcodes
    start_format='START %s'
    end_format='ENDE %s'
    encoder='Code128'
    label_dims = (20, 20) * mm
    margins = (10, 10) * mm
    gaps = (10, 10) * mm
    procs_per_page = int(pagesize[1] / (label_dims[1]
                                        + 2 * margins[1] + gaps[1]))

    # make rows
    for i, process in enumerate(processes.keys()):
        row_pos = i * label_dims[1] + margins[1] * 1 if i in (0, procs_per_page) else 0
        style = getSampleStyleSheet()
        # center text and wrap if necessary
        style['Normal'].alignment = 1
        
        text = start_format.format(process)
        p = Paragraph(text, style=style["Normal"])
        width, height = p.wrapOn(self, *label_dims)
        p.drawOn(self, margins[0], row_pos)
        start_bc = createBarcodeDrawing(encoder,
                                        **dict(value=start_format.format(process),
                                               height=label_dims[1],
                                               width=label_dims[0]
                                        ))
        start_bc.drawOn(self, margins[0], row_pos[0] + height)

        text_pos_x = margins[0] + labels_dims[0] + gaps[0]
        text_pos_y = 0
        step_dims = (pagesize[0] - 2 * label_dims[0] + 2 * gaps[0],
                      label_dims[1] / len(processes[key]))
        for j, step in processes[key]:
            text = "%i. %s".format(j, step)
            p = Paragraph(text, style=style["Normal"])
            width, height = p.wrapOn(self, *step_dims)
            p.drawOn(self, text_pos_x, text_pos_y + row_pos)
            text_pos_y += height

        end_bc = createBarcodeDrawing(encoder,
                                      **dict(value=end_format.format(process),
                                             height=label_dims[1],
                                             width=label_dims[0]
                                      ))
        end_bc.drawOn(self, pagesize[0] - label_dims[0] - margins[0], row_pos[0])



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

