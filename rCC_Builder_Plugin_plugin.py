from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class RCC_Builder_Plugin_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='RCC_Modeller',
            objectName='RCC_Builder', registerQuery=False)
        pickedDefault = ''
        self.modelKw = AFXBoolKeyword(self.cmd, 'model', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.ModelNKw = AFXStringKeyword(self.cmd, 'ModelN', True, 'Demo-1')
        self.SETKw = AFXStringKeyword(self.cmd, 'SET', True, '1')
        self.XYZKw = AFXStringKeyword(self.cmd, 'XYZ', True, 'Z-axis')
        self.concreteKw = AFXBoolKeyword(self.cmd, 'concrete', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.con_wKw = AFXFloatKeyword(self.cmd, 'con_w', True, 25)
        self.con_hKw = AFXFloatKeyword(self.cmd, 'con_h', True, 45)
        self.con_lenKw = AFXFloatKeyword(self.cmd, 'con_len', True, 400)
        self.meshSKw = AFXFloatKeyword(self.cmd, 'meshS', True, 10)
        self.stirrupKw = AFXBoolKeyword(self.cmd, 'stirrup', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.s_llKw = AFXFloatKeyword(self.cmd, 's_ll', True, 20)
        self.s_slKw = AFXFloatKeyword(self.cmd, 's_sl', True, 40)
        self.s_spKw = AFXFloatKeyword(self.cmd, 's_sp', True, 30)
        self.mesh_strpKw = AFXFloatKeyword(self.cmd, 'mesh_strp', True, 5)
        self.rebarKw = AFXBoolKeyword(self.cmd, 'rebar', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.lengthKw = AFXFloatKeyword(self.cmd, 'length', True, 430)
        self.Long_distKw = AFXFloatKeyword(self.cmd, 'Long_dist', True, 10)
        self.Short_distKw = AFXFloatKeyword(self.cmd, 'Short_dist', True, 20)
        self.mesh_rebarKw = AFXFloatKeyword(self.cmd, 'mesh_rebar', True, 10)
        self.Long_noKw = AFXFloatKeyword(self.cmd, 'Long_no', True, 3)
        self.Short_noKw = AFXFloatKeyword(self.cmd, 'Short_no', True, 3)
        self.Con_ofstKw = AFXFloatKeyword(self.cmd, 'Con_ofst', True, -20)
        self.ofstKw = AFXFloatKeyword(self.cmd, 'ofst', True, 0)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import rCC_Builder_PluginDB
        return rCC_Builder_PluginDB.RCC_Builder_PluginDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='RCC Builder...', 
    object=RCC_Builder_Plugin_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import RCC_Builder',
    applicableModules=ALL,
    version='1.0.0',
    author='Musfick Alam',
    description='Abaqus Plugin to Model RCC Elements',
    helpUrl='N/A'
)
