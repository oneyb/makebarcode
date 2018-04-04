#!/usr/bin/env python

#----------------------------------------------------------------------
"""
Create barcodes and embed in a PDF
"""

from makebarcode import BarcodeCanvas

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
                 for x in range(recipe.get('n_labels_y') *
                                recipe.get('n_labels_x'))]

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

