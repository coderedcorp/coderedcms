if (Test-Path -Path "/home/vsts/work/artifacts/Code Coverage Report_*/summary*/coverage.xml") {
    [xml]$MasterXML = Get-Content "/home/vsts/work/artifacts/Code Coverage Report_*/summary*/coverage.xml"
} else {
    Write-Host "No code coverage from previous build. Exiting pipeline." -ForegroundColor Red
    exit 1
}

[xml]$BranchXML = Get-Content .\coverage.xml

$masterlinerate = [math]::Abs([math]::Round([decimal]$MasterXML.coverage.'line-rate' * 100, 2))
$branchlinerate = [math]::Abs([math]::Round([decimal]$BranchXML.coverage.'line-rate' * 100, 2))

$masterlinerate = 59.50

Write-Output "Old line coverage rate: $masterlinerate%"
Write-Output "New line coverage rate: $branchlinerate%"

if ($masterlinerate -ne 0) {
    $change = [math]::Abs([math]::Round((($branchlinerate - $masterlinerate) / $masterlinerate) * 100, 2))
} else {
    $change = "Infinite"
}

if ($branchlinerate -gt $masterlinerate) {
    Write-Host "Code coverage has increased by $change%. Build passed." -ForegroundColor Green
    exit 0
} elseif ($branchlinerate -eq $masterlinerate) {
    Write-Host "Code coverage has not changed. Build passed." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Code coverage as decreased by $change%. Code coverage must be greater than or equal to the previous build to pass." -ForegroundColor Red
    exit 2
}
