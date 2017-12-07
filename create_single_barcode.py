#!/usr/bin/env python

#----------------------------------------------------------------------
"""
Create single barcode
"""


from reportlab.pdfgen import canvas

class SingleBarcodeCanvas(canvas.Canvas):

    def draw_labels(self, code, x, y, encoder, show_text=1): 
        """Draws barcode label on the Canvas-based SingleBarcodeCanvas class"""

        from reportlab.graphics import barcode

        if show_text==0:
            height = 0
        else:
            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            style = getSampleStyleSheet()
            # center text and wrap if necessary
            style['Normal'].alignment = 1
            p = Paragraph(code, style=style["Normal"])
            width, height = p.wrapOn(self, x, y)
            p.drawOn(self, 0, 0)

        encoded = barcode.createBarcodeDrawing(encoder,
                                               **dict(value  =code,
                                                      height =y - height,
                                                      width  =x))
        # import pdb; pdb.set_trace() 
        encoded.drawOn(self, 0, 0 + height)


# if __name__ == '__main__':
def main():

    import argparse
    import importlib

    parser = argparse.ArgumentParser()
    parser.add_argument('-c',  '--code', help='String to be encoded')
    parser.add_argument('-y',  '--height',        default=2, dest='y', type=float)
    parser.add_argument('-x',  '--width',         default=2, dest='x', type=float)
    parser.add_argument('-e',  '--encoder',       default='Code128', help='Encoder to be used. E.g. QR')
    parser.add_argument('-s',  '--show_text',     default=1, type=int)
    parser.add_argument('-f',  '--filename',      default='barcode.pdf')
    parser.add_argument('-le', '--list-encoders', dest='le', default=False)
    args = parser.parse_args()

    if args.le:
        import sys
        from reportlab.graphics import barcode
        print('\nAccepted encoders are:\n')
        sys.stdout.write('\t' + '\n\t'.join(barcode.getCodeNames()) + '\n\n')
        raise NameError, "{0} not an accepted barcode encoder".format(args.encoder)
        sys.exit(0)


    # import pdb; pdb.set_trace() 

    # Reportlab imports
    from reportlab.graphics import barcode
    from reportlab.lib.units import cm

    # Set important variables
    if args.encoder not in barcode.getCodeNames():
        import sys
        print('\nStopping here.\nAccepted encoders are:\n')
        sys.stdout.write('\t' + '\n\t'.join(barcode.getCodeNames()) + '\n\n')
        raise NameError, "{0} not an accepted barcode encoder".format(args.barcode)

    # make the pdf
    pdf = SingleBarcodeCanvas(args.filename
                              ,pagesize = (args.x * cm, args.y * cm)
                              # ,bottomup = 0
    )
     
    #ef draw_labels(self, code, h, w, encoder, show_text=1): 
    pdf.draw_labels(args.code, args.x * cm, args.y * cm, args.encoder, args.show_text)
    pdf.showPage()
    pdf.save()

if __name__ == '__main__':
    main()

