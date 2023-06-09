# -*- coding: utf-8 -*-

"""
**"Runtime" Definition**

Runtime is where you execute your code. For example, if this code is running
in a CI build environment, then the runtime is "ci". If this code is running
on your local laptop, then the runtime is "local". If this code is running on
AWS Lambda, then the runtime is "lambda"

This module automatically detect what is the current runtime.

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import os
import enum
from pathlib import Path


class RunTimeEnum(str, enum.Enum):
    local = "loc"
    local_unit_test = "loc_utest"
    local_int_test = "loc_itest"
    ci = "ci"
    ci_unit_test = "ci_utest"
    ci_int_test = "ci_itest"
    ec2 = "ec2"
    unknown = "unknown"


CURRENT_RUNTIME: str = RunTimeEnum.unknown

IS_LOCAL: bool = False
IS_LOCAL_UNIT_TEST: bool = False
IS_LOCAL_INT_TEST: bool = False
IS_CI: bool = False
IS_CI_UNIT_TEST: bool = False
IS_CI_INT_TEST: bool = False
IS_EC2: bool = False

# if you use AWS CodeBuild for CI/CD
# ref: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
if "CODEBUILD_CI" in os.environ:  # pragma: no cover
    IS_CI = True

    if "PYTEST_UNIT_TEST" in os.environ:
        CURRENT_RUNTIME = RunTimeEnum.ci_unit_test.value
        IS_CI_UNIT_TEST = True
    elif "PYTEST_INT_TEST" in os.environ:
        CURRENT_RUNTIME = RunTimeEnum.ci_int_test.value
        IS_CI_INT_TEST = True
    else:
        CURRENT_RUNTIME = RunTimeEnum.ci.value
elif str(Path.home().absolute()) in [
    "/home/ec2-user",
    "/home/ubuntu",
]:
    IS_EC2 = True
    CURRENT_RUNTIME = RunTimeEnum.ec2.value
# if you use GitHub CI for CI/CD
# ref: https://docs.github.com/en/actions/learn-github-actions/variables
# if you use Circle CI for CI/CD
# ref: https://circleci.com/docs/variables/
else:  # pragma: no cover
    IS_LOCAL = True
    if "PYTEST_UNIT_TEST" in os.environ:
        CURRENT_RUNTIME = RunTimeEnum.local_unit_test.value
        IS_LOCAL_UNIT_TEST = True
    elif "PYTEST_INT_TEST" in os.environ:
        CURRENT_RUNTIME = RunTimeEnum.local_int_test.value
        IS_LOCAL_INT_TEST = True
    else:
        CURRENT_RUNTIME = RunTimeEnum.local.value
        IS_LOCAL = True
