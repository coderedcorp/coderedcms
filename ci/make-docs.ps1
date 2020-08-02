#!/usr/bin/env pwsh

<#
.SYNOPSIS
Builds the documentation as HTML.
#>

# Get path.
$scriptDir = Split-Path $PSCommandPath -Parent
$projectDir = (Get-Item $scriptDir).Parent
$docsDir = Join-Path -Path $projectDir -ChildPath "docs"
$docsBuildDir = Join-Path -Path $docsDir -ChildPath "_build"

$ExitCode = 0

# Clean previously built docs.
sphinx-build -M clean $docsDir $docsBuildDir

# Make docs, treat warnigs as errors.
sphinx-build -M html $docsDir $docsBuildDir -W
$ExitCode = $LastExitCode

# Write output for humans.
if ($ExitCode -eq 0) {
    Write-Host "Docs have been built! 📜" -ForegroundColor Green
}
else {
    # Write the error in a way that shows up as the failure reason in Azure Pipelines.
    Write-Host "##vso[task.LogIssue type=error;]There were warnings or errors building the docs."
}

# Exit with sphinx's code.
exit $ExitCode
