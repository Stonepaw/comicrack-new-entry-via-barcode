"""
serieschooserform.py
Author: Stonepaw
Last modified 30/09/2010
"""

import clr
import System
from System import Array
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
import System.Drawing
import System.Windows.Forms

from System.Windows.Forms import Form

class SeriesChooserForm(Form):
	def __init__(self, seriesnames):
		self.InitializeComponent()
		self._lbSeries.Items.AddRange(Array[str](seriesnames))
		self._lbSeries.SelectedIndex = 0
	
	def InitializeComponent(self):
		self._lbSeries = System.Windows.Forms.ListBox()
		self._label1 = System.Windows.Forms.Label()
		self._btnAccept = System.Windows.Forms.Button()
		self._btnCancel = System.Windows.Forms.Button()
		self._label2 = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# lbSeries
		# 
		self._lbSeries.FormattingEnabled = True
		self._lbSeries.HorizontalScrollbar = True
		self._lbSeries.Location = System.Drawing.Point(2, 55)
		self._lbSeries.Name = "lbSeries"
		self._lbSeries.Size = System.Drawing.Size(220, 121)
		self._lbSeries.TabIndex = 0
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(2, 9)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(220, 16)
		self._label1.TabIndex = 3
		self._label1.Text = "Multiple series were found. "
		# 
		# btnAccept
		# 
		self._btnAccept.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._btnAccept.DialogResult = System.Windows.Forms.DialogResult.OK
		self._btnAccept.Location = System.Drawing.Point(25, 182)
		self._btnAccept.Name = "btnAccept"
		self._btnAccept.Size = System.Drawing.Size(75, 23)
		self._btnAccept.TabIndex = 1
		self._btnAccept.Text = "Accept"
		self._btnAccept.UseVisualStyleBackColor = True
		# 
		# btnCancel
		# 
		self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self._btnCancel.Location = System.Drawing.Point(124, 182)
		self._btnCancel.Name = "btnCancel"
		self._btnCancel.Size = System.Drawing.Size(75, 23)
		self._btnCancel.TabIndex = 2
		self._btnCancel.Text = "Cancel"
		self._btnCancel.UseVisualStyleBackColor = True
		# 
		# label2
		# 
		self._label2.Location = System.Drawing.Point(2, 29)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(125, 23)
		self._label2.TabIndex = 4
		self._label2.Text = "Select wanted series:"
		# 
		# multipleResultsForm
		# 
		self.AcceptButton = self._btnAccept
		self.CancelButton = self._btnCancel
		self.ClientSize = System.Drawing.Size(225, 211)
		self.Controls.Add(self._label2)
		self.Controls.Add(self._btnCancel)
		self.Controls.Add(self._btnAccept)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._lbSeries)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "multipleResultsForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "Select Series"
		self.ResumeLayout(False)
