<<<<<<< HEAD
import math
from dicttoxml import dicttoxml
import xmltodict
from Constants import *
import win32ui
from EurekaSimLib import *
import random
import time
import math
from enum import IntEnum
from win32com.client import VARIANT
import pythoncom

class EAxisPos(IntEnum):
    LeftAxis = 0
    BottomAxis=1
    RightAxis=2
    TopAxis=3

class Colour:
    def __init__(self,red=0,green=0,blue=0):
        self.R=red
        self.G=green
        self.B=blue

    def setRGB(self,red=0,green=0,blue=0):
        self.R=red
        self.G=green
        self.B=blue

    def toRGB(self,iColor):
        hexColor = '%08x' % iColor
        self.R=int(hexColor[0:2],16)
        self.G=int(hexColor[2:4],16)
        self.B=int(hexColor[4:6],16)

    def toInt(self):
        colourHex = '00%02x%02x%02x' % (self.B,self.G,self.R)
        icolour = int(colourHex,16)
        return icolour
    @staticmethod
    def fromInt(iColor):
        hexColor = '%08x' % iColor
        blue=int(hexColor[2:4],16)
        green=int(hexColor[4:6],16)
        red=int(hexColor[6:8],16)
        return Colour(red,green,blue)


class ExperimentInfo():

    def __init__(self):
        self.RootText =""
        self.ExperimentGroup =""
        self.ExperimentName =""
        self.ObjectType =""
        self.Colour =0
        self.SimulationPattern =""
        self.SimulationInterval =0

    def Serilize(self):
        dicForm = vars(self)
        xml = dicttoxml(dicForm, attr_type=False, custom_root='ExperimentInfo')
        return xml
    def Deserilize(sel,strXML):
        doc = xmltodict.parse(strXML)
        infoDic = doc['ExperimentInfo']
        for k, v in infoDic.items():
            setattr(sel, k, v)

class ObjectPattern:
    def __init__(self):
        self.m_strObjectType = "Cube"
        self.m_Color = Colour(0, 0, 255)
        self.m_strSimulationPattern = "Rotate"
        self.m_lSimulationInterval = 100

    def Serialize(self):
        info = ExperimentInfo()
        info.ObjectType = self.m_strObjectType
        info.Colour = self.m_Color.toInt()
        info.SimulationPattern = self.m_strSimulationPattern
        info.SimulationInterval = self.m_lSimulationInterval
        return info

    def DeSerialize(self,info):
        self.m_strObjectType= info.ObjectType
        self.m_Color = Colour.fromInt(int(info.Colour))
        self.m_strSimulationPattern = info.SimulationPattern
        self.m_lSimulationInterval= int(info.SimulationInterval,10)

    def OnPropertyChanged(self,GroupName,PropertyName,PropertyValue):
        if GroupName != OBJECT_PROPERTIES_TITLE:
            return
        elif PropertyName == OBJECT_TYPE_TITLE:
            self.m_strObjectType = PropertyValue
        elif PropertyName == OBJECT_COLOR_TITLE:
            self.m_Color = Colour.fromInt(int(PropertyValue,10))
        elif PropertyName == OBJECT_SIMULATION_PATTERN_TITLE:
            self.m_strSimulationPattern = PropertyValue
        elif PropertyName == OBJECT_SIMULATION_INTERVAL_TITLE:
            self.m_lSimulationInterval = int(PropertyValue,10)


class GraphPoints():

    def __init__(self):
        self.m_Angle = 0.0
        self.m_x = 0.0
        self.m_y = 0.0
        self.m_z = 0.0

class ObjectDemoExperiment():

    def __init__(self,objManager):
        self.m_PlotInfoArray=[]
        self.m_ObjectPattern=ObjectPattern()
        self.m_objManager=objManager

    def LoadAllExperiments(self):
        SessionID = self.m_objManager.m_objAddin.m_lSessionID
        objExperimentTreeView = ExperimentTreeView()
        try:
            objExperimentTreeView.DeleteAllExperiments(SessionID)
            objExperimentTreeView.SetRootNodeName(PY_SAMPLE_EXPERIMENT_TYPE_GROUP_1_PROPERTIES, 1)
            objExperimentTreeView.AddExperiment(SessionID, OBJECT_3D_TREE_ROOT_TITLE,OBJECT_3D_TREE_LEAF_PATTERN_TITLE)
            objExperimentTreeView.Refresh()
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnTreeNodeSelect(self,ExperimentGroup,ExperimentName):
        try:
            self.OnReloadExperiment(ExperimentGroup, ExperimentName)
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnTreeNodeDblClick(self,ExperimentGroup,ExperimentName):
        try:
            if ExperimentGroup == OBJECT_3D_TREE_ROOT_TITLE and ExperimentName == OBJECT_3D_TREE_LEAF_PATTERN_TITLE:
                 self.ShowObjectProperties()
            else:
                self.m_objManager.ResetPropertyGrid()
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnReloadExperiment(self,ExperimentGroup,ExperimentName):
        try:
            if ExperimentGroup == OBJECT_3D_TREE_ROOT_TITLE:
                 self.DrawObject(ExperimentName)
            else:
                pass
        except Exception as ex:
            win32ui.MessageBox(ex)

    def ShowObjectProperties(self):
        objPropertyWindow = PropertyWindow()
        strGroupName = ""
        try:
            objPropertyWindow.RemoveAll()
            strGroupName = OBJECT_PROPERTIES_TITLE
            objPropertyWindow.AddPropertyGroup(strGroupName)
            objPropertyWindow.AddPropertyItemsAsString(strGroupName, OBJECT_TYPE_TITLE, OBJECT_TYPES, self.m_ObjectPattern.m_strObjectType, "Select the Object from the List",False)
            objPropertyWindow.AddColorPropertyItem(strGroupName, OBJECT_COLOR_TITLE,self.m_ObjectPattern.m_Color.toInt(), "Select the Color")
            objPropertyWindow.AddPropertyItemsAsString(strGroupName, OBJECT_SIMULATION_PATTERN_TITLE,OBJECT_PATTERN_TYPES, self.m_ObjectPattern.m_strSimulationPattern, "Select the Simulation Pattern", False)
            strInterval= str(self.m_ObjectPattern.m_lSimulationInterval)
            objPropertyWindow.AddPropertyItemAsString(strGroupName,OBJECT_SIMULATION_INTERVAL_TITLE, strInterval, "Simulation Interval In Milli Seconds")
            objPropertyWindow.EnableHeaderCtrl(False)
            objPropertyWindow.EnableDescriptionArea(True)
            objPropertyWindow.SetVSDotNetLook(True)
            objPropertyWindow.MarkModifiedProperties(True, True)
        except Exception as ex:
            win32ui.MessageBox(ex)
    
    def Serialize(self):
        try:
            return self.m_ObjectPattern.Serialize()
        except Exception as ex:
            win32ui.MessageBox(ex)
            return ExperimentInfo()
       

    def DeSerialize(self,info):
        try:
            return self.m_ObjectPattern.DeSerialize(info)
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnPropertyChanged(self,GroupName, PropertyName,PropertyValue):
        try:
            if GroupName == OBJECT_PROPERTIES_TITLE:
                self.m_ObjectPattern.OnPropertyChanged(GroupName, PropertyName, PropertyValue)
               
            self.DrawScene()
        except Exception as ex:
            win32ui.MessageBox(ex)

    def DrawScene(self):
        try:
            self.OnReloadExperiment(self.m_objManager.m_strExperimentGroup, self.m_objManager.m_strExperimentName)
        except Exception as ex:
            win32ui.MessageBox(ex)

    def DrawObject(self,ExperimentName):
        try:
            if self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_CUBE:
                self.DrawCube()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_BALL:
                self.DrawBall()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_PYRAMID:
                self.DrawPyramid()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_AEROPLANE:
                self.DrawAeroplane()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_CLOCK:
                self.DrawClock()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_PENDULUM:
                self.DrawPendulum()
        except Exception as ex:
            win32ui.MessageBox(ex)


    def StartSimulation(self,ExperimentGroup,ExperimentName):
        if ExperimentGroup == OBJECT_3D_TREE_ROOT_TITLE and ExperimentName == OBJECT_3D_TREE_LEAF_PATTERN_TITLE:
            try:
                self.StartObjectSimulation()
            except Exception as ex:
                 win32ui.MessageBox(ex)
        else:
            pass

    def StartObjectSimulation(self):
            self.m_objManager.SetSimulationStatus(True)
            applicationView = ApplicationView()
            Angle = 0.0
            x = 0.0
            y = 0.0 
            z = 0.0
            i = 0 #Indicate Random Movment after each iteration
            while self.m_objManager.m_bSimulationActive:
                applicationView.BeginGraphicsCommands()
                if self.m_ObjectPattern.m_strSimulationPattern == OBJECT_PATTERN_TYPE_ROTATE:
                    x = 0.1
                    y = 1.0
                    z = 0.1
                elif self.m_ObjectPattern.m_strSimulationPattern == OBJECT_PATTERN_TYPE_RANDOM:
                    if i==0:
                        x = 1.0
                        y = 0.1
                        z = 0.1
                    elif i==1:
                        x = 0.1
                        y = 1.0
                        z = 0.1
                    elif i==2:
                        x = 0.1
                        y = 0.1
                        z = 1.0
                    i=random.randint(0,2)
                if self.m_objManager.m_b3DMode == False:
                    x=0
                    y=0
                applicationView.RotateObject(Angle, x, y, z)
                applicationView.EndGraphicsCommands()
                applicationView.Refresh()
                #Process the Results
                self.OnNextSimulationPoint(Angle, x, y, z)
                Angle = Angle + 5
                if  Angle > 360:
                    self.m_PlotInfoArray.clear()
                    Angle = 0
                time.sleep(self.m_ObjectPattern.m_lSimulationInterval/1000)

    def OnNextSimulationPoint(self,Angle,x,y, z):
        strStatus ="Simulation Points (Angle:{0},X:{1},Y:{2},Z:{3})\n".format(Angle, x, y, z)
                                            
        if self.m_objManager.m_bShowExperimentalParamaters:
            self.m_objManager.AddOperationStatus(strStatus)

        if self.m_objManager.m_bLogSimulationResultsToCSVFile:
            strLog = "Simulation Points (Angle:{0},X:{1},Y:{2},Z:{3})\n".format(Angle, x, y, z)
            self.m_objManager.LogSimulationPoint(strLog)

        if self.m_objManager.m_bDisplayRealTimeGraph:
            self.PlotSimulationPoint(Angle, x, y, z)
    
    def PlotSimulationPoint(self,Angle,x,y,z):
            Point = GraphPoints()
            Point.m_Angle = Angle
            Point.m_x = x
            Point.m_y = y
            Point.m_z = z
            self.m_PlotInfoArray.append(Point)
            strStatus= "Plot Data Points Count ={0}" .format (len(self.m_PlotInfoArray))
            self.m_objManager.SetStatusBarMessage(strStatus)
            self.DisplayObjectDemoGraph()

    def InitializeSimulationGraph(self, ExperimentName):
        
            for point in self.m_PlotInfoArray:
                del point

            self.m_PlotInfoArray.clear()

            applicationChart = ApplicationChart()
            try:
            
                applicationChart.DeleteAllCharts()
                applicationChart.Initialize2dChart(3)

                applicationChart.Set2dGraphInfo(0, "Angle Vs X", "Angle(Degree)","X", True)
                applicationChart.Set2dAxisRange(0, int(EAxisPos.BottomAxis), 0, 365)
                applicationChart.Set2dAxisRange(0, int(EAxisPos.LeftAxis), 0, 2)

                applicationChart.Set2dGraphInfo(1, "Angle Vs Y", "Angle(Degree)","Y",True)
                applicationChart.Set2dAxisRange(1, int(EAxisPos.BottomAxis), 0, 365)
                applicationChart.Set2dAxisRange(1, int(EAxisPos.LeftAxis), 0, 2)

                applicationChart.Set2dGraphInfo(2, "Angle Vs Z", "Angle(Degree)","Z", True)
                applicationChart.Set2dAxisRange(2, int(EAxisPos.BottomAxis), 0, 365)
                applicationChart.Set2dAxisRange(2, int(EAxisPos.LeftAxis), 0, 2)

                applicationChart.ResizeChartWindow()
            
            except:
                    pass


    def DisplayObjectDemoGraph(self):
        try:
            iArraySize = len(self.m_PlotInfoArray)
            if iArraySize <2 or iArraySize % 10 == 0:
                return
            sabX=[[1.0,1.0,1.0] for i in range(0,iArraySize)]
            sabY=[[1.0,1.0,1.0] for i in range(0,iArraySize)]
            sabZ=[[1.0,1.0,1.0] for i in range(0,iArraySize)]

            for i in range(iArraySize):
                try:
                    info=self.m_PlotInfoArray[i]
                    val=info.m_Angle
                    sabX[i][1]=val
                    sabY[i][1]=val
                    sabZ[i][1]=val

                    val=info.m_x
                    sabX[i][2]=val
                    val=info.m_y
                    sabY[i][2]=val
                    val=info.m_z
                    sabZ[i][2]=val
                except  Exception as e:
                    win32ui.MessageBox(str(e))

            saX=VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,sabX)
            saY=VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,sabY)
            saZ=VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,sabZ)
            

            if iArraySize % 5 == 0:
                applicationChart = ApplicationChart()
                applicationChart.Set2dChartData(0, saX)
                applicationChart.Set2dChartData(1, saY)
                applicationChart.Set2dChartData(2, saZ)
            
        except Exception as e:
            win32ui.MessageBox(str(e))
         
    def DrawClock(self):
            #Draw using ApplicationView Interface
            applicationView = ApplicationView()
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255, \
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)
            applicationView.StartNewDisplayList()

            x1 = 0.0
            y1 = 0.0

            segments = 100
            radius = 1.0

            #Drawing Clock main Circle

            applicationView.SetLineWidth(4)
            applicationView.SetColorf(1, 0, 0)
            self.DrawCircle(segments, radius, x1, y1)

            #Drawing Minute Line
            applicationView.SetColorf(1, 1, 0)
            applicationView.SetLineWidth(2)
            applicationView.BeginDraw(int(GL_LINES))
            applicationView.Set2DVertexf(x1, y1)
            applicationView.Set2DVertexf(x1, ((radius / 3.0) * 2.0))
            applicationView.EndDraw()

            #Drawing Hour Line
            applicationView.SetColorf(1, 0, 0)
            applicationView.SetLineWidth(2)
            applicationView.BeginDraw(int(GL_LINES))
            applicationView.Set2DVertexf(x1, y1)
            applicationView.Set2DVertexf((radius / 3.0),(radius / 3.0))
            applicationView.EndDraw()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawCircle(self, segments,radius, sx, sy):
        try:
            openGLView = OpenGLView()
            openGLView.glBegin(GL_LINE_LOOP)
            for i in range(0,segments):
                theta = (2.0 * 3.142 * i / segments) #get the current angle
                x = (radius * math.cos(theta))
                y = (radius * math.sin(theta))
                openGLView.glVertex2f(x + sx, y + sy)
            openGLView.glEnd()
        except Exception as e:
            win32ui.MessageBox(str(e))
                        
    def DrawCube(self):
            applicationView = ApplicationView()
            #We can use all the normal OpenGL API defined in the standard Opengl header file
            radius = 0.34
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255.0,\
               self.m_ObjectPattern.m_Color.G / 255.0, self.m_ObjectPattern.m_Color.B / 255.0,1.0)
            applicationView.StartNewDisplayList()

            #Draw using Native IOpenGLView Interface
            openGLView = OpenGLView()
            openGLView.glBegin(GL_QUAD_STRIP)
            openGLView.glColor3f(1.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, 0.3)
            openGLView.glColor3f(1.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, 0.3)
            openGLView.glColor3f(0.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, -0.3)
            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, -0.3)
            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, -0.3)
            openGLView.glColor3f(0.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, -0.3)
            openGLView.glColor3f(1.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, 0.3)
            openGLView.glEnd()

            openGLView.glBegin(GL_QUADS)
            openGLView.glColor3f(1.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, 0.3)
            openGLView.glColor3f(0.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, -0.3)
            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, -0.3)
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, 0.3)
            openGLView.glColor3f(0.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, -0.3)
            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, -0.3)
            openGLView.glColor3f(1.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, 0.3)

            openGLView.glEnd()

            openGLView.glColor3f(1.0, 1.0, 1.0)
            openGLView.glRasterPos3f(-radius, radius, radius)
            openGLView.glRasterPos3f(-radius, -radius, radius)
            openGLView.glRasterPos3f(radius, radius, radius)
            openGLView.glRasterPos3f(radius, -radius, radius)
            openGLView.glRasterPos3f(radius, radius, -radius)
            openGLView.glRasterPos3f(radius, -radius, -radius)
            openGLView.glRasterPos3f(-radius, radius, -radius)
            openGLView.glRasterPos3f(-radius, -radius, -radius)

            #Set the Inner Sphere Color
            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawPendulum(self):
        applicationView = ApplicationView()
        applicationView.InitializeEnvironment(True)
        applicationView.BeginGraphicsCommands()

        # Set the background color
        applicationView.SetBkgColor(
            self.m_ObjectPattern.m_Color.R / 255.0,
            self.m_ObjectPattern.m_Color.G / 255.0,
            self.m_ObjectPattern.m_Color.B / 255.0,
            1.0
        )
        applicationView.StartNewDisplayList()

        openGLView = OpenGLView()

        # === Geometry constants ===
        blockW = 1.0
        blockH = 0.12
        blockD = 0.3
        blockY = 1.0
        sphereRadius = 0.22
        stringLength = 1.0
        pivotY = blockY
        bobY = pivotY - stringLength

        # === Draw the fixed support block ===
        openGLView.glColor3f(0.5, 0.5, 0.5)
        openGLView.glBegin(GL_QUADS)

        # Top face
        openGLView.glVertex3f(-blockW, blockY + blockH, -blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, -blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, blockD)

        # Bottom face
        openGLView.glVertex3f(-blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, blockD)
        openGLView.glVertex3f(-blockW, blockY, blockD)

        # Sides
        # Side front
        openGLView.glVertex3f(-blockW, blockY, blockD)
        openGLView.glVertex3f(blockW, blockY, blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, blockD)

        # Side back
        openGLView.glVertex3f(-blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, -blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, -blockD)

        # Side left
        openGLView.glVertex3f(-blockW, blockY, -blockD)
        openGLView.glVertex3f(-blockW, blockY, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, -blockD)

        # Side right
        openGLView.glVertex3f(blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, -blockD)

        openGLView.glEnd()

        # === Oscillating part ===
        simType = self.m_ObjectPattern.m_strSimulationPattern
        if simType.lower() == "oscillate":
            openGLView.glPushMatrix()
            openGLView.glTranslatef(0.0, pivotY, 0.0)
            openGLView.glRotatef(self.m_fOscillationAngle, 0.0, 0.0, 1.0)
            openGLView.glTranslatef(0.0, -pivotY, 0.0)

        # Draw the string
        openGLView.glColor3f(0.1, 0.1, 0.1)
        openGLView.glLineWidth(3.0)  # Make the line thicker
        openGLView.glBegin(GL_LINES)
        openGLView.glVertex3f(0.0, pivotY, 0.0)
        openGLView.glVertex3f(0.0, bobY, 0.0)
        openGLView.glEnd()

        # Draw the bob (sphere)
        openGLView.glPushMatrix()
        openGLView.glTranslatef(0.0, bobY, 0.0)
        applicationView.SetColorf(0.8, 0.0, 0.0)
        applicationView.DrawSphere(sphereRadius, 25, 25)
        openGLView.glPopMatrix()

        if simType.lower() == "oscillate":
            openGLView.glPopMatrix()

        applicationView.EndNewDisplayList()
        applicationView.EndGraphicsCommands()
        applicationView.Refresh()


        # === Oscillating part ===
        simType = self.m_ObjectPattern.m_strSimulationPattern
        if simType.lower() == "oscillate":
            openGLView.glPushMatrix()
            openGLView.glTranslatef(0.0, pivotY, 0.0)
            openGLView.glRotatef(self.m_fOscillationAngle, 0.0, 0.0, 1.0)
            openGLView.glTranslatef(0.0, -pivotY, 0.0)

            # Draw String
            openGLView.glColor3f(0.1, 0.1, 0.1)
            openGLView.glLineWidth(2.0)
            openGLView.glBegin(GL_LINES)
            openGLView.glVertex3f(0.0, pivotY, 0.0)
            openGLView.glVertex3f(0.0, bobY, 0.0)
            openGLView.glEnd()

            # Draw Bob (Sphere)
            openGLView.glPushMatrix()
            openGLView.glTranslatef(0.0, bobY, 0.0)
            applicationView.SetColorf(0.8, 0.0, 0.0)
            applicationView.DrawSphere(sphereRadius, 25, 25)
            openGLView.glPopMatrix()

            if simType.lower() == "oscillate":
                openGLView.glPopMatrix()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

            applicationView = ApplicationView()
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

                        #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255,\
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)

            SECTIONS = 25
            RADIUS = 1.0
            applicationView.StartNewDisplayList()
            applicationView.SetColorf(0.0, 0.0, 1.0)
            applicationView.DrawSphere(RADIUS, SECTIONS, SECTIONS)

                        #Draw One more spehere inside it
            applicationView.SetColorf(1.0, 1.0, 1.0)
            applicationView.DrawSphere(RADIUS / 1.5, SECTIONS, SECTIONS)
            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()
    def DrawPyramid(self):

            applicationView = ApplicationView()
            #We can use all the normal OpenGL API defined in the standard Opengl header file
            radius = 0.34
            applicationView.ResetScene()
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255, \
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)
            applicationView.StartNewDisplayList()

            #Draw using Native IOpenGLView Interface
            openGLView = OpenGLView()
            openGLView.glTranslatef(0.01, 0.0, 0.01)
            openGLView.glColor3f(0.0, 0.4, 0.8)

            # We're telling OpenGL that we want to render triangles.
            openGLView.glBegin(GL_TRIANGLES)

            # Each of the pyramid's faces will have 3 vertices.
            # We'll start drawing at the top, then go down to the bottom left,
            # then to the right.

            # When we start our next triangle, we're going to be going back to
            # the top-middle. Imagine drawing a pyramid without ever lifting your
            # pen up.

            # New Triangle - Front
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            # New Triangle - Right
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(1.0, -1.0, -1.0)

            # New Triangle - Back
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, -1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)

            # New Triangle - left
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-1.0, -1.0, 1.0)

            # New Triangle - Bottom 1
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)

            # New Triangle - Bottom 2
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)      # Note: we're starting from the last point
                                                              # of the previous triangle.

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, -1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            openGLView.glEnd()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawAeroplane(self):

            applicationView = ApplicationView()

            #We can use all the normal OpenGL API defined in the standard Opengl header file
            #const float radius = 0.34f

            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255, \
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)
            applicationView.StartNewDisplayList()

            #Draw using Native IopenGLView Interface
            openGLView = OpenGLView()

            openGLView.glTranslatef(0.01, 0.0, 0.01)
            openGLView.glColor3f(0.0, 0.4, 0.8)
            openGLView.glBegin(GL_TRIANGLES)
            openGLView.glVertex3f(0.0, 0.0, 0.001)
            openGLView.glVertex3f(0.0, -0.5, 1.0)
            openGLView.glVertex3f(0.0, 1.0, 0.001)
            openGLView.glEnd()
            openGLView.glColor3f(0.0, 0.3, 0.7)
            openGLView.glBegin(GL_TRIANGLE_STRIP)
            openGLView.glVertex3f(1.0, -0.5, 0.0)
            openGLView.glVertex3f(0.0, 0.0, 0.2)
            openGLView.glVertex3f(0.0, 2.0, 0.0)
            openGLView.glVertex3f(-1.0, -0.5, 0.0)
            openGLView.glEnd()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawBall(self):
        applicationView = ApplicationView()
        applicationView.InitializeEnvironment(True)
        applicationView.BeginGraphicsCommands()

        # Set the Background Color
        applicationView.SetBkgColor(
            self.m_ObjectPattern.m_Color.R / 255.0,
            self.m_ObjectPattern.m_Color.G / 255.0,
            self.m_ObjectPattern.m_Color.B / 255.0,
            1.0
        )
        applicationView.StartNewDisplayList()

        # Draw a sphere
        applicationView.SetColorf(1.0, 0.0, 1.0)  # blue ball
        applicationView.DrawSphere(0.5, 30, 30)

        applicationView.EndNewDisplayList()
        applicationView.EndGraphicsCommands()
        applicationView.Refresh()

=======
import math
from dicttoxml import dicttoxml
import xmltodict
from Constants import *
import win32ui
from EurekaSimLib import *
import random
import time
import math
from enum import IntEnum
from win32com.client import VARIANT
import pythoncom

class EAxisPos(IntEnum):
    LeftAxis = 0
    BottomAxis=1
    RightAxis=2
    TopAxis=3

class Colour:
    def __init__(self,red=0,green=0,blue=0):
        self.R=red
        self.G=green
        self.B=blue

    def setRGB(self,red=0,green=0,blue=0):
        self.R=red
        self.G=green
        self.B=blue

    def toRGB(self,iColor):
        hexColor = '%08x' % iColor
        self.R=int(hexColor[0:2],16)
        self.G=int(hexColor[2:4],16)
        self.B=int(hexColor[4:6],16)

    def toInt(self):
        colourHex = '00%02x%02x%02x' % (self.B,self.G,self.R)
        icolour = int(colourHex,16)
        return icolour
    @staticmethod
    def fromInt(iColor):
        hexColor = '%08x' % iColor
        blue=int(hexColor[2:4],16)
        green=int(hexColor[4:6],16)
        red=int(hexColor[6:8],16)
        return Colour(red,green,blue)


class ExperimentInfo():

    def __init__(self):
        self.RootText =""
        self.ExperimentGroup =""
        self.ExperimentName =""
        self.ObjectType =""
        self.Colour =0
        self.SimulationPattern =""
        self.SimulationInterval =0

    def Serilize(self):
        dicForm = vars(self)
        xml = dicttoxml(dicForm, attr_type=False, custom_root='ExperimentInfo')
        return xml
    def Deserilize(sel,strXML):
        doc = xmltodict.parse(strXML)
        infoDic = doc['ExperimentInfo']
        for k, v in infoDic.items():
            setattr(sel, k, v)

class ObjectPattern:
    def __init__(self):
        self.m_strObjectType = "Cube"
        self.m_Color = Colour(0, 0, 255)
        self.m_strSimulationPattern = "Rotate"
        self.m_lSimulationInterval = 100

    def Serialize(self):
        info = ExperimentInfo()
        info.ObjectType = self.m_strObjectType
        info.Colour = self.m_Color.toInt()
        info.SimulationPattern = self.m_strSimulationPattern
        info.SimulationInterval = self.m_lSimulationInterval
        return info

    def DeSerialize(self,info):
        self.m_strObjectType= info.ObjectType
        self.m_Color = Colour.fromInt(int(info.Colour))
        self.m_strSimulationPattern = info.SimulationPattern
        self.m_lSimulationInterval= int(info.SimulationInterval,10)

    def OnPropertyChanged(self,GroupName,PropertyName,PropertyValue):
        if GroupName != OBJECT_PROPERTIES_TITLE:
            return
        elif PropertyName == OBJECT_TYPE_TITLE:
            self.m_strObjectType = PropertyValue
        elif PropertyName == OBJECT_COLOR_TITLE:
            self.m_Color = Colour.fromInt(int(PropertyValue,10))
        elif PropertyName == OBJECT_SIMULATION_PATTERN_TITLE:
            self.m_strSimulationPattern = PropertyValue
        elif PropertyName == OBJECT_SIMULATION_INTERVAL_TITLE:
            self.m_lSimulationInterval = int(PropertyValue,10)


class GraphPoints():

    def __init__(self):
        self.m_Angle = 0.0
        self.m_x = 0.0
        self.m_y = 0.0
        self.m_z = 0.0

class ObjectDemoExperiment():

    def __init__(self,objManager):
        self.m_PlotInfoArray=[]
        self.m_ObjectPattern=ObjectPattern()
        self.m_objManager=objManager

    def LoadAllExperiments(self):
        SessionID = self.m_objManager.m_objAddin.m_lSessionID
        objExperimentTreeView = ExperimentTreeView()
        try:
            objExperimentTreeView.DeleteAllExperiments(SessionID)
            objExperimentTreeView.SetRootNodeName(PY_SAMPLE_EXPERIMENT_TYPE_GROUP_1_PROPERTIES, 1)
            objExperimentTreeView.AddExperiment(SessionID, OBJECT_3D_TREE_ROOT_TITLE,OBJECT_3D_TREE_LEAF_PATTERN_TITLE)
            objExperimentTreeView.Refresh()
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnTreeNodeSelect(self,ExperimentGroup,ExperimentName):
        try:
            self.OnReloadExperiment(ExperimentGroup, ExperimentName)
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnTreeNodeDblClick(self,ExperimentGroup,ExperimentName):
        try:
            if ExperimentGroup == OBJECT_3D_TREE_ROOT_TITLE and ExperimentName == OBJECT_3D_TREE_LEAF_PATTERN_TITLE:
                 self.ShowObjectProperties()
            else:
                self.m_objManager.ResetPropertyGrid()
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnReloadExperiment(self,ExperimentGroup,ExperimentName):
        try:
            if ExperimentGroup == OBJECT_3D_TREE_ROOT_TITLE:
                 self.DrawObject(ExperimentName)
            else:
                pass
        except Exception as ex:
            win32ui.MessageBox(ex)

    def ShowObjectProperties(self):
        objPropertyWindow = PropertyWindow()
        strGroupName = ""
        try:
            objPropertyWindow.RemoveAll()
            strGroupName = OBJECT_PROPERTIES_TITLE
            objPropertyWindow.AddPropertyGroup(strGroupName)
            objPropertyWindow.AddPropertyItemsAsString(strGroupName, OBJECT_TYPE_TITLE, OBJECT_TYPES, self.m_ObjectPattern.m_strObjectType, "Select the Object from the List",False)
            objPropertyWindow.AddColorPropertyItem(strGroupName, OBJECT_COLOR_TITLE,self.m_ObjectPattern.m_Color.toInt(), "Select the Color")
            objPropertyWindow.AddPropertyItemsAsString(strGroupName, OBJECT_SIMULATION_PATTERN_TITLE,OBJECT_PATTERN_TYPES, self.m_ObjectPattern.m_strSimulationPattern, "Select the Simulation Pattern", False)
            strInterval= str(self.m_ObjectPattern.m_lSimulationInterval)
            objPropertyWindow.AddPropertyItemAsString(strGroupName,OBJECT_SIMULATION_INTERVAL_TITLE, strInterval, "Simulation Interval In Milli Seconds")
            objPropertyWindow.EnableHeaderCtrl(False)
            objPropertyWindow.EnableDescriptionArea(True)
            objPropertyWindow.SetVSDotNetLook(True)
            objPropertyWindow.MarkModifiedProperties(True, True)
        except Exception as ex:
            win32ui.MessageBox(ex)
    
    def Serialize(self):
        try:
            return self.m_ObjectPattern.Serialize()
        except Exception as ex:
            win32ui.MessageBox(ex)
            return ExperimentInfo()
       

    def DeSerialize(self,info):
        try:
            return self.m_ObjectPattern.DeSerialize(info)
        except Exception as ex:
            win32ui.MessageBox(ex)

    def OnPropertyChanged(self,GroupName, PropertyName,PropertyValue):
        try:
            if GroupName == OBJECT_PROPERTIES_TITLE:
                self.m_ObjectPattern.OnPropertyChanged(GroupName, PropertyName, PropertyValue)
               
            self.DrawScene()
        except Exception as ex:
            win32ui.MessageBox(ex)

    def DrawScene(self):
        try:
            self.OnReloadExperiment(self.m_objManager.m_strExperimentGroup, self.m_objManager.m_strExperimentName)
        except Exception as ex:
            win32ui.MessageBox(ex)

    def DrawObject(self,ExperimentName):
        try:
            if self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_CUBE:
                self.DrawCube()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_BALL:
                self.DrawBall()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_PYRAMID:
                self.DrawPyramid()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_AEROPLANE:
                self.DrawAeroplane()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_CLOCK:
                self.DrawClock()
            elif self.m_ObjectPattern.m_strObjectType == OBJECT_TYPE_PENDULUM:
                self.DrawPendulum()
        except Exception as ex:
            win32ui.MessageBox(ex)


    def StartSimulation(self,ExperimentGroup,ExperimentName):
        if ExperimentGroup == OBJECT_3D_TREE_ROOT_TITLE and ExperimentName == OBJECT_3D_TREE_LEAF_PATTERN_TITLE:
            try:
                self.StartObjectSimulation()
            except Exception as ex:
                 win32ui.MessageBox(ex)
        else:
            pass

    def StartObjectSimulation(self):
            self.m_objManager.SetSimulationStatus(True)
            applicationView = ApplicationView()
            Angle = 0.0
            x = 0.0
            y = 0.0 
            z = 0.0
            i = 0 #Indicate Random Movment after each iteration
            while self.m_objManager.m_bSimulationActive:
                applicationView.BeginGraphicsCommands()
                if self.m_ObjectPattern.m_strSimulationPattern == OBJECT_PATTERN_TYPE_ROTATE:
                    x = 0.1
                    y = 1.0
                    z = 0.1
                elif self.m_ObjectPattern.m_strSimulationPattern == OBJECT_PATTERN_TYPE_RANDOM:
                    if i==0:
                        x = 1.0
                        y = 0.1
                        z = 0.1
                    elif i==1:
                        x = 0.1
                        y = 1.0
                        z = 0.1
                    elif i==2:
                        x = 0.1
                        y = 0.1
                        z = 1.0
                    i=random.randint(0,2)
                if self.m_objManager.m_b3DMode == False:
                    x=0
                    y=0
                applicationView.RotateObject(Angle, x, y, z)
                applicationView.EndGraphicsCommands()
                applicationView.Refresh()
                #Process the Results
                self.OnNextSimulationPoint(Angle, x, y, z)
                Angle = Angle + 5
                if  Angle > 360:
                    self.m_PlotInfoArray.clear()
                    Angle = 0
                time.sleep(self.m_ObjectPattern.m_lSimulationInterval/1000)

    def OnNextSimulationPoint(self,Angle,x,y, z):
        strStatus ="Simulation Points (Angle:{0},X:{1},Y:{2},Z:{3})\n".format(Angle, x, y, z)
                                            
        if self.m_objManager.m_bShowExperimentalParamaters:
            self.m_objManager.AddOperationStatus(strStatus)

        if self.m_objManager.m_bLogSimulationResultsToCSVFile:
            strLog = "Simulation Points (Angle:{0},X:{1},Y:{2},Z:{3})\n".format(Angle, x, y, z)
            self.m_objManager.LogSimulationPoint(strLog)

        if self.m_objManager.m_bDisplayRealTimeGraph:
            self.PlotSimulationPoint(Angle, x, y, z)
    
    def PlotSimulationPoint(self,Angle,x,y,z):
            Point = GraphPoints()
            Point.m_Angle = Angle
            Point.m_x = x
            Point.m_y = y
            Point.m_z = z
            self.m_PlotInfoArray.append(Point)
            strStatus= "Plot Data Points Count ={0}" .format (len(self.m_PlotInfoArray))
            self.m_objManager.SetStatusBarMessage(strStatus)
            self.DisplayObjectDemoGraph()

    def InitializeSimulationGraph(self, ExperimentName):
        
            for point in self.m_PlotInfoArray:
                del point

            self.m_PlotInfoArray.clear()

            applicationChart = ApplicationChart()
            try:
            
                applicationChart.DeleteAllCharts()
                applicationChart.Initialize2dChart(3)

                applicationChart.Set2dGraphInfo(0, "Angle Vs X", "Angle(Degree)","X", True)
                applicationChart.Set2dAxisRange(0, int(EAxisPos.BottomAxis), 0, 365)
                applicationChart.Set2dAxisRange(0, int(EAxisPos.LeftAxis), 0, 2)

                applicationChart.Set2dGraphInfo(1, "Angle Vs Y", "Angle(Degree)","Y",True)
                applicationChart.Set2dAxisRange(1, int(EAxisPos.BottomAxis), 0, 365)
                applicationChart.Set2dAxisRange(1, int(EAxisPos.LeftAxis), 0, 2)

                applicationChart.Set2dGraphInfo(2, "Angle Vs Z", "Angle(Degree)","Z", True)
                applicationChart.Set2dAxisRange(2, int(EAxisPos.BottomAxis), 0, 365)
                applicationChart.Set2dAxisRange(2, int(EAxisPos.LeftAxis), 0, 2)

                applicationChart.ResizeChartWindow()
            
            except:
                    pass


    def DisplayObjectDemoGraph(self):
        try:
            iArraySize = len(self.m_PlotInfoArray)
            if iArraySize <2 or iArraySize % 10 == 0:
                return
            sabX=[[1.0,1.0,1.0] for i in range(0,iArraySize)]
            sabY=[[1.0,1.0,1.0] for i in range(0,iArraySize)]
            sabZ=[[1.0,1.0,1.0] for i in range(0,iArraySize)]

            for i in range(iArraySize):
                try:
                    info=self.m_PlotInfoArray[i]
                    val=info.m_Angle
                    sabX[i][1]=val
                    sabY[i][1]=val
                    sabZ[i][1]=val

                    val=info.m_x
                    sabX[i][2]=val
                    val=info.m_y
                    sabY[i][2]=val
                    val=info.m_z
                    sabZ[i][2]=val
                except  Exception as e:
                    win32ui.MessageBox(str(e))

            saX=VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,sabX)
            saY=VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,sabY)
            saZ=VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,sabZ)
            

            if iArraySize % 5 == 0:
                applicationChart = ApplicationChart()
                applicationChart.Set2dChartData(0, saX)
                applicationChart.Set2dChartData(1, saY)
                applicationChart.Set2dChartData(2, saZ)
            
        except Exception as e:
            win32ui.MessageBox(str(e))
         
    def DrawClock(self):
            #Draw using ApplicationView Interface
            applicationView = ApplicationView()
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255, \
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)
            applicationView.StartNewDisplayList()

            x1 = 0.0
            y1 = 0.0

            segments = 100
            radius = 1.0

            #Drawing Clock main Circle

            applicationView.SetLineWidth(4)
            applicationView.SetColorf(1, 0, 0)
            self.DrawCircle(segments, radius, x1, y1)

            #Drawing Minute Line
            applicationView.SetColorf(1, 1, 0)
            applicationView.SetLineWidth(2)
            applicationView.BeginDraw(int(GL_LINES))
            applicationView.Set2DVertexf(x1, y1)
            applicationView.Set2DVertexf(x1, ((radius / 3.0) * 2.0))
            applicationView.EndDraw()

            #Drawing Hour Line
            applicationView.SetColorf(1, 0, 0)
            applicationView.SetLineWidth(2)
            applicationView.BeginDraw(int(GL_LINES))
            applicationView.Set2DVertexf(x1, y1)
            applicationView.Set2DVertexf((radius / 3.0),(radius / 3.0))
            applicationView.EndDraw()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawCircle(self, segments,radius, sx, sy):
        try:
            openGLView = OpenGLView()
            openGLView.glBegin(GL_LINE_LOOP)
            for i in range(0,segments):
                theta = (2.0 * 3.142 * i / segments) #get the current angle
                x = (radius * math.cos(theta))
                y = (radius * math.sin(theta))
                openGLView.glVertex2f(x + sx, y + sy)
            openGLView.glEnd()
        except Exception as e:
            win32ui.MessageBox(str(e))
                        
    def DrawCube(self):
            applicationView = ApplicationView()
            #We can use all the normal OpenGL API defined in the standard Opengl header file
            radius = 0.34
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255.0,\
               self.m_ObjectPattern.m_Color.G / 255.0, self.m_ObjectPattern.m_Color.B / 255.0,1.0)
            applicationView.StartNewDisplayList()

            #Draw using Native IOpenGLView Interface
            openGLView = OpenGLView()
            openGLView.glBegin(GL_QUAD_STRIP)
            openGLView.glColor3f(1.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, 0.3)
            openGLView.glColor3f(1.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, 0.3)
            openGLView.glColor3f(0.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, -0.3)
            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, -0.3)
            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, -0.3)
            openGLView.glColor3f(0.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, -0.3)
            openGLView.glColor3f(1.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, 0.3)
            openGLView.glEnd()

            openGLView.glBegin(GL_QUADS)
            openGLView.glColor3f(1.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, 0.3)
            openGLView.glColor3f(1.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, 0.3)
            openGLView.glColor3f(0.0, 1.0, 1.0)
            openGLView.glVertex3f(0.3, 0.3, -0.3)
            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-0.3, 0.3, -0.3)
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, 0.3)
            openGLView.glColor3f(0.0, 0.0, 0.0)
            openGLView.glVertex3f(-0.3, -0.3, -0.3)
            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, -0.3)
            openGLView.glColor3f(1.0, 1.0, 0.0)
            openGLView.glVertex3f(0.3, -0.3, 0.3)

            openGLView.glEnd()

            openGLView.glColor3f(1.0, 1.0, 1.0)
            openGLView.glRasterPos3f(-radius, radius, radius)
            openGLView.glRasterPos3f(-radius, -radius, radius)
            openGLView.glRasterPos3f(radius, radius, radius)
            openGLView.glRasterPos3f(radius, -radius, radius)
            openGLView.glRasterPos3f(radius, radius, -radius)
            openGLView.glRasterPos3f(radius, -radius, -radius)
            openGLView.glRasterPos3f(-radius, radius, -radius)
            openGLView.glRasterPos3f(-radius, -radius, -radius)

            #Set the Inner Sphere Color
            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawPendulum(self):
        applicationView = ApplicationView()
        applicationView.InitializeEnvironment(True)
        applicationView.BeginGraphicsCommands()

        # Set the background color
        applicationView.SetBkgColor(
            self.m_ObjectPattern.m_Color.R / 255.0,
            self.m_ObjectPattern.m_Color.G / 255.0,
            self.m_ObjectPattern.m_Color.B / 255.0,
            1.0
        )
        applicationView.StartNewDisplayList()

        openGLView = OpenGLView()

        # === Geometry constants ===
        blockW = 1.0
        blockH = 0.12
        blockD = 0.3
        blockY = 1.0
        sphereRadius = 0.22
        stringLength = 1.0
        pivotY = blockY
        bobY = pivotY - stringLength

        # === Draw the fixed support block ===
        openGLView.glColor3f(0.5, 0.5, 0.5)
        openGLView.glBegin(GL_QUADS)

        # Top face
        openGLView.glVertex3f(-blockW, blockY + blockH, -blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, -blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, blockD)

        # Bottom face
        openGLView.glVertex3f(-blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, blockD)
        openGLView.glVertex3f(-blockW, blockY, blockD)

        # Sides
        # Side front
        openGLView.glVertex3f(-blockW, blockY, blockD)
        openGLView.glVertex3f(blockW, blockY, blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, blockD)

        # Side back
        openGLView.glVertex3f(-blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, -blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, -blockD)

        # Side left
        openGLView.glVertex3f(-blockW, blockY, -blockD)
        openGLView.glVertex3f(-blockW, blockY, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(-blockW, blockY + blockH, -blockD)

        # Side right
        openGLView.glVertex3f(blockW, blockY, -blockD)
        openGLView.glVertex3f(blockW, blockY, blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, blockD)
        openGLView.glVertex3f(blockW, blockY + blockH, -blockD)

        openGLView.glEnd()

        # === Oscillating part ===
        simType = self.m_ObjectPattern.m_strSimulationPattern
        if simType.lower() == "oscillate":
            openGLView.glPushMatrix()
            openGLView.glTranslatef(0.0, pivotY, 0.0)
            openGLView.glRotatef(self.m_fOscillationAngle, 0.0, 0.0, 1.0)
            openGLView.glTranslatef(0.0, -pivotY, 0.0)

        # Draw the string
        openGLView.glColor3f(0.1, 0.1, 0.1)
        openGLView.glLineWidth(3.0)  # Make the line thicker
        openGLView.glBegin(GL_LINES)
        openGLView.glVertex3f(0.0, pivotY, 0.0)
        openGLView.glVertex3f(0.0, bobY, 0.0)
        openGLView.glEnd()

        # Draw the bob (sphere)
        openGLView.glPushMatrix()
        openGLView.glTranslatef(0.0, bobY, 0.0)
        applicationView.SetColorf(0.8, 0.0, 0.0)
        applicationView.DrawSphere(sphereRadius, 25, 25)
        openGLView.glPopMatrix()

        if simType.lower() == "oscillate":
            openGLView.glPopMatrix()

        applicationView.EndNewDisplayList()
        applicationView.EndGraphicsCommands()
        applicationView.Refresh()


        # === Oscillating part ===
        simType = self.m_ObjectPattern.m_strSimulationPattern
        if simType.lower() == "oscillate":
            openGLView.glPushMatrix()
            openGLView.glTranslatef(0.0, pivotY, 0.0)
            openGLView.glRotatef(self.m_fOscillationAngle, 0.0, 0.0, 1.0)
            openGLView.glTranslatef(0.0, -pivotY, 0.0)

            # Draw String
            openGLView.glColor3f(0.1, 0.1, 0.1)
            openGLView.glLineWidth(2.0)
            openGLView.glBegin(GL_LINES)
            openGLView.glVertex3f(0.0, pivotY, 0.0)
            openGLView.glVertex3f(0.0, bobY, 0.0)
            openGLView.glEnd()

            # Draw Bob (Sphere)
            openGLView.glPushMatrix()
            openGLView.glTranslatef(0.0, bobY, 0.0)
            applicationView.SetColorf(0.8, 0.0, 0.0)
            applicationView.DrawSphere(sphereRadius, 25, 25)
            openGLView.glPopMatrix()

            if simType.lower() == "oscillate":
                openGLView.glPopMatrix()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

            applicationView = ApplicationView()
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

                        #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255,\
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)

            SECTIONS = 25
            RADIUS = 1.0
            applicationView.StartNewDisplayList()
            applicationView.SetColorf(0.0, 0.0, 1.0)
            applicationView.DrawSphere(RADIUS, SECTIONS, SECTIONS)

                        #Draw One more spehere inside it
            applicationView.SetColorf(1.0, 1.0, 1.0)
            applicationView.DrawSphere(RADIUS / 1.5, SECTIONS, SECTIONS)
            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()
    def DrawPyramid(self):

            applicationView = ApplicationView()
            #We can use all the normal OpenGL API defined in the standard Opengl header file
            radius = 0.34
            applicationView.ResetScene()
            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255, \
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)
            applicationView.StartNewDisplayList()

            #Draw using Native IOpenGLView Interface
            openGLView = OpenGLView()
            openGLView.glTranslatef(0.01, 0.0, 0.01)
            openGLView.glColor3f(0.0, 0.4, 0.8)

            # We're telling OpenGL that we want to render triangles.
            openGLView.glBegin(GL_TRIANGLES)

            # Each of the pyramid's faces will have 3 vertices.
            # We'll start drawing at the top, then go down to the bottom left,
            # then to the right.

            # When we start our next triangle, we're going to be going back to
            # the top-middle. Imagine drawing a pyramid without ever lifting your
            # pen up.

            # New Triangle - Front
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            # New Triangle - Right
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(1.0, -1.0, -1.0)

            # New Triangle - Back
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, -1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)

            # New Triangle - left
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(0.0, 1.0, 0.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-1.0, -1.0, 1.0)

            # New Triangle - Bottom 1
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)

            # New Triangle - Bottom 2
            openGLView.glColor3f(1.0, 0.0, 0.0)
            openGLView.glVertex3f(-1.0, -1.0, -1.0)      # Note: we're starting from the last point
                                                              # of the previous triangle.

            openGLView.glColor3f(0.0, 1.0, 0.0)
            openGLView.glVertex3f(1.0, -1.0, -1.0)

            openGLView.glColor3f(0.0, 0.0, 1.0)
            openGLView.glVertex3f(1.0, -1.0, 1.0)

            openGLView.glEnd()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()

    def DrawAeroplane(self):

            applicationView = ApplicationView()

            #We can use all the normal OpenGL API defined in the standard Opengl header file
            #const float radius = 0.34f

            applicationView.InitializeEnvironment(True)
            applicationView.BeginGraphicsCommands()

            #Set the Background Color
            applicationView.SetBkgColor(self.m_ObjectPattern.m_Color.R / 255, \
                                        self.m_ObjectPattern.m_Color.G / 255,\
                                        self.m_ObjectPattern.m_Color.B / 255, 1)
            applicationView.StartNewDisplayList()

            #Draw using Native IopenGLView Interface
            openGLView = OpenGLView()

            openGLView.glTranslatef(0.01, 0.0, 0.01)
            openGLView.glColor3f(0.0, 0.4, 0.8)
            openGLView.glBegin(GL_TRIANGLES)
            openGLView.glVertex3f(0.0, 0.0, 0.001)
            openGLView.glVertex3f(0.0, -0.5, 1.0)
            openGLView.glVertex3f(0.0, 1.0, 0.001)
            openGLView.glEnd()
            openGLView.glColor3f(0.0, 0.3, 0.7)
            openGLView.glBegin(GL_TRIANGLE_STRIP)
            openGLView.glVertex3f(1.0, -0.5, 0.0)
            openGLView.glVertex3f(0.0, 0.0, 0.2)
            openGLView.glVertex3f(0.0, 2.0, 0.0)
            openGLView.glVertex3f(-1.0, -0.5, 0.0)
            openGLView.glEnd()

            applicationView.EndNewDisplayList()
            applicationView.EndGraphicsCommands()
            applicationView.Refresh()


>>>>>>> a62bc40d1fc44dc9aa3c2f1df1bd9a8ca9d1bb88
