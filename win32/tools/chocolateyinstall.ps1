$ErrorActionPreference = 'Stop'

$packageName = $env:ChocolateyPackageName
$packageTitle = $env:ChocolateyPackageTitle
$packageVersion = $env:ChocolateyPackageVersion
$installDir = Join-Path $(Get-ToolsLocation) $packageName
$url64 = "https://sourceforge.net/projects/$packageName/files/$packageTitle-$packageVersion/$packageName-$packageVersion-win64-all-in-one.zip/download"
$checksum64 = 'f8268f919dd87f138f4ce0f7b450da08a331b619'
$checksumType64 = 'sha1'

# Install package from all-in-one ZIP
Install-ChocolateyZipPackage -PackageName $packageName -UnzipLocation $installDir `
                             -Url64bit $url64 -checksum64 $checksum64 -checksumType64 $checksumType64

# Create start menu link
$extractedArchiveDir = Join-Path $installDir "$packageTitle-$packageVersion"
$startMenuDir = Join-Path $([Environment]::GetFolderPath("StartMenu")) "Programs"
Install-ChocolateyShortcut $(Join-Path $startMenuDir "$packageTitle.lnk") `
                           $(Join-Path $extractedArchiveDir "$packageTitle.exe") 

Write-Output "==> $packageTitle has been installed to '$installDir'."
