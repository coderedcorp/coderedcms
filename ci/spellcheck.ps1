#!/usr/bin/env pwsh

<#
.SYNOPSIS
Checks spelling of code and docs.
#>

# Get path.
$scriptDir = Split-Path $PSCommandPath -Parent
$projectDir = (Get-Item $scriptDir).Parent

# Set working directory to root of project.
Push-Location $projectDir

$ExitCode = 0

# Run spell checker.
codespell `
    --skip="migrations,vendor,_build,*.css.map,*.jpg,*.png,*.pyc" `
    --ignore-words-list="assertIn" `
    coderedcms docs
$ExitCode = $LastExitCode

# Print output.
if ($ExitCode -eq 0) {
    Write-Host "Spelling looks good!"
}
else {
    # Write the error in a way that shows up as the failure reason in Azure Pipelines.
    Write-Host -ForegroundColor Red `
        "##vso[task.LogIssue type=error;]Spelling errors! 👩‍🏫"
}

# Unset working directory and exit with pytest's code.
Pop-Location
exit $ExitCode
