# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def RCC_Modeller(model, ModelN,  SET, XYZ, concrete, con_w, con_h, con_len, meshS, stirrup, s_ll, s_sl, s_sp, mesh_strp, 
                     rebar, length, Short_dist, Long_dist, mesh_rebar, Short_no, Long_no, Con_ofst, ofst):
    # Imprort necessary modules
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    # Create Main Model if not exists
    if model==True:
        mdb.Model(name=ModelN, modelType=STANDARD_EXPLICIT)
        a = mdb.models[ModelN].rootAssembly
    else:
        a = mdb.models[ModelN].rootAssembly
    
    # Create Longitudinal Rebar
    if rebar==True:
        s = mdb.models[ModelN].ConstrainedSketch(name='__profile__', sheetSize=length)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.Line(point1=(0.0, -length/2), point2=(0.0, length/2))
        s.VerticalConstraint(entity=g[2], addUndoState=False)
        p = mdb.models[ModelN].Part(name='rebar-'+SET, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = mdb.models[ModelN].parts['rebar-'+SET]
        p.BaseWire(sketch=s)
        s.unsetPrimaryObject()
        p = mdb.models[ModelN].parts['rebar-'+SET]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models[ModelN].sketches['__profile__']
        a = mdb.models[ModelN].rootAssembly
        # Generate Mesh for Rebar
        p = mdb.models[ModelN].parts['rebar-'+SET]
        p.seedPart(size=mesh_rebar, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models[ModelN].parts['rebar-'+SET]
        p.generateMesh()
    # Create Stirrup
    if stirrup==True:
        s = mdb.models[ModelN].ConstrainedSketch(name='__profile__', sheetSize=s_ll)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(-s_sl/2, -s_ll/2), point2=(s_sl/2, s_ll/2))
        p = mdb.models[ModelN].Part(name='stirrup-'+SET, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = mdb.models[ModelN].parts['stirrup-'+SET]
        p.BaseWire(sketch=s)
        s.unsetPrimaryObject()
        p = mdb.models[ModelN].parts['stirrup-'+SET]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models[ModelN].sketches['__profile__']
        # Generate Mesh for Stirrup
        p = mdb.models[ModelN].parts['stirrup-'+SET]
        p.seedPart(size=mesh_strp, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models[ModelN].parts['stirrup-'+SET]
        p.generateMesh()
    # Create assembly instances and sets
    if rebar==True:
        a1 = mdb.models[ModelN].rootAssembly
        a1.DatumCsysByDefault(CARTESIAN)
        p = mdb.models[ModelN].parts['rebar-'+SET]
        a1.Instance(name='rebar-'+SET+'-1', part=p, dependent=ON)
        a1 = mdb.models[ModelN].rootAssembly
        a = mdb.models[ModelN].rootAssembly
        # Create Set for Core & Dummy Rebar
        a = mdb.models[ModelN].rootAssembly
        a1 = mdb.models[ModelN].rootAssembly
        rebar_list=('rebar-'+SET+'-1', )
        a1.translate(instanceList=rebar_list, vector=(-0.5*(Short_no-1)*Short_dist, 0.0, -0.5*(Long_no-1)*Long_dist))
        a.LinearInstancePattern(instanceList=rebar_list, 
                                direction1=(1.0, 0.0, 0.0), direction2=(0.0, 0.0, 1.0), 
                                number1=Short_no, number2=Long_no, 
                                spacing1=Short_dist, spacing2=Long_dist)
        # Remove Mid Rebar
        for i in range (2, Short_no):
            for j in range (2, Long_no):
                a2 = mdb.models[ModelN].rootAssembly
                a2.deleteFeatures(('rebar-'+SET+'-1-lin-'+str(i)+'-'+str(j), ))
    # Add Stirrup in Assembly
    if stirrup==True:
        a = mdb.models[ModelN].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models[ModelN].parts['stirrup-'+SET]
        a.Instance(name='stirrup-'+SET+'-1', part=p, dependent=ON)
        #session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
        a = mdb.models[ModelN].rootAssembly
        a.rotate(instanceList=('stirrup-'+SET+'-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(10.0, 0.0, 0.0), angle=90.0)
        a = mdb.models[ModelN].rootAssembly
        s_no=int(con_len/(s_sp))+1
        a.translate(instanceList=('stirrup-'+SET+'-1', ), vector=(0.0, Con_ofst-con_len*0.5+0.5*(con_len-s_sp*(s_no-1)), 0.0))
        a1 = mdb.models[ModelN].rootAssembly
        a1.LinearInstancePattern(instanceList=('stirrup-'+SET+'-1', ), direction1=(0.0, 1.0, 0.0), direction2=(1.0, 0.0, 0.0), 
                                number1=s_no, number2=1, spacing1=s_sp, spacing2=2.0)
    # Create Concrete Part
    if concrete==True:
        s1 = mdb.models[ModelN].ConstrainedSketch(name='__profile__', sheetSize=con_len)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.rectangle(point1=(-con_h/2, -con_len/2), point2=(con_h/2, con_len/2))
        p = mdb.models[ModelN].Part(name='concrete-'+SET, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = mdb.models[ModelN].parts['concrete-'+SET]
        p.BaseSolidExtrude(sketch=s1, depth=con_w)
        s1.unsetPrimaryObject()
        p = mdb.models[ModelN].parts['concrete-'+SET]
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models[ModelN].sketches['__profile__']
        a1 = mdb.models[ModelN].rootAssembly
        p = mdb.models[ModelN].parts['concrete-'+SET]
        a1.Instance(name='concrete-'+SET+'-1', part=p, dependent=ON)
        a1 = mdb.models[ModelN].rootAssembly
        a1.translate(instanceList=('concrete-'+SET+'-1', ), vector=(0.0, 0.0, -con_w/2))
        a = mdb.models[ModelN].rootAssembly
        a.translate(instanceList=('concrete-'+SET+'-1', ), vector=(0.0, Con_ofst, 0.0))
        # Generate Mesh for Concrete
        p = mdb.models[ModelN].parts['concrete-'+SET]
        p.seedPart(size=meshS, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models[ModelN].parts['concrete-'+SET]
        p.generateMesh()
    # Create Sets for Wire Creation
    #del a.features['rebar-1-lin-2-2']
    all_object=[]
    if rebar==True:
        all_object.append('rebar-'+SET+'-1')
        for x in [1, Short_no]:
            for y in range(2, Long_no+1):
                all_object.append('rebar-'+SET+'-1-lin-'+str(x)+'-'+str(y))
        for x in [1, Long_no]:
            for y in range(2, Short_no+1):
                all_object.append('rebar-'+SET+'-1-lin-'+str(y)+'-'+str(x))
        all_object.append('rebar-'+SET+'-1-lin-'+str(Short_no)+'-1')
    if stirrup==True:
        all_object.append('stirrup-'+SET+'-1')
        for i in range(2, s_no+1):
            all_object.append('stirrup-'+SET+'-1-lin-'+str(i)+'-1')
    if concrete==True:
        all_object.append('concrete-'+SET+'-1')
    a = mdb.models[ModelN].rootAssembly
    # Apply Offset if required
    if ofst!=0.0 and rebar==True:
        ofst_list=[]
        ofst_list.append('rebar-'+SET+'-1')
        for x in [1, Short_no]:
            for y in range(2, Long_no+1):
                ofst_list.append('rebar-'+SET+'-1-lin-'+str(x)+'-'+str(y))
        for x in [1, Long_no]:
            for y in range(2, Short_no+1):
                ofst_list.append('rebar-'+SET+'-1-lin-'+str(y)+'-'+str(x))
        a1 = mdb.models[ModelN].rootAssembly
        a1.translate(instanceList=ofst_list, vector=(-ofst, 0.0, 0.0))
    # Rotate Model if required
    if XYZ=='X-axis':
        a.rotate(instanceList=all_object, axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=-90.0)
    elif XYZ=='Z-axis':
        a.rotate(instanceList=all_object, axisPoint=(0.0, 0.0, 0.0), axisDirection=(10.0, 0.0, 0.0), angle=90.0)
        a.rotate(instanceList=all_object, axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=-90.0)