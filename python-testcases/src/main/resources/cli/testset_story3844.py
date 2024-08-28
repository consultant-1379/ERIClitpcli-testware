'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     April 2014
@author:    Maria Varley
@summary:   Integration test for litp show print property value
            Agile: LITPCDS-3844
'''

from litp_generic_test import GenericTest, attr


class Story3844(GenericTest):

    '''
    As a LITP User I want "litp show" to print value of a specific property,
    so I can retrieve only the information I need
    '''

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
        super(Story3844, self).setUp()
        self.ms_node = self.get_management_node_filename()

    @attr('all', 'revert', 'story3844', 'story3844_tc01', 'cdb_priority1')
    def test_01_p_show_property_value(self):
        """
        @tms_id: litpcds_3844_tc01
        @tms_requirements_id: LITPCDS-3844
        @tms_title: Show command with option
        @tms_description: Verify litp show command on paths with various
        optional arguments
        @tms_test_steps:
        @step: Execute 'litp show -h'
        @result: The output contains expected text
        @step: Execute 'litp show --help'
        @result: The output contains expected text
        @step: Execute 'litp show' command with '-o subnet'
        @result: The output contains expected text
        @step: Execute 'litp show' command with '--options subnet'
        @result: The output contains expected text
        @step: Execute 'litp show' command with '-o subnet -j'
        @result: The output contains only the item in json format
        @result: The output in json format does not equal the subnet value
        @tms_test_precondition: NA
        @tms_execution_type: Automated

        """
        # Execute litp show -h command
        cmd = self.cli.get_help_cmd("-h", "show")
        stdout, _, _ = self.run_command(self.ms_node, cmd,
                                        default_asserts=True,
                                        add_to_cleanup=False)
        self.assertNotEqual(stdout, [], "Standard output is not empty")

        # Check the output contains the --options argument
        self.assertTrue(self.is_text_in_list(
            "--options PROPERTY", stdout), \
            "--options option is not in litp create help")

        # Check the output contains the -o argument
        self.assertTrue(self.is_text_in_list(
            "-o PROPERTY", stdout), \
            "-o option is not in litp create help")

        # Execute litp show --help command
        cmd = self.cli.get_help_cmd(help_action="show")
        stdout, _, _ = self.run_command(self.ms_node, cmd,
                                        default_asserts=True,
                                        add_to_cleanup=False)
        self.assertNotEqual(stdout, [], "Standard output is not empty")

        # Check the output contains the --options argument
        self.assertTrue(self.is_text_in_list(
            "--options PROPERTY", stdout), \
            "--options option is not in litp create help")

        # Check the output contains the -o argument
        self.assertTrue(self.is_text_in_list(
            "-o PROPERTY", stdout), \
            "-o option is not in litp create help")

        # Check show command with -o argument prints property value
        # Get path
        route_inherited_path = self.find(
            self.ms_node, "/deployments", \
            "reference-to-route", True)[0]

        route_path = self.find(
        self.ms_node, "/infrastructure", \
        "route", True)[0]

        # Save property value
        route_subnet = self.execute_show_data_cmd(
            self.ms_node, route_path, "subnet")

        # Execute show command with -o argument
        show_property_result, _, _ = self.execute_cli_show_cmd(
            self.ms_node, route_inherited_path, "-o subnet")
        show_property_result = "".join(show_property_result)

        # Check values match
        self.assertEqual(show_property_result, route_subnet)

        # Execute show command with -o argument
        show_property_result, _, _ = self.execute_cli_show_cmd(
            self.ms_node, route_inherited_path, \
            "--options subnet")
        show_property_result = "".join(show_property_result)

        # Check values match
        self.assertEqual(show_property_result, route_subnet)

        # Execute show command with -o and -j arguments
        show_property_result, _, _ = self.execute_cli_show_cmd(
            self.ms_node, route_inherited_path, "-o subnet -j")
        self.assertNotEqual(show_property_result, route_subnet)

    @attr('all', 'revert', 'story3844', 'story3844_tc02')
    def test_02_n_show_nonexistent_property_value(self):
        """
        @tms_id: litpcds_3844_tc02
        @tms_requirements_id: LITPCDS-3844
        @tms_title: Show command with non-existent property
        @tms_description: Verify litp show command on paths with non-existent
        property
        @tms_test_steps:
        @step: Execute 'litp show' with an invalid property
        @result: Validation error: InvalidPropertyError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        # Check show command with -o argument prints an error when
        # property does not exist
        # Get path
        storage_profile_path = self.find(
            self.ms_node, "/deployments", \
            "reference-to-storage-profile", True)[0]

        # Execute show command with -o argument
        stdout, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, storage_profile_path, \
            "-o storageprofilename", expect_positive=False)

        # Check Error outpuuted
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("InvalidPropertyError", stderr))
        self.assertEqual(1, returnc)

    @attr('all', 'revert', 'story3844', 'story3844_tc03')
    def test_03_n_show_multiple_properties(self):
        """
        @tms_id: litpcds_3844_tc03
        @tms_requirements_id: LITPCDS-3844
        @tms_title: Show command with multiple non-existent properties &
        multiple -o flags
        @tms_description: Verify litp show command with non-existent
        properties and the usage of '-o' multiple times
        @tms_test_steps:
        @step: Execute 'litp show' with invalid properties
        @result: Message displayed: unrecognized arguments
        @step: Execute 'litp show' with multiple '-o' flags
        @result: Message displayed: -o may only be specified once
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # Find os profile path
        os_profile_path = self.find(self.ms_node,
                         "/software", "os-profile", True)[0]

        # Execute show command with -o property property
        stdout, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, os_profile_path, \
            "-o breed arch", expect_positive=False)

        # Check Error outpuuted
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("unrecognized arguments", stderr))
        self.assertEqual(2, returnc)

        # Execute show command with -o property -o property
        stdout, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, os_profile_path, \
            "-o name -o version", expect_positive=False)

        # Check Error outpuuted
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list(
            "-o may only be specified once", stderr))
        self.assertEqual(2, returnc)

    @attr('all', 'revert', 'story3844', 'story3844_tc04')
    def test_04_np_show_property_with_other_arguments(self):
        """
        @tms_id: litpcds_3844_tc04
        @tms_requirements_id: LITPCDS-3844
        @tms_title: Show command with multiple arguments
        @tms_description: Verify litp show command with multiple arguments
        @tms_test_steps:
        @step: Execute 'litp show' with '-o' & '-h' arguments
        @result: The output contains expected text
        @step: Execute 'litp show' with '-o' & '-T' arguments
        @result: Message displayed: litp show: error:
        @step: Execute 'litp show' with '-o' & '-r' arguments
        @result: The output contains expected text
        @step: Execute 'litp show' with '-o' & '-n' arguments
        @result: Message displayed: litp show: error:
        @step: Execute 'litp show' with '-o' & '-o' arguments
        @result: Message displayed: litp show: error:
        @step: Execute 'litp show' with '-o' & '-p' arguments
        @result: Message displayed:litp show: error:
        @step: Execute 'litp show' with '-o' & '-l' arguments
        @result: Message displayed: litp show: error:
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
         # Get path
        route_path = self.find(
            self.ms_node, "/deployments", \
            "reference-to-route", True)[0]

        # Save property value
        route_gw = self.execute_show_data_cmd(
        self.ms_node, route_path, "gateway")

        route_gw = self.excl_inherit_symbol(route_gw)

        # Execute show command with -o and -h arguments
        stdout, _, _ = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -h", expect_positive=True)
        self.assertTrue(self.is_text_in_list("Usage: litp show", \
                        stdout), "did not get expected message")

        # Execute show command with -o and -T arguments
        _, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -T", expect_positive=False)
        self.assertTrue(self.is_text_in_list("litp show: error:", \
                        stderr), "did not get expected message")
        self.assertEqual(2, returnc)

        # Execute show command with -o and -r arguments
        stdout, _, _ = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -r", expect_positive=True)
        show_property_result = "".join(stdout)
        self.assertEqual(show_property_result, route_gw)

        # Execute show command with -o and -n arguments
        _, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -n", expect_positive=False)
        self.assertTrue(self.is_text_in_list("litp show: error:", \
                        stderr), "did not get expected message")
        self.assertEqual(2, returnc)

        # Execute show command with -o and -o arguments
        _, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -o", expect_positive=False)
        self.assertTrue(self.is_text_in_list("litp show: error:", \
                        stderr), "did not get expected message")
        self.assertEqual(2, returnc)

        # Execute show command with -o and -p arguments
        _, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -p", expect_positive=False)
        self.assertTrue(self.is_text_in_list("litp show: error:", \
                        stderr), "did not get expected message")
        self.assertEqual(2, returnc)

        # Execute show command with -o and -l arguments
        _, stderr, returnc = self.execute_cli_show_cmd(
            self.ms_node, route_path, \
            "-o gateway -l", expect_positive=False)
        self.assertTrue(self.is_text_in_list("litp show: error:", \
                        stderr), "did not get expected message")
        self.assertEqual(2, returnc)

    @attr('all', 'revert', 'story3844', 'story3844_tc05', 'cdb_priority1')
    def test_05_p_show_property_value_ForRemoval(self):
        """
        @tms_id: litpcds_3844_tc05
        @tms_requirements_id: LITPCDS-3844
        @tms_title: Show command with item ForRemoval
        @tms_description: Verify that the state of the item-type does
        not impact on the show -o command
        @tms_test_steps:
        @step: Mark item ForRemoval
        @result: Item is in ForRemoval state
        @step: Execute 'litp show' command with '-o' argument
        @result: Property is displayed
        @step: Re-inherit item
        @result: Item is in Applied state
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # Get path
        route_inherited_path = self.find(
            self.ms_node, "/deployments", \
            "reference-to-route", True)[0]

        # find base item
        base_item_path = self.deref_inherited_path(
                            self.ms_node, route_inherited_path)

        # Check the 'state' value of the item
        # before test is performed
        get_data_cmd = self.cli.get_show_data_value_cmd(
            route_inherited_path, "state")
        stdout, _, _ = self.run_command(
            self.ms_node, get_data_cmd, default_asserts=True)
        stdout = "".join(stdout)
        self.assertEqual("Applied", stdout)

        try:
            # Save property value
            route_subnet = self.execute_show_data_cmd(
                self.ms_node, route_inherited_path, "subnet")
            route_subnet = self.excl_inherit_symbol(route_subnet)

            # Remove item-type
            self.execute_cli_remove_cmd(
                self.ms_node, route_inherited_path, add_to_cleanup=False)

            # Execute show command with -o argument
            show_property_result, _, _ = self.execute_cli_show_cmd(
                self.ms_node, route_inherited_path, "-o subnet")
            show_property_result = "".join(show_property_result)

            # Check value is printed correctly
            self.assertEqual(show_property_result, route_subnet)

        finally:
            # Recreate item-type
            self.execute_cli_inherit_cmd(
                self.ms_node, route_inherited_path, \
                base_item_path, add_to_cleanup=False)

            # find the 'state' value of the item
            get_data_cmd = self.cli.get_show_data_value_cmd(
                route_inherited_path, "state")
            stdout, _, _ = self.run_command(
                self.ms_node, get_data_cmd, default_asserts=True)
            stdout = "".join(stdout)
            self.assertEqual("Applied", stdout)
