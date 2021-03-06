; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{0D13DAF6-02E1-4DC4-B919-8B6A9FAE64A6}
AppName=GarlicSim
AppVerName=GarlicSim 0.5
AppPublisher=Ram Rachum
AppPublisherURL=http://garlicsim.org
AppSupportURL=http://garlicsim.org
AppUpdatesURL=http://garlicsim.org
ChangesAssociations=yes
ChangesEnvironment=yes
DefaultDirName={pf}\GarlicSim
DefaultGroupName=GarlicSim
AllowNoIcons=yes
LicenseFile=py2exe_dist/lib/garlicsim_wx/copyright.txt
OutputDir=.
OutputBaseFilename=GarlicSim
Compression=lzma
SolidCompression=yes

[Registry]
Root: HKCR; Subkey: ".gssp"; ValueType: string; ValueName: ""; ValueData: "GarlicSimSimulationPickle"; Flags: uninsdeletevalue

Root: HKCR; Subkey: "GarlicSimSimulationPickle"; ValueType: string; ValueName: ""; ValueData: "GarlicSim Simulation Pickle"; Flags: uninsdeletekey

Root: HKCR; Subkey: "GarlicSimSimulationPickle\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\lib\garlicsim_wx\misc\icon_bundle\images\garlicsim_document.ico,0"

Root: HKCR; Subkey: "GarlicSimSimulationPickle\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\GarlicSim.exe"" ""%1"""

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked


[Files]
Source: "py2exe_dist/GarlicSim.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "py2exe_dist/*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\GarlicSim"; Filename: "{app}\GarlicSim.exe"
Name: "{group}\{cm:UninstallProgram,GarlicSim}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\GarlicSim"; Filename: "{app}\GarlicSim.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\GarlicSim.exe"; Description: "{cm:LaunchProgram,GarlicSim}"; Flags: nowait postinstall skipifsilent
