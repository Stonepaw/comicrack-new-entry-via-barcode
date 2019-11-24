"""
barcodeinputform.py

Author: Stonepaw
Last Modified 30/09/2010
"""

import clr
import System
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
import System.Drawing

import System.Windows.Forms
from System.Windows.Forms import MessageBox, MessageBoxButtons, DialogResult, MessageBoxIcon, Form

clr.AddReference("Google.GData.GoogleBase")
import Google.GData.GoogleBase
from Google.GData.GoogleBase import GBaseService, GBaseQuery, GBaseUriFactory

clr.AddReference("Google.GData.Client")
import Google.GData.Client
from Google.GData.Client import GDataRequestException

from ncvbutilities import FindBarcodeType, ParseIssueNames, FindPublisher

from serieschooserform import SeriesChooserForm

class BarcodeInputForm(Form):
    def __init__(self):
        self.InitializeComponent()
        self._issue = ""
        self._series = ""
        self._publisher = ""
    
    def InitializeComponent(self):
        self._label1 = System.Windows.Forms.Label()
        self._tbBarcode = System.Windows.Forms.TextBox()
        self._btnSearch = System.Windows.Forms.Button()
        self._btnCancel = System.Windows.Forms.Button()
        self._backgroundWorker = System.ComponentModel.BackgroundWorker()
        self._progressBar = System.Windows.Forms.ProgressBar()
        self.SuspendLayout()
        # 
        # label1
        # 
        self._label1.AutoSize = True
        self._label1.Location = System.Drawing.Point(12, 15)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(50, 13)
        self._label1.TabIndex = 6
        self._label1.Text = "Barcode:"
        # 
        # tbBarcode
        # 
        self._tbBarcode.Location = System.Drawing.Point(68, 12)
        self._tbBarcode.MaxLength = 18
        self._tbBarcode.Name = "tbBarcode"
        self._tbBarcode.Size = System.Drawing.Size(195, 20)
        self._tbBarcode.TabIndex = 0
        # 
        # btnSearch
        # 
        self._btnSearch.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnSearch.Location = System.Drawing.Point(111, 38)
        self._btnSearch.Name = "btnSearch"
        self._btnSearch.Size = System.Drawing.Size(73, 23)
        self._btnSearch.TabIndex = 2
        self._btnSearch.Text = "Search"
        self._btnSearch.UseVisualStyleBackColor = True
        self._btnSearch.Click += self.BtnSearchClick
        # 
        # btnCancel
        # 
        self._btnCancel.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._btnCancel.Location = System.Drawing.Point(190, 38)
        self._btnCancel.Name = "btnCancel"
        self._btnCancel.Size = System.Drawing.Size(73, 23)
        self._btnCancel.TabIndex = 3
        self._btnCancel.Text = "Cancel"
        self._btnCancel.UseVisualStyleBackColor = True
        self._btnCancel.Click += self.BtnCancelClick
        # 
        # progressBar
        # 
        self._progressBar.Location = System.Drawing.Point(12, 44)
        self._progressBar.MarqueeAnimationSpeed = 30
        self._progressBar.Name = "progressBar"
        self._progressBar.Size = System.Drawing.Size(80, 10)
        self._progressBar.Style = System.Windows.Forms.ProgressBarStyle.Marquee
        self._progressBar.TabIndex = 7
        self._progressBar.Visible = False
        # 
        # backgroundWorker
        # 
        self._backgroundWorker.DoWork += self.BackgroundWorkerDoWork
        self._backgroundWorker.RunWorkerCompleted += self.BackgroundWorkerCompleted
        # 
        # BarcodeInputForm
        # 
        self.AcceptButton = self._btnSearch
        self.CancelButton = self._btnCancel
        self.ClientSize = System.Drawing.Size(275, 67)
        self.Controls.Add(self._progressBar)
        self.Controls.Add(self._btnCancel)
        self.Controls.Add(self._btnSearch)
        self.Controls.Add(self._tbBarcode)
        self.Controls.Add(self._label1)
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
        self.Location = System.Drawing.Point(0, 2)
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.Name = "BarcodeInputForm"
        self.ShowIcon = False
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = "Scan barcode"
        self.FormClosing += self.BarcodeInputFormFormClosing
        self.ResumeLayout(False)
        self.PerformLayout()

    def BtnSearchClick(self, sender, e):
        if not self._backgroundWorker.IsBusy:
            barcode = self._tbBarcode.Text
            if barcode:
                #first checks if the barcode contains  letters:
                try:
                    int(barcode)
                except ValueError:
                    MessageBox.Show("The value entered can only contain numbers. Please enter a valid barcode", "Barcode not valid")
                    self._tbBarcode.Text = ""
                    return
                #Several cases here depending on if the barcode is upc or ean and what supplmentals are added
                if len(barcode) not in [12, 13, 14, 15, 17, 18]:
                    MessageBox.Show("The barcode entered was not a vaild UPC/EAN. Please try again", "Barcode not valid")
                    return
                else: 
                    barcode, self._issue, type = FindBarcodeType(barcode)
                    if barcode:    
                        self._publisher = FindPublisher(barcode)
                        self._backgroundWorker.RunWorkerAsync(dict({"Barcode" : barcode, "Type" : type}))
                        self._progressBar.Visible = True
                    else:
                        self.DialogResult = DialogResult.Cancel
            else:
                MessageBox.Show("Please enter a barcode", "No Barcode entered")
            
    def BackgroundWorkerDoWork(self, sender, e):
        #This authentication key is registered to itsallaboutbooks@gmail.com. If you modify this code please get your own!
        service = GBaseService("ComicRackScript-ComicBookUPCLookup-0.1", "ABQIAAAAzulI5GIkvOKDpM9Tqwtm8BT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQsqv51rrx1UhUH_ExWXJ0ZIR-1cg")
        query = GBaseQuery(GBaseUriFactory.Default.SnippetsFeedUri)
        query.GoogleBaseQuery = "[" + e.Argument["Type"] + "(text): \"" + e.Argument["Barcode"] + "\"]"
        results = service.Query(query)
        names = []
        for entry in results.Entries:
            names.append(entry.Title.Text)
        
        fixednames = ParseIssueNames(names)
        
        e.Result = fixednames

    def BackgroundWorkerCompleted(self, sender, e):
        self._progressBar.Visible = False
        
       #Catch any errors.
        if e.Error:
            MessageBox.Show("An error occured when trying to find the series. The error was:\n\n" + e.Error.InnerException.Message + "\n" + e.Error.Message, "Error occured", MessageBoxButtons.OK, MessageBoxIcon.Error)
            self.DialogResult = DialogResult.Abort
        else:
            series = e.Result
            #series should be list
            #If more than one series:
            if len(series) > 1:
                chooser = SeriesChooserForm(series)
                result = chooser.ShowDialog()
                if result == DialogResult.OK:
                    self._series = chooser._lbSeries.SelectedItem
                    self.DialogResult = DialogResult.OK
                else:
                    self.DialogResult = DialogResult.Cancel
            elif len(series) == 1:
                self._series = series[0]
                self.DialogResult = DialogResult.OK
            else:
                MessageBox.Show("No comics found with this barcode", "No results")
                self.DialogResult = DialogResult.Cancel


    def BtnCancelClick(self, sender, e):
        if self._backgroundWorker.IsBusy:
            self.DialogResult = DialogResult.None

    def BarcodeInputFormFormClosing(self, sender, e):
        if self._backgroundWorker.IsBusy:
            e.Cancel = True
            
    def GetSeries(self):
        return self._series

    def GetIssue(self):
        return self._issue
   
    def GetPublisher(self):
       return self._publisher
