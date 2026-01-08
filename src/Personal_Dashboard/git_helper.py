import git
import os


def get_untracked_files(pth):
    try:
        repo = git.Repo(pth)
    except git.NoSuchPathError:
        return ()
    files = repo.untracked_files
    del repo
    return tuple(files)


def get_modified_files(pth):
    try:
        repo = git.Repo(pth)
    except git.NoSuchPathError:
        return ()
    files = []
    diffs = repo.index.diff(None)
    for d in diffs:
        files.append(d.a_path)
    return tuple(files)


def get_unsynced_repos():
    base_path = "/home/sam/git"

    subdirs = os.listdir(base_path)
    unsynced = {}
    for d in subdirs:
        sub_pth = os.path.join(base_path, d)
        if os.path.isdir(sub_pth):
            repos = os.listdir(sub_pth)
            for r in repos:
                repo_pth = os.path.join(sub_pth, r)
                if os.path.isdir(repo_pth):
                    untracked = get_untracked_files(repo_pth)
                    modified = get_modified_files(repo_pth)
                    if len(untracked) > 0 or len(modified) > 0:
                        unsynced[repo_pth] = {
                            "untracked": untracked,
                            "modified": modified,
                        }
    return unsynced


if __name__ == "__main__":
    unsynced = get_unsynced_repos()
    for repo in sorted(unsynced.keys()):
        print(
            repo
            + " Untracked:"
            + repr(len(unsynced[repo]["untracked"]))
            + " Modified:"
            + repr(len(unsynced[repo]["modified"]))
        )
