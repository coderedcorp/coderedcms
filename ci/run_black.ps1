$ExitCode = 0
$GitDiff = git diff origin/master
# If there is no diff between master, then black everything.
if ( $GitDiff -eq $null ) {
    black --diff .
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
}
# Else black just the diff.
else {
    Write-Output $GitDiff | black --diff
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    # If the project_template changed, then black the testproject too.
    $GitDiffTempl = Write-Output $GitDiff | Select-String -Pattern "^diff .*/project_template/.*"
    if ( $GitDiffTempl -ne $null ) {
        black /coderedcms/
        if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    }
}
exit $ExitCode
