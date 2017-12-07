#!/usr/bin/env python

#----------------------------------------------------------------------
"""
Create barcodes and embed in a PDF
"""

from reportlab.pdfgen import canvas

class BarcodeCanvas(canvas.Canvas):

    def draw_labels(self, codes, encoder, label_height, label_width,
                    no_labels_x, no_labels_y, x_gap, x_offset, y_gap, y_offset, show_text=1): 
        """Draws barcode labels on the Canvas-based BarcodeCanvas class"""

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
                                                          height=(label_height - height) * 0.98,
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
    parser.add_argument('-le', '--list-encoders', default=False,     dest='le')
    parser.add_argument('-lr', '--list-recipes',  default=False,     dest='lr')
    args = parser.parse_args()

    if args.le:
        import sys
        from reportlab.graphics import barcode
        print('\nAccepted encoders are:\n')
        sys.stdout.write('\t' + '\n\t'.join(barcode.getCodeNames()) + '\n\n')
        raise NameError, "{0} not an accepted barcode encoder".format(args.encoder)
        sys.exit(0)

    if args.lr:
        import sys
        from recipe_database import DATABASE as DB
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
    from recipe_database import DATABASE as DB

    # Set important variables
    if args.encoder not in barcode.getCodeNames():
        import sys
        print('\nStopping here.\nAccepted encoders are:\n')
        sys.stdout.write('\t' + '\n\t'.join(barcode.getCodeNames()) + '\n\n')
        raise NameError, "{0} not an accepted barcode encoder".format(args.barcode)


    recipe = DB.get(args.recipe)
    pagesize = getattr(pagesizes, recipe.pop('pagesize') if recipe.get('pagesize') is not None else 'A4')

    try:
        codes = eval(args.codes)
    except NameError:
        locals().update(recipe)
        codes = eval(args.codes)
    except:
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
