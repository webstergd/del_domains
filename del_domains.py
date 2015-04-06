from optparse import OptionParser

from crits.core.basescript import CRITsBaseScript
from crits.core.class_mapper import class_from_value


class CRITsScript(CRITsBaseScript):
    def __init__(self, username=None):
        self.username = username

    def print_delete_objects(self, object_list):
        print "\nObjects to delete:\n---------------"
        for object_name in object_list:
            print "    [+] {0}".format(object_name)
        print "\n"

    def print_found_objects(self, object_list, error_list):
        print "\nObjects found to delete:\n---------------"
        for object_name in object_list:
            print "    [+] {0}".format(object_name)
        print "\n"
        print "\nObjects not found to delete:\n---------------"
        for object_name in error_list:
            print "    [+] {0}".format(object_name)
        print "\n"

    def run_analysis_cleanup(self, obj_list, delay):
        for obj in obj_list:

            ###
            # How do I find the task_id
            ###
            #delete_analysis(task_id, self.username)
            Service.objects(obj.id, obj._meta['crits_type']).delete())

            ###
            # Add delay
            ###
            run_triage(obj)


    def run(self, argv):
        parser = OptionParser()
        parser.add_option('-d', '--domain', dest='domain', help='domain list')
        parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                            default=False,
                            help='Verbose mode')
        parser.add_option('-T', '--type', dest='type_', default='Domain',
                            help='CRITs type query for (default: Domain)')
        (opts, args) = parser.parse_args(argv)

        domain_list = []
        if opts.domain:
            domain_list = opts.services.split(',')
            if opts.verbose:
                self.print_delete_objects(domain_list)


        error_list = []
        for domain in domain_list
            #domain_obj = Domain.objects(domain_iexact=domain).first()
            obj = class_from_value(opts.type_, domain)
            if not obj:
                error_list.append(domain)
            obj_list.append(obj)
        if opts.verbose:
            self.print_object_stats(obj_list, error_list)

        run_cleanup(obj_list, 1)
        print("Done!")
