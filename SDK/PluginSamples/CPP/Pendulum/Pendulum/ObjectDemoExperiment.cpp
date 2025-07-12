// PlusTwoPhysicsExperiment.cpp : implementation file
//

#include "stdafx.h"
#include "ObjectDemoExperiment.h"
#include "PendulumSimulation.h"
#include "AddinSimulationManager.h"
#include "PropSliderCtrl.h"

// CPlusTwoPhysicsExperiment
using namespace ATL;


CObjectDemoExperiment::CObjectDemoExperiment(CAddinSimulationManager* pManager)
{
	m_pManager = pManager;
	m_fOscillationAngle = 0.0f;

}

CObjectDemoExperiment::~CObjectDemoExperiment()
{
}

void CObjectDemoExperiment::LoadAllExperiments()
{
	CComPtr<IExperimentTreeView> ExperimentTreeView;
	HRESULT HR = ExperimentTreeView.CoCreateInstance(CLSID_ExperimentTreeView);
	if (FAILED(HR))
	{
		return;
	}
	long SessionID = m_pManager->m_pAddin->m_lSessionID;
	ExperimentTreeView->DeleteAllExperiments(SessionID);
	ExperimentTreeView->SetRootNodeName(CString(CPP_SAMPLE_EXPERIMENT_TYPE_GROUP_1_PROPERTIES).AllocSysString(), TRUE);

#if FALSE //Will Implement this Later
	ExperimentTreeView->AddExperiment(SessionID, CString(MECHANICS_TREE_ROOT_TITLE).AllocSysString(), CString(MECHANICS_TREE_SIMPLE_PENDULUM_TITLE).AllocSysString());
	ExperimentTreeView->AddExperiment(SessionID, CString(MECHANICS_TREE_ROOT_TITLE).AllocSysString(), CString(MECHANICS_TREE_PROJECTILE_MOTION_TITLE).AllocSysString());
	ExperimentTreeView->AddExperiment(SessionID, CString(MECHANICS_TREE_ROOT_TITLE).AllocSysString(), CString(MECHANICS_TREE_PLANETORY_MOTION_TITLE).AllocSysString());
#endif //Will Implement this Later

	ExperimentTreeView->AddExperiment(SessionID, CString(OBJECT_3D_TREE_ROOT_TITLE).AllocSysString(), CString(OBJECT_3D_TREE_LEAF_PATTERN_TITLE).AllocSysString());

	ExperimentTreeView->Refresh();


}

void CObjectDemoExperiment::OnTreeNodeSelect(BSTR ExperimentGroup, BSTR ExperimentName)
{
	OnReloadExperiment(ExperimentGroup, ExperimentName);
}
void CObjectDemoExperiment::OnTreeNodeDblClick(BSTR ExperimentGroup, BSTR ExperimentName)
{
	if (CString(ExperimentGroup) == OBJECT_3D_TREE_ROOT_TITLE && CString(ExperimentName) == OBJECT_3D_TREE_LEAF_PATTERN_TITLE)
	{
		ShowObjectProperties();
	}
	else
	{
		m_pManager->ResetPropertyGrid();
	}
}
void CObjectDemoExperiment::OnReloadExperiment(BSTR ExperimentGroup, BSTR ExperimentName)
{
	if (CString(ExperimentGroup) == OBJECT_3D_TREE_ROOT_TITLE)
	{
		DrawObject(ExperimentName);
	}
	else
	{
		
	}

}



// CPlusTwoPhysicsExperiment member functions


void CObjectDemoExperiment::ShowObjectProperties()
{
#if TRUE
	CComPtr<IPropertyWindow> PropertyWindow;
	HRESULT HR = PropertyWindow.CoCreateInstance(CLSID_PropertyWindow);
	CString strGroupName = _T("");
	if (SUCCEEDED(HR))
	{
		PropertyWindow->RemoveAll();
		strGroupName = OBJECT_PROPERTIES_TITLE;
		PropertyWindow->AddPropertyGroup(strGroupName.AllocSysString());
		PropertyWindow->AddPropertyItemsAsString(strGroupName.AllocSysString(), OBJECT_TYPE_TITLE, OBJECT_TYPES, m_ObjectPattern.m_strObjectType.AllocSysString(), _T("Select the Object from the List"), FALSE);
		PropertyWindow->AddColorPropertyItem(strGroupName.AllocSysString(), OBJECT_COLOR_TITLE, m_ObjectPattern.m_Color, _T("Select the Color"));
		PropertyWindow->AddPropertyItemsAsString(strGroupName.AllocSysString(), OBJECT_SIMULATION_PATTERN_TITLE, OBJECT_PATTERN_TYPES, m_ObjectPattern.m_strSimulationPattern.AllocSysString(), _T("Select the Simulation Pattern"), FALSE);
		CString strInterval;
		strInterval.Format(_T("%d"), m_ObjectPattern.m_lSimulationInterval);
		PropertyWindow->AddPropertyItemAsString(strGroupName.AllocSysString(), OBJECT_SIMULATION_INTERVAL_TITLE, strInterval.AllocSysString(), _T("Simulation Interval In Milli Seconds"));


		PropertyWindow->EnableHeaderCtrl(FALSE);
		PropertyWindow->EnableDescriptionArea(TRUE);
		PropertyWindow->SetVSDotNetLook(TRUE);
		PropertyWindow->MarkModifiedProperties(TRUE, TRUE);

	}
#else //This shows all the property Options // But some methods has Bugs 
	CComPtr<IPropertyWindow> PropertyWindow;
	HRESULT HR = PropertyWindow.CoCreateInstance(CLSID_PropertyWindow);
	CString strGroupName = _T("");
	if (SUCCEEDED(HR))
	{
		PropertyWindow->RemoveAll();
		strGroupName = _T("Custom Group");
		PropertyWindow->AddPropertyGroup(strGroupName.AllocSysString());
		PropertyWindow->AddFilePathItem(strGroupName.AllocSysString(), _T("File Path"), _T("C:\\Test\\"), TRUE, _T("Icon Files(*.ico)|*.ico|All Files(*.*)|*.*||"), _T("ico"), _T("Select the File Path"));
		PropertyWindow->AddFilePathItem(strGroupName.AllocSysString(), _T("Folder Path"), _T("D:\\Test\\"), FALSE, _T(""), _T(""), _T("Select the Folder Path"));
		PropertyWindow->AddColorPropertyItem(strGroupName.AllocSysString(), _T("Select Color"), RGB(255, 0, 0), _T("Select the Color"));

		VARIANT DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4;
		DefaultValue.vt = VT_BSTR;
		DefaultValue.bstrVal = _T("C:\\");
		AddParam1.vt = VT_BSTR;
		AddParam2.vt = VT_BSTR;
		AddParam3.vt = VT_BSTR;
		AddParam4.vt = VT_BSTR;

		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1"), _T("Place"), _T("Enter Your Place"), NormalEdit, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);
		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1,Group 2"), _T("Name"), _T("Enter Your Name"), NormalEdit, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);
		DefaultValue.bstrVal = _T("C:\\test.txt");
		AddParam1.bstrVal = _T("Icon Files(*.ico)|*.ico|All Files(*.*)|*.*||");
		AddParam2.bstrVal = _T("ico");
		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1"), _T("File Path"), _T("Enter Your File Path"), FilePathEdit, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);
		DefaultValue.bstrVal = _T("C:\\");
		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1,Group 2"), _T("Folder Path"), _T("Enter Folder Path"), FolderPathEdit, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);
		DefaultValue.vt = VT_UI4;
		DefaultValue.llVal = RGB(0, 255, 0);
		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1"), _T("Default Color"), _T("Enter Your File Path"), ColorEdit, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);

		DefaultValue.vt = VT_BSTR;
		DefaultValue.bstrVal = _T("Petrol");
		AddParam1.vt = VT_BSTR;
		AddParam1.bstrVal = _T("Diesel,Gas,Petrol,Electric");
		AddParam2.vt = VT_I4;
		AddParam2.llVal = FALSE;
		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1,Group 2"), _T("Select Engine"), _T("Select Your Engines"), ComboEdit, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);
		AddParam2.llVal = TRUE;
		PropertyWindow->AddHierarchyItem(_T("New Group"), _T("Sub Item Group1"), _T("Select Engine"), _T("Select The latest Engines"), ComboReadOnly, DefaultValue, AddParam1, AddParam2, AddParam3, AddParam4);

		CSliderProp* pProp = new CSliderProp(_T("Range Values"), 10, _T("Select the Range Values"));
		VARIANT VarControl;
		VarControl.vt = VT_BYREF;
		VarControl.byref = pProp;
		PropertyWindow->AddCustomPropertyItem(_T("New Group"), VarControl);


		PropertyWindow->EnableHeaderCtrl(FALSE);
		PropertyWindow->EnableDescriptionArea(TRUE);
		PropertyWindow->SetVSDotNetLook(TRUE);
		PropertyWindow->MarkModifiedProperties(TRUE, TRUE);


	}
	//This section demonstrates Other property Controls which is present in this Framework
#endif
	
}

void CObjectDemoExperiment::Serialize(CArchive& ar)
{
	if (ar.IsStoring())
	{
		m_ObjectPattern.Serialize(ar);
	}
	else
	{
		m_ObjectPattern.Serialize(ar);
	}
}

void CObjectDemoExperiment::OnPropertyChanged(BSTR GroupName, BSTR PropertyName, BSTR PropertyValue)
{
	if (CString(GroupName) == OBJECT_PROPERTIES_TITLE)
	{
		m_ObjectPattern.OnPropertyChanged(GroupName, PropertyName, PropertyValue);
	}
	DrawScene();
}

void CObjectDemoExperiment::DrawScene()
{
	OnReloadExperiment(m_pManager->m_strExperimentGroup.AllocSysString(), m_pManager->m_strExperimentName.AllocSysString());

	CComPtr<IApplicationView> ApplicationView;
	if (SUCCEEDED(ApplicationView.CoCreateInstance(CLSID_ApplicationView)))
	{
		ApplicationView->Refresh();  // force refresh after drawing
	}
}


void CObjectDemoExperiment::DrawObject(CString ExperimentName)
{
	if (m_ObjectPattern.m_strObjectType == OBJECT_TYPE_PENDULUM)
	{
		DrawPendulum();
	}

}


void CObjectDemoExperiment::DrawBall()
{
	//Draw using ApplicationView Interface
	CComPtr<IApplicationView> ApplicationView;
	HRESULT HR = ApplicationView.CoCreateInstance(CLSID_ApplicationView);
	if (FAILED(HR))
	{
		return;
	}

	ApplicationView->InitializeEnvironment(TRUE);
	ApplicationView->BeginGraphicsCommands();

	//Set the Background Color
	ApplicationView->SetBkgColor(GetRValue(m_ObjectPattern.m_Color) / (float)255, GetGValue(m_ObjectPattern.m_Color) / (float)255,
		GetBValue(m_ObjectPattern.m_Color) / (float)255, 1);

	int SECTIONS = 25;
	double RADIUS = 1.0;
	
	HR = ApplicationView->StartNewDisplayList();
	if (HR == E_FAIL)
	{
		return;
	}

	ApplicationView->SetColorf(0.0f, 0.0f, 1.0f);
	
	ApplicationView->DrawSphere(RADIUS, SECTIONS, SECTIONS);
	//Draw One more spehere inside it
	
	ApplicationView->SetColorf(1.0f, 1.0f, 1.0f);

	ApplicationView->DrawSphere(RADIUS/1.5, SECTIONS, SECTIONS);

	ApplicationView->EndNewDisplayList();
	ApplicationView->EndGraphicsCommands();
	ApplicationView->Refresh();
}


#include <gl/GL.h>
#include <gl/GLU.h>

void CObjectDemoExperiment::DrawPendulum()
{
	CComPtr<IApplicationView> ApplicationView;
	if (FAILED(ApplicationView.CoCreateInstance(CLSID_ApplicationView))) return;

	ApplicationView->InitializeEnvironment(TRUE);
	ApplicationView->BeginGraphicsCommands();

	ApplicationView->SetBkgColor(
		GetRValue(m_ObjectPattern.m_Color) / 255.0f,
		GetGValue(m_ObjectPattern.m_Color) / 255.0f,
		GetBValue(m_ObjectPattern.m_Color) / 255.0f,
		1.0f
	);

	if (FAILED(ApplicationView->StartNewDisplayList())) return;

	CComPtr<IOpenGLView> GL;
	if (FAILED(GL.CoCreateInstance(CLSID_OpenGLView))) return;

	// === Geometry constants ===
	float blockW = 1.0f, blockH = 0.12f, blockD = 0.3f;
	float blockY = 1.0f;
	float sphereRadius = 0.22f;
	float stringLength = 1.0f;
	float pivotY = blockY;  // top of the string
	float bobY = pivotY - stringLength;

	// Draw fixed Cuboid (support)
	GL->glColor3f(0.5f, 0.5f, 0.5f);
	GL->glBegin(GL_QUADS);
	// top face
	GL->glVertex3f(-blockW, blockY + blockH, -blockD); GL->glVertex3f(blockW, blockY + blockH, -blockD);
	GL->glVertex3f(blockW, blockY + blockH, blockD); GL->glVertex3f(-blockW, blockY + blockH, blockD);
	// bottom face
	GL->glVertex3f(-blockW, blockY, -blockD); GL->glVertex3f(blockW, blockY, -blockD);
	GL->glVertex3f(blockW, blockY, blockD); GL->glVertex3f(-blockW, blockY, blockD);
	// sides
	GL->glVertex3f(-blockW, blockY, blockD); GL->glVertex3f(blockW, blockY, blockD);
	GL->glVertex3f(blockW, blockY + blockH, blockD); GL->glVertex3f(-blockW, blockY + blockH, blockD);

	GL->glVertex3f(-blockW, blockY, -blockD); GL->glVertex3f(blockW, blockY, -blockD);
	GL->glVertex3f(blockW, blockY + blockH, -blockD); GL->glVertex3f(-blockW, blockY + blockH, -blockD);

	GL->glVertex3f(-blockW, blockY, -blockD); GL->glVertex3f(-blockW, blockY, blockD);
	GL->glVertex3f(-blockW, blockY + blockH, blockD); GL->glVertex3f(-blockW, blockY + blockH, -blockD);

	GL->glVertex3f(blockW, blockY, -blockD); GL->glVertex3f(blockW, blockY, blockD);
	GL->glVertex3f(blockW, blockY + blockH, blockD); GL->glVertex3f(blockW, blockY + blockH, -blockD);
	GL->glEnd();

	// ==== Oscillating part (string + bob) ====
	CString simType = m_ObjectPattern.m_strSimulationPattern;
	if (simType.CompareNoCase(_T("Oscillate")) == 0)
	{
		GL->glPushMatrix();
		// Rotate around pivot point at top center
		GL->glTranslatef(0.0f, pivotY, 0.0f);
		GL->glRotatef(m_fOscillationAngle, 0.0f, 0.0f, 1.0f);
		GL->glTranslatef(0.0f, -pivotY, 0.0f);
	}

	// Draw String
	GL->glColor3f(0.1f, 0.1f, 0.1f);
	GL->glLineWidth(2.0f);
	GL->glBegin(GL_LINES);
	GL->glVertex3f(0.0f, pivotY, 0.0f);
	GL->glVertex3f(0.0f, bobY, 0.0f);
	GL->glEnd();

	// Draw Sphere (Bob)
	GL->glPushMatrix();
	GL->glTranslatef(0.0f, bobY, 0.0f);
	ApplicationView->SetColorf(0.8f, 0.0f, 0.0f);
	ApplicationView->DrawSphere(sphereRadius, 25, 25);
	GL->glPopMatrix();

	if (simType.CompareNoCase(_T("Oscillate")) == 0)
	{
		GL->glPopMatrix(); // Undo swing transformation
	}

	ApplicationView->EndNewDisplayList();
	ApplicationView->EndGraphicsCommands();
	ApplicationView->Refresh();
}


void CObjectDemoExperiment::StartSimulation(BSTR ExperimentGroup, BSTR ExperimentName)
{

	if (CString(ExperimentGroup) == OBJECT_3D_TREE_ROOT_TITLE && CString(ExperimentName) == OBJECT_3D_TREE_LEAF_PATTERN_TITLE)
	{
		StartObjectSimulation();
	}
	else
	{

	}
}

void CObjectDemoExperiment::StartObjectSimulation()
{
	m_pManager->SetSimulationStatus(TRUE);

	CComPtr<IApplicationView> ApplicationView;
	HRESULT HR = ApplicationView.CoCreateInstance(CLSID_ApplicationView);
	if (FAILED(HR)) return;

	CString simType = m_ObjectPattern.m_strSimulationPattern;
	float Angle = 0.0f, x = 0.0f, y = 0.0f, z = 0.0f;
	int i = 0;
	float time = 0.0f;
	float timeStep = 0.05f;
	float amplitude = 30.0f;  // degrees
	float frequency = 1.5f;   // oscillations per second

	while (m_pManager->m_bSimulationActive)
	{
		ApplicationView->BeginGraphicsCommands();

		if (simType.CompareNoCase(_T("Rotate")) == 0)
		{
			x = 0.0f; y = 1.0f; z = 0.0f;
			Angle += 5.0f;
			if (Angle > 360.0f) Angle = 0.0f;
			ApplicationView->RotateObject(Angle, x, y, z);
		}
		else if (simType.CompareNoCase(_T("Random Movement")) == 0)
		{
			switch (i)
			{
			case 0: x = 1.0f; y = 0.1f; z = 0.1f; break;
			case 1: x = 0.1f; y = 1.0f; z = 0.1f; break;
			case 2: x = 0.1f; y = 0.1f; z = 1.0f; break;
			}
			i = rand() % 3;
			Angle += 5.0f;
			if (Angle > 360.0f) Angle = 0.0f;
			ApplicationView->RotateObject(Angle, x, y, z);
		}
		else if (simType.CompareNoCase(_T("Oscillate")) == 0)
		{
			m_fOscillationAngle = amplitude * sinf(2.0f * 3.14159f * frequency * time); // use radians
			time += timeStep;

			DrawScene();  // Redraw with new angle
		}

		ApplicationView->EndGraphicsCommands();
		ApplicationView->Refresh();

		OnNextSimulationPoint(Angle, x, y, z);

		Sleep(30);  // Added for smoother animation during testing
					// Sleep(m_ObjectPattern.m_lSimulationInterval);  // original (you can revert to this later)
	}
}




void CObjectDemoExperiment::OnNextSimulationPoint(float Angle, float x, float y, float z)
{
	CString strStatus;
	strStatus.Format(_T("Simulation Points (Angle:%.3f,X:%.3f,Y:%.3f,Z:%.3f)\n"), Angle,x,y,z);

	if (m_pManager->m_bShowExperimentalParamaters)
	{
		m_pManager->AddOperationStatus(strStatus);
	}

	if (m_pManager->m_bLogSimulationResultsToCSVFile)
	{
		CString strLog;
		strLog.Format(_T("%.3f,%.3f,%.3f,%.3f\n"), Angle, x, y, z);
		m_pManager->LogSimulationPoint(strLog);
	}

	if (m_pManager->m_bDisplayRealTimeGraph)
	{
		PlotSimulationPoint(Angle,x,y,z);
	}
}

void CObjectDemoExperiment::PlotSimulationPoint(float Angle, float x, float y, float z)
{
	CGraphPoints* pPoint = new CGraphPoints();
	pPoint->m_Angle = Angle;
	pPoint->m_x = x;
	pPoint->m_y = y;
	pPoint->m_z = z;

	m_PlotInfoArray.Add(pPoint);

	CString strStatus;
	strStatus.Format(_T("Plot Data Points Count =%d"), m_PlotInfoArray.GetCount());
	m_pManager->SetStatusBarMessage(strStatus);

	DisplayObjectDemoGraph();

}


void CObjectDemoExperiment::InitializeSimulationGraph(CString ExperimentName)
{
	
	for (int i = 0; i < m_PlotInfoArray.GetCount(); i++)
	{
		CGraphPoints* pPoint = (CGraphPoints*)m_PlotInfoArray.GetAt(i);
		delete pPoint;
	}
	m_PlotInfoArray.RemoveAll();

	CComPtr<IApplicationChart> ApplicationChart;
	HRESULT HR = ApplicationChart.CoCreateInstance(CLSID_ApplicationChart);
	if (SUCCEEDED(HR))
	{
		ApplicationChart->DeleteAllCharts();
		ApplicationChart->Initialize2dChart(3);

		ApplicationChart->Set2dGraphInfo(0, _T("Angle Vs X"), _T("Angle(Degree)"), _T("X"), TRUE);
		ApplicationChart->Set2dAxisRange(0, EAxisPos::BottomAxis, 0, 365);
		ApplicationChart->Set2dAxisRange(0, EAxisPos::LeftAxis, 0, 2);

		ApplicationChart->Set2dGraphInfo(1, _T("Angle Vs Y"), _T("Angle(Degree)"), _T("Y"), TRUE);
		ApplicationChart->Set2dAxisRange(1, EAxisPos::BottomAxis, 0, 365);
		ApplicationChart->Set2dAxisRange(1, EAxisPos::LeftAxis, 0, 2);

		ApplicationChart->Set2dGraphInfo(2, _T("Angle Vs Z"), _T("Angle(Degree)"), _T("Z"), TRUE);
		ApplicationChart->Set2dAxisRange(2, EAxisPos::BottomAxis, 0, 365);
		ApplicationChart->Set2dAxisRange(2, EAxisPos::LeftAxis, 0, 2);

		ApplicationChart->ResizeChartWindow();
	}

}


void CObjectDemoExperiment::DisplayObjectDemoGraph()
{
	int iArraySize = (int)m_PlotInfoArray.GetCount();

	if (iArraySize <2)
	{
		return;
	}

	COleSafeArray			saX;
	COleSafeArray			saY;
	COleSafeArray			saZ;
	
	SAFEARRAYBOUND			sabX[2];
	SAFEARRAYBOUND			sabY[2];
	SAFEARRAYBOUND			sabZ[2];
	
	sabX[0].cElements = iArraySize;// give this exact
	sabX[1].cElements = 2; //number of columns + 1 (because the first column is where we put 
										 // the row labels - ie in 1.1, 2.1, 3.1, 4,1 etc
	sabX[0].lLbound = sabX[1].lLbound = 1;

	saX.Create(VT_R8, 2, sabX);

	//
	sabY[0].cElements = iArraySize;// give this exact
	sabY[1].cElements = 2; //number of columns + 1 (because the first column is where we put 
									  // the row labels - ie in 1.1, 2.1, 3.1, 4,1 etc
	sabY[0].lLbound = sabY[1].lLbound = 1;

	saY.Create(VT_R8, 2, sabY);

	//

	sabZ[0].cElements = iArraySize;// give this exact
	sabZ[1].cElements = 2; //number of columns + 1 (because the first column is where we put 
									  // the row labels - ie in 1.1, 2.1, 3.1, 4,1 etc
	sabZ[0].lLbound = sabZ[1].lLbound = 1;

	saZ.Create(VT_R8, 2, sabZ);

	//

	long index[2] = { 0,0 }; //a 2D graph needs a 2D array as index array

	for (int i = 0; i < iArraySize; i++)
	{
		CGraphPoints* pInfo = (CGraphPoints*)m_PlotInfoArray.GetAt(i);
		index[0] = i + 1;
		index[1] = 1;
		double pValue = pInfo->m_Angle;
		saX.PutElement(index, &pValue);
		saY.PutElement(index, &pValue);
		saZ.PutElement(index, &pValue);
		
		//Now plot the other Y Value for each data
		index[1] = 2;
		pValue = pInfo->m_x; //set the X 
		saX.PutElement(index, &pValue);

		pValue = pInfo->m_y; //set the Y
		saY.PutElement(index, &pValue);

		pValue = pInfo->m_z; //set the Z
		saZ.PutElement(index, &pValue);

	}
	//Refresh Graph on Only 10th Data entry
	if (iArraySize % 5 == 0)
	{
		CComPtr<IApplicationChart> ApplicationChart;
		HRESULT HR = ApplicationChart.CoCreateInstance(CLSID_ApplicationChart);
		if (SUCCEEDED(HR))
		{
			ApplicationChart->Set2dChartData(0, saX);
			ApplicationChart->Set2dChartData(1, saY);
			ApplicationChart->Set2dChartData(2, saZ);
			
		}
		
	}
}

void CObjectDemoExperiment::DrawCircle(float segments, float radius, float sx, float sy)
{
	CComPtr<IOpenGLView> OpenGLView;
	HRESULT HR = OpenGLView.CoCreateInstance(CLSID_OpenGLView);
	if (FAILED(HR))
	{
		return;
	}

	OpenGLView->glBegin(GL_LINE_LOOP);
	for (int i = 0; i<segments; i++)
	{
		float theta = (float)(2.0*3.142*float(i) / float(segments)); //get the current angle
		float x = (float)(radius*cos(theta));
		float y = (float)(radius*sin(theta));
		OpenGLView->glVertex2f(x + sx, y + sy);
	}
	OpenGLView->glEnd();
}
