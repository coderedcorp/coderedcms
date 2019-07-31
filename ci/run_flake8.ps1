$ExitCode = 0
$GitDiff = git diff origin/master
# If there is no diff between master, then flake8 everything.
if ( $GitDiff -eq $null ) {
    flake8 .
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
}
# Else flake8 just the diff.
else {
    Write-Output $GitDiff | flake8 --diff
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    # If the project_template changed, then flake8 the testproject too.
    $GitDiffTempl = Write-Output $GitDiff | Select-String -Pattern "^diff .*/project_template/.*"
    if ( $GitDiffTempl -ne $null ) {
        flake8 testproject
        if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    }
}
exit $ExitCode
