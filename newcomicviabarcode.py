"""
barcodescanner.py
Author: Stonepaw
Modified: 30/09/2010
"""
import clr

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import DialogResult
from barcodeinputform import BarcodeInputForm

#@Name New Comic Entry via barcode
#@Hook NewBooks
#@Description Adds a new fileless comic entry via a scanned barcode
#@Image barcode.png

def barcodescanner(books):
    try:
        form = BarcodeInputForm()
        if form.ShowDialog() == DialogResult.OK:
            book = ComicRack.App.AddNewBook(False)
            book.Number = form.GetIssue()
            book.Series = form.GetSeries()
            book.Publisher = form.GetPublisher()
            
            ComicRack.Browser.SelectComics([book])
    finally:
        form.Dispose()
