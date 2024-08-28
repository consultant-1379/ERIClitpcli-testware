'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     February 2014
@author:    Kieran Duggan
@summary:   Integration test for utilizing the new REST API
            for all read(show) operations.
Agile:      STORY-630
'''

from litp_generic_test import GenericTest, attr


class Story630(GenericTest):
    """
    As a Product Designer I want the LITP CLI to utilize the new REST API
    for all read operations (show) so that the old interface can be deprecated
    """

    def setUp(self):
        """
        Description:
            Runs before every single test
        Actions:
            1. Call the super class setup method
            2. Set up variables used in the tests
        Results:
            The super class prints out diagnostics and variables
            common to all tests are available.
        """

        # 1. Call super class setup
        super(Story630, self).setUp()

        # 2. Set up variables used in the test
        self.test_node = self.get_management_node_filename()
        self.results = None
        self.setup_cmds = []

    def tearDown(self):
        """
            Description:
                Run after each test and performs the following:
            Actions:
                1. Cleanup after test if global results value has been used
                2. Call the superclass teardown method
            Results:
                Items used in the test are cleaned up and the
                super class prints out end test diagnostics
        """

        # 2. call teardown
        super(Story630, self).tearDown()

    @attr('all', 'revert', 'cdb_priority1')
    def test_01_p_validate_cli_shorthand_commands(self):
        """
        @tms_id: litpcds_630_tc01
        @tms_requirements_id: LITPCDS-630
        @tms_title: validate cli shorthand commands
        @tms_description: Verify the output is not empty when executing show
                        command on node item with shorthand optional argument
        @tms_test_steps:
        @step: Run show command on node item with '-l' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-j' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-r' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-T' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-lj' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-Tj' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-ljr' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-Tjr' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-jr' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-lrn 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-Trn 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-ljrn 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-Tjrn 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '-h' optional argument
        @result: Output is not empty
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        #1. Get node1 path in deployments.
        path = self.find(self.test_node, "/deployments", "node")[0]

        # 2. loop through the list of paths running commands on each of them.
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-l'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-j'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-r'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-T'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-lj'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-Tj'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-lr'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-Tr'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-ljr'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-Tjr'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-jr'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-lrn 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-Trn 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-ljrn 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-Tjrn 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='-jrn 2'))
        self.setup_cmds.append(self.cli.get_show_cmd("/", args='-h'))
        self.results = self.run_commands([self.test_node], self.setup_cmds)

        # 3. assert that the commands were run succussfully
        self.assertEqual([], self.get_errors(self.results))
        self.assertTrue(self.is_std_out_in_all(self.results),
                        "Error std_out is empty for one of the show commands")

    @attr('all', 'revert')
    def test_02_p_validate_cli_long_commands(self):
        """
        @tms_id: litpcds_630_tc02
        @tms_requirements_id: LITPCDS-630
        @tms_title: validate cli shorthand commands
        @tms_description: Verify the output is not empty when executing show
                        command on node item with longhand optional argument
        @tms_test_steps:
        @step: Run show command on node item with '--list' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--json' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--recursive' optional
                argument
        @result: Output is not empty
        @step: Run show command on node item with '--Tree' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--list --json' optional
                argument
        @result: Output is not empty
        @step: Run show command on node item with '--tree --json' optional
                argument
        @result: Output is not empty
        @step: Run show command on node item with '--list --recursion' optional
                argument
        @result: Output is not empty
        @step: Run show command on node item with '--list --json --recursion'
                optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--tree --json --recursion'
                optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--json --recursion' optional
                argument
        @result: Output is not empty
        @step: Run show command on node item with '--list --recursion
                --depth 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--list --json --recursive
                        --depth 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--tree --json '--recursive
                --depth 2' optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--json --recursive--depth 2'
                optional argument
        @result: Output is not empty
        @step: Run show command on node item with '--help' optional argument
        @result: Output is not empty
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        # 1. Get node1 path in deployments.
        path = self.find(self.test_node, "/deployments", "node")[0]

        # 2. Run long cli args commands on node1 path.
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='--list'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='--json'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--recursive'))
        self.setup_cmds.append(self.cli.get_show_cmd(path, args='--tree'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--list --json'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--tree --json'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--list '
                                                          '--recursive'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--tree '
                                                          '--recursive'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--list --json '
                                                          '--recursive'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--tree --json '
                                                          '--recursive'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--json '
                                                          '--recursive'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--list --recursive '
                                                          '--depth 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--tree --recursive '
                                                          '--depth 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--list --json '
                                                          '--recursive '
                                                          '--depth 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--tree --json '
                                                          '--recursive '
                                                          '--depth 2'))
        self.setup_cmds.append(self.cli.get_show_cmd(path,
                                                     args='--json --recursive '
                                                          '--depth 2'))
        self.setup_cmds.append(self.cli.get_show_cmd("/", args='--help'))
        self.results = self.run_commands([self.test_node], self.setup_cmds)

        #3. assert that the commands were run succussfully
        self.assertEqual([], self.get_errors(self.results))
        self.assertTrue(self.is_std_out_in_all(self.results),
                        "Error std_out is empty for one of the show commands")

    @attr('all', 'revert', 'cdb_priority1')
    def test_03_n_validate_incorrect_cli(self):
        """
        @tms_id: litpcds_630_tc03
        @tms_requirements_id: LITPCDS-630
        @tms_title: validate cli shorthand commands
        @tms_description: Verify the output is an error message when executing
                        show command on the root path  with invalid shorthand
                        optional argument
        @tms_test_steps:
        @step: Run show command on root path with '-lT' optional
                argument
        @result: Message displayed: -T/--tree: not allowed with argument
                -l/--list
        @step: Run show command on root path with '-ln' optional
                argument
        @result: Message displayed: argument -n/--depth
        @step: Run show command on root path with '-rn' optional
                argument
        @result: Message displayed: argument -n/--depth: expected one argument
        @step: Run show command on root path with '-lir' optional
                argument
        @result: Message displayed: -l/--list: ignored explicit argument 'ir'
        @step: Run show command on root path with '-blah' optional
                argument
        @result: Message displayed: unrecognized arguments: -blah
        @step: Run show command on root path with '-rn 0' optional
                argument
        @result: Message displayed: unrecognized arguments: argument -
                n/--depth: 0 is not a valid depth argument
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # run a show command which has invalid args
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/", "-lT",
                                                  expect_positive=False)

        # assert error in standard error
        self.assertTrue(
        self.is_text_in_list(
            "-T/--tree: not allowed with argument -l/--list", std_err),
        "Expected unrecognized arguments error was missing from stderr")

        # run a show command which has invalid args
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/", "-ln",
                                                  expect_positive=False)

        #assert error in standard error
        self.assertTrue(
        self.is_text_in_list("argument -n/--depth", std_err),
        "Expected unrecognized arguments error was missing from stderr")

        # run a show command which has invalid args
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/", "-rn",
                                                  expect_positive=False)

        #assert error in standard error
        self.assertTrue(
        self.is_text_in_list(
            "argument -n/--depth: expected one argument", std_err),
        "Expected unrecognized arguments error was missing from stderr")

        # run a show command which has invalid args
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/", "-lir",
                                                  expect_positive=False)

        #assert error in standard error - Note LITPCDS-2734 relating to below
        #was rejected
        self.assertTrue(
        self.is_text_in_list(
            "-l/--list: ignored explicit argument 'ir'", std_err),
        "Expected unrecognized arguments error was missing from stderr")

        # run a show command which has invalid args
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/", "-blah",
                                                  expect_positive=False)

        #assert error in standard error
        self.assertTrue(
        self.is_text_in_list("unrecognized arguments: -blah", std_err),
        "Expected unrecognized arguments error was missing from stderr")

        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/", "-rn 0",
                                                  expect_positive=False)

        #assert error in standard error
        self.assertTrue(
        self.is_text_in_list(
            "argument -n/--depth: 0 is not a valid depth argument", std_err),
        "Expected arguments error was missing from stderr")

    @attr('all', 'revert')
    def test_04_n_show_cli_path_negative(self):
        """
        @tms_id: litpcds_630_tc04
        @tms_requirements_id: LITPCDS-630
        @tms_title: show cli on invalid path
        @tms_description: Verify the output is an error message/Validation
                        error when executing show command with '-l' argument
                        on an invalid path optional argument
        @tms_test_steps:
        @step: Run show command on '/invalid' path with '-l' optional
                argument
        @result: Validation error: InvalidLocationError
        @step: Run show command on '/*' path with '-l' optional
                argument
        @result: Message displayed: unrecognized arguments
        @step: Run show command on '/?[a-z]*s$' path with '-l' optional
                argument
        @result: Message displayed: argument -p/--path: /?[a-z]*s$ is not a
                valid path argument
        @step: Run show command on '/invaliddeployments' path with '-l'
                optional argument
        @result: Validation error: InvalidLocationError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node,
                                                  "/invalid",
                                                  "-l",
                                                  expect_positive=False)

        #assert InvalidLocationError in standard error
        self.assertTrue(
        self.is_text_in_list("InvalidLocationError", std_err),
        "Expected InvalidLocationError was missing from stderr")

        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/*",
                                                  "-l",
                                                  expect_positive=False)

        #assert error in standard error
        self.assertTrue(
        self.is_text_in_list("unrecognized arguments:", std_err),
        "Unrecognized argument error was missing from stderr")

        _, std_err, _ = self.execute_cli_show_cmd(self.test_node, "/?[a-z]*s$",
                                                  "-l",
                                                  expect_positive=False)

        #assert error in standard error
        self.assertTrue(
        self.is_text_in_list(
            "argument -p/--path: /?[a-z]*s$ is not a valid path argument",
                                                                    std_err),
        "Expected arguments error was missing from stderr")

        # run a show command on an invalid path
        _, std_err, _ = self.execute_cli_show_cmd(self.test_node,
                                                  "/invaliddeployments",
                                                  "-l",
                                                  expect_positive=False)

        #assert InvalidLocationError in standard error
        self.assertTrue(
        self.is_text_in_list("InvalidLocationError", std_err),
        "Expected InvalidLocationError was missing from stderr")
