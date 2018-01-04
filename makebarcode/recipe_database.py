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
