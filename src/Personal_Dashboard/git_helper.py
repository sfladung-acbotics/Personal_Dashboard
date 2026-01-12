import git
import os


def get_untracked_files(pth):
    try:
        repo = git.Repo(pth)
    except (git.NoSuchPathError, git.InvalidGitRepositoryError):
        return ()
    files = repo.untracked_files
    del repo
    return tuple(files)


def get_modified_files(pth):
    try:
        repo = git.Repo(pth)
    except (git.NoSuchPathError, git.InvalidGitRepositoryError):
        return ()
    files = []
    diffs = repo.index.diff(None)
    for d in diffs:
        files.append(d.a_path)
    return tuple(files)


def get_repo_sync_Status(repo_pth):
    unsynced = {}
    if os.path.isdir(repo_pth):
        untracked = get_untracked_files(repo_pth)
        modified = get_modified_files(repo_pth)
        if len(untracked) > 0 or len(modified) > 0:
            unsynced[repo_pth] = {
                "untracked": untracked,
                "modified": modified,
            }
    return unsynced


def get_unsynced_repos(base_path):
    unsynced = {}
    if os.path.isdir(base_path):
        repos = os.listdir(base_path)
        for r in repos:
            repo_pth = os.path.join(base_path, r)
            unsynced |= get_repo_sync_Status(repo_pth)
    return unsynced


def get_unsynced_repos_double_depth(base_path):
    # base_path = "/home/sam/git"

    subdirs = os.listdir(base_path)
    unsynced = {}
    for d in subdirs:
        sub_pth = os.path.join(base_path, d)
        if os.path.isdir(sub_pth):
            unsynced |= get_unsynced_repos(sub_pth)
    return unsynced


if __name__ == "__main__":
    unsynced = get_unsynced_repos_double_depth("/home/sam/git")
    for repo in sorted(unsynced.keys()):
        print(
            repo
            + " Untracked:"
            + repr(len(unsynced[repo]["untracked"]))
            + " Modified:"
            + repr(len(unsynced[repo]["modified"]))
        )
    unsynced = get_unsynced_repos("/home/sam/LibrePCB-Workspace/data/libraries/local")
    for repo in sorted(unsynced.keys()):
        print(
            repo
            + " Untracked:"
            + repr(len(unsynced[repo]["untracked"]))
            + " Modified:"
            + repr(len(unsynced[repo]["modified"]))
        )
