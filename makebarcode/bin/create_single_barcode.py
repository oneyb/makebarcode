#!/usr/bin/env python

#----------------------------------------------------------------------
"""
Create single barcode
"""

# # TODO: different output formats
# from reportlab.graphics import renderPM
# test = barcode.createBarcodeDrawing('Code128', **dict(value='00001', width=188.9, height=99.3))
# renderPM.drawToFile(test, 'test.png', 'PNG')
 

from makebarcode import SingleBarcodeCanvas

# if __name__ == '__main__':
def main():

    import argparse
    import importlib

    parser = argparse.ArgumentParser()
    parser.add_argument('-c',  '--code', help='String to be encoded')
    parser.add_argument('-y',  '--height',        default=2, dest='y', type=float, help='In centimeters')
    parser.add_argument('-x',  '--width',         default=3, dest='x', type=float, help='In centimeters')
    parser.add_argument('-e',  '--encoder',       default='Code128', help='Encoder to be used. E.g. QR')
    parser.add_argument('-s',  '--show_text',     default=1, type=int)
    parser.add_argument('-f',  '--filename',      default='barcode.pdf')
    parser.add_argument('-le', '--list-encoders', default=False, dest='le')
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

