import os
import platform
import subprocess

FNULL = open(os.devnull, 'w')
pl = platform.system()
pla = "dd"
print("detected platform:", pl)

IS_WINDOWS = "Windows" in pl
IS_LINUX = "Linux" in pl
IS_MAC = "Darwin" in pl


def get_package_manager_command():
    if os.system("pacman") == 1:
        # for arch linux look at this: https://snapcraft.io/install/ffmpeg/arch
        raise NotImplementedError(
            "arch linux is not supported yet to install ffmopeg with the installer.\nplease do the steps shown at https://snapcraft.io/install/ffmpeg/arch and start the installer again")
    if os.system("apt") == 0:
        return "sudo apt install ffmpeg"


def install_ffmpeg_win():
    if not os.path.exists(r"c:\ProgramData\Microsoft\Windows\Start Menu\Programs\7-Zip\7-Zip File Manager.lnk"):
        while True:
            i = input(
                "didnt find 7zip in default path. do you have it[Y/N]? ").lower()
            if i == "n":
                print("installing 7zip")
                from requests import get
                c = get("https://www.7-zip.org/a/7z1900.exe").content
                open("7z_installer.exe", "wb+").write(c)
                os.system(".\\7z_installer.exe")
            elif i == "y":
                break
            else:
                print("the answer should be Y or N or y or n.")


def install_ffmpeg():
    try:
        subprocess.check_call("ffmpeg", stdout=FNULL, stderr=FNULL)
    except subprocess.CalledProcessError as e:
        if not e.returncode == 1:
            if IS_WINDOWS:
                install_ffmpeg_win()
            elif IS_MAC:
                if os.system("brew install ffmpeg") != 0:
                    raise ValueError("please install brew or network error")
            elif IS_LINUX:
                os.system(get_package_manager_command())
            else:
                raise OSError("unsupported operating system: {}".format(pl))
        else:
            print("ffmpeg already installed")


def main():
    install_ffmpeg()


main()
