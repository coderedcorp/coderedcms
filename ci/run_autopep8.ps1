$ExitCode = 0
$GitDiff = git diff --name-only origin/master
$GitDiffPep = Write-Output $GitDiff | Select-String -Pattern ".*\.py" | Select-String -NotMatch ".*/project_template/.*"
# If there is no diff between master, then run everything.
if ( $GitDiffPep -eq $null ) {
    autopep8 -r --diff coderedcms/
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
}
# Else run just the diff.
else {
    autopep8 -r --diff $GitDiffPep
    if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    # If the project_template changed, then run the testproject too.
    $GitDiffTempl = Write-Output $GitDiff | Select-String -Pattern ".*/project_template/.*"
    if ( $GitDiffTempl -ne $null ) {
        #autopep8 -r --diff testproject/
        if ($LastExitCode -ne 0) { $ExitCode = $LastExitCode }
    }
}
exit $ExitCode
