[xml]$OldXML = Get-Content "/home/vsts/work/artifacts/Code Coverage Report_*/summary*/coverage.xml"
[xml]$NewXML = Get-Content .\coverage.xml

$oldlinerate = $OldXML.coverage.'line-rate'
$newlinerate = $NewXML.coverage.'line-rate'

$oldoutput = -join("Old line coverage rate: ", $oldlinerate)
$newoutput = -join("New line coverage rate: ", $newlinerate)

Write-Output $oldoutput
Write-Output $newoutput

if ($newlinerate -gt $oldlinerate) {
    Write-Output "Code coverage has increased. Build passed."
    exit 0
} else if ($newlinerate -eq $oldlinerate) {
    Write-Output "Code coverage has not changed. Build passed."
    exit 0
} else {
    Write-Error "Code coverage as decreased. Code coverage must be greater than or equal to the previous build to pass."
    exit 1
}