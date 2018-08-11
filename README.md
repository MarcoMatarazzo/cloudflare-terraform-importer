# CloudFlare Terraform Importer Primer

This script uses CloudFlare API to read your current zones and records, and generates all the necessary files to import them in Terraform without the need to write .tf files from scratch.

## Usage

The project is pretty simple and straightforward, and should only require plain Python 2.x - and Terraform knowledge, that is outside the scope of this README.

### Configuration

Create your configuration from the sample:

    cp config.ini.sample config.ini

Then, add your CloudFlare email and api key (read [here](https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-) if you don't know how to find them). 

You can also change the directory in which all files will get created. Default is *./tf_output_*.

### Generating the files

You can simply run the script with:

    ./init.py

It will create all files in the output directory, that will then contain:
* one zone_name.tf file for each zone
* one import-zone_name.sh shell script to actually import the enumerated resources in your .tfstate

### Import into Terraform

At this point, you will just need to move the files in your terraform directory and execute the shell scripts (you will need to make them executable).

Note: if you choose to have better resource names in your .tf files, you will have to also change them in the corresponding import script(s).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
