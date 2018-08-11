# CloudFlare Terraform Importer Primer

A script that reads your CloudFlare data and generates the necessary files to import them in Terraform.

It works by connecting to CloudFlare API and generating both .tf files (so you don't have to write them from scratch) and some import scripts that will use Terraform import capabilities to populate your .tfstate.

## Installation

    git clone https://github.com/MarcoMatarazzo/cloudflare-terraform-importer.git

That's it.

## Requirements

You should only require plain Python 2.x on a Linux box - and Terraform knowledge, that is outside the scope of this README.

## Usage

## A Warning in advance

__BACKUP YOUR TERRAFORM FILE, ESPECIALLY YOUR .TFSTATE FILE__ before using this script.

You should be already doing it, but you know, better safe than sorry.

Let me repeat myself: __BACKUP YOUR FILES__ before using this script.

### Configuration

Create your configuration from the sample:

    cp config.ini.sample config.ini

Then, add your CloudFlare email and api key (read [here](https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-) if you don't know how to find them). 

You can also change the directory in which all files will get created. Default is _./tf_output_.

### Generating the files

Run the script with:

    ./init.py

It will create all files in the output directory, that will then contain:
* one zone_name.tf file for each zone
* one import-zone_name.sh shell script to actually import the enumerated resources in your .tfstate

You probably want to make the shell script executable:

    chmod +x *.sh

### Import into Terraform

Move the files in your terraform directory. 

You may want to reorganize the .tf files, depending on your situation. Note that if you change resource names, you will have to also change them in the corresponding import script(s). A better idea could be to slightly edit the python script to generate a more fitting resource name.

After that, execute the shell scripts that will import the resources. They will execute multiple `terraform import` with the needed parameters for your newly added resources.

You can then check that everything is ok with `terraform plan`.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
