$ExitCode = 0
$GitDiff = git diff --name-only origin/master
$GitDiffBlack = git diff --name-only origin/master | Select-String -Pattern ".*\.py" | Select-String -NotMatch ".*/project_template/.*"
# If there is no diff between master, then black everything.
if ( $GitDiff -eq $null ) {
    black --check .
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
}
# Else black just the diff.
else {
    black --check $GitDiffBlack
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    # If the project_template changed, then black the testproject too.
    $GitDiffTempl = Write-Output $GitDiff | Select-String -Pattern ".*/project_template/.*"
    if ( $GitDiffTempl -ne $null ) {
        black --check testproject/
        if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    }
}
exit $ExitCode
