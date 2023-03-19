packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu18" {
  ami_name      = var.output_ami_name
  instance_type = "t2.micro"
  region        = "us-east-1"
  ssh_username  = "ubuntu"

  source_ami_filter {
    filters = {
      name                = var.source_ami_name
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = [var.source_ami_owner_account_id]
  }

  /*----------------------------------------------------------------------------
  If you want to build on a custom VPC, you can uncomment the following block
  ----------------------------------------------------------------------------*/
  # if none default VPC, you need to explicitly set this to true
  associate_public_ip_address = true

#  vpc_filter {
#    filters = {
#      "tag:Name": "aws_landing_zone-dev-vpc",
#      "isDefault": "false",
#    }
#  }

  # make sure you are using a public subnet
  subnet_filter {
    filters = {
      "tag:Name": "aws_landing_zone-dev/public/1"
    }
    most_free = true
    random = false
  }

  # make sure the security group has ssh inbound rule
  security_group_filter {
    filters = {
      "tag:Name": "aws_landing_zone-dev/sg/allow-restricted-traffic-from-authorized-ip"
    }
  }

  /*----------------------------------------------------------------------------
  If you want to use a custom IAM role, you can use ``iam_instance_profile``
  ----------------------------------------------------------------------------*/
  iam_instance_profile = "ec2-power-user-role"

  /*----------------------------------------------------------------------------
  If you need to add additional volume to your AMI, you can do it here
  ----------------------------------------------------------------------------*/
#  launch_block_device_mappings {
#      device_name = "/dev/sda1"
#      # in the most of the cases, you should set delete_on_termination = true
#      # the AMI has the snapshot of the volume already. When you use the output
#      # of this build as a image, it will create a ebs volume from the snapshot.
#      # If you set delete_on_termination = false, you will end up with a volume
#      # after the build and you have to clean up your self
#      delete_on_termination = true
#      /*
#      gp3 would be the optimal choice for most of the cases since Dec 2020
#
#      reference:
#
#      - Introducing new Amazon EBS general purpose volumes, gp3: https://aws.amazon.com/about-aws/whats-new/2020/12/introducing-new-amazon-ebs-general-purpose-volumes-gp3/
#      - Migrate your Amazon EBS volumes from gp2 to gp3 and save up to 20% on costs: https://aws.amazon.com/blogs/storage/migrate-your-amazon-ebs-volumes-from-gp2-to-gp3-and-save-up-to-20-on-costs/
#      */
#      volume_type = "gp3"
#      volume_size = 30
#  }
#
#  ami_block_device_mappings {
#     device_name = "/dev/sda1"
#     delete_on_termination = true
#     volume_type = "gp3"
#  }
}

build {
  name    = "install python"
  sources = [
    "source.amazon-ebs.ubuntu18"
  ]

  provisioner "shell" {
    inline = [
      "sleep 10",
      # verify ebs attachment
      "lsblk",
      "df -h",
    ]
  }


  /*----------------------------------------------------------------------------
  if you need to sudo install something, do it in the ``inline`` block
  ----------------------------------------------------------------------------*/
#  provisioner "shell" {
#    inline = [
#      "sudo apt-get install -y curl",
#      "sudo apt-get install -y wget",
#      "sudo apt-get install -y git",
#      "sudo apt-get install -y unzip",
#    ]
#  }


  /*----------------------------------------------------------------------------
  if you need to run complicate logic in Python, and it has zero dependency
  and fits in one file, you can upload the script to the server and run it.
  make sure you have the right shebang ``#!/usr/bin/env python`` in the first line
  ----------------------------------------------------------------------------*/
#  provisioner "shell" {
#    script = "zero_deps_script.py"
#  }


  /*----------------------------------------------------------------------------
  if your Python script has some simple dependencies, please pre-configure
  the pyenv https://github.com/pyenv/pyenv and then use the pyenv to install
  some user Python versions, and then use the user Python to install dependencies
  and run code. DON't directly install anything to the system Python
  ----------------------------------------------------------------------------*/
#  provisioner "file" {
#    source = "requirements.txt"
#    destination = "/tmp/requirements.txt"
#  }
#
#  provisioner "file" {
#    source = "some_deps_script.py"
#    destination = "/tmp/some_deps_script.py"
#  }
#
#  provisioner "shell" {
#    inline = [
#      "~/.pyenv/shims/pip install -r /tmp/requirements.txt",
#      "~/.pyenv/shims/python /tmp/some_deps_script.py",
#    ]
#  }


  /*----------------------------------------------------------------------------
  if you need to run super complicate logic in Python, and you need split your code
  into modules and create a Python library for it, this is the solution.

  You should create a bash script to prepare the Python virtualenv,
  then explicitly use the virtualenv Python interpreter to run your scripts.
  Please read the sample ``complicated_script.sh`` for more details.
  ----------------------------------------------------------------------------*/
  provisioner "shell" {
    script = "complicated_script.sh"
  }
}