"""
Maintains version of coderedcms.
4th element is for pre-releases. Leave blank for stable releases.

    X.Y.ZaN   # Alpha release
    X.Y.ZbN   # Beta release
    X.Y.ZrcN  # Release Candidate
    X.Y.Z     # Final release

5th element is for dev/post releases. Leave blank for stable releases.

    X.Y.Z.devN   # Development release
    X.Y.Z.postN  # Post release (e.g. docs changes but no actual code changes)

See: https://www.python.org/dev/peps/pep-0440/
"""

release = ["3", "0", "0", "", "dev0"]


def _get_version() -> str:
    v = "{0}.{1}.{2}".format(release[0], release[1], release[2])
    if release[3]:
        v = "{0}{1}".format(v, release[3])
    if release[4]:
        v = "{0}.{1}".format(v, release[4])
    return v


__version__ = _get_version()
__shortversion__ = "{0}.{1}".format(release[0], release[1])
