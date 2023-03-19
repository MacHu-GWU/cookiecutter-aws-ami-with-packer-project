# -*- coding: utf-8 -*-

import typing as T
import subprocess
import dataclasses
from datetime import datetime

import jinja2
from pathlib_mate import Path
from boto_session_manager import BotoSesManager


def filter_packer_files(path: Path) -> bool:
    return path.basename.endswith("pkr.hcl") or path.basename.endswith("pkrvars.hcl")


# ------------------------------------------------------------------------------
# Define your project-width parameter object here.
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Param:
    """
    The project-width parameter object.
    """
    source_ami_name: T.Optional[str] = dataclasses.field(default=None)
    source_ami_owner_account_id: T.Optional[str] = dataclasses.field(default=None)
    output_ami_name: T.Optional[str] = dataclasses.field(default=None)
    aws_profile: T.Optional[str] = dataclasses.field(default=None)


@dataclasses.dataclass
class Project:
    """
    This is a wrapper around the packer cli, run the packer command from Python.
    """
    dir_workspace: Path = dataclasses.field()
    param: Param = dataclasses.field()

    @property
    def dir_templates(self) -> Path:
        """
        This is the directory where all the packer template source code are stored.
        """
        return self.dir_workspace / "templates"

    def clean_up(self):
        """
        Delete existing .pkc.hcl and .pkrvars.hcl files in the workspace directory.
        """
        for path in self.dir_workspace.select_file(
            filters=filter_packer_files,
            recursive=False,
        ):
            path.remove()

    def render(
        self,
        clean_up: bool = True,
    ):
        """
        Generate all the packer template files in the workspace directory,
        by rendering the jinja2 template with the parameter object.
        """
        if clean_up:
            self.clean_up()

        # render all the packer template files
        for path in self.dir_templates.select_file(
            filters=filter_packer_files,
            recursive=False,
        ):
            path_out = self.dir_workspace / path.basename
            path_out.write_text(
                jinja2.Template(path.read_text()).render(param=self.param)
            )

    def packer_validate(
        self,
        render: bool = True,
        clean_up: bool = True,
        verbose: bool = True,
    ):
        """
        Reference:

        - https://developer.hashicorp.com/packer/docs/commands/validate
        """
        if render:
            self.render(clean_up=clean_up)

        args = ["packer", "validate"]
        for path in self.dir_workspace.select_file(
            filters=lambda p: p.basename.endswith(".pkrvars.hcl"),
            recursive=False,
        ):
            args.append(f"-var-file={path}")

        args.append(f"{self.dir_workspace}")

        if verbose:
            print("run 'packer validate' command:")
            print("packer validate \\\n\t" + " \\\n\t".join(args[2:]))

        with dir_here.temp_cwd():
            subprocess.run(args, check=True)

    def packer_build(
        self,
        render: bool = True,
        clean_up: bool = True,
        validate: bool = True,
        dry_run: bool = True,
        verbose: bool = True,
    ):
        if render:
            self.render(clean_up=clean_up)

        if validate:
            self.packer_validate(render=False, verbose=verbose)

        args = [
            "packer",
            "build",
            "-debug",
        ]

        for path in self.dir_workspace.select_file(
            filters=lambda p: p.basename.endswith(".pkrvars.hcl"),
            recursive=False,
        ):
            args.append(f"-var-file={path}")

        args.append(f"{self.dir_workspace}")

        if verbose:
            print("run 'packer build' command:")
            print("packer build \\\n\t" + " \\\n\t".join(args[2:]))

        with dir_here.temp_cwd():
            if dry_run is False:
                subprocess.run(args, check=True)


def tag_image(
    bsm: BotoSesManager,
    image_name: str,
    tags: T.Optional[T.Dict[str, str]] = None,
):
    # find image id
    response = bsm.ec2_client.describe_images(
        Filters=[
            dict(
                Name="name",
                Values=[
                    image_name,
                ],
            ),
        ],
    )
    image_id = response["Images"][0]["ImageId"]

    # update tags
    create_tags_kwargs = dict(
        Resources=[
            image_id,
        ]
    )
    if tags:
        create_tags_kwargs["Tags"] = [dict(Key=k, Value=v) for k, v in tags.items()]
    bsm.ec2_client.create_tags(**create_tags_kwargs)

# ------------------------------------------------------------------------------
# Execution script starts from here
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    dir_here = Path.dir_here(__file__)

    # initialize your parameter object with values
    # you may read sensitive data from external store, such as AWS SSM Parameter Store
    param = Param(
        source_ami_name="ubuntu/images/*ubuntu-xenial-16.04-amd64-server-*",
        source_ami_owner_account_id="099720109477",
        output_ami_name="aws-ami-with-packer-example-{}".format(
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        ),
        aws_profile = "{{ cookiecutter.aws_profile }}",
    )

    # use the aws profile to create the AWS boto3 session
    bsm = BotoSesManager(profile_name=param.aws_profile)

    # initialize your project object
    # we set ``dir_workspace`` to the current directory
    # and pass the parameter object
    project = Project(
        dir_workspace=dir_here,
        param=param,
    )

    # run packer build
    project.packer_build(
        render=True,
        clean_up=True,
        validate=True,
        dry_run=False,  # set to True to do a dry run
        verbose=True,
    )

    # post process
    image_name = param.output_ami_name
    tags = {
        "Name": image_name,
        "tech:project_name": "poc",
        "tech:env_name": "dev",
        "tech:version": "v16",
        "tech:human_creator": "{{ cookiecutter.author_name }}",
        "tech:machine_creator": "packer",
        "auto:delete_at": "na",
        "bus:ou": "app",
        "bus:team": "app",
        "bus:project": "poc",
        "bus:owner": "{{ cookiecutter.author_name }}",
    }
    tag_image(bsm=bsm, image_name=image_name, tags=tags)
