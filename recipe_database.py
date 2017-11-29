from reportlab.lib.units import mm
from reportlab.graphics import barcode

DATABASE = {
    # Herma 4474
    'herma_4474':        { 
        'label_width':   48.5 * mm
        ,'label_height': 25.4 * mm
        ,'x_offset':     8.0  * mm 
        ,'y_offset':     21.5 * mm 
        ,'x_gap':        0    * mm
        ,'y_gap':        0    * mm
        ,'no_labels_x':  4
        ,'no_labels_y':  10
        ,'pagesize':     'A4'
    }
    # Avery 3475
    ,'avery_3475' :      {
        'label_width':   70.  * mm
        ,'label_height': 36.  * mm
        ,'x_offset':     1.0  * mm 
        ,'y_offset':     6.0  * mm 
        ,'x_gap':        0    * mm
        ,'y_gap':        0    * mm
        ,'no_labels_x':  3
        ,'no_labels_y':  8
        ,'pagesize':     'A4'
    }
    # Avery L7120
    ,'avery_L7120':      { 
        'label_width':   35.0 * mm
        ,'label_height': 35.0 * mm
        ,'x_offset':     7.0  * mm 
        ,'y_offset':     13.  * mm 
        ,'x_gap':        5.0  * mm
        ,'y_gap':        4.9  * mm
        ,'no_labels_x':  5
        ,'no_labels_y':  7
        ,'pagesize':     'A4'
    }
}

ENCODER_FUNCTIONS = {
    'Codabar'          : barcode.common.Codabar,
    'Code11'           : barcode.common.Code11,
    'Code128'          : barcode.code128.Code128,
    'Code128Auto'      : barcode.code128.Code128Auto,
    'EAN13'            : barcode.eanbc.Ean13BarcodeWidget,
    'EAN5'             : barcode.eanbc.Ean5BarcodeWidget,
    'EAN8'             : barcode.eanbc.Ean8BarcodeWidget,
    'ECC200DataMatrix' : barcode.ecc200datamatrix.ECC200DataMatrix,
    'I2of5'            : barcode.common.I2of5,
    'ISBN'             : barcode.eanbc.ISBNBarcodeWidget,
    'MSI'              : barcode.common.MSI,
    'FIM'              : barcode.usps.FIM,
    'POSTNET'          : barcode.usps.POSTNET,
    'QR'               : barcode.qr.QrCode,
    'Standard39'       : barcode.code39.Standard39,
    'Extended39'       : barcode.code39.Extended39,
    'Extended93'       : barcode.code93.Extended93,
    'Standard93'       : barcode.code93.Standard93,
    'UPCA'             : barcode.eanbc.UPCA,
    'USPS_4State'      : barcode.usps4s.USPS_4State
}
