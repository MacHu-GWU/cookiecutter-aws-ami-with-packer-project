# -*- coding: utf-8 -*-

from s3pathlib import context
from boto_session_manager import BotoSesManager

from .runtime import IS_LOCAL, IS_CI, IS_EC2

# environment aware boto session manager
if IS_LOCAL:
    bsm = BotoSesManager(
        profile_name="my_aws_profile",
        region_name="us-east-1",
    )
elif IS_EC2:
    bsm = BotoSesManager(
        region_name="us-east-1",
    )
elif IS_CI:
    bsm = BotoSesManager(
        region_name="us-east-1",
    )
else:  # pragma: no cover
    raise NotImplementedError

# Set default s3pathlib boto session
context.attach_boto_session(boto_ses=bsm.boto_ses)
