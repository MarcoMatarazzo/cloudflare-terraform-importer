#!/usr/bin/env python2

#
# LICENSE: MIT
#
# Copyright (C) 2018 Marco Matarazzo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import requests
import configparser

def main():
    global headers
    
    read_config()

    headers = {
        "X-Auth-Email": cf_email,
        "X-Auth-Key": cf_key
    }

    try:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    except:
        print "Error while creating output directory."
        exit()

    provider_file = open('%s/provider.tf' % outdir, "w")
    provider_file.write( 'provider "cloudflare" {\n')
    provider_file.write( '    email = "%s"\n' % cf_email )
    provider_file.write( '    token = "%s"\n' % cf_key )
    provider_file.write( '}\n')
    provider_file.close()

    zones = get_cf_data( 'zones' )

    for zone in zones:
        # print "* Zone found: %s (id: %s)" % (zone['name'], zone['id'])
        zone_file = open('%s/%s.tf' % ( outdir, zone['name'] ), "w")
        import_file = open('%s/import-%s.sh' % ( outdir, zone['name'] ), "w")
        import_file.write( '#!/bin/bash\n\n' )
        records = get_cf_data( 'zones/%s/dns_records' % zone['id'] )
        for record in records:
            # print "  - Record found: %s %s %s %s" % ( record['type'], record['name'], record['content'], record['priority'] if record['type'] == 'MX' else '')
            record_name = "%s-%s" % ( record['name'].replace('.','_').replace('*','STAR'), record['id'] ) # This can be made better according to your tastes
            zone_file.write( 'resource "cloudflare_record" "%s" {\n' % record_name )
            zone_file.write( '  domain  = "%s"\n' % zone['name'] )
            zone_file.write( '  name    = "%s"\n' % record['name'].replace(".%s" % zone['name'],'') )
            zone_file.write( '  value   = "%s"\n' % record['content'].replace(".%s" % zone['name'],'') )
            zone_file.write( '  type    = "%s"\n' % record['type'] )
            if record['type'] == 'MX':
                zone_file.write( '  priority = "%s"\n' % record['priority'] ) 
            zone_file.write( '  ttl     = %s\n' % record['ttl'] )
            zone_file.write( '  proxied = %s\n' % ('true' if record['proxied'] else 'false') )
            zone_file.write( '}\n')
            zone_file.write( '\n')
            import_file.write( 'terraform import cloudflare_record.%s %s/%s\n' % ( record_name, zone['name'], record['id'] ) )
        zone_file.close()
        import_file.close()
    
    print "All files created in directory %s." % outdir

def read_config():
    global cf_email
    global cf_key
    global outdir
    
    config = configparser.ConfigParser()
    
    try:
        config.read('config.ini')
        cf_email = config.get('cloudflare', 'email')
        cf_key = config.get('cloudflare', 'key')
        outdir = config.get('output', 'dir_name')
    except:
        print "Error while reading configuration file."
        exit()
    
def get_cf_data( api ):
    page = 1
    total_pages = 999
    result = []
    params = "?page=1&per_page=100"
    
    while page < total_pages:
        url = 'https://api.cloudflare.com/client/v4/%s%s' % ( api, params )
        # print "  Calling %s..." % url
        
        try:
            r = requests.get( url, headers=headers ).json()
        except:
            print "Error while calling API."
            exit()
    
        success = r['success']
        if success is False:
            print "Error in API answer."
            exit()
        
        count = int(r['result_info']['count'])
        total_count = int(r['result_info']['total_count'])
        page = int(r['result_info']['page'])
        total_pages = int(r['result_info']['total_pages'])
        # print "  Got %d/%d results." % ( count, total_count )

        params = "?page=%d&per_page=100" % (page+1)
        result += r['result']
    
    return result

if __name__ == '__main__':
    main()