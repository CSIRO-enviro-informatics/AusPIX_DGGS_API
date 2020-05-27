variable "public_key_path" {
  description = "Public key path"
  default = "~/.ssh/id_rsa.pub"
}

provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_instance" "auspix_dggs_api_ec2" {
  ami           = "ami-03ed5bd63ba378bd8"
  instance_type = "t2.micro"
  key_name = "${aws_key_pair.minimal-test-key.key_name}"
  /*user_data = <<-EOF
      #! /bin/bash
      echo "TRIPLESTORE_CACHE_URL=${var.triplestore_cache_url}" >> /etc/environment
    EOF*/
}

data "aws_ami" "ec2-ami" {
  owners = ["self"]
  filter {
    name   = "state"
    values = ["available"]
  }
  filter {
    name   = "name"
    values = ["auspix-dggs-api-image*"]
  }
  most_recent = true
}

resource "aws_key_pair" "minimal-test-key" {
  key_name = "minimal-test-key"
  public_key = "${file(var.public_key_path)}"
}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = "${aws_instance.auspix_dggs_api_ec2.id}"
  allocation_id = "${var.eip_allocation_id}"
}

output "public_dns_name" {
    value = aws_instance.minimal-test.public_dns 
}
