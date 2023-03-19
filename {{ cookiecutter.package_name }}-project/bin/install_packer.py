# -*- coding: utf-8 -*-

import subprocess
from pathlib_mate import Path

# manually edit this url to define the pre-compiled binary you want to use
download_packer_url = "https://releases.hashicorp.com/packer/1.8.3/packer_1.8.3_linux_amd64.zip"

dir_here = Path(__file__).absolute().parent
path_packer_zip = dir_here.joinpath(download_packer_url.split("/")[-1])
path_packer_binary = dir_here.joinpath("packer")
dir_usr_local_bin = Path("/usr/local/bin")
path_usr_local_bin_packer = dir_usr_local_bin.joinpath("packer")

with dir_here.temp_cwd():
    if not path_packer_zip.exists():
        args = ["wget", download_packer_url]
        subprocess.run(args)

    if path_packer_binary.exists():
        path_packer_binary.remove_if_exists()
    if path_usr_local_bin_packer.exists():
        path_usr_local_bin_packer.remove_if_exists()

    args = ["unzip", f"{path_packer_zip}"]
    subprocess.run(args)

    args = ["sudo", "mv", f"{path_packer_binary}", f"{dir_usr_local_bin}"]
    # print("run this command in your terminal to copy packer to your /usr/local/bin folder, this cannot be done on MacOS")
    # print(" ".join(args))
    subprocess.run(args)
