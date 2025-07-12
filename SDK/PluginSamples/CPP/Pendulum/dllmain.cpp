// dllmain.cpp : Implementation of DllMain.

#include "stdafx.h"
#include "resource.h"
#include "Pendulum_i.h"
#include "dllmain.h"
#include "xdlldata.h"

CPendulumModule _AtlModule;

class CPendulumApp : public CWinApp
{
public:

// Overrides
	virtual BOOL InitInstance();
	virtual int ExitInstance();

	DECLARE_MESSAGE_MAP()
};

BEGIN_MESSAGE_MAP(CPendulumApp, CWinApp)
END_MESSAGE_MAP()

CPendulumApp theApp;

BOOL CPendulumApp::InitInstance()
{
#ifdef _MERGE_PROXYSTUB
	if (!PrxDllMain(m_hInstance, DLL_PROCESS_ATTACH, NULL))
		return FALSE;
#endif
	return CWinApp::InitInstance();
}

int CPendulumApp::ExitInstance()
{
	return CWinApp::ExitInstance();
}
