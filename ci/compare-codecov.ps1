#!/usr/bin/env pwsh

<#
.SYNOPSIS
Used by Azure Pipelines to compare code coverage reports between master and current branch.

.PARAMETER wd
The working directory in which to search for current coverage.xml.
#>

param(
    [string] $wd,
    [string] $org = "coderedcorp",
    [string] $project = "coderedcms"
)

# Hide "UI" and progress bars.
$ProgressPreference = "SilentlyContinue"

# Get latest coverage from master.
$ApiBase = "https://dev.azure.com/$org/$project"
$masterBuildJson = (Invoke-WebRequest "$ApiBase/_apis/build/builds?branchName=refs/heads/master&api-version=5.1").Content | ConvertFrom-Json
$masterLatestId = $masterBuildJson.value[0].id
$masterCoverageJson = (Invoke-WebRequest "$ApiBase/_apis/test/codecoverage?buildId=$masterLatestId&api-version=5.1-preview.1").Content | ConvertFrom-Json
foreach ($cov in $masterCoverageJson.coverageData.coverageStats) {
    if ($cov.label -eq "Lines") {
        $masterlinerate = [math]::Round(($cov.covered / $cov.total) * 100, 2)
    }
}

# Get current code coverage from coverage.xml file.
$coveragePath = Get-ChildItem -Recurse -Filter "coverage.xml" $wd
if (Test-Path -Path $coveragePath) {
    [xml]$BranchXML = Get-Content $coveragePath
}
else {
    Write-Host "No code coverage from this build. Is pytest configured to output code coverage? Exiting." -ForegroundColor Red
    exit 1
}
$branchlinerate = [math]::Round([decimal]$BranchXML.coverage.'line-rate' * 100, 2)

Write-Output ""
Write-Output "Master line coverage rate:  $masterlinerate%"
Write-Output "Branch line coverage rate:  $branchlinerate%"

if ($masterlinerate -eq 0) {
    $change = "Infinite"
}
else {
    $change = [math]::Abs($branchlinerate - $masterlinerate)
}

if ($branchlinerate -gt $masterlinerate) {
    Write-Host "Coverage increased by $change% 😀" -ForegroundColor Green
    exit 0
}
elseif ($branchlinerate -eq $masterlinerate) {
    Write-Host "Coverage has not changed." -ForegroundColor Green
    exit 0
}
else {
    Write-Host "Coverage decreased by $change% 😭" -ForegroundColor Red
    exit 4
}
