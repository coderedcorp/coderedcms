#!/usr/bin/env pwsh

<#
.SYNOPSIS
Runs unit tests. Outputs test results and code coverage report.
#>

# Get path.
$scriptDir = Split-Path $PSCommandPath -Parent
$projectDir = (Get-Item $scriptDir).Parent

# Set working directory to root of project.
Push-Location $projectDir

$ExitCode = 0

# Run unit tests.
pytest coderedcms/ --ds=coderedcms.tests.settings --junitxml=junit/test-results.xml --cov=coderedcms --cov-report=xml --cov-report=html
$ExitCode = $LastExitCode

# Print code coverage if succeeded.
if ($ExitCode -eq 0) {
    [xml]$BranchXML = Get-Content coverage.xml
    $LineRate = [math]::Round([decimal]$BranchXML.coverage.'line-rate' * 100, 2)
    Write-Output "All unit tests passed! 🥳"
    Write-Output "Code coverage: $LineRate%"
}

# Unset working directory and exit with pytest's code.
Pop-Location
exit $ExitCode
