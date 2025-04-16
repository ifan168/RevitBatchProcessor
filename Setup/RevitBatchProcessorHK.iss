#define AppName "Revit Batch Processor 华科版"
#define AppVersion "1.12.0"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
PrivilegesRequired=lowest
AppId={{B5CA57EA-7BB2-4620-916C-AE98376C1EF1}}
DisableDirPage=auto
DefaultDirName={localappdata}\RevitBatchProcessor
SetupLogging=True
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
DefaultGroupName=Revit Batch Processor
OutputBaseFilename=RevitBatchProcessorSetup华科版_v{#AppVersion}

[Files]
Source: "C:\Users\Administrator\source\repos\RevitBatchProcessor\BatchRvtGUI\bin\x64\Release\*"; DestDir: "{app}"; Flags: ignoreversion createallsubdirs recursesubdirs
Source: "C:\Users\Administrator\source\repos\RevitBatchProcessor\BatchRvtAddin2020\bin\x64\Release\*"; DestDir: "{userappdata}\Autodesk\Revit\Addins\2020\BatchRvt"; Flags: ignoreversion createallsubdirs recursesubdirs
Source: "C:\Users\Administrator\source\repos\RevitBatchProcessor\BatchRvtAddin2020\BatchRvtAddin2020.addin"; DestDir: "{userappdata}\Autodesk\Revit\Addins\2020"; Flags: ignoreversion
[Icons]
Name: "{group}\Revit Batch Processor (GUI)"; Filename: "{app}\BatchRvtGUI.exe"; WorkingDir: "{app}"

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "chinesetraditional"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
