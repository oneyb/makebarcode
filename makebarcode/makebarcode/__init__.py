
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
                                               **dict(value=code,
                                                      height=y - height,
                                                      width=x))
        # import pdb; pdb.set_trace() 
        encoded.drawOn(self, 0, 0 + height)

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
