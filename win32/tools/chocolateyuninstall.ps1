$ErrorActionPreference = 'Stop'
$packageName = $env:ChocolateyPackageName
$packageTitle = $env:ChocolateyPackageTitle
$packageVersion = $env:ChocolateyPackageVersion
$installDir = Join-Path $(Get-ToolsLocation) $packageName

# Remove package files and clean up install directory
Uninstall-ChocolateyZipPackage $packageName "$packageName-$packageVersion-win64-all-in-one.zip"
Remove-Item $installDir -Recurse

# Remove start menu link
$startMenuDir = Join-Path $([Environment]::GetFolderPath("StartMenu")) "Programs"
Remove-Item $(Join-Path $startMenuDir "$packageTitle.lnk")
