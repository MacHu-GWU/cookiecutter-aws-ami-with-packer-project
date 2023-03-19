variable "source_ami_name" {
  type        = string
  description = "What is the ami name of the source image, you can find that in Launch EC2 menu or the AMI Catalog menu."
}

variable "source_ami_owner_account_id" {
  type        = string
  description = "The source ami owner AWS account id, you can find that in Launch EC2 menu or the AMI Catalog menu."
}

variable "output_ami_name" {
  type        = string
  description = "The generated AMI name, it has to be unique in a region."
}
