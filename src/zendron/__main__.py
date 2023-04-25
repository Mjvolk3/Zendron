import subprocess

from zendron import load


def main():
    print("Sync Starting")
    load.main()
    subprocess.run("dendron importPod --podId dendron.markdown --wsRoot .", shell=True)
    subprocess.run("rm -r zotero_pod", shell=True)
    print("Sync Complete")


if __name__ == "__main__":
    main()
