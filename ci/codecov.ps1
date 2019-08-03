#!/usr/bin/env pwsh

param(
    [string]$BuildId
)

$ApiBase = "https://dev.azure.com/coderedcorp/coderedcms"

# Get latest coverage from master.
$masterBuildJson = (Invoke-WebRequest "$ApiBase/_apis/build/builds?branchName=refs/heads/master&api-version=5.1").Content | ConvertFrom-Json
$masterLatestId = $masterBuildJson.value[0].id
$masterCoverageJson = (Invoke-WebRequest "$ApiBase/_apis/test/codecoverage?buildId=$masterLatestId&api-version=5.1-preview.1").Content | ConvertFrom-Json
foreach ($cov in $masterCoverageJson.coverageData.coverageStats) {
    if ($cov.label -eq "Lines") {
        $masterCoverage = [math]::Round(($cov.covered / $cov.total) * 100, 2)
    }
}
# Get coverage from current build.
$branchCoverageJson = (Invoke-WebRequest "$ApiBase/_apis/test/codecoverage?buildId=$BuildId&api-version=5.1-preview.1").Content | ConvertFrom-Json
foreach ($cov in $branchCoverageJson.coverageData.coverageStats) {
    if ($cov.label -eq "Lines") {
        $branchCoverage = [math]::Round(($cov.covered / $cov.total) * 100, 2)
    }
}

# Print coverages.
Write-Output "Master line coverage rate: $masterCoverage%"
Write-Output "Branch line coverage rate: $branchCoverage%"

# Compare coverages.
if ($masterCoverage -eq 0) {
    $change = "Infinite"
}
else {
    $change = [math]::Abs([math]::Round($masterCoverage - $branchCoverage))
    }

    # Determine pass/fail.
    if ($branchCoverage -gt $masterCoverage) {
        Write-Host "Coverage increased by $change% 🥳" -ForegroundColor Green
        exit 0
    }
    elseif ($branchCoverage -eq $masterCoverage) {
        Write-Host "Coverage has not changed." -ForegroundColor Green
        exit 0
    }
    else {
        Write-Host "Coverage decreased by $change% 😭" -ForegroundColor Red
        exit 1
    }
