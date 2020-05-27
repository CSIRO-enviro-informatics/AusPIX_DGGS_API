Initiate AWS credentials


note - you'll need appropriate certificates for your site at ../../../certs relative to the packer directory
note - the Caddyfile is coded to expect a *.loci.cat site you'll like need to change this

In the packer directory, run this to get packer to build a new AMI

```
$ packer build loci-auspix-dggs-api-image.json
```

Run this in the terraform directory to bring up the dggs api 

```
$ terraform apply loci-auspix-dggs-api-image.json
```

