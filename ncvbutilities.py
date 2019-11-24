"""
ncvbutilities.py
Author: Stonepaw

Last Modified 30/09/2010

Description: Contains common funtions


"""
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox, MessageBoxButtons, MessageBoxIcon, DialogResult

publishers = {"0761941":"DC Comics", "761941":"DC Comics", "0759606":"Marvel Comics", "759606":"Marvel Comics", "0761568":"Dark Horse", "761568":"Dark Horse", "844284":"Boom! Studios", "0844284":"Boom! Studios"}

#_______________Other Functions_________________#
def ParseIssueNumber(issueCode):
    """Notes: Issue code comes in a five digit number.
    The first three numbers are the issue number padded in zeroes
    The fouth number is for varient covers starting at 1
    The fith number seems to always be 1
    """
    if len(issueCode) == 5:
        issueNumber = issueCode[:3].lstrip("0")
        return issueNumber
    else:
        return None
    
def ParseIssueNames(names):
    """Because comics use the same upc for the whole series now parse out the series name from
    the returned list
    
    Noteable items that come after the series name: "issue #" and "#"
    
    There is probably a better way to do this but it seems to work in most cases.
    
    names: a list of series titles
    """
    fixednames = []
    
    for name in names:
        if name.Contains("issue"):
            n = name.split("issue")[0].strip()
            if not n in fixednames:
                fixednames.append(n)
                
        elif name.Contains("#"):
            n = name.split("#")[0].strip()
            if not n in fixednames:
                fixednames.append(n)
                
        else:
            fixednames.append(name)
    return fixednames

def FindBarcodeType(barcode):
    issueNumber = ""
    type = ""
    barcodeLength = len(barcode)
    #UPC-A            
    if barcodeLength == 12:
        result = MessageBox.Show("No issue code was entered. The script can try and look for the series but no issue number will be entered.\n\nContinue?", "No Issue code", MessageBoxButtons.YesNo, MessageBoxIcon.Question)
        if result == DialogResult.Yes:
            type = "upc"
        else:
            return None, None, None
    #EAN
    elif barcodeLength == 13:
        result = MessageBox.Show("No issue code was entered. The script can try and look for the series but no issue number will be entered.\n\nContinue?", "No Issue code", MessageBoxButtons.YesNo, MessageBoxIcon.Question)
        if result == DialogResult.Yes:
            type = "ean"                    
        else:
            return None, None, None
        
    #UPC-A + UPC-5
    elif barcodeLength == 17:
        issueNumber = ParseIssueNumber(barcode[12:17])
        barcode = barcode[0:12]
        type = "upc"
    
    #EAN-13 + UPC-5
    elif barcodeLength == 18:
        issueNumber = ParseIssueNumber(barcode[13:18])
        barcode = barcode[0:13]
        type = "ean"
        
    #UPC-A + UPC-2
    elif barcodeLength == 14:
        issueNumber = barcode[12:14]
        barcode = barcode[0:12]
        type = "upc"
        
    #EAN-13 + UPC-2
    elif barcodeLength == 15:
        issueNumber = barcode[13:15]
        barcode = barcode[0:13]
        type = "ean"
    return barcode, issueNumber, type

def FindPublisher(barcode):
    #only company prefix
    barcode = barcode[:-6]    
    if barcode in publishers:
        #print "Found publisher"
        return publishers[barcode]
    else:
        #print "Didn't find publisher"
        return ""
