"""
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     March 2014
@author:    Padraic Doyle
@summary:   Integration tests: As a LITP admin I want to snapshot LVM
            volumes present in my deployment when I am doing maintenance
            operations so that I can revert to them later on.
            Agile: LITPCDS-2115
"""
from litp_generic_test import GenericTest, attr
from litp_cli_utils import CLIUtils


class Story2115(GenericTest):
    """
    As a LITP admin I want to snapshot LVM volumes present in my
    deployment when I am doing maintenance operations so that
    I can revert to them later on.
    """
    def setUp(self):
        """ Runs before every single test """
        super(Story2115, self).setUp()
        self.ms_node = self.get_management_node_filenames()[0]
        self.mn_nodes = self.get_managed_node_filenames()
        self.cli = CLIUtils()
        self.template_str = "{0}Createsandexecutesasetoftasks(aplan)that" \
                            "isusedto{1}filesystemsnapshots."

    def tearDown(self):
        """ Runs after every single test """
        super(Story2115, self).tearDown()

    @staticmethod
    def format_str_no_whitespace(cmd_output):
        """
        Description:
            Converts a list to a string and removes all whitespace
                characters
        Args:
            cmd_output (list): Output of the help command to be converted
        """
        return "".join(cmd_output).replace(' ', '')

    @attr('all', 'revert', 'story2115', 'story2115_tc01')
    def test_01_p_create_snapshot_cmd_help(self):
        """
        @tms_id: litpcds_2115_tc01
        @tms_requirements_id: LITPCDS-2115
        @tms_title: 'litp create_snapshot' command help
        @tms_description: Verify that a user can view
            help for the 'litp create_snapshot' command.
        @tms_test_steps:
            @step: Execute 'litp --help' on MS
            @result: Output contains expected info about create_snapshot
            @step: Execute 'litp create_snapshot --help' on MS
            @result: Output contains expected info about create_snapshot
            @step: Execute 'litp -h' on MS
            @result: Output contains expected info about create_snapshot
            @step: Execute 'litp create_snapshot -h' on MS
            @result: Output contains expected info about create_snapshot
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log("info", "1. Run 'litp --help'")
        cmd = self.cli.get_help_cmd()
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify create_snapshot action "
                         "is listed with a summary")
        create_msg = "create_snapshotCreatesandexecutesasetoftasks" \
                     "(aplan)usedtocreatefilesystemsnapshots."
        help_str = self.format_str_no_whitespace(out)
        self.assertTrue(create_msg in help_str,
                        '{0} not in {1}'.format(create_msg, help_str))

        self.log("info", "2. Run 'litp create_snapshot --help'")
        cmd = self.cli.get_help_cmd(help_action='create_snapshot')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that description is provided for "
                         "create_snapshot action, including 'Usage', "
                         "'Arguments', and an example.")
        usage_strs = ["Usage: litp create_snapshot [-h] "
                      "[-n NAME [-e EXCLUDE_NODES]] [-j]",
                      "Optional Arguments:", "Example: litp create_snapshot"]
        for usage_str in usage_strs:
            self.assertTrue(self.is_text_in_list(usage_str, out),
                            "{0} not found in 'litp create_snapshot --help' "
                            "output".format(usage_str))

        self.log("info", "3. Run 'litp -h'")
        cmd = self.cli.get_help_cmd(help_arg='-h')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that create_snapshot action is "
                         "listed with a summary.")
        create_msg = "create_snapshotCreatesandexecutesasetoftasks" \
        "(aplan)usedtocreatefilesystemsnapshots."
        help_str = self.format_str_no_whitespace(out)
        self.assertTrue(create_msg in help_str,
                        '{0} not in {1}'.format(create_msg, help_str))

        self.log("info", "4. Run 'litp create_snapshot -h'")
        cmd = self.cli.get_help_cmd(help_arg='-h',
                                    help_action='create_snapshot')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that description is provided for "
                         "create_snapshot action, including 'Usage', "
                         "'Arguments', and an example.")
        for usage_str in usage_strs:
            self.assertTrue(self.is_text_in_list(usage_str, out),
                            "{0} not found in 'litp create_snapshot -h' "
                            "output".format(usage_str))

    @attr('all', 'revert', 'story2115', 'story2115_tc02')
    def test_02_p_remove_snapshot_cmd_help(self):
        """
        @tms_id: litpcds_2115_tc02
        @tms_requirements_id: LITPCDS-2115
        @tms_title: 'litp remove_snapshot' command help
        @tms_description: Verify that a user can view
            help for the 'litp remove_snapshot' command.
        @tms_test_steps:
            @step: Execute 'litp --help' on MS
            @result: Output contains expected info about remove_snapshot
            @step: Execute 'litp remove_snapshot --help' on MS
            @result: Output contains expected info about remove_snapshot
            @step: Execute 'litp -h' on MS
            @result: Output contains expected info about remove_snapshot
            @step: Execute 'litp remove_snapshot -h' on MS
            @result: Output contains expected info about remove_snapshot
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log("info", "1. Run 'litp --help'")
        cmd = self.cli.get_help_cmd()
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify remove_snapshot action "
                         "is listed with a summary")
        remove_msg = self.template_str.format("remove_snapshot", "remove")
        help_str = self.format_str_no_whitespace(out)
        self.assertTrue(remove_msg in help_str,
                        '{0} not in {1}'.format(remove_msg, help_str))

        self.log("info", "2. Run 'litp remove_snapshot --help'")
        cmd = self.cli.get_help_cmd(help_action='remove_snapshot')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that description is provided for "
                         "remove_snapshot action, including 'Usage', "
                         "'Arguments', and an example.")
        usage_strs = ["Usage: litp remove_snapshot [-h] "
                      "[-n NAME [-e EXCLUDE_NODES]] [-j] [-f]",
                      "Optional Arguments:", "Example: litp remove_snapshot"]
        for usage_str in usage_strs:
            self.assertTrue(self.is_text_in_list(usage_str, out),
                            "{0} not found in 'litp remove_snapshot --help' "
                            "output".format(usage_str))

        self.log("info", "3. Run 'litp -h'")
        cmd = self.cli.get_help_cmd(help_arg='-h')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that remove_snapshot action is "
                         "listed with a summary.")
        remove_msg = self.template_str.format("remove_snapshot", "remove")
        help_str = self.format_str_no_whitespace(out)
        self.assertTrue(remove_msg in help_str,
                        '{0} not in {1}'.format(remove_msg, help_str))

        self.log("info", "4. Run 'litp remove_snapshot -h'")
        cmd = self.cli.get_help_cmd(help_arg='-h',
                                    help_action='remove_snapshot')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that description is provided for "
                         "remove_snapshot action, including 'Usage', "
                         "'Arguments', and an example.")
        for usage_str in usage_strs:
            self.assertTrue(self.is_text_in_list(usage_str, out),
                            "{0} not found in 'litp remove_snapshot -h' "
                            "output".format(usage_str))

    @attr('all', 'revert', 'story2115', 'story2115_tc03')
    def test_03_p_restore_snapshot_cmd_help(self):
        """
        @tms_id: litpcds_2115_tc03
        @tms_requirements_id: LITPCDS-2115
        @tms_title: 'litp restore_snapshot' command help
        @tms_description: Verify that a user can view
            help for the 'litp restore_snapshot' command.
        @tms_test_steps:
            @step: Execute 'litp --help' on MS
            @result: Output contains expected info about restore_snapshot
            @step: Execute 'litp restore_snapshot --help' on MS
            @result: Output contains expected info about restore_snapshot
            @step: Execute 'litp -h' on MS
            @result: Output contains expected info about restore_snapshot
            @step: Execute 'litp restore_snapshot -h' on MS
            @result: Output contains expected info about restore_snapshot
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log("info", "1. Run 'litp --help'")
        cmd = self.cli.get_help_cmd()
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify restore_snapshot action "
                         "is listed with a summary")
        restore_msg = self.template_str.format("restore_snapshot", "restore")
        help_str = self.format_str_no_whitespace(out)
        self.assertTrue(restore_msg in help_str,
                        '{0} not in {1}'.format(restore_msg, help_str))

        self.log("info", "2. Run 'litp restore_snapshot --help'")
        cmd = self.cli.get_help_cmd(help_action='restore_snapshot')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that description is provided for "
                         "restore_snapshot action, including 'Usage', "
                         "'Arguments', and an example.")
        usage_strs = ["Usage: litp restore_snapshot [-h] [-j] [-f]",
                      "Optional Arguments:", "Example: litp restore_snapshot"]
        for usage_str in usage_strs:
            self.assertTrue(self.is_text_in_list(usage_str, out),
                            "{0} not found in 'litp restore_snapshot --help' "
                            "output".format(usage_str))

        self.log("info", "3. Run 'litp -h'")
        cmd = self.cli.get_help_cmd(help_arg='-h')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that restore_snapshot action is "
                         "listed with a summary.")
        restore_msg = self.template_str.format("restore_snapshot", "restore")
        help_str = self.format_str_no_whitespace(out)
        self.assertTrue(restore_msg in help_str,
                        '{0} not in {1}'.format(restore_msg, help_str))

        self.log("info", "4. Run 'litp restore_snapshot -h'")
        cmd = self.cli.get_help_cmd(help_arg='-h',
                                    help_action='restore_snapshot')
        out = self.run_command(self.ms_node, cmd, default_asserts=True)[0]

        self.log("info", "Verify that description is provided for "
                         "restore_snapshot action, including 'Usage', "
                         "'Arguments', and an example.")
        for usage_str in usage_strs:
            self.assertTrue(self.is_text_in_list(usage_str, out),
                            "{0} not found in 'litp restore_snapshot -h' "
                            "output".format(usage_str))
