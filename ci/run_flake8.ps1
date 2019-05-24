$ExitCode = 0
# If we're on master then flake8 everything.
$GitBranch = git rev-parse --abbrev-ref HEAD
if ( $GitBranch -eq "master") {
    flake8 coderedcms testproject
    if ($LastExitCode -ne 0) { $ExitCode = 1 }
}
# Else flake8 just the diff.
else {
    git diff origin/master | flake8 --diff
    if ($LastExitCode -ne 0) { $ExitCode = 1 }
    # If the project_template changed, then flake8 the testproject too.
    $GitDiffTempl = git diff origin/master | Select-String -Pattern "^diff .*/project_template/.*"
    if ( $GitDiffTempl -ne $null ) {
        flake8 testproject
        if ($LastExitCode -ne 0) { $ExitCode = 1 }
    }
}
exit $ExitCode
