$ErrorActionPreference = 'Stop'

$packageName = $env:ChocolateyPackageName
$packageTitle = $env:ChocolateyPackageTitle
$packageVersion = $env:ChocolateyPackageVersion

$packageArgs = @{
  packageName   = $packageName
  fileType      = 'msi'
  softwareName  = 'MComix'
  url64bit      =  "https://sourceforge.net/projects/$packageName/files/$packageTitle-$packageVersion/$packageName-win64-$packageVersion.msi/download"
  checksum64    = 'FIXME'
  checksumType64=  'sha1'
  silentArgs    = "/qn /norestart /l*v `"$($env:TEMP)\$($packageName).$($env:chocolateyPackageVersion).MsiInstall.log`""
  validExitCodes= @(0, 3010, 1641)
}

Install-ChocolateyPackage @packageArgs
