[Setup]
AppName=Unir PDF
AppVersion=1.0
DefaultDirName={pf}\UnirPDF
DefaultGroupName=Unir PDF
OutputDir=dist
OutputBaseFilename=UnirPDF_Installer
SetupIconFile=icono.ico

[Files]
Source: "dist\Unir_pdfs_1.2.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\Unir PDF"; Filename: "{app}\Unir_pdfs_1.2.exe"
Name: "{group}\Unir PDF"; Filename: "{app}\Unir_pdfs_1.2.exe"
