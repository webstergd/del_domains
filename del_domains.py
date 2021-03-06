from optparse import OptionParser

from crits.core.basescript import CRITsBaseScript
from crits.core.class_mapper import class_from_value, class_from_id
from crits.domains.domain import Domain
from crits.services.analysis_result import AnalysisResult
from crits.services.handlers import run_triage

import time
import json


class CRITsScript(CRITsBaseScript):
    def __init__(self, username=None):
        self.username = username

    def print_delete_objects(self, object_list):
        print "\nObjects supplied to clean up:\n---------------"
        for object_name in object_list:
            print "    [+] {0}".format(object_name)
        print "\n"

    def print_found_objects(self, object_list, error_list):
        print "\nObjects found to cleanup:\n---------------"
        for object_name in object_list:
            print "    [+] {0}".format(object_name.id)
        print "\n"
        print "\nObjects not found to cleanup:\n---------------"
        for object_name in error_list:
            print "    [+] {0}".format(object_name)
        print "\n"

    def run_analysis_cleanup(self, obj_list, type_, delay):
        print "\nCleaning Analysis for:\n---------------"
        for obj in obj_list:
            results = AnalysisResult.objects(object_type=type_, object_id=str(obj.id))
            print("    [+] {0}".format(obj.id))

            for result in results:
                result.delete()

            time.sleep(float(delay))
            run_triage(obj, self.username)

    def delete_domains(self, obj_list, type_, delay):
        print "\nDeleting Domains for:\n---------------"
        for obj in obj_list:
            print("    [+] {0}".format(obj.id))
            obj.delete()

            time.sleep(float(delay))


    def run(self, argv):
        parser = OptionParser()
        parser.add_option('-d', '--domain', dest='domain', help='domain')
        parser.add_option('-l', '--domain_list', dest='domain_list', help='domain list')
        parser.add_option('-i', '--id_list', dest='id_list', help='id list')
        parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                            default=False,
                            help='Verbose mode')
        parser.add_option('-T', '--type', dest='type_', default='Domain',
                            help='CRITs type query for (default: Domain)')
        parser.add_option('--delete', dest='delete', action='store_true',
                            default=False,
                            help='Delete Domains')
        parser.add_option('--csv', dest='csv', action='store_true',
                            default=False,
                            help='Treat file as CSV')
        (opts, args) = parser.parse_args(argv)

        domain_list = []
        if opts.domain_list:
            with open(opts.domain_list) as infile:
                for line in infile:
                    if opts.csv:
                        domain_list = [x.strip() for x in line.split(',')]
                    else:
                        domain_list.append(line.strip())
        elif opts.domain:
            domain_list = opts.domain.split(',')
        if opts.verbose:
            self.print_delete_objects(domain_list)

        error_list = []
        obj_list = []
        for domain in domain_list:
            #domain_obj = Domain.objects(domain_iexact=domain).first()
            obj = class_from_value(opts.type_, domain)
            if not obj:
                error_list.append(domain)
            else:
                obj_list.append(obj)
        if opts.verbose:
            self.print_found_objects(obj_list, error_list)

        if opts.id_list:
            with open(opts.id_list) as infile:
                for line in infile:
                    result = json.loads(line.strip())
                    obj = class_from_id(opts.type_, result['object_id'])
                    obj_list.append(obj) 

        if opts.delete:
            self.delete_domains(obj_list, opts.type_, 0.5)
        else:
            self.run_analysis_cleanup(obj_list, opts.type_, 0.5)
        print("Done!")
