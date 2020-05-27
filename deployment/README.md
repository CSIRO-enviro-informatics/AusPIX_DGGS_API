Initiate AWS credentials


note - a valid elastic ip address is required and should be in a new `secrets.tf` file in the terraform directory like (replacing square brackets stuff):
```
variable "eip_allocation_id" {
    default = "eipalloc-[rest of eipallocid]"
}
```
note - a valid dns entry corresponding pointing at the AWS ip and Caddyfile correctly configured, see below 
note - you'll need appropriate certificates for your site at ../../../certs relative to the packer directory
note - the Caddyfile is coded to expect a dns name like *.loci.cat site you'll like need to change this to your name

In the packer directory, run this to get packer to build a new AMI

```
$ packer build loci-auspix-dggs-api-image.json
```

Run this in the terraform directory to bring up the dggs api 

```
$ terraform apply loci-auspix-dggs-api-image.json
```

