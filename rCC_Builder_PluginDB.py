from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class RCC_Builder_PluginDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'RCC Builder',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
            
        VFrame_1 = FXVerticalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXCheckButton(p=VFrame_1, text='Create New Model', tgt=form.modelKw, sel=0)
        HFrame_1 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=HFrame_1, ncols=16, labelText='Model Name:  ', tgt=form.ModelNKw, sel=0)
        AFXTextField(p=HFrame_1, ncols=12, labelText='Set Value:  ', tgt=form.SETKw, sel=0)
        ComboBox_2 = AFXComboBox(p=HFrame_1, ncols=0, nvis=1, text='Select Member Primary Axis (Assembly):', tgt=form.XYZKw, sel=0)
        ComboBox_2.setMaxVisible(10)
        ComboBox_2.appendItem(text='X-axis')
        ComboBox_2.appendItem(text='Y-axis')
        ComboBox_2.appendItem(text='Z-axis')
        l = FXLabel(p=VFrame_1, text='Note: Use a unique Set Value in the same model to avoid override', opts=JUSTIFY_LEFT)
        fileName = os.path.join(thisDir, 'figure_one.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_1, text='', ic=icon)
        if isinstance(self, FXHorizontalFrame):
            FXVerticalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=self, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        HFrame_4 = FXHorizontalFrame(p=self, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        GroupBox_1 = FXGroupBox(p=HFrame_4, text='Concrete', opts=FRAME_GROOVE)
        FXCheckButton(p=GroupBox_1, text='Create Concrete Part', tgt=form.concreteKw, sel=0)
        VFrame_3 = FXVerticalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_3, ncols=12, labelText='Width: ', tgt=form.con_wKw, sel=0)
        AFXTextField(p=VFrame_3, ncols=12, labelText='Height:', tgt=form.con_hKw, sel=0)
        AFXTextField(p=VFrame_3, ncols=12, labelText='Length:', tgt=form.con_lenKw, sel=0)
        AFXTextField(p=VFrame_3, ncols=10, labelText='Mesh Size:', tgt=form.meshSKw, sel=0)
        GroupBox_2 = FXGroupBox(p=HFrame_4, text='Stirrup', opts=FRAME_GROOVE)
        FXCheckButton(p=GroupBox_2, text='Create Stirrup part', tgt=form.stirrupKw, sel=0)
        VFrame_4 = FXVerticalFrame(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_4, ncols=11, labelText='Width:   ', tgt=form.s_llKw, sel=0)
        AFXTextField(p=VFrame_4, ncols=11, labelText='Height:  ', tgt=form.s_slKw, sel=0)
        AFXTextField(p=VFrame_4, ncols=11, labelText='Spacing:', tgt=form.s_spKw, sel=0)
        AFXTextField(p=VFrame_4, ncols=9, labelText='Mesh Size:', tgt=form.mesh_strpKw, sel=0)
        GroupBox_3 = FXGroupBox(p=HFrame_4, text='Longitudinal Rebar', opts=FRAME_GROOVE)
        HFrame_5 = FXHorizontalFrame(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_5 = FXVerticalFrame(p=HFrame_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        FXCheckButton(p=VFrame_5, text='Create Rebar Part', tgt=form.rebarKw, sel=0)
        AFXTextField(p=VFrame_5, ncols=11, labelText='Length:  ', tgt=form.lengthKw, sel=0)
        AFXTextField(p=VFrame_5, ncols=9, labelText='H. Spacing:', tgt=form.Long_distKw, sel=0)
        AFXTextField(p=VFrame_5, ncols=9, labelText='V. Spacing:', tgt=form.Short_distKw, sel=0)
        AFXTextField(p=VFrame_5, ncols=10, labelText='Mesh Size:', tgt=form.mesh_rebarKw, sel=0)
        if isinstance(HFrame_5, FXHorizontalFrame):
            FXVerticalSeparator(p=HFrame_5, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        else:
            FXHorizontalSeparator(p=HFrame_5, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=2, pb=2)
        GroupBox_6 = FXGroupBox(p=HFrame_5, text='No of Rebar:', opts=FRAME_GROOVE)
        AFXTextField(p=GroupBox_6, ncols=10, labelText='H. Direction:', tgt=form.Long_noKw, sel=0)
        AFXTextField(p=GroupBox_6, ncols=11, labelText='V. Direction', tgt=form.Short_noKw, sel=0)
        AFXTextField(p=GroupBox_6, ncols=7, labelText='Concrete Offset:', tgt=form.Con_ofstKw, sel=0)
        AFXTextField(p=GroupBox_6, ncols=10, labelText='Rebar Offset:', tgt=form.ofstKw, sel=0)
        VFrame_6 = FXVerticalFrame(p=HFrame_5, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        fileName = os.path.join(thisDir, 'figure_two.png')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=HFrame_5, text='', ic=icon)
