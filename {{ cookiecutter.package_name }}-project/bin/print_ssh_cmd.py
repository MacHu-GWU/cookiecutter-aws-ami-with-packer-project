# -*- coding: utf-8 -*-

"""
Generate the ssh command to connect to ec2.
1. Edit the parameters
2. Run this script
3. Copy and paste to terminal
Requirements:
- Python >= 3.7
- You have to put your ec2 key pair (.pem) file at ${HOME}/${AWS_ACCOUNT_ALIAS}/${AWS_REGION}/${KEY_NAME}
Ref:
- Default user name for AMI: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance
- For Amazon Linux 2 or the Amazon Linux AMI, the username is ec2-user.
- For a CentOS AMI, the username is centos.
- For a Debian AMI, the username is admin.
- For a Fedora AMI, the username is ec2-user or fedora.
- For a RHEL AMI, the username is ec2-user or root.
- For a SUSE AMI, the username is ec2-user or root.
- For an Ubuntu AMI, the username is ubuntu.
"""

import typing as T
from pathlib import Path


def get_aws_account_alias(iam_client) -> str:
    return iam_client.list_account_aliases()["AccountAliases"][0]


def iterate_instance_dict(response: dict) -> T.List[
    T.Tuple[dict, str, str, str],
]:
    """
    parse the ec2_client.describe_instances() response, iterate enriched information.
    """
    rows = list()
    for reservation_dct in response["Reservations"]:
        for inst_dct in reservation_dct["Instances"]:
            id = inst_dct["InstanceId"]
            state = inst_dct["State"]["Name"]
            tags = {
                dct["Key"]: dct["Value"]
                for dct in inst_dct["Tags"]
            }
            name = tags.get("Name", "unknown")
            rows.append((inst_dct, id, state, name))
    return rows


def get_image_name(ec2_client, image_id: str) -> str:
    image_dct = ec2_client.describe_images(
        ImageIds=[image_id, ]
    )["Images"][0]
    image_name = image_dct["Name"]
    return image_name


def get_pem_file_path(
    aws_account_alias: str,
    aws_region: str,
    key_name: str
) -> Path:
    return (
        Path.home().absolute()
        / "ec2-pem"
        / aws_account_alias
        / aws_region
        / f"{key_name}.pem"
    )


def get_ssh_cmd(
    path_pem_file: T.Union[Path, str],
    username: str,
    public_ip: str,
) -> str:
    return "ssh -i {ec2_pem} {username}@{public_ip}".format(
        ec2_pem=path_pem_file, username=username, public_ip=public_ip,
    )


if __name__ == "__main__":
    ssh_cmd = get_ssh_cmd(
        path_pem_file=get_pem_file_path(
            aws_account_alias="awshsh-app-dev",
            aws_region="{{ cookiecutter.aws_region }}",
            key_name="sanhe-dev",
        ),
        username="ubuntu",
        public_ip="111.111.111.111",
    )
    print(ssh_cmd)