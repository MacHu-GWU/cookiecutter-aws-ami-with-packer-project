``aws-ami-with-packer-project``
==============================================================================
This is a project template that can manage mass amount of EC2 AMI images building using packer. You can easily generate a project skeleton for your own project.


Usage
------------------------------------------------------------------------------
Enter the following command, it will use the latest template.

.. code-block:: bash

    pip install cookiecutter
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-ami-with-packer-project

Or, you can use a specific released version, you can find `full list of release at here <https://github.com/MacHu-GWU/cookiecutter-aws-ami-with-packer-project/releases>`_.

.. code-block:: bash

    # use specific version
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-ami-with-packer-project --checkout tags/${version}
    # for example (v1 is the latest as of 2023-03-19)
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-ami-with-packer-project --checkout tags/v1

Then fill in some information::

    package_name [my_package]: ...
    author_name [Firstname Lastname]: ...
    author_email [firstname.lastname@email.com]: ...
    ...
