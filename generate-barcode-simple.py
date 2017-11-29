#!/usr/bin/env python

#----------------------------------------------------------------------
"""
Create barcodes and embed in a PDF
"""

from recipe_database import SCANNER

from reportlab.pdfgen import canvas



def find_dims_simple(code, label_width, label_height, encoder,
                     tolerance=SCANNER.get('tolerance')):
    barWidth, barHeight = label_width * 0.9, label_height 
    while True:
        encoded = encoder(code, barWidth=barWidth)
        if encoded.width >= label_width:
            barWidth = barWidth - 0.1 
        else:
            break
    while True:
        encoded = encoder(code, barHeight=barHeight)
        if encoded.height >= label_height * .76:
            barHeight = barHeight - 0.1
        else:
            break
    # TODO: adjust string height
    # while True:
    #     c.drawString(x + label_width / 3, y + label_height * 0.9, code)
    #     encoded = encoder(code, barHeight=barHeight, barWidth=barWidth)
    #     if encoded.height >= label_height * .76:
    #         barHeight = barHeight - 0.1 * mm
    #     else:
    #         break
    if barWidth <= tolerance:
        raise BaseException, "the paper or label size results in 'barWidth' being too narrow"
    return barWidth, barHeight

def find_dims(code, label_width, label_height, encoder,
              tolerance=SCANNER.get('tolerance')):
    """Better way of finding dimensions of barcode"""

    encoded = encoder(code)
    barWidth, barHeight = encoded.barWidth, label_height

    # Find width
    barcode_barWidth_ratio = encoded.width / encoded.barWidth
    while True:
        encoded = encoder(code, barHeight=barHeight,
                          barWidth=label_width / barcode_barWidth_ratio)
        if encoded.width <= label_width:
            barcode_barWidth_ratio = barcode_barWidth_ratio - 0.01
        else:
            barWidth = label_width / barcode_barWidth_ratio
            break

    # TODO: use drawHumanReadable
    # TODO: adjust string height
    # while True:
    #     c.drawString(x + label_width / 3, y + label_height * 0.9, code)
    #     encoded = encoder(code, barHeight=barHeight, barWidth=barWidth)
    #     if encoded.height >= label_height * .76:
    #         barHeight = barHeight - 0.01 * mm
    #     else:
    #         break

    # find height
    while True:
        encoded = encoder(code, barWidth=barWidth, barHeight=barHeight)
        if encoded.height >= label_height * .76:
            barHeight = barHeight - 0.1 
        else:
            break
    # import pdb; pdb.set_trace() 
    if barWidth <= tolerance:
        raise BaseException, "the paper or label size results in 'barWidth' being too narrow"
    return barWidth, barHeight


# barWidth2, barHeight2 = find_dims_old(codes[0], label_width, label_height)
# print((barWidth, barHeight, barWidth2, barHeight2))

class BarcodeCanvas(canvas.Canvas):

    def draw_labels(self, codes, encoder, label_height, label_width,
                    no_labels_x, no_labels_y, x_gap, x_offset, y_gap, y_offset): 
        """Draws barcode labels on the Canvas-based BarcodeCanvas class"""
        # import pdb; pdb.set_trace() 
        # settings based on command line or recipes

        # print codes

        barWidth, barHeight = find_dims(codes[0], label_width, label_height, encoder)

        for i, code in enumerate(codes):
            if i % no_labels_x == 0:
                x = x_offset
            y = y_offset + i / no_labels_x * label_height + i / no_labels_x * y_gap
            encoded = encoder(code, barHeight=barHeight, barWidth=barWidth)
            encoded.drawOn(self, x, y)
            self.drawString(x + label_width / 2.67, y + label_height * 0.9, code)
            # if i == 5:
            #     import pdb; pdb.set_trace() 
            x = x + label_width + x_gap


# if __name__ == '__main__':
def main():

    import argparse
    import importlib

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--codes', default='0001')
    parser.add_argument('-f', '--filename', default='barcodes')
    parser.add_argument('-r', '--recipe', default='avery_3475')
    parser.add_argument('-b', '--barcode', default='code128')
    parser.add_argument('-l', '--list-recipes', dest='lr',
                        action='store_true', default=True)
    args = parser.parse_args()

    # TODO: prettier --list-recipes
    # if args.lr:
    #     from recipe_database import DATABASE as DB
    #     from pprint import pprint as pp
    #     pp(DB.keys())

    # Reportlab imports
    from reportlab.graphics.shapes import Drawing 
    from reportlab.graphics import renderPDF, barcode
    import reportlab.lib.pagesizes

    # import recipes
    from recipe_database import SCANNER, ENCODER_FUNCTIONS
    from recipe_database import DATABASE as DB
    
    # Set important variables
    encoder = ENCODER_FUNCTIONS.get(args.barcode)
    if encoder is None:
        print('\nAccepted encoders:\n')
        import sys; sys.stdout.write('\t' + '\n\t'.join(ENCODER_FUNCTIONS.keys()) + '\n\n')
        raise NameError, "{0} not an accepted barcode encoder".format(args.barcode)


    recipe = DB.get(args.recipe)
    pagesize = getattr(reportlab.lib.pagesizes, recipe.pop('pagesize') if recipe.get('pagesize') is not None else 'A4')

    try:
        codes = eval(args.codes)
    except NameError:
        locals().update(recipe)
        codes = eval(args.codes)
    except:
        codes = [args.codes
                 for c in range(recipe.get('no_labels_y') *
                                recipe.get('no_labels_x'))]

    import pdb; pdb.set_trace

    # make the pdf
    pdf = BarcodeCanvas(args.filename,
                        pagesize = pagesize,
                        bottomup = 0,
                        pageCompression = 0,
                        # encoding=rl_config.defaultEncoding,
                        verbosity = 0,
                        encrypt = None
    )
     
    
    pdf.draw_labels(codes, encoder, **recipe)
    pdf.showPage()
    pdf.save()
    # # Testing
    # import pdb; pdb.set_trace() 
    # c = BarcodeCanvas('test'+args.filename
    #                   ,pagesize = pagesize
    # )
    # c.drawString(42, 42, "Hello World...")
    # c.showPage()
    # c.save()

if __name__ == '__main__':
    main()
