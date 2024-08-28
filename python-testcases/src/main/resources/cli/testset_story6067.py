"""
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     February 2015
@author:    Maurizio, Maria
@summary:   Integration test for LITPCDS-6067
            Agile:
            Epic: N/A
            Story: LITPCDS-6067:
                As a LITP administrator in a disaster recovery situation
                I want to be able to restore my deployment from the MS
                and a backed up version of the model
            Sub-Task: LITPCDS-8334
            Story: TORF-184851
                As a LITP User I want the ability to reinstall
                a peer node that is already deployed
"""
from litp_generic_test import GenericTest, attr


class Story6067(GenericTest):
    """
        LITPCDS-6067:
        As a LITP administrator in a disaster recovery situation
        I want to be able to restore my deployment from the MS
        and a backed up version of the model.
    """

    def setUp(self):
        """Runs before every test to perform required setup"""
        super(Story6067, self).setUp()
        self.ms_node = self.get_management_node_filename()
        self.node_url = self.find(self.ms_node, '/deployments', 'node')[0]
        self.item_type = 'story6067'

    def tearDown(self):
        """Runs after every test to perform required cleanup/teardown"""
        super(Story6067, self).tearDown()

    def check_for_error(self, stderr, error_type):
        """
        Description:
            Check that "ValidationError" is in given error message.
        Args:
            stderr (list): Error messages returned by CLI command
            error_type (str): Expected error type
        """
        self.assertTrue(self.is_text_in_list(error_type, stderr),
                        '{0} not found on error message {1}'.format(
                            error_type, stderr))

    def check_prepare_restore_is_on_help(self, cmd, stdout):
        """
        Description:
            Check that help menu contains prepare_restore command.
        Args:
            cmd (str): Help command string used
            stdout (list): Help command output
        """
        self.assertTrue(self.is_text_in_list('prepare_restore', stdout),
                        'prepare_restore is not in {0}'.format(cmd))

    def check_prepare_restore_help_has_usage(self, cmd, stdout):
        """
        Description:
            Check that prepare_restore help contains usage instructions.
        Args:
            cmd (str): Help command string used
            stdout (list): Help command output
        """
        usage = "Usage: litp prepare_restore [-h] [-j] [-p PATH]"
        self.assertTrue(self.is_text_in_list(usage, stdout),
                        "Usage is not in {0}".format(cmd))

    @attr('all', 'revert', 'story6067', 'story6067_tc09')
    def test_09_n_prepare_restore_with_path(self):
        """
        @tms_id: litpcds_6067_tc09
        @tms_requirements_id: LITPCDS-6067
        @tms_title: Test "prepare_restore" command with invalid arguments
        @tms_description:
            Verify that when user runs "litp prepare_restore" specifying
            option to valid path, command is successful.
            When user runs "litp update -p /litp/prepare-restore" specifying
            option to a path that is not a node, "ValidationError" is thrown
        @tms_test_steps:
            @step: Execute 'litp prepare_restore -p /'
            @result: Command runs successfully with no errors returned
            @step: Execute 'litp prepare_restore -p <PATH TO NODE>'
            @result: Command runs successfully with no errors returned
            @step: Execute 'litp prepare_restore -o path="/"'
            @result: "unrecognized arguments" error thrown
            @step: Execute 'litp prepare_restore -o path="/"'' command
            @result: "unrecognized arguments" error is thrown
            @step: Execute "litp update -p /litp/prepare-restore -o path='/ms'"
            @result: ValidationError thrown
            @step: Execute "litp update -p /litp/prepare-restore
                   -o path='/deployment'"
            @result: ValidationError thrown
            @step: Execute 'litp restore_model'
            @result: Model restored successfully
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        cmd_args = ['-p /', '-p {0}'.format(self.node_url)]
        for arg in cmd_args:
            _, stderr, rc = self.execute_cli_prepare_restore_cmd(
                self.ms_node, arg)
            self.assertEqual(0, rc)
            self.assertEqual([], stderr)

        _, stderr, rc = self.execute_cli_prepare_restore_cmd(
                self.ms_node, '-o path="/"', expect_positive=False)
        self.check_for_error(stderr, 'unrecognized arguments')

        val_error = "ValidationError in property: \"path\"    " \
                    "Item is not a node '{0}'"
        non_node_paths = ['/ms', '/deployments']
        for path in non_node_paths:
            _, stderr, _ = self.execute_cli_update_cmd(
                self.ms_node, url='/litp/prepare-restore',
                props='path="{0}"'.format(path), expect_positive=False)
            self.check_for_error(stderr, val_error.format(path))

        self.execute_cli_restoremodel_cmd(self.ms_node)

    @attr('all', 'revert', 'story6067', 'story6067_tc11')
    def test_11_p_prepare_restore_help(self):
        """
        @tms_id: litpcds_6067_tc11
        @tms_requirements_id: LITPCDS-6067
        @tms_title: Verify help for 'prepare_restore' command
        @tms_description:
            This test will verify that litp help shows description
            of the "prepare_restore" command and that litp prepare_restore
            help shows usage of the "prepare_restore" command
        @tms_test_steps:
            @step: Execute 'litp -h' command
            @result: Help output contains description
                of "prepare_restore" command
            @step: Execute 'litp --help' command
            @result: Help output contains description
                of "prepare_restore" command
            @step: Execute "litp prepare_restore -h" command
            @result: Usage of "prepare_restore" command is in output
            @step: Execute "litp prepare_restore --help" command
            @result: Usage of "prepare_restore" command is in output
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        cmd = self.cli.get_help_cmd("-h")
        stdout, _, _ = self.run_command(self.ms_node, cmd)
        self.check_prepare_restore_is_on_help(cmd, stdout)

        cmd = self.cli.get_help_cmd("--help")
        stdout, _, _ = self.run_command(self.ms_node, cmd)
        self.check_prepare_restore_is_on_help(cmd, stdout)

        cmd = self.cli.get_help_cmd("-h", "prepare_restore")
        stdout, _, _ = self.run_command(self.ms_node, cmd)
        self.check_prepare_restore_help_has_usage(cmd, stdout)

        cmd = self.cli.get_help_cmd("--help", "prepare_restore")
        stdout, _, _ = self.run_command(self.ms_node, cmd)
        self.check_prepare_restore_help_has_usage(cmd, stdout)
