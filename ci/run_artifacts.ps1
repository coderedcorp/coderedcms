[xml]$OldXML = Get-Content "/home/vsts/work/artifacts/Code Coverage Report_*/summary*/coverage.xml"
[xml]$NewXML = Get-Content .\coverage.xml

$oldlinerate = $OldXML.coverage.'line-rate'
$newlinerate = $NewXML.coverage.'line-rate'

$oldoutput = -join("Old line coverage rate: ", $oldlinerate)
$newoutput = -join("New line coverage rate: ", $newlinerate)

Write-Output $oldoutput
Write-Output $newoutput

if ($newlinerate -ge $oldlinerate) {
    exit 0
} else {
    exit 1
}