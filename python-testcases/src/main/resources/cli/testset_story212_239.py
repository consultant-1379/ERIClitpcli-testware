#!/usr/bin/env python

"""
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     April 2016
@author:    Terry Farrell
@summary:   Integration test for "litp import --help" & "litp import -h" and
            "litp export --help" & "litp export -h"
            Agile: STORY LITPCDS-212 and LITPCDS-239
"""

from litp_generic_test import GenericTest, attr
from litp_cli_utils import CLIUtils
from litp_generic_utils import GenericUtils
import test_constants as consts


class Story212Story239(GenericTest):
    """
    As a system admin I want to export and import the current deployment model
    to an XML file(s) so that I can use it as a basis for a future deployment
    """

    def setUp(self):
        """ Runs before every single test """
        super(Story212Story239, self).setUp()
        self.test_node = self.get_management_node_filename()
        self.cli = CLIUtils()
        self.gen_utils = GenericUtils()

    def tearDown(self):
        """ Runs after every single test """
        super(Story212Story239, self).tearDown()

    @attr('all', 'revert', 'tooltest', 'story212_239', 'story212_239_tc11')
    def test_11_p_export_help(self):
        """
         @tms_id: litpcds_212_239_tc11
         @tms_requirements_id: LITPCDS-212,LITPCDS-239
         @tms_title: litp export help
         @tms_description: Verify litp export help command
         @tms_test_steps:
             @step: Execute litp export -h command
             @result: The output contains expected text
             @step: Execute litp export --help command
             @result: The output contains expected text
         @tms_test_precondition: NA
         @tms_execution_type: Automated
        """
        usage = 'litp export [-h] -p PATH [-f FILE] ' \
                'Exports the deployment model to a local XML file.'.\
                replace(' ', '')
        required_arguments = '-p PATH, --path PATH  Location of item in ' \
                             'the LITP model'.replace(' ', '')
        optional_arguments = '-h, --help Show this help message and exit' \
                             '-f FILE, --file FILE  XML file to which to ' \
                             'export'.replace(' ', '')
        example = 'litp export -p /deployments/dep1 -f dep1.xml'.\
                  replace(' ', '')

        export_cmds = ["{0} {1} {2}".format(self.cli.litp_path,
                                            "export", "-h"),
                       "{0} {1} {2}".format(self.cli.litp_path,
                                            "export", "--help")]

        for index, cmd in enumerate(export_cmds):
            self.log('info', '{0}. Execute: {1}'.format(index + 1, cmd))
            stdout = self.run_command(self.test_node, cmd,
                                      add_to_cleanup=False,
                                      logging=False,
                                      default_asserts=True)[0]
            self.assertNotEqual(stdout, [], "Standard output is empty")

            self.assertEqual(self.gen_utils.get_text_in_help(stdout, 'Usage'),
                             usage,
                             'Usage string did not match')
            self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                             'Required Arguments'),
                             required_arguments,
                             'Required Arguments string did not match')
            self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                             'Optional Arguments'),
                             optional_arguments,
                             'Optional Arguments string did not match')
            self.assertEqual(self.gen_utils.get_text_in_help(
                             stdout,
                             'Example'),
                             example,
                             'Example string did not match')

    @attr('all', 'revert', 'tooltest', 'story212_239', 'story212_239_tc13')
    def test_13_p_import_help(self):
        """
         @tms_id: litpcds_212_239_tc13
         @tms_requirements_id: LITPCDS-212,LITPCDS-239
         @tms_title: litp import help
         @tms_description: Verify litp import help command
         @tms_test_steps:
             @step: Execute litp import -h command
             @result: The output contains expected text
             @step: Execute litp import --help command
             @result: The output contains expected text
         @tms_test_precondition: NA
         @tms_execution_type: Automated
        """
        usage = 'litp import [-h] [-j] source_path destination_path' \
                'Imports packages into Yum repositories.'.replace(' ', '')
        required_arguments = ' source_path Absolute path with rpm packages.' \
                             ' This can be a single RPM or a directory' \
                             ' of RPMs. destination_path  Absolute path to ' \
                             'destination repo directory or one of "litp" ' \
                             'or "3pp_rhel7" to import RPMs into the LITP or' \
                             ' 3PP repo. This should be used for LITP RPMs ' \
                             'only.'.\
                             replace(' ', '')
        optional_arguments = '-h, --help Show this help message and exit' \
                             '-j, --json Output raw JSON response from ' \
                             'server'.replace(' ', '')
        example = 'litp import /mnt/rhel-iso {0}os litp import' \
                  ' /root/libyaml-0.1.3-1.el7.x86_64.rpm {1}/'.\
                  replace(' ', '').format(consts.PARENT_PKG_REPO_DIR,
                                          consts.PP_PKG_REPO_DIR)

        import_cmds = ["{0} {1} {2}".format(self.cli.litp_path,
                                            "import", "-h"),
                       "{0} {1} {2}".format(self.cli.litp_path,
                                            "import", "--help")]

        for index, cmd in enumerate(import_cmds):
            self.log('info', '{0}. Execute: {1}'.format(index + 1, cmd))
            stdout = self.run_command(self.test_node, cmd,
                                      add_to_cleanup=False,
                                      logging=False,
                                      default_asserts=True)[0]
            self.assertNotEqual(stdout, [], "Standard output is empty")

            self.assertEqual(self.gen_utils.get_text_in_help(stdout, 'Usage'),
                             usage,
                             'Usage string did not match')
            self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                             'Required Arguments'),
                             required_arguments,
                             'Required Arguments string did not match')
            self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                             'Optional Arguments'),
                             optional_arguments,
                             'Optional Arguments string did not match')
            self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                             'Examples'),
                             example,
                             'Examples string did not match')
