import re
import os
from git import Repo
from packaging.version import Version

def find_files(folder_path, branch_name=None):
    repo = Repo('.')
    if branch_name:
        tree = repo.tree(branch_name)
    else:
        current_branch = repo.active_branch
        tree = repo.tree(current_branch.commit.hexsha)
    pattern = re.compile(r'V(\d+\.\d+\.\d+)_.*')
    versions = []
    matches = []
    for blob in tree.traverse():
        if blob.path.startswith(folder_path):
            filename = os.path.basename(blob.path)
            # print(filename)
            match = pattern.match(filename)
            if match:
                matches.append(filename)
                version = match.group(1)
                versions.append(version)
    versions = [Version(v) for v in versions]
    main_max_version = max(versions)
    print(matches)
    return main_max_version


main_max_version = find_files( 'snowflake/prd', 'main',)

print("Maximum version is:", main_max_version)

current_branch_max_version = find_files('snowflake/prd')

print("Current maximum version is:", current_branch_max_version)

def version_diff(version1, version2):
    v1_components = [version1.major, version1.minor, version1.micro]
    v2_components = [version2.major, version2.minor, version2.micro]

    diff = []
    for v1, v2 in zip(v1_components, v2_components):
        diff.append(v2 - v1)
    if sum(diff) == 1:
        print("new version number is valid")
        return True
    else:
        print("new version number seems not valid")
        return False

version1 = main_max_version
version2 = current_branch_max_version

print("Version difference is:", version_diff(version1, version2))
