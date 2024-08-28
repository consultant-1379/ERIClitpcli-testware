# -*- coding: utf-8 -*-
# coding: utf-8

"""
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     April 2015
@author:    Padraic Doyle, Alejandro Blanco, Artur Daschevici, Lorcan Hamill
@summary:   Integration test for story 4060: As a packager of a product to be
            deployed on LITP I want the contents of my LITP compliant ISO to be
            imported.
            Agile: STORY-4060
"""
from litp_generic_test import GenericTest, attr
from litp_cli_utils import CLIUtils


class Story4060(GenericTest):
    """
    Description:
        I want the contents of my LITP compliant ISO to be imported.
    """

    def setUp(self):
        """ Setup variables for every test """
        super(Story4060, self).setUp()
        self.ms_node = self.get_management_node_filename()
        self.cli = CLIUtils()

    def tearDown(self):
        """ Called after every test"""
        super(Story4060, self).tearDown()

    @attr('all', 'revert', 'story4060', 'story4060_tc39')
    def test_39_p_help_for_the_import_iso_command(self):
        """
        @tms_id:
            litpcds_4060_tc39
        @tms_requirements_id:
            LITPCDS-4026
        @tms_title:
            This test will verify help for the 'import_iso' command
        @tms_description:
            This test will verify help for the 'import_iso' command

        @tms_test_steps:
        @step: Execute "litp --help" command
        @result: "import_iso" command description is in output
        @step: Execute "litp import_iso --help" command
        @result: litp import_iso usage is in output

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        cmd = self.cli.get_help_cmd(help_arg='--help')
        stdout, stderr, returnc = self.run_command(self.ms_node, cmd)
        exp = ("import_iso          "
               "Imports packages and VM images from a LITP-compliant")

        self.assertEquals(0, returnc)
        self.assertEquals([], stderr)
        self.assertTrue(self.is_text_in_list(exp, stdout))

        cmd = self.cli.get_help_cmd(help_arg='--help',
                                    help_action='import_iso')
        stdout, stderr, returnc = self.run_command(self.ms_node, cmd,
                                                   add_to_cleanup=False)
        self.assertEquals(0, returnc)
        self.assertEquals([], stderr)
        self.assertTrue(
            self.is_text_in_list(
                'Usage: litp import_iso [-h] [-j] source_path',
                stdout
            )
        )
