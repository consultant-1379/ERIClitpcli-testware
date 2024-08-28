"""
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     June 2014
@author:    Padraic Doyle
@summary:   Integration test for story 2093. As a LITP User I want to upgrade
            RHEL & 3pps on the nodes so that I can apply security patches.
            Agile: STORY_2093
"""

from litp_generic_test import GenericTest, attr
from litp_cli_utils import CLIUtils


class Story2093(GenericTest):
    """
    As a LITP User I want to upgrade RHEL & 3pps on the nodes so that I can
    apply security patches.
    """

    def setUp(self):
        """ Runs before every single test """
        super(Story2093, self).setUp()
        self.cli = CLIUtils()
        self.ms_node = self.get_management_node_filename()

    def tearDown(self):
        """ Runs after every single test """
        super(Story2093, self).tearDown()

    @attr('all', 'revert', 'story2093', '2093_12')
    def test_12_p_a_user_can_view_help_for_the_litp_upgrade_command(self):
        """
        @tms_id: litpcds_2093_tc12
        @tms_requirements_id: LITPCDS-2093
        @tms_title: User can view help for the litp upgrade command
        @tms_description: This test will verify that a user can view help for
            the litp upgrade command.
        @tms_test_steps:
            @step:Execute 'litp --help'
            @result: The output contains expected text
            @step:Execute 'litp -h'
            @result: The output contains expected text
            @step:Execute 'litp upgrade --help'
            @result: The output contains expected text
            @step:Execute 'litp upgrade -h'
            @result: The output contains expected text
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        descriptions = ['Usage: litp upgrade', 'Optional Arguments:',
                        'Example: litp upgrade -p /dep']
        help_args = ['--help', '-h']

        for index, arg in enumerate(help_args, 1):
            self.log('info', '{0}. Execute litp {1} command'
                .format(index, arg))
            cmd = self.cli.get_help_cmd(help_arg=arg)
            out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]
            exp = "upgrade             " \
                "Updates the packages on a defined node or cluster to a"
            self.assertTrue(self.is_text_in_list(exp, out),
                "Expected text not in litp {0} command output".format(arg))

        for index, arg in enumerate(help_args, 3):
            self.log('info', '{0}. Execute litp upgrade {1} command.'
                .format(index, arg))
            cmd = self.cli.get_help_cmd(help_arg=arg, help_action='upgrade')
            out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

            for description in descriptions:
                self.assertTrue(self.is_text_in_list(description, out),
                    "{0} not in {1}".format(description, out))
