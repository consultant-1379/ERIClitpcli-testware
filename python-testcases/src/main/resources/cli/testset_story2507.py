#!/usr/bin/env python

'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     April 2016
@author:    Terry Farrell
@summary:   Integration test for import with --replace argument
            Agile: STORY LITPCDS-2507
'''

from litp_generic_test import GenericTest, attr
from litp_cli_utils import CLIUtils
from litp_generic_utils import GenericUtils


class Story2507(GenericTest):

    '''
    As a LITP administrator I want to be able to import an XML file into an
    existing model so that I can replace the existing model
    with the contents of the file
    '''

    def setUp(self):
        """
        Description:
            Runs before every single test
        Actions:
            1. Set up variables used in the tests
        Results:
            The super class prints out diagnostics and variables
            common to all tests are available.
        """
        super(Story2507, self).setUp()
        # 1. Set up variable used in the tests
        self.test_node = self.get_management_node_filename()
        self.cli = CLIUtils()
        self.gen_utils = GenericUtils()

    def tearDown(self):
        """
        Description:
            Runs after every single test
        Actions:
            1. Perform Test Cleanup
       Results:
            Items used in the test are cleaned up and the
            super class prints out end test diagnostics
        """
        super(Story2507, self).tearDown()

    @attr('all', 'revert', 'tooltest', 'story2507', 'story2507_tc01')
    def test_01_p_load_help(self):

        """
        @tms_id: litpcds_2507_tc01
        @tms_requirements_id: LITPCDS-2507
        @tms_title: load cmd help
        @tms_description: Verify litp 'load --help' and 'load -h' command
        contains expected text
        @tms_test_steps:
        @step: Execute 'litp load -h'
        @result: The output contains expected text
        @step: Execute 'litp load --help'
        @result: The output contains expected text
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        usage = 'litp load [-h] -p PATH -f FILE [--merge | ' \
                '--replace] [-j]Loads the deployment model from a ' \
                'local XML file.'

        required_arguments = '-p PATH, --path PATH  Location of item in ' \
                             'the LITP model -f FILE, --file FILE  XML ' \
                             'file to load'

        optional_arguments = '-h, --help Show this help message and exit' \
                             '--merge Merge XML file into deployment model,' \
                             'creating items which do not exist and updating' \
                             'model values with values from the file ' \
                             '--replace Recreate the active model with ' \
                             'contents of the specified XML file, removing ' \
                             'items not present in the file' \
                             '-j, --json Output raw JSON response from server'

        example = 'litp load -p /infrastructure/networking/' \
                  'networks -f networks.xml'

        self.log('info', '1. Execute the following command: litp load -h')
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "load", "-h")
        stdout, _, _ = self.run_command(self.test_node, cmd,
                                        add_to_cleanup=False, logging=False,
                                        default_asserts=True)
        self.assertEqual(self.gen_utils.get_text_in_help(stdout, 'Usage'),
                         usage.replace(' ', ''), 'Usage string did not match')
        self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                         'Required Arguments'),
                         required_arguments.replace(' ', ''),
                         'Required Arguments string did not match')
        self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                         'Optional Arguments'),
                         optional_arguments.replace(' ', ''),
                         'Optional Arguments string did not match')
        self.assertEqual(self.gen_utils.get_text_in_help(stdout, 'Example'),
                         example.replace(' ', ''),
                         'Example string did not match')

        self.log('info', '2. Execute the following command: litp load --help')
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "load", "--help")
        stdout, _, _ = self.run_command(self.test_node, cmd,
                                        add_to_cleanup=False, logging=False,
                                        default_asserts=True)
        self.assertEqual(self.gen_utils.get_text_in_help(stdout, 'Usage'),
                         usage.replace(' ', ''), 'Usage string did not match')
        self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                         'Required Arguments'),
                         required_arguments.replace(' ', ''),
                         'Required Arguments string did not match')
        self.assertEqual(self.gen_utils.get_text_in_help(stdout,
                         'Optional Arguments'),
                         optional_arguments.replace(' ', ''),
                         'Optional Arguments string did not match')
        self.assertEqual(self.gen_utils.get_text_in_help(stdout, 'Example'),
                         example.replace(' ', ''),
                         'Example string did not match')
