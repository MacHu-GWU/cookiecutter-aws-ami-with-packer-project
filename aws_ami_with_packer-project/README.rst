aws_ami_with_packer
==============================================================================


About this project
------------------------------------------------------------------------------
This project is an example projects that can manage mass amount of EC2 AMI image build using packer.

Please move to the `amis/example <./amis/example>`_ directory and read the ``README.rst`` file for the tutorial.


Be careful when you deregister an AMI
------------------------------------------------------------------------------
Be careful when you deregister an AMI from the console, the underlying snapshot will not be automatically deleted, it still cost you money. You cannot undo deregister an AMI, but you can create a new AMI from the snapshot. If you are 100% sure the snapshot will not be used, you can delete that. Note that the snapshot costs 0.05GB / month. AWS has an "Archive" tier for in-frequently used snapshots, which is 0.0125GB / month, but is has 0.03GB of data retrieved, in other word, if you will not use an image in the next month, you should consider using the "Archive" tier.

Reference:

- How can I recover an accidentally deleted AMI?
: https://aws.amazon.com/premiumsupport/knowledge-center/recover-ami-accidentally-deleted-ec2/#:~:text=It%20isn't%20possible%20to,launched%20from%20the%20deleted%20AMI.
- EBS Pricing: https://aws.amazon.com/ebs/pricing/
- Archive Amazon EBS snapshots: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_snapshot_tier.html#
