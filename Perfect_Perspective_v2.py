import bpy
import blf
from bpy import context
from bpy.props import PointerProperty, EnumProperty
from math import cos, sin, radians, sqrt
from mathutils import Vector
from bpy_extras import view3d_utils


#https://pomax.github.io/three-point-perspective/#using-rational-mapping-instead

###### GENERICINTRO ######
bl_info = {
    'name': 'Perfect Perspective for Grease Pencil',
    'category': 'All',
    'author': 'Nerses Chorekchyan',
    'version': (1, 1, 0),
    'blender': (3, 1, 0),
    'location': '',
    'description': 'A Perfect Perspective Toolset for Grease Pencil'
}

#Global Vars
OnePP_name = "One Point Perspective"
TwoPP_name = "Two Point Perspective"
ThreePP_name = "Three Point Perspective"
Assist_name = "Assist Tool"
Perspective_Collection = "Perspective Tools"
Archive_Collection = "Archive"


#PANEL FOR UI###############
class PP_PT_main(bpy.types.Panel):
    bl_idname = "PP_PT_main"
    bl_label = "Perspective Tools Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Perfect Perspective"

    def draw(self, context):        
        #Staging
        scene = context.scene
        layout = self.layout
        PPSettings = scene.PPSettings
        NewOperator = layout.operator
        
        #Perspective Type
        rowPerspectiveDesc = layout.row()
        rowPerspectiveDesc.label(text="Perspective Type")
        rowPerspectiveType = layout.row()
        rowPerspectiveType.prop(PPSettings, "PerspectiveTypeEnum", text="Type", expand=True)

        rowShared = layout.row()
        rowShared.label(text="Line Settings:")
        rowLine = layout.row()
        rowLine.prop(PPSettings, "lineWidth", text="Width")
        rowLine.prop(PPSettings, "lineStrength", text="Strength")
        
        #Color Pickers
        rowPerspectiveColor = layout.row()        
        rowPerspectiveColor.prop(PPSettings, "lineColor", text="Line Color")
        rowAssistColor = layout.row()        
        rowAssistColor.prop(PPSettings, "assistColor", text="Assist Color")

        
        if PPSettings.PerspectiveTypeEnum == 'OnePP_Option':
            

            #One Point Perspective Settings
            rowOne = layout.row()
            rowLineCountRadius = layout.row()
            rowLineCountRadius.prop(PPSettings, "lineCount", text="Line Count")
            rowLineCountRadius.prop(PPSettings, "radius", text="Radius")
            row_vp1pos = layout.row()        
            row_vp1pos.prop(PPSettings, "vpONEpos", text="VP1 Pos")
        
        elif PPSettings.PerspectiveTypeEnum == 'TwoPP_Option':
            rowOptions = layout.row()
            rowOptions.prop(PPSettings, "ceiling", text="Draw Ceiling")
            rowOptions.prop(PPSettings, "verts", text="Draw Verticals")
            row_steps = layout.row()
            row_steps.prop(PPSettings, "Steps", text="Steps")
            row_pFact = layout.row()
            row_pFact.prop(PPSettings, "pFact", text="Perspective Factor")
            row_opos = layout.row()        
            row_opos.prop(PPSettings, "opos", text="Obs Pos")
            row_vp1pos = layout.row()        
            row_vp1pos.prop(PPSettings, "vp1pos", text="VP1 Pos")
            row_vp2pos = layout.row()        
            row_vp2pos.prop(PPSettings, "vp2pos", text="VP2 Pos")
            
        elif PPSettings.PerspectiveTypeEnum == 'ThreePP_Option':
            rowOptions = layout.row()
            rowOptions.prop(PPSettings, "verts", text="Draw Verticals")
            row_steps = layout.row()
            row_steps.prop(PPSettings, "Steps", text="Steps")
            row_pFact = layout.row()
            row_pFact.prop(PPSettings, "pFact", text="Perspective Factor")
            row_pFactY = layout.row()
            row_pFactY.prop(PPSettings, "pFactY", text="Perspective Factor Y")
            row_opos = layout.row()        
            row_opos.prop(PPSettings, "opos", text="Obs Pos")
            row_vp1pos = layout.row()        
            row_vp1pos.prop(PPSettings, "vp1pos", text="VP1 Pos")
            row_vp2pos = layout.row()        
            row_vp2pos.prop(PPSettings, "vp2pos", text="VP2 Pos")
            row_vp3pos = layout.row()        
            row_vp3pos.prop(PPSettings, "vp3pos", text="VP3 Pos")
            



        

        

        
        #Two and Three Point Perspective Settings
#        rowDivider2 = layout.row()
#        rowDivider2.label(text="Two & Three Point Settings:")
                
#        rowOptions = layout.row()
#        rowOptions.prop(PPSettings, "verts", text="Draw Verticals")
#        row_steps = layout.row()
#        row_steps.prop(PPSettings, "Steps", text="Steps")
#        row_pFact = layout.row()
#        row_pFact.prop(PPSettings, "pFact", text="Perspective Factor")
        
        #Two and Three Point Perspective Settings
#        rowDivider3 = layout.row()
#        rowDivider3.label(text="Three Point Settings:")
        
#        row_pFactY = layout.row()
#        row_pFactY.prop(PPSettings, "pFactY", text="Perspective Factor Y")
        
#        rowDivider3 = layout.row()
        
        NewOperator("pp.generator", icon='MESH_CUBE', text = "(re)Generate Perspective")
        NewOperator("pp.clear", icon='MESH_CUBE', text="Clear All")
        NewOperator("pp.archive", icon='MESH_CUBE', text="Archive Grid")
        rowEsc = layout.row()
        rowEsc.label(text="ESC to Cancel Assist")        
        NewOperator("pp.assist", icon='MESH_CUBE', text="Perspective Assists")

        
#        row_opos = layout.row()        
#        row_opos.prop(PPSettings, "opos", text="Obs Pos")
#        row_vp1pos = layout.row()        
#        row_vp1pos.prop(PPSettings, "vp1pos", text="VP1 Pos")
#        row_vp2pos = layout.row()        
#        row_vp2pos.prop(PPSettings, "vp2pos", text="VP2 Pos")
#        row_vp3pos = layout.row()        
#        row_vp3pos.prop(PPSettings, "vp3pos", text="VP3 Pos")


class PP_OT_properties(bpy.types.PropertyGroup):

    PerspectiveTypeEnum : bpy.props.EnumProperty(
        name = "",
        description = "Select an Option",
        items = [
            ('OnePP_Option' , "One", "Set mode for One Point Perspective"),
            ('TwoPP_Option' , "Two", "Set mode for Two Point Perspective"),
            ('ThreePP_Option' , "Three", "Set mode for Three Point Perspective"),
        ],
        default = 'TwoPP_Option'
    )
    
    Steps : bpy.props.IntProperty(
        name = "Steps",
        description = "How many steps from Obvserver to VPs",
        default = 20,
        min = 1,
        max = 100
        )  
    pFact : bpy.props.FloatProperty(
        name = "pFact",
        description = "Perspective Factor",
        default = .25,
        soft_min = 0.01,
        soft_max = 1
        )  
    pFactY : bpy.props.FloatProperty(
        name = "pFactY",
        description = "Perspective Factor Y",
        default = .25,
        soft_min = 0.01,
        soft_max = 1
        )  
    lineWidth : bpy.props.IntProperty(
        name = "lineWidth",
        description = "",
        default = 10,
        min = 1,
        soft_max = 50
        ) 
    lineCount : bpy.props.IntProperty(
        name = "lineCount",
        description = "",
        default = 20,
        min = 1,
        soft_max = 100
        )  
    lineStrength : bpy.props.FloatProperty(
        name = "lineStrength",
        description = "",
        default = 1,
        min = 0,
        max = 1
        )  
    radius : bpy.props.FloatProperty(
        name = "radius",
        description = "",
        default = 3,
        min = 0,
        soft_max = 100
        )  
    opos : bpy.props.FloatVectorProperty(
        name = "opos",
        description = "Observer Position",
        subtype = "COORDINATES",
        default = (0,-5),
        soft_min = -10,
        soft_max = 10,
        size = 2
        )
    vp1pos : bpy.props.FloatVectorProperty(
        name = "vp1pos",
        description = "VP1 Position",
        subtype = "COORDINATES",
        default = (-5,0),
        soft_min = -10,
        soft_max = 10,
        size = 2
        )
    vpONEpos : bpy.props.FloatVectorProperty(
        name = "vpONEpos",
        description = "VP1 Position",
        subtype = "COORDINATES",
        default = (0,0),
        soft_min = -10,
        soft_max = 10,
        size = 2
        )
    vp2pos : bpy.props.FloatVectorProperty(
        name = "vp2pos",
        description = "VP2 Position",
        subtype = "COORDINATES",
        default = (5,0),
        soft_min = -10,
        soft_max = 10,
        size = 2
        )  
    vp3pos : bpy.props.FloatVectorProperty(
        name = "vp3pos",
        description = "VP3 Position",
        subtype = "COORDINATES",
        default = (0,5),
        soft_min = -10,
        soft_max = 10,
        size = 2
        )
    lineColor : bpy.props.FloatVectorProperty(
        name = "Perspective Color Picker",
        subtype = "COLOR",
        default = (0,0,0,0.5),
        min = 0,
        max = 1,
        size = 4
        )    
    assistColor : bpy.props.FloatVectorProperty(
        name = "Assist Color Picker",
        subtype = "COLOR",
        default = (0,0,1,1),
        min = 0,
        max = 1,
        size = 4
        )
    verts : bpy.props.BoolProperty(
        name = "verts",
        description = "Draw Vertical Lines",
        default = False
        )
    ceiling : bpy.props.BoolProperty(
        name = "Ceiling",
        description = "Draw Ceiling Lines",
        default = True
        )


class PP_OT_vpstore(bpy.types.PropertyGroup):
    vp0pos: bpy.props.FloatVectorProperty(size = 2)
    vp1pos: bpy.props.FloatVectorProperty(size = 2)
    vp2pos: bpy.props.FloatVectorProperty(size = 2)
    vp3pos: bpy.props.FloatVectorProperty(size = 2)
    pFact: bpy.props.FloatProperty()
    pFactY: bpy.props.FloatProperty()
    temp: bpy.props.BoolProperty()


class PP_OT_generator(bpy.types.Operator):
    bl_idname = "pp.generator"
    bl_label = "Perfect Perspective Generator"
    bl_options = {'UNDO'}
    def execute(self,context):

        ###########Repalce Me########
        PerspectiveType = bpy.context.scene.PPSettings.PerspectiveTypeEnum
        ceiling = bpy.context.scene.PPSettings.ceiling
        steps = bpy.context.scene.PPSettings.Steps
        pFact = bpy.context.scene.PPSettings.pFact
        pFactY = bpy.context.scene.PPSettings.pFactY
        lineWidth = bpy.context.scene.PPSettings.lineWidth
        lineStrength = bpy.context.scene.PPSettings.lineStrength
        verts = bpy.context.scene.PPSettings.verts
        lineColor = bpy.context.scene.PPSettings.lineColor
        lineCount = bpy.context.scene.PPSettings.lineCount
        assistColor = bpy.context.scene.PPSettings.assistColor
        vp0pos = bpy.context.scene.PPSettings.opos
        vpONEpos = bpy.context.scene.PPSettings.vpONEpos
        vp1pos = bpy.context.scene.PPSettings.vp1pos
        vp2pos = bpy.context.scene.PPSettings.vp2pos
        vp3pos = bpy.context.scene.PPSettings.vp3pos
        radius = bpy.context.scene.PPSettings.radius
        ###########Repalce Me########

        def distanceToRatio(s):
          return 1.0 - 1.0 / (1.0 + pFact * s)

        def distanceToRatioY(s):
          return 1.0 - 1.0 / (1.0 + pFactY * s)

        def get(x, y, z):
            HC = lli_input(vp0pos, vp0pos + Vector((0,10)), vp2pos, vp1pos)
            dyC = vp0pos.y - HC.y
            yScale = 5.0
            yFactor = dyC / yScale
            
            if (x==0 and y==0 and z==0):
                return vp0pos

            px = vp0pos.lerp(vp1pos, distanceToRatio(x))
            pz = vp0pos.lerp(vp2pos, distanceToRatio(z))
            ground = lli_input(vp1pos, pz, vp2pos, px)
            
            if (y==0):
                return ground
          
            inZ = (ground.x < vp0pos.x)

            if inZ:
                rx = (ground.x - vp2pos.x) / (vp0pos.x - vp2pos.x)
            else: 
                rx = (vp1pos.x - ground.x) / (vp1pos.x - vp0pos.x)
                
            if inZ:
                onAxis = lli_input(vp2pos, vp0pos, ground, ground + Vector((0, 10)))
            else: 
                onAxis =lli_input(vp1pos, vp0pos, ground, ground + Vector((0, 10)))
                
            ry = (ground.y - HC.y) / (onAxis.y - HC.y)
            return ground - Vector((0, rx * ry * y * yFactor))

        def get3(x, y, z):
            
            vp0pos = bpy.context.scene.PPSettings.opos

            if (x==0 and y==0 and z==0):
                return vp0pos

            px = vp0pos.lerp(vp1pos, distanceToRatio(x))
            pz = vp0pos.lerp(vp2pos, distanceToRatio(z))

            if (y==0):
                return lli_input(vp1pos, pz, vp2pos, px)

            py = vp0pos.lerp(vp3pos, distanceToRatioY(y))
            YZ = lli_input(vp3pos, pz, vp2pos, py)
            XY = lli_input(vp3pos, px, vp1pos, py)
            
            return lli_input(XY, vp2pos, vp1pos, YZ)
        
        def get3mirror(x, y, z, mirror):
            
            vp0pos = mirror

            if (x==0 and y==0 and z==0):
                return vp0pos

            px = vp0pos.lerp(vp1pos, distanceToRatio(x))
            pz = vp0pos.lerp(vp2pos, distanceToRatio(z))

            if (y==0):
                return lli_input(vp1pos, pz, vp2pos, px)

            py = vp0pos.lerp(vp3pos, distanceToRatioY(y))
            YZ = lli_input(vp3pos, pz, vp2pos, py)
            XY = lli_input(vp3pos, px, vp1pos, py)
            
            return lli_input(XY, vp2pos, vp1pos, YZ)

        def lli_input(l1p1, l1p2, l2p1, l2p2):
          return lli(l1p1.x, l1p1.y, l1p2.x, l1p2.y, l2p1.x, l2p1.y, l2p2.x, l2p2.y)

        def lli(x1, y1, x2, y2, x3, y3, x4, y4):
            d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if (d == 0):
#                return None
                d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) + 0.0000000001
 

            c12 = (x1 * y2 - y1 * x2)
            c34 = (x3 * y4 - y3 * x4)
            nx = c12 * (x3 - x4) - c34 * (x1 - x2)
            ny = c12 * (y3 - y4) - c34 * (y1 - y2)
            return Vector((nx/d, ny/d))

        def grid_generator(typeName, line_width, verts, isAssist):

            #is_assist = "no"
            gp_name = typeName
            
            try:
                bpy.data.collections[Perspective_Collection]
            except:
                bpy.data.collections.new(Perspective_Collection)
                bpy.context.scene.collection.children.link(bpy.data.collections[Perspective_Collection])

            #data is added to an object and linked to the scene
            bpy.data.grease_pencils.new(gp_name)


            if vp0pos.y == vp1pos.y or vp0pos.y ==vp2pos.y or vp0pos.y == vp3pos.y:
                vp0pos.y = vp0pos.y + .00000015
            if vp0pos.x == vp1pos.x or vp0pos.x ==vp2pos.x or vp0pos.y == vp3pos.y:
                vp0pos.x = vp0pos.x + .00000015

            if vp1pos.x ==vp2pos.x or vp1pos.x == vp3pos.x:
                vp1pos.x = vp1pos.x + .00000001        
            if vp1pos.y ==vp2pos.y or vp1pos.y == vp3pos.y:
                vp1pos.y = vp1pos.y + .00000001

            if vp2pos.x == vp3pos.x:
                vp2pos.x = vp2pos.x + .00000002       
            if vp2pos.y == vp3pos.y:
                vp2pos.y = vp2pos.y + .00000002
            
            gp_data = bpy.data.grease_pencils[gp_name]
            gp_data.vpstore.vp0pos = vp0pos
            gp_data.vpstore.vp1pos = vp1pos
            gp_data.vpstore.vp2pos = vp2pos
            gp_data.vpstore.vp3pos = vp3pos
            gp_data.vpstore.pFact = pFact
            gp_data.vpstore.pFactY = pFactY
            


            bpy.data.objects.new(gp_data.name, gp_data)
            gp_obj = bpy.data.objects[gp_name]
            gp_obj.location.y += 0.01
            
            bpy.data.collections[Perspective_Collection].objects.link(gp_obj)

            #Create Material and Assign
            mat_name = gp_name + " Material"

            try: 
                bpy.data.materials[mat_name].user_clear()
                bpy.data.materials.remove(bpy.data.materials[mat_name])
                gp_obj.data.materials.append(gp_mat)
            except:
                bpy.data.materials.new(name = mat_name)
                bpy.data.materials.create_gpencil_data(bpy.data.materials[mat_name])

                if isAssist == False:
                    bpy.data.materials[mat_name].grease_pencil.color = lineColor
                else:
                    bpy.data.materials[mat_name].grease_pencil.color = AssistColor
                    
                gp_obj.data.materials.append(bpy.data.materials[mat_name])

            #Create initial layer, frame, stroke
            gp_layer = gp_data.layers.new(gp_name)
            gp_layer.lock = True
            gp_frame = gp_layer.frames.new(bpy.context.scene.frame_current)

            if typeName == OnePP_name:

                #Create the OnePP Map
                for x in range(lineCount):
                    
                    gp_data.vpstore.vp1pos = vpONEpos
                    OnePP_Map_Strokes = gp_frame.strokes.new()
                    OnePP_Map_Strokes.line_width = line_width
                    OnePP_Map_Strokes.points.add(count=2)
                    
                    angle=radians(180/lineCount*(x+1))
                    OnePP_Map_Strokes.points[0].co = (vpONEpos.x + (radius * sin(angle)), 0, vpONEpos.y + (radius * cos(angle)))
                    OnePP_Map_Strokes.points[1].co = (vpONEpos.x - (radius * sin(angle)), 0, vpONEpos.y - (radius * cos(angle)))
                    OnePP_Map_Strokes.points[0].vertex_color = lineColor
                    OnePP_Map_Strokes.points[1].vertex_color = lineColor 
                    OnePP_Map_Strokes.points[0].strength = lineStrength
                    OnePP_Map_Strokes.points[1].strength = lineStrength
                    
                                   
                
            if typeName == TwoPP_name:
                #Make Initial Points to VP1
                gp_stroke_vp1 = gp_frame.strokes.new()
                gp_stroke_vp1.line_width = line_width
                gp_stroke_vp1.points.add(count=steps)
                     
                #Make Initial Points to VP2
                gp_stroke_vp2 = gp_frame.strokes.new()
                gp_stroke_vp2.line_width = line_width
                gp_stroke_vp2.points.add(count=steps)  
                
                
                #Make Initial Points to VP1
                gp_stroke_vp3 = gp_frame.strokes.new()
                gp_stroke_vp3.line_width = line_width
                gp_stroke_vp3.points.add(count=steps)
                     
                #Make Initial Points to VP2
                gp_stroke_vp4 = gp_frame.strokes.new()
                gp_stroke_vp4.line_width = line_width
                gp_stroke_vp4.points.add(count=steps)  

#                if ceiling == True:

                yDiff = (vp2pos.y) - (vp1pos.y)
                xDiff = (vp2pos.x) - (vp1pos.x)
                
                if xDiff == 0:
                    xDiff = 0.0000001
                if yDiff == 0:
                    yDiff = 0.0000001

                m = yDiff / xDiff
                Pm = -1/m
                
                b = vp1pos.y -(m * vp1pos.x)
                
                Pb = vp0pos.y - (Pm * vp0pos.x)
                x = (b - Pb) / (Pm - m)
                
                # y = Pm * x + Pb
                y = Pm * (b - Pb) / (Pm - m) + Pb
                
                intersection = Vector((x,y))
                #reflection: 
                Rx = 2 * intersection.x - vp0pos.x
                Ry = 2 * intersection.y - vp0pos.y
                reflection = Vector((Rx, Ry))
                    
                for step in range(steps):

                    a = get3(step, 0, 0)
                    b = get3(0, 0, step)
                    
                    if ceiling == True:
                        c = get3mirror(step, 0, 0, reflection)
                        d = get3mirror(0, 0, step, reflection)

                    if a is None:
                        a = vp1pos
                    if b is None:
                        b = vp2pos
                        
                    if verts == True:
                        
                        for inner_step in range(steps): 
                            stepstrength = lineStrength / (step + 1) 
                            reverse_stepstrength = lineStrength - (lineStrength / (step + 1))
                            inner_get = get3(step, 0, inner_step)  
                            inner_get_ceiling = get3mirror(step, 0, inner_step,reflection)
                            
                            if inner_get_ceiling is None:
                                inner_get_ceiling = vp2pos                 
                            gp_stroke_vp1_inner_ceiling_grid = gp_frame.strokes.new()
                            gp_stroke_vp1_inner_ceiling_grid.line_width = line_width
                            gp_stroke_vp1_inner_ceiling_grid.points.add(count=2)
                            gp_stroke_vp1_inner_ceiling_grid.points[0].co = (inner_get_ceiling.x, 0, inner_get_ceiling.y)
                            gp_stroke_vp1_inner_ceiling_grid.points[1].co = (inner_get.x, 0, inner_get.y)
                            gp_stroke_vp1_inner_ceiling_grid.points[0].strength = reverse_stepstrength
                            gp_stroke_vp1_inner_ceiling_grid.points[1].strength = reverse_stepstrength
                            
                            if inner_get is None:
                                inner_get = vp2pos                 
                            gp_stroke_vp1_inner_grid = gp_frame.strokes.new()
                            gp_stroke_vp1_inner_grid.line_width = line_width
                            gp_stroke_vp1_inner_grid.points.add(count=2)
                            gp_stroke_vp1_inner_grid.points[0].co = (inner_get.x, 0, inner_get.y)
                            gp_stroke_vp1_inner_grid.points[1].co = (inner_get_ceiling.x, 0, inner_get_ceiling.y)
                            gp_stroke_vp1_inner_grid.points[0].strength = stepstrength
                            gp_stroke_vp1_inner_grid.points[1].strength = stepstrength
         
                        gp_stroke_vp1.points[step].co = (a.x,0,a.y)
                        gp_stroke_vp1_grid = gp_frame.strokes.new()
                        gp_stroke_vp1_grid.line_width = line_width
                        gp_stroke_vp1_grid.points.add(count=2)
                        gp_stroke_vp1_grid.points[0].co = (vp2pos.x,0,vp2pos.y)
                        gp_stroke_vp1_grid.points[1].co = gp_stroke_vp1.points[step].co
                        gp_stroke_vp1_grid.points[0].co = (vp2pos.x,0,vp2pos.y)
                        gp_stroke_vp1_grid.points[1].co = gp_stroke_vp1.points[step].co
                        
                        gp_stroke_vp1_grid.points[0].strength = lineStrength
                        gp_stroke_vp1_grid.points[1].strength = lineStrength
                        
                        gp_stroke_vp2.points[step].co = (b.x,0,b.y)
                        gp_stroke_vp2_grid = gp_frame.strokes.new()
                        gp_stroke_vp2_grid.line_width = line_width
                        gp_stroke_vp2_grid.points.add(count=2)
                        gp_stroke_vp2_grid.points[0].co = (vp1pos.x,0,vp1pos.y)
                        gp_stroke_vp2_grid.points[1].co = gp_stroke_vp2.points[step].co
                        gp_stroke_vp2_grid.points[0].strength = lineStrength
                        gp_stroke_vp2_grid.points[1].strength = lineStrength

                    elif verts == False:                   
                        gp_stroke_vp1.points[step].co = (a.x,0,a.y)
                        gp_stroke_vp2.points[step].co = (b.x,0,b.y)
                        
                        gp_stroke_vp1_grid = gp_frame.strokes.new()
                        gp_stroke_vp1_grid.line_width = line_width
                        gp_stroke_vp1_grid.points.add(count=2)
                        gp_stroke_vp1_grid.points[0].co = (vp2pos.x,0,vp2pos.y)
                        gp_stroke_vp1_grid.points[1].co = gp_stroke_vp1.points[step].co
                        gp_stroke_vp1_grid.points[0].strength = lineStrength
                        gp_stroke_vp1_grid.points[1].strength = lineStrength
                        
                        gp_stroke_vp2_grid = gp_frame.strokes.new()
                        gp_stroke_vp2_grid.line_width = line_width
                        gp_stroke_vp2_grid.points.add(count=2)
                        gp_stroke_vp2_grid.points[0].co = (vp1pos.x,0,vp1pos.y)
                        gp_stroke_vp2_grid.points[1].co = gp_stroke_vp2.points[step].co
                        gp_stroke_vp2_grid.points[0].strength = lineStrength
                        gp_stroke_vp2_grid.points[1].strength = lineStrength
                        

                    if ceiling == True and c is not None:
                        
                        gp_stroke_vp3.points[step].co = (c.x,0,c.y)
                        gp_stroke_vp4.points[step].co = (d.x,0,d.y)

                        gp_stroke_vp3_grid = gp_frame.strokes.new()
                        gp_stroke_vp3_grid.line_width = line_width
                        gp_stroke_vp3_grid.points.add(count=2)
                        gp_stroke_vp3_grid.points[0].co = vp2pos.x,0,vp2pos.y
                        gp_stroke_vp3_grid.points[1].co = gp_stroke_vp3.points[step].co
                        gp_stroke_vp3_grid.points[0].strength = lineStrength
                        gp_stroke_vp3_grid.points[1].strength = lineStrength
                        
                        gp_stroke_vp4_grid = gp_frame.strokes.new()
                        gp_stroke_vp4_grid.line_width = line_width
                        gp_stroke_vp4_grid.points.add(count=2)
                        gp_stroke_vp4_grid.points[0].co = vp1pos.x,0,vp1pos.y
                        gp_stroke_vp4_grid.points[1].co = gp_stroke_vp4.points[step].co
                        gp_stroke_vp4_grid.points[0].strength = lineStrength
                        gp_stroke_vp4_grid.points[1].strength = lineStrength
                              


            if typeName == ThreePP_name:

                if verts == True:
                    #Generate Grid
                    for step in range(steps):
                        try:
                            a = get3(step, 0, 0)
                            b = get3(0, 0, step)
                            c = get3(0,step,0)
                        except:
                            return {'CANCELED'}
                        
#                        if a is None:
#                            a = vp1pos
#                        if b is None:
#                            b = vp2pos
#                        if c is None:
#                            c = vp3pos
                        
                        for inner_step in range(steps):
                            stepstrength = lineStrength / (step + 1) 
                            inner_get = get3(step, 0, inner_step) 
#                            if inner_get is None:
#                                inner_get = vp1pos               
                            gp_stroke_vp1_inner_grid = gp_frame.strokes.new()
                            gp_stroke_vp1_inner_grid.line_width = line_width
                            gp_stroke_vp1_inner_grid.points.add(count=2)
                            
                            
#                            try: 
                            gp_stroke_vp1_inner_grid.points[0].co = (inner_get.x, 0, inner_get.y)
#                            except:
#                                gp_stroke_vp1_inner_grid.points[0].co = (0, 0, 0)
                            
                            gp_stroke_vp1_inner_grid.points[1].co = (vp3pos.x, 0, vp3pos.y)
                            gp_stroke_vp1_inner_grid.points[0].strength = stepstrength
                            gp_stroke_vp1_inner_grid.points[1].strength = stepstrength

                            
                            inner_get = get3(inner_step, 0, step)
                            gp_stroke_vp1_inner_grid = gp_frame.strokes.new()
                            gp_stroke_vp1_inner_grid.line_width = line_width
                            gp_stroke_vp1_inner_grid.points.add(count=2)
                            
                            
                            
#                            try: 
                            gp_stroke_vp1_inner_grid.points[0].co = (inner_get.x, 0, inner_get.y)
#                            except:
#                                gp_stroke_vp1_inner_grid.points[0].co = (0, 0, 0)
                            
                            gp_stroke_vp1_inner_grid.points[1].co = (vp3pos.x, 0, vp3pos.y)
                            gp_stroke_vp1_inner_grid.points[0].strength = stepstrength
                            gp_stroke_vp1_inner_grid.points[1].strength = stepstrength

                            stepstrength = lineStrength / (step + 1) 
                            
#                            try:
                            inner_get = get3(0, inner_step, step)   
#                            except: 
#                                return {'CANCELED'}
                                         
                            gp_stroke_vp3_inner_grid = gp_frame.strokes.new()
                            gp_stroke_vp3_inner_grid.line_width = line_width
                            gp_stroke_vp3_inner_grid.points.add(count=2)
                            
                            if inner_get is None:
                                gp_stroke_vp3_inner_grid.points[0].co = (vp2pos.x, 0, vp2pos.y)
                            else:
                                gp_stroke_vp3_inner_grid.points[0].co = (inner_get.x, 0, inner_get.y)

                            gp_stroke_vp3_inner_grid.points[1].co = (vp1pos.x, 0, vp1pos.y)
                            gp_stroke_vp3_inner_grid.points[0].strength = stepstrength
                            gp_stroke_vp3_inner_grid.points[1].strength = stepstrength
                            
                            inner_get = get3(step, inner_step, 0)                
                            gp_stroke_vp3_inner_grid = gp_frame.strokes.new()
                            gp_stroke_vp3_inner_grid.line_width = line_width
                            gp_stroke_vp3_inner_grid.points.add(count=2)
                            

#                            if inner_get is None:
#                                gp_stroke_vp3_inner_grid.points[0].co = (vp2pos.x, 0, vp2pos.y)
#                            else:
                            gp_stroke_vp3_inner_grid.points[0].co = (inner_get.x, 0, inner_get.y)

                            gp_stroke_vp3_inner_grid.points[1].co = (vp2pos.x, 0, vp2pos.y)
                            gp_stroke_vp3_inner_grid.points[0].strength = stepstrength
                            gp_stroke_vp3_inner_grid.points[1].strength = stepstrength
                            
                       # for inner_step in range(steps):

                
                if verts == False:
                    
                    #Make Initial Points to VP1
                    gp_stroke_vp1 = gp_frame.strokes.new()
                    gp_stroke_vp1.line_width = line_width
                    gp_stroke_vp1.points.add(count=steps)

                         
                    #Make Initial Points to VP2
                    gp_stroke_vp2 = gp_frame.strokes.new()
                    gp_stroke_vp2.line_width = line_width
                    gp_stroke_vp2.points.add(count=steps)

                    
                    #Make Initial Points to VP3
                    gp_stroke_vp3 = gp_frame.strokes.new()
                    gp_stroke_vp3.line_width = line_width
                    gp_stroke_vp3.points.add(count=steps)
                    
                    for point in gp_stroke_vp3.points:
                        point.strength = lineStrength
                    
                    gp_stroke_vp3b = gp_frame.strokes.new()
                    gp_stroke_vp3b.line_width = line_width
                    gp_stroke_vp3b.points.add(count=steps)
                    
                    for point in gp_stroke_vp3b.points:
                        point.strength = 0

                    for step in range(steps):
                        
                        stepstrength = lineStrength / (step + 1) 
                        
                    
                        a = get3(step, 0, 0)
                        b = get3(0, 0, step)
                        c = get3(0,step,0)
                    #    except:
                    #        return {'CANCELED'}
                            
                        gp_stroke_vp1.points[step].co = (a.x,0,a.y)
                       
                        
                        gp_stroke_vp1.points[step].strength = lineStrength
                        gp_stroke_vp1_grid = gp_frame.strokes.new()
                        gp_stroke_vp1_grid.line_width = line_width
                        gp_stroke_vp1_grid.points.add(count=2)
                        gp_stroke_vp1_grid.points[0].co = (vp2pos.x,0,vp2pos.y)
                        gp_stroke_vp1_grid.points[1].co = gp_stroke_vp1.points[step].co
                        gp_stroke_vp1_grid.points[0].strength = stepstrength
                        gp_stroke_vp1_grid.points[1].strength = stepstrength
                        
                        gp_stroke_vp2.points[step].co = (b.x,0,b.y)
                            
                        gp_stroke_vp2.points[step].strength = lineStrength
                        gp_stroke_vp2_grid = gp_frame.strokes.new()
                        gp_stroke_vp2_grid.line_width = line_width
                        gp_stroke_vp2_grid.points.add(count=2)
                        gp_stroke_vp2_grid.points[0].co = (vp1pos.x,0,vp1pos.y)
                        gp_stroke_vp2_grid.points[1].co = gp_stroke_vp2.points[step].co
                        gp_stroke_vp2_grid.points[0].strength = stepstrength
                        gp_stroke_vp2_grid.points[1].strength = stepstrength
                        
                  #      try:
                        gp_stroke_vp3.points[step].co = (c.x,0,c.y)
               #         except:
                #            gp_stroke_vp3.points[step].co = (vp3pos.x, 0, vp3pos.y)

                        #avoid duplicate central line
                        if step > 0:
                            gp_stroke_vp3.points[step].co = (vp3pos.x, 0, vp3pos.y)
                            gp_stroke_vp3.points[step].strength = lineStrength
                            gp_stroke_vp3_grid_a = gp_frame.strokes.new()
                            gp_stroke_vp3_grid_a.line_width = line_width
                            gp_stroke_vp3_grid_a.points.add(count=2)
                            
                            gp_stroke_vp3_grid_a.points[0].co = (a.x,0,a.y)
                               
                            gp_stroke_vp3_grid_a.points[1].co = gp_stroke_vp3.points[step].co
                            gp_stroke_vp3_grid_a.points[0].strength = lineStrength
                            gp_stroke_vp3_grid_a.points[1].strength = lineStrength
               
                            gp_stroke_vp3_grid_b = gp_frame.strokes.new()
                            gp_stroke_vp3_grid_b.line_width = line_width
                            gp_stroke_vp3_grid_b.points.add(count=2)
                            
                            gp_stroke_vp3_grid_b.points[0].co = (b.x,0,b.y)
                                
                            gp_stroke_vp3_grid_b.points[1].co = gp_stroke_vp3.points[step].co
                            gp_stroke_vp3_grid_b.points[0].strength = lineStrength
                            gp_stroke_vp3_grid_b.points[1].strength = lineStrength

                            if c is not None:
                                    
                                gp_stroke_vp3b.points[step].co = (c.x,0,c.y)
                                gp_stroke_vp3b_grid_a = gp_frame.strokes.new()
                                gp_stroke_vp3b_grid_a.line_width = line_width
                                gp_stroke_vp3b_grid_a.points.add(count=2)
                                gp_stroke_vp3b_grid_a.points[0].co = (vp1pos.x,0,vp1pos.y)
                                gp_stroke_vp3b_grid_a.points[1].co = gp_stroke_vp3b.points[step].co
                                gp_stroke_vp3b_grid_a.points[0].strength = lineStrength
                                gp_stroke_vp3b_grid_a.points[1].strength = lineStrength
                            
                                gp_stroke_vp3b.points[step].co = (c.x,0,c.y)
                                gp_stroke_vp3b_grid_b = gp_frame.strokes.new()
                                gp_stroke_vp3b_grid_b.line_width = line_width
                                gp_stroke_vp3b_grid_b.points.add(count=2)
                                gp_stroke_vp3b_grid_b.points[0].co = (vp2pos.x,0,vp2pos.y)
                                gp_stroke_vp3b_grid_b.points[1].co = gp_stroke_vp3b.points[step].co
                                gp_stroke_vp3b_grid_b.points[0].strength = lineStrength
                                gp_stroke_vp3b_grid_b.points[1].strength = lineStrength
                                
                            else:
                                
                                gp_stroke_vp3b.points[step].co = vp2pos.x, 0, vp2pos.y
                                gp_stroke_vp3b_grid_a = gp_frame.strokes.new()
                                gp_stroke_vp3b_grid_a.line_width = line_width
                                gp_stroke_vp3b_grid_a.points.add(count=2)
                                gp_stroke_vp3b_grid_a.points[0].co = (vp1pos.x,0,vp1pos.y)
                                gp_stroke_vp3b_grid_a.points[1].co = gp_stroke_vp3b.points[step].co
                                gp_stroke_vp3b_grid_a.points[0].strength = lineStrength
                                gp_stroke_vp3b_grid_a.points[1].strength = lineStrength
                            
                            
                                gp_stroke_vp3b.points[step].co = (c.x,0,c.y)
                                gp_stroke_vp3b_grid_b = gp_frame.strokes.new()
                                gp_stroke_vp3b_grid_b.line_width = line_width
                                gp_stroke_vp3b_grid_b.points.add(count=2)
                                gp_stroke_vp3b_grid_b.points[0].co = (vp2pos.x,0,vp2pos.y)
                                gp_stroke_vp3b_grid_b.points[1].co = gp_stroke_vp3b.points[step].co
                                gp_stroke_vp3b_grid_b.points[0].strength = lineStrength
                                gp_stroke_vp3b_grid_b.points[1].strength = lineStrength

                                

        match PerspectiveType:
            case "OnePP_Option":
                vp_count=1
                typeName=OnePP_name
            case "TwoPP_Option":
                vp_count=2
                typeName=TwoPP_name
            case "ThreePP_Option":
                vp_count=3
                typeName=ThreePP_name

        try:
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[typeName])
        except:
            "Not There"   
              
        grid_generator(typeName,lineWidth,verts,False)
        
        return {'FINISHED'}

class PPCLEAR_OT_obj(bpy.types.Operator):
    bl_idname = "pp.clear"
    bl_label = "Clear Active Perfect Perspective Objects"
    bl_options = {'UNDO'}
    
    def execute(self,context):
        
        #Clear assists first as they have dependancies
        try:
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[Assist_name])
        except:
            "OK"
        try:
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[OnePP_name])
        except:
            "OK"
        try:
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[TwoPP_name])
        except:
            "OK"
        try:
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[ThreePP_name])
        except:
            "OK"       
    
        return {'FINISHED'}


###Archive Active Perspective Grids
class PP_OT_archive(bpy.types.Operator):
    bl_idname = "pp.archive"
    bl_label = "Archive Perfect Perspective Grid"
    bl_options = {'UNDO'}
        
    def execute(self,context):
        
        def archive(type):
            for i in range(99):
                try:
                    bpy.data.objects[type]
                    new_name = type + str(i)
                    try:
                        bpy.data.objects[new_name]
                    except:
                        try: 
                            bpy.data.grease_pencils[new_name]
                        except:
                            bpy.data.objects[type].name = new_name
                            bpy.data.collections[Perspective_Collection].objects.unlink(bpy.data.objects[new_name])
                            bpy.data.collections[Archive_Collection].objects.link(bpy.data.objects[new_name]) 
                            #bpy.data.objects[new_name].hide_viewport = True
                            bpy.data.grease_pencils[type].name = new_name
      
                except:
                    "whoops"
            return {'FINISHED'}

        try:
            bpy.data.collections[Archive_Collection]
        except:
            new_collection = bpy.data.collections.new(Archive_Collection)

        working_collection = bpy.data.collections[Archive_Collection]
        working_collection.hide_render = True
        working_collection.hide_viewport = True

        try:
            bpy.context.scene.collection.children.link(working_collection)
        except:
            "Already There"

        archive(ThreePP_name)
        archive(TwoPP_name)
        archive(OnePP_name)

        return {'FINISHED'}


def AssistCreate(gp_name, pp_type):

    ###########Repalce Me########
#    PerspectiveType = bpy.context.scene.PPSettings.PerspectiveTypeEnum
    lineWidth = bpy.context.scene.PPSettings.lineWidth
    lineStrength = bpy.context.scene.PPSettings.lineStrength
    verts = bpy.context.scene.PPSettings.verts
    assistColor = bpy.context.scene.PPSettings.assistColor
    vp0pos = bpy.context.scene.PPSettings.opos
    vpONEpos = bpy.context.scene.PPSettings.vpONEpos
    vp1pos = bpy.context.scene.PPSettings.vp1pos
    vp2pos = bpy.context.scene.PPSettings.vp2pos
    vp3pos = bpy.context.scene.PPSettings.vp3pos
    ###########Repalce Me########

    try:
        bpy.data.collections[Perspective_Collection]
    except:
        bpy.data.collections.new(Perspective_Collection)
        bpy.context.scene.collection.children.link(bpy.data.collections[Perspective_Collection])
    
    
    if pp_type == 3:
        dummygp = ThreePP_name
        try:
            bpy.data.grease_pencils[dummygp]
            dummygp_data = bpy.data.grease_pencils[dummygp]
        except:
            dummygp_data = bpy.data.grease_pencils.new(dummygp)
            dummygp_data.vpstore.vp0pos = vp0pos
            dummygp_data.vpstore.vp1pos = vp1pos
            dummygp_data.vpstore.vp2pos = vp2pos
            dummygp_data.vpstore.vp3pos = vp3pos
            dummygp_data.vpstore.temp = True
            
            dummygp_obj = bpy.data.objects.new(dummygp_data.name, dummygp_data)
            bpy.data.collections[Perspective_Collection].objects.link(dummygp_obj)
            dummygp_layer = dummygp_data.layers.new(dummygp_data.name)
            dummygp_layer.lock = True
            dummygp_frame = dummygp_layer.frames.new(bpy.context.scene.frame_current)
            dummygp_stroke = dummygp_frame.strokes.new()
            dummygp_stroke.line_width = lineWidth
    
            dummygp_stroke.points.add(count = 3)
            dummygp_stroke.points[0].co = (vp1pos.x,0,vp1pos.y)
            dummygp_stroke.points[1].co = (vp2pos.x,0,vp2pos.y)   
            dummygp_stroke.points[2].co = (vp3pos.x,0,vp3pos.y)
            
            for point in dummygp_stroke.points:
                point.strength = 0


        assist_data = bpy.data.grease_pencils.new(gp_name)
        assist_obj = bpy.data.objects.new(assist_data.name, assist_data)
        assist_obj.show_in_front = True
        assist_obj.location = bpy.data.objects[dummygp].location
        assist_obj.scale = bpy.data.objects[dummygp].scale
        assist_obj.rotation_euler = bpy.data.objects[dummygp].rotation_euler
        bpy.data.collections[Perspective_Collection].objects.link(assist_obj)
        
        assist_layer = assist_data.layers.new(gp_name)
        assist_layer.lock = True
        assist_frame = assist_layer.frames.new(bpy.context.scene.frame_current)

        
        assist_stroke = assist_frame.strokes.new()
        assist_stroke.line_width = lineWidth
        assist_stroke.points.add(count = 3)

        assist_stroke2 = assist_frame.strokes.new()
        assist_stroke2.points.add(count = 3)
        assist_stroke2.line_width = lineWidth 
        
        assist_stroke3 = assist_frame.strokes.new()
        assist_stroke3.points.add(count = 3)
        assist_stroke3.line_width = lineWidth
        
        assist_stroke.points[0].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke.points[1].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke.points[2].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke2.points[0].co = (dummygp_data.vpstore.vp2pos[0], 0, dummygp_data.vpstore.vp2pos[1])
        assist_stroke2.points[1].co = (dummygp_data.vpstore.vp2pos[0], 0, dummygp_data.vpstore.vp2pos[1])
        assist_stroke2.points[2].co = (dummygp_data.vpstore.vp2pos[0], 0, dummygp_data.vpstore.vp2pos[1])
        assist_stroke3.points[0].co = (dummygp_data.vpstore.vp3pos[0], 0, dummygp_data.vpstore.vp3pos[1])
        assist_stroke3.points[1].co = (dummygp_data.vpstore.vp3pos[0], 0, dummygp_data.vpstore.vp3pos[1])
        assist_stroke3.points[2].co = (dummygp_data.vpstore.vp3pos[0], 0, dummygp_data.vpstore.vp3pos[1])
       
        #Assist Stroke Colors
        for point in assist_stroke.points:
            point.vertex_color = assistColor
        for point in assist_stroke2.points:
            point.vertex_color = assistColor
        for point in assist_stroke3.points:
            point.vertex_color = assistColor

    if pp_type == 2:
        dummygp = TwoPP_name
        try:
            bpy.data.grease_pencils[dummygp]
            dummygp_data = bpy.data.grease_pencils[dummygp]
        except:
            dummygp_data = bpy.data.grease_pencils.new(dummygp)
            dummygp_data.vpstore.vp0pos = vp0pos
            dummygp_data.vpstore.vp1pos = vp1pos
            dummygp_data.vpstore.vp2pos = vp2pos
            dummygp_data.vpstore.vp3pos = vp3pos
            dummygp_data.vpstore.temp = True
            
            dummygp_obj = bpy.data.objects.new(dummygp_data.name, dummygp_data)
            bpy.data.collections[Perspective_Collection].objects.link(dummygp_obj)
            dummygp_layer = dummygp_data.layers.new(dummygp_data.name)
            dummygp_layer.lock = True
            dummygp_frame = dummygp_layer.frames.new(bpy.context.scene.frame_current)
            dummygp_stroke = dummygp_frame.strokes.new()
            dummygp_stroke.line_width = lineWidth
    
            dummygp_stroke.points.add(count = 3)
            dummygp_stroke.points[0].co = (vp1pos.x,0,vp1pos.y)
            dummygp_stroke.points[1].co = (vp2pos.x,0,vp2pos.y)
            
            for point in dummygp_stroke.points:
                point.strength = 0


        assist_data = bpy.data.grease_pencils.new(gp_name)
        assist_obj = bpy.data.objects.new(assist_data.name, assist_data)
        assist_obj.show_in_front = True
        assist_obj.location = bpy.data.objects[dummygp].location
        assist_obj.scale = bpy.data.objects[dummygp].scale
        assist_obj.rotation_euler = bpy.data.objects[dummygp].rotation_euler
        bpy.data.collections[Perspective_Collection].objects.link(assist_obj)
        
        assist_layer = assist_data.layers.new(gp_name)
        assist_layer.lock = True
        assist_frame = assist_layer.frames.new(bpy.context.scene.frame_current)

        
        assist_stroke = assist_frame.strokes.new()
        assist_stroke.line_width = lineWidth
        assist_stroke.points.add(count = 3)

        assist_stroke2 = assist_frame.strokes.new()
        assist_stroke2.points.add(count = 3)
        assist_stroke2.line_width = lineWidth 
        
        assist_stroke.points[0].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke.points[1].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke.points[2].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke2.points[0].co = (dummygp_data.vpstore.vp2pos[0], 0, dummygp_data.vpstore.vp2pos[1])
        assist_stroke2.points[1].co = (dummygp_data.vpstore.vp2pos[0], 0, dummygp_data.vpstore.vp2pos[1])
        assist_stroke2.points[2].co = (dummygp_data.vpstore.vp2pos[0], 0, dummygp_data.vpstore.vp2pos[1])
       
        #Assist Stroke Colors
        for point in assist_stroke.points:
            point.vertex_color = assistColor
        for point in assist_stroke2.points:
            point.vertex_color = assistColor

    if pp_type == 1:
        dummygp = OnePP_name
        try:
            bpy.data.grease_pencils[dummygp]
            dummygp_data = bpy.data.grease_pencils[dummygp]
        except:
            dummygp_data = bpy.data.grease_pencils.new(dummygp)
            dummygp_data.vpstore.vp1pos = vpONEpos
            dummygp_data.vpstore.temp = True
            
            dummygp_obj = bpy.data.objects.new(dummygp_data.name, dummygp_data)
            bpy.data.collections[Perspective_Collection].objects.link(dummygp_obj)
            dummygp_layer = dummygp_data.layers.new(dummygp_data.name)
            dummygp_layer.lock = True
            dummygp_frame = dummygp_layer.frames.new(bpy.context.scene.frame_current)
            dummygp_stroke = dummygp_frame.strokes.new()
            dummygp_stroke.line_width = lineWidth
    
            dummygp_stroke.points.add(count = 3)
            dummygp_stroke.points[0].co = (vpONEpos.x,0,vpONEpos.y)
            dummygp_stroke.points[1].co = (vp2pos.x,0,vp2pos.y)
            
            for point in dummygp_stroke.points:
                point.strength = 0


        assist_data = bpy.data.grease_pencils.new(gp_name)
        assist_obj = bpy.data.objects.new(assist_data.name, assist_data)
        assist_obj.show_in_front = True
        assist_obj.location = bpy.data.objects[dummygp].location
        assist_obj.scale = bpy.data.objects[dummygp].scale
        assist_obj.rotation_euler = bpy.data.objects[dummygp].rotation_euler
        bpy.data.collections[Perspective_Collection].objects.link(assist_obj)
        
        assist_layer = assist_data.layers.new(gp_name)
        assist_layer.lock = True
        assist_frame = assist_layer.frames.new(bpy.context.scene.frame_current)

        
        assist_stroke = assist_frame.strokes.new()
        assist_stroke.line_width = lineWidth
        assist_stroke.points.add(count = 3)
        
        assist_stroke.points[0].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke.points[1].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
        assist_stroke.points[2].co = (dummygp_data.vpstore.vp1pos[0], 0, dummygp_data.vpstore.vp1pos[1])
       
        #Assist Stroke Colors
        for point in assist_stroke.points:
            point.vertex_color = assistColor



class PERSPECTIVE_OT_guide(bpy.types.Operator):

    ###Three Point Perspective Assists
    bl_idname = "pp.assist"
    bl_label = "Perfect Perspective Assists"

    handle = None  # Draw handle

    @staticmethod
    def on_update(self, context):
        
        #Ensure Grease Pencil Selection
        try:    
            if not bpy.context.object.type  == 'GPENCIL':
                return {'CANCELLED'}
        except:
            return {'CANCELLED'}

        try:
            self.handle
        except ReferenceError:
            context.space_data.draw_handler_remove(__class__.handle, 'WINDOW')
            __class__.handle = None
            return

        #Get the mouse position thanks to the event            
        mouse_pos = Mouse.get()

        #Contextual active object, 2D and 3D regions
        self.object = bpy.context.object
        region = bpy.context.region
        region3D = bpy.context.space_data.region_3d

        #The direction indicated by the mouse position from the current view
        self.view_vector = view3d_utils.region_2d_to_vector_3d(region, region3D, mouse_pos)
        #The view point of the user
        self.view_point = view3d_utils.region_2d_to_origin_3d(region, region3D, mouse_pos)
        #The 3D location in this direction
        self.world_loc = view3d_utils.region_2d_to_location_3d(region, region3D, mouse_pos, self.view_vector)
 
        z = Vector( (0,0,1) )
        self.normal = z

        if self.object:
            
            match bpy.context.scene.PPSettings.PerspectiveTypeEnum:
                case 'OnePP_Option':
                    assist_Mouse(bpy.data.grease_pencils[Assist_name].layers[Assist_name].frames[0], self, bpy.data.objects[OnePP_name])
                case 'TwoPP_Option':
                    assist_Mouse(bpy.data.grease_pencils[Assist_name].layers[Assist_name].frames[0], self, bpy.data.objects[TwoPP_name])
                case 'ThreePP_Option':
                    assist_Mouse(bpy.data.grease_pencils[Assist_name].layers[Assist_name].frames[0], self, bpy.data.objects[ThreePP_name])
                    
            assist_Extension(bpy.data.grease_pencils[Assist_name].layers[Assist_name].frames[0])

            self.object.rotation_euler = z.rotation_difference( self.normal ).to_euler()

    def modal(self, context, event):
        try:
            bpy.data.grease_pencils[Assist_name].layers[Assist_name]
        except:
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            try:
                self.on_update(self, context)
            except:
                bpy.data.objects.remove(bpy.data.objects[Assist_name])
                bpy.data.grease_pencils.remove(bpy.data.grease_pencils[Assist_name])

                match bpy.context.scene.PPSettings.PerspectiveTypeEnum:
                    case 'OnePP_Option':
                        if bpy.data.grease_pencils[OnePP_name].vpstore.temp == True:
                            bpy.data.objects.remove(bpy.data.objects[OnePP_name])
                            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[OnePP_name])
                    case 'TwoPP_Option':
                        if bpy.data.grease_pencils[TwoPP_name].vpstore.temp == True:
                            bpy.data.objects.remove(bpy.data.objects[TwoPP_name])
                            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[TwoPP_name])
                    case 'ThreePP_Option':
                        if bpy.data.grease_pencils[ThreePP_name].vpstore.temp == True:
                            bpy.data.objects.remove(bpy.data.objects[ThreePP_name])
                            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[ThreePP_name])               

                return {'CANCELLED'}

        #ESC to Escape Assists
        elif event.type in {'ESC'}:
            context.space_data.draw_handler_remove(__class__.handle, 'WINDOW')
            __class__.handle = None

            bpy.data.objects.remove(bpy.data.objects[Assist_name])
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[Assist_name])
                
            match bpy.context.scene.PPSettings.PerspectiveTypeEnum:
                case 'OnePP_Option':
                    if bpy.data.grease_pencils[OnePP_name].vpstore.temp == True:
                        bpy.data.objects.remove(bpy.data.objects[OnePP_name])
                        bpy.data.grease_pencils.remove(bpy.data.grease_pencils[OnePP_name])
                case 'TwoPP_Option':
                    if bpy.data.grease_pencils[TwoPP_name].vpstore.temp == True:
                        bpy.data.objects.remove(bpy.data.objects[TwoPP_name])
                        bpy.data.grease_pencils.remove(bpy.data.grease_pencils[TwoPP_name])
                case 'ThreePP_Option':
                    if bpy.data.grease_pencils[ThreePP_name].vpstore.temp == True:
                        bpy.data.objects.remove(bpy.data.objects[ThreePP_name])
                        bpy.data.grease_pencils.remove(bpy.data.grease_pencils[ThreePP_name])  
            
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        # Prevent the operator from being invoked again while running.
        line_width = bpy.context.scene.PPSettings.lineWidth 
        line_color = bpy.context.scene.PPSettings.lineColor
        assist_color = bpy.context.scene.PPSettings.assistColor
        PerspectiveType = bpy.context.scene.PPSettings.PerspectiveTypeEnum
        
        if __class__.handle is not None:
            return {'CANCELLED'}
        
        try:
            bpy.data.grease_pencils[Assist_name]
            bpy.data.grease_pencils.remove(bpy.data.grease_pencils[Assist_name])
            bpy.data.objects.remove(bpy.data.objects[Assist_name])
            gp_Assist = AssistCreate(Assist_name) 
            
            
        except:
            if PerspectiveType == 'ThreePP_Option':
                gp_Assist = AssistCreate(Assist_name,3)
            elif PerspectiveType == 'TwoPP_Option':
                gp_Assist = AssistCreate(Assist_name,2)
            elif PerspectiveType == 'OnePP_Option':
                gp_Assist = AssistCreate(Assist_name,1)
                
            bpy.data.objects[Assist_name].hide_select = True 

        gp_Assist = bpy.data.grease_pencils[Assist_name]  
     
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            context.window_manager.modal_handler_add(self)
            __class__.handle = context.space_data.draw_handler_add(
                self.on_update, (self, context), 'WINDOW', 'POST_PIXEL')
            return {'RUNNING_MODAL'}

        self.gp_Assist.layers[Assist_name].frames[0].strokes[1].points[1].co = self.world_loc
        return {'CANCELLED'}








class Mouse(bpy.types.Operator):
    """Allow getting mouse coordinates outside of operator events"""
    bl_idname = "wm.mouse"
    bl_label = "Mouse"
    bl_options = {'INTERNAL'}
    _data = [-1, -1]

    def invoke(self, context, event, *, data=_data):
        data[:] = event.mouse_region_x, event.mouse_region_y
        return {'PASS_THROUGH'}

    @classmethod
    def get(cls, data=_data, call=bpy.ops._op_call):
        # Reduce overhead by skipping operator parsing.
        call('WM_OT_mouse', {}, {}, 'INVOKE_DEFAULT')
        return data

    # Keymap handling is automatic
    @classmethod
    def register(cls):
        kc = bpy.context.window_manager.keyconfigs.addon
        km = kc.keymaps.get("3D View")
        if km is None:
            km = kc.keymaps.new("3D View", space_type='VIEW_3D', region_type='WINDOW')
        kmi = km.keymap_items.new(cls.bl_idname, 'MOUSEMOVE', 'ANY')
        cls.keymaps = [(km, kmi)]
    @classmethod
    def unregister(cls):
        for km, kmi in cls.keymaps: km.keymap_items.remove(kmi)


#ASSIST HELPER FUNCTIONS
#Draws line to mouse
def assist_Mouse(frame,cursor,object):
    for stroke in range(len(frame.strokes)):
        #0 = X, 1 = Y, 2 = Z

        for axis in range(len(frame.strokes[stroke].points[1].co)):
            try:
                frame.strokes[stroke].points[1].co[axis] = (cursor.world_loc[axis] - object.location[axis]) / object.scale[axis]
            except ZeroDivisionError:
                "Can't Divide by Zero"
            axis += 1
    stroke += 1

#Draws line past mouse
def assist_Extension(frame):

    for stroke in range(len(frame.strokes)):
        #0 = X, 1 = Y, 2 = Z
        for axis in range(len(frame.strokes[stroke].points[2].co)):
            try:
                frame.strokes[stroke].points[2].co[axis] = frame.strokes[stroke].points[0].co[axis] - 20 * (frame.strokes[stroke].points[0].co[axis] - frame.strokes[stroke].points[1].co[axis])
            except ZeroDivisionError:
                "Can't Divide by Zero"
            axis += 1 

 
def filter_callback(self, object):
    ###OBJECT SELECTOR CALLBACK FUNCTION
    return object.name in self.my_collection.objects.keys()



register_me = [
    PP_OT_properties, 
    PP_PT_main,
    PP_OT_generator,
    PPCLEAR_OT_obj,
    PP_OT_archive,
    Mouse,
    PERSPECTIVE_OT_guide,
    PP_OT_vpstore
    ]

def register():
    for i in register_me:
        bpy.utils.register_class(i)
        
    bpy.types.Scene.PPSettings = bpy.props.PointerProperty(type=PP_OT_properties)
    bpy.types.GreasePencil.vpstore = bpy.props.PointerProperty(type=PP_OT_vpstore)

def unregister():
    for i in register_me:
        bpy.utils.unregister_class(i)
        
    del bpy.types.Scene.PPSettings
    del bpy.types.GreasePencil.vpstore

if __name__ == '__main__':
    register()
