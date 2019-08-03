param([string]$wd)

if (Test-Path -Path "$wd/current-artifacts/Code Coverage Report_*/summary*/coverage.xml") {
    [xml]$BranchXML = Get-Content "$wd/current-artifacts/Code Coverage Report_*/summary*/coverage.xml"
} else {
    Write-Host "No code coverage from this build. Is pytest configured to output code coverage? Exiting pipeline." -ForegroundColor Red
    exit 1
}

if (Test-Path -Path "$wd/previous-artifacts/Code Coverage Report_*/summary*/coverage.xml") {
    [xml]$MasterXML = Get-Content "$wd/previous-artifacts/Code Coverage Report_*/summary*/coverage.xml"
} else {
    Write-Host "No code coverage from previous build. Exiting pipeline." -ForegroundColor Red
    exit 2
}

$masterlinerate = [math]::Round([decimal]$MasterXML.coverage.'line-rate' * 100, 2)
$branchlinerate = [math]::Round([decimal]$BranchXML.coverage.'line-rate' * 100, 2)

Write-Output "Master line coverage rate:  $masterlinerate%"
Write-Output "Branch line coverage rate:  $branchlinerate%"

if ($masterlinerate -eq 0) {
    $change = "Infinite"
} else {
    $change = [math]::Abs($branchlinerate - $masterlinerate)
}

if ($branchlinerate -gt $masterlinerate) {
    Write-Host "Coverage increased by $change% 😀" -ForegroundColor Green
    exit 0
} elseif ($branchlinerate -eq $masterlinerate) {
    Write-Host "Coverage has not changed." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Coverage decreased by $change% 😭" -ForegroundColor Red
    exit 4
}
