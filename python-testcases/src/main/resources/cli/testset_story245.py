'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     November 2013
@author:    Gabor
@summary:   Integration test for litp create, inherit, update, remove, plan
            commands with both short and longhand optional arguments
            Agile: EPIC-183, STORY-LITPCDS-245, Sub-Task: STORY-LIPTCDS-1494
                   BUG-LITPCDS-9072
'''


from litp_generic_test import GenericTest, attr
from rest_utils import RestUtils
from litp_cli_utils import CLIUtils
from json_utils import JSONUtils
import test_constants


class Story245(GenericTest):

    '''
    As a Product Designer I want a CLI that uses only the new REST API,
    so that the old API can be retired
    '''

    def setUp(self):
        """
        Description:
            Runs before every single test.
        Actions:
            1. Call the super class setup method
            2. Set up variables used in the tests
        Results:
            The super class prints out diagnostics and variables
            common to all tests are available.
        """
        # 1. Call super class setup
        super(Story245, self).setUp()
        self.ms_node = self.get_management_node_filename()
        self.ms_ip_address = self.get_node_att(self.ms_node, 'ipv4')
        self.rest = RestUtils(self.ms_ip_address)
        self.cli = CLIUtils()
        self.json = JSONUtils()
        self.os_path = test_constants.LITP_DEFAULT_OS_PROFILE_PATH_RHEL7

    def tearDown(self):
        """
        Description:
            Runs after every single test.
        Actions:
            1. Perform Test Cleanup
            2. Call superclass teardown
        Results:
            Items used in the test are cleaned up and the
        """
        self.rest.clean_paths()
        super(Story245, self).tearDown()

    def create_profile(self, profile_name, add_to_cleanup=True):
        """
        Description:
            Create test profile os245
        Args:
            profile_name (str): profile name
            add_to_cleanup (bool): If True add to list of
                                   commands to cleanup
                                   on teardown.
        Actions:
            1. Get profiles collection path
            2. Create test profile os245
        Results:
            Path in litp tree to the created test os245
        """
        # GET PROFILES PATH
        profiles = self.find(self.ms_node, "/", "profile", False)
        profiles_path = profiles[0]

        # CREATE TEST PROFILE WITH CLI
        profile_url = profiles_path + "/" + profile_name
        props = "name='test-profile' version='rhel7' " \
            " path='{0}' arch='x86_64' breed='redhat'".format(self.os_path)
        _, _, _ = self.execute_cli_create_cmd(self.ms_node, \
            profile_url, "os-profile", props, \
            expect_positive=True, add_to_cleanup=add_to_cleanup)
        return profile_url

    def create_package(self, package_name, add_to_cleanup=True):
        """
        Description:
            Create test package
        Args:
            package_name (str): package name
            add_to_cleanup (bool): If True add to list of
                                   commands to cleanup
                                   on teardown.
        Actions:
            1. Get softwate items collection path
            2. Create test package
        Results:
            Path in litp tree to the created test package
        """
        # GET ITEMS PATH
        items = self.find(self.ms_node, "/software", "software-item", False)
        items_path = items[0]

        # CREATE A PACKAGE WITH CLI
        package_url = items_path + "/remote-access"
        props = "name='{0}'".format(package_name)
        _, _, _ = self.execute_cli_create_cmd(self.ms_node, \
            package_url, "package", props, expect_positive=True, \
                add_to_cleanup=add_to_cleanup)
        return package_url

    def create_node(self, node_name, add_to_cleanup=True):
        """
        Description:
            Create test node node245
        Args:
            node_name (str): node name
            add_to_cleanup (bool): If True add to list of
                                   commands to cleanup
                                   on teardown
        Actions:
            1. Get nodes collection path
            2. Create test node node245
        Results:
            Path in litp tree to the created test node245
        """
        # GET NODES PATH
        nodes = self.find(self.ms_node, "/", "node", False)
        nodes_path = nodes[0]

        # CREATE TEST NODE WITH CLI
        node_url = nodes_path + "/" + node_name
        props = "hostname='node245'"
        _, _, _ = self.execute_cli_create_cmd(self.ms_node, \
            node_url, "node", props, expect_positive=True, \
                add_to_cleanup=add_to_cleanup)
        return node_url

    def create_os_link(self, node_url, source_path='', add_to_cleanup=True):
        """
        Description:
            Create os link to the test node245
        Args:
            node_url (str): node url
            add_to_cleanup (bool): If True add to list of
                                   commands to cleanup
                                   on teardown.
        Actions:
            1. Create os link
        Results:
            Path in litp tree to the created os link
        """
        # CREATE OS LINK WITH CLI
        os_url = node_url + "/os"
        _, _, _ = self.execute_cli_inherit_cmd(self.ms_node, \
          os_url, source_path, expect_positive=True, \
                add_to_cleanup=add_to_cleanup)
        return os_url

    def inherit_package_item(self, package_name, source_path,
                                                        add_to_cleanup=True):
        """
        Description:
            Create package link to the test node245
        Args:
            node_url (str): node url
            package_name (str): package name
            add_to_cleanup (bool): If True add to list of
                                   commands to cleanup
                                   on teardown.
        Actions:
            1. Create package link
        Results:
            Path in litp tree to the created package link
        """
        # GET NODE1 PATH
        nodes = self.find(self.ms_node, "/", "node")
        node1_path = nodes[0]

        # LINK PACKAGE WITH CLI
        package_url = node1_path + "/items/{0}".format(package_name)
        _, _, _ = self.execute_cli_inherit_cmd(self.ms_node, \
          package_url, source_path, expect_positive=True, \
                    add_to_cleanup=add_to_cleanup)
        return package_url

    @attr('all', 'revert', 'story245', 'story245_tc01', 'cdb_priority1')
    def test_01_p_cli_create_item(self):
        """
        @tms_id: litpcds_245_tc01
        @tms_requirements_id: LITPCDS-245
        @tms_title: Create item through cli and rest
        @tms_description: Verify an item created with '-j' argument is
        equal to an item created with '--json' and is equal to an item created
        with REST. Also verify that an item can be created/removed multiple
        times.
        @tms_test_steps:
        @step: Create os profile item with -j argument and specified
               properties
        @result: Item is created successfully
        @step: Remove os profile item item
        @result: OS profile item is removed
        @step: Create os profile item with --json argument and specified
               properties
        @result: Item is created successfully
        @step: Check properties from test profile item
        @result: Properties match those specified in create command
        @step: Remove os profile item
        @result: OS profile item is removed
        @step: Create os profile item with REST
        @result: Item is created successfully
        @step: Check os profile item created with -j is equal to
               os profile item created with --json
        @result: The two profiles are equal
        @step: Check os profile item created with -j is equal to
               os profile item created REST
        @result: The two profiles are equal
        @step: Create firewall rule
        @result: Firewall rule created
        @step: Remove Firewall rule
        @result: Firewall rule removed
        @step: Create firewall rule
        @result: Firewall rule created
        @step: Remove Firewall rule
        @result: Firewall rule removed
        @step: Create firewall rule
        @result: Firewall rule created
        @step: Remove Firewall rule
        @result: Firewall rule removed
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET PROFILES PATH
        profiles = self.find(self.ms_node, "/", "profile", False)
        profiles_path = profiles[0]

        self.log('info', '1. Create test profile item with -j argument')
        profile_url = profiles_path + "/os245_1"
        props = "name='test-profile' version='rhel7' " \
            " path='{0}' arch='x86_64' breed='redhat'".format(self.os_path)
        litp_create1, _, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, "-j")

        self.log('info', '2. Delete profile url used in item')
        self.execute_cli_remove_cmd(self.ms_node, profile_url)

        self.log('info', '3. Create test profile item with --json argument')
        litp_create2, _, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, "--json")

        self.log('info', '4. Check properties from test profile item')
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("rhel7", props["version"])
        self.assertEqual(self.os_path, props["path"])
        self.assertEqual("x86_64", props["arch"])
        self.assertEqual("redhat", props["breed"])

        self.log('info', '5. Delete profile url used in item')
        self.execute_cli_remove_cmd(self.ms_node, profile_url)

        self.log('info', '5. CREATE TEST PROFILE WITH REST')
        message_data = \
           '{"id":"os245_1","type":"os-profile","properties":' \
           '{"name":"test-profile","version":"rhel7",' \
           '"path":"%s",' \
           '"arch":"x86_64","breed":"redhat"}}' % self.os_path

        stdout, stderr, status = self.rest.post(profiles_path,
                                                header=self.rest.HEADER_JSON,
                                                data=message_data)
        self.assertEqual(201, status)
        self.assertEqual("", stderr)

        # CONVERT OUTPUT IN JSON STRUCTURE
        # Replace localhost with ip address in string so comparison with
        # rest output can be made
        create_output = stdout.replace(self.ms_ip_address, "localhost")
        rest_create = self.json.load_json(create_output)

        # COMPARE CLI CREATE AND REST CREATE OUTPUT
        self.assertEqual(litp_create1, litp_create2)
        self.assertEqual(litp_create1, rest_create)

         # Find firewall cluster config in model
        fw_cluster_config = self.find(
            self.ms_node, "/deployments", "firewall-cluster-config")[0]

        # 5. Create firewall rule
        firewall_rule = fw_cluster_config + "/rules/fw001"

        props = "'name=131 test13'"
        self.execute_cli_create_cmd(
            self.ms_node, firewall_rule, "firewall-rule", props)
        self.execute_cli_remove_cmd(self.ms_node, firewall_rule)

        props = "name='131 test13'"
        self.execute_cli_create_cmd(
            self.ms_node, firewall_rule, "firewall-rule", props)
        self.execute_cli_remove_cmd(self.ms_node, firewall_rule)

        props = 'name="131 test13"'
        self.execute_cli_create_cmd(
            self.ms_node, firewall_rule, "firewall-rule", props)

    @attr('all', 'revert', 'story245', 'story245_tc02')
    def test_02_n_cli_create_duplicate_element(self):
        """
        @tms_id: litpcds_245_tc02
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create duplicate element
        @tms_description: Verify create command fails when an item
                          already exists in specified location
        @tms_test_steps:
        @step: Create os profile item
        @result: os profile item created
        @step: Create the same os profile item again
        @result: Validation error is thrown, the item already exists in the
        model
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # CREATE TEST PROFILE
        profile_url = self.create_profile("os245_2")

        self.log('info', '1. CREATE TEST PROFILE AGAIN')
        props = "name='test-profile' version='rhel7' " \
            " path='{0}' arch='x86_64' breed='redhat'".format(self.os_path)
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, expect_positive=False)

        self.log('info', '2. Assert Validation Error')
        self.assertTrue(self.is_text_in_list("ItemExistsError", stderr),
                        "ItemExistsError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Item already exists in model",
                                             stderr),
                        "'Item already exists in model' is missing "
                        "from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc03')
    def test_03_n_cli_create_invalid_property_value(self):
        """
        @tms_id: litpcds_245_tc03
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create invalid property value
        @tms_description: Verify create command fails when invalid property
        values used
        @tms_test_steps:
        @step: Cli create os-profile item with invalid property
        @result: ValidationError in property, invalid property value
        @step: Check item is not created
        @result: Item is not created
        @step: Cli create os-profile item with invalid property that contains
               a comma
        @result: Validation error is thrown: invalid property value
        @step: Check item is not created
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET PROFILES PATH
        profiles = self.find(self.ms_node, "/", "profile", False)
        profiles_path = profiles[0]

        self.log('info', 'Create item with invalid property name')
        profile_url = profiles_path + "/os245_3"
        props = "name='test-profile' version='rhel7' path='@?&$*' " \
            "arch='x86_64' breed='test'"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, expect_positive=False)

        self.log('info', 'Validation error is thrown, invalid property value')
        self.assertTrue(self.is_text_in_list("ValidationError in property:",
                                             stderr),
                        "ValidationError is missing from errorput")

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

        # BUG 9072
        # Validation error not triggered when property value
        # contains ","
        #
        # Verifying that attempting to create an item with a property value
        # ending with "," throws an error

        # CREATE TEST PROFILE WITH INVALID PROPERY VALUE
        profile_url = profiles_path + "/os245_3"
        props = "name='test-profile' version='rhel7' path='{0}' " \
            "arch='x86_64' breed='test,'".format(profile_url)
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, expect_positive=False)

        expected_error = \
          "ValidationError in property: \"breed\"    Invalid value 'test,'"
        self.assertTrue(self.is_text_in_list(expected_error, stderr),
            "[{0}] is missing from errorput".format(expected_error))

        # CHECK ITEM HAS NOT BEEN CREATED
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc04')
    def test_04_n_cli_create_invalid_property_name(self):
        """
        @tms_id: litpcds_245_tc04
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create invalid property name
        @tms_description: Cannot create an item with an invalid property name
        @tms_test_steps:
        @step: Cli create os-profile item with invalid property name
        @result: Validation error is thrown: PropertyNotAllowedError
        @step: Check item is not created
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET PROFILES PATH
        profiles = self.find(self.ms_node, "/", "profile", False)
        profiles_path = profiles[0]

        self.log('info', 'CREATE TEST PROFILE WITH INVALID PROPERY')
        profile_url = profiles_path + "/os245_4"
        props = "name='test-profile' version='rhel7' " \
            " path='{0}' arch='x86_64' invalid='test' breed='redhat'".format(
                                                                self.os_path)
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, expect_positive=False)

        self.assertTrue(
            self.is_text_in_list("PropertyNotAllowedError", stderr),
            "PropertyNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("is not an allowed property "
                                             "of os-profile", stderr),
                        "'is not an allowed property of os-profile' "
                        "is missing from errorput")

        # CHECK ITEM HAS NOT BEEN CREATED
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc05')
    def test_05_n_cli_create_missing_mandatory(self):
        """
       @tms_id: litpcds_245_tc05
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create item with missing mandatory property
        @tms_description: Verify item with missing mandatory property is
                          not created
        @tms_test_steps:
        @step:Create node item with missing required property
        @result: Validation error is thrown: MissingRequiredPropertyError
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET NODES PATH
        nodes_path = self.find(self.ms_node, "/", "node", False)[0]

        self.log('info', 'Create node property with missing property')
        node_url = nodes_path + "/node245_5"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          node_url, "node", expect_positive=False)

        self.log('info', 'Validation error is thrown, '
                         'MissingRequiredPropertyError')
        self.assertTrue(self.is_text_in_list(
            "MissingRequiredPropertyError", stderr),
            "MissingRequiredPropertyError is not in errorput")
        self.assertTrue(self.is_text_in_list(
            '"node" is required to have a property with name "hostname"',
            stderr), 'Expected message is not seen in standard error')

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          node_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc06')
    def test_06_n_cli_create_incorrect_path(self):
        """
        @tms_id: litpcds_245_tc06
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create item with invalid path
        @tms_description: Verify item with invalid path is not created
        @tms_test_steps:
        @step: Create item with invalid path
        @result: Validation error is thrown: InvalidLocationError
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create item with invalid path')
        profile_url = "/invalid_path/os245_6"
        props = "name='test-profile' version='rhel7' path='/test/' " \
            "arch='x86_64' breed='test'"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, expect_positive=False)

        self.log('info', 'Validation error is thrown, invalid location')
        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Path not found", stderr),
                        "'Path not found' is missing from errorput")

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc07')
    def test_07_n_cli_create_nonexisting_type(self):
        """
        @tms_id: litpcds_245_tc07
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create invalid item type
        @tms_description: Verify create command fails with invalid item type
        @tms_test_steps:
        @step: Create item with invalid item type
        @result: Validation error is thrown: InvalidTypeError
        @step: Check item is not created
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET PROFILES PATH
        profiles_path = self.find(self.ms_node, "/", "profile", False)[0]

        self.log('info', 'Create item with invalid item type')
        profile_url = profiles_path + "/os245_7"
        props = "name='test-profile' version='rhel7' path='/test/' " \
            "arch='x86_64' breed='test'"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "invalidtype", props, expect_positive=False)

        self.log('info', 'Validation error is thrown, invalid type error')
        self.assertTrue(self.is_text_in_list("InvalidTypeError", stderr),
                        "InvalidTypeError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Item type not registered",
                                             stderr),
                        "'Item type not registered' is missing from errorput")

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc08')
    def test_08_n_cli_create_incorrect_type(self):
        """
        @tms_id: litpcds_245_tc08
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create invalid child type
        @tms_description: Verify item cannot be created under invalid item type
        @tms_test_steps:
        @step: Create item under incorrect item type
        @result: Validation error is thrown: InvalidChildTypeError
        @step: Check item is not created
        @result: Item is not created
        @step: Create item under root path
        @result: Validation error is thrown
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET PROFILES PATH
        profiles_path = self.find(self.ms_node, "/", "profile", False)[0]

        self.log('info', 'Create item under incorrect item type')
        profile_url = profiles_path + "/os245_8"
        props = "name='test-profile' version='rhel7' path='/test/' " \
            "arch='x86_64' breed='test'"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "node", props, expect_positive=False)

        self.log('info', 'Validation error is thrown')
        self.assertTrue(self.is_text_in_list("InvalidChildTypeError", stderr),
                        "InvalidChildTypeError is missing from errorput")
        self.assertTrue(self.is_text_in_list("is not an allowed type", stderr),
                        "'is not an allowed type' is missing from errorput")

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

        self.log('info', 'Create item under root path')
        props = "hostname='test_node'"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          "/", "node", props, expect_positive=False)

        self.log('info', 'Check item is not created')
        self.assertTrue(self.is_text_in_list("ValidationError", stderr),
                        "ValidationError is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc09')
    def test_09_n_cli_create_option(self):
        """
        @tms_id: litpcds_245_tc09
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create with invalid optional argument "-i"
        @tms_description: Verify item with invalid option argument -i
                          is not created
        @tms_test_steps:
        @step: Create item with invalid option -i
        @result: Message displayed: unrecognized arguments
        @step: Check item is not created
        @result: Item is not created
        @step: Create item with invalid option --invalid
        @result: Message displayed: unrecognized arguments
        @step: Check item is not created
        @result: Item is not created
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET PROFILES PATH
        profiles = self.find(self.ms_node, "/", "profile", False)
        profiles_path = profiles[0]

        self.log('info', 'Create item with invalid option -i')
        profile_url = profiles_path + "/os245_9"
        props = "name='test-profile' version='rhel7' " \
            " path='{0}' arch='x86_64' breed='redhat'".format(self.os_path)

        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, "-i", expect_positive=False)

        self.log('info', 'Validation error is thrown')
        self.assertTrue(self.is_text_in_list("unrecognized arguments: -i",
                                             stderr),
                        "'unrecognized arguments: -i' is not in errorput")

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

        self.log('info', 'Create item with invalid option --invalid')
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, \
          profile_url, "os-profile", props, "--invalid", expect_positive=False)

        self.assertTrue(self.is_text_in_list(\
            "unrecognized arguments: --invalid", stderr), \
                        "'unrecognized arguments: --invalid' " \
                        "is not in errorput")

        self.log('info', 'Check item is not created')
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc10')
    def test_10_n_cli_create_command_style(self):
        """
        @tms_id: litpcds_245_tc10
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create command wth incorrect syntax
        @tms_description: Verify issuing a create command with an incorrect
                          syntax returns an error string
        @tms_test_steps:
        @step: Issue create command with invalid syntax: no arguments
        @result: Message displayed: argument -t/--type is required
        @step: Issue create command with invalid syntax: create /test
        @result: Message displayed: invalid choice: '/test'
        @step: Issue create command with invalid syntax: create -p /
        @result:Message displayed: argument -p/--path: expected one argument
        @step: Issue create command with invalid syntax:
        @result: Message displayed: argument -t/--type is required
        @step: Issue create command with invalid syntax:
               create --path / --type collections --options none
        @result: Message displayed: litp create: error: argument -o/--options:
        @step:  Issue create command with invalid syntax:
                create -p -o /deployments
        @result: Message displayed argument -p/--path: expected one argument
        @step:  Issue create command with invalid syntax: create -p
                /deployments -t cluster
        @result: Validation error is thrown: ItemExistsError
        @step:  Issue create command with invalid syntax: create -p
                /deployments/ -t cluster
        @result: Validation error is thrown: ItemExistsError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Issue create command with invalid syntax, '
                         'no arguments')
        cmd = "{0} {1}".format(self.cli.litp_path, "create")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("argument -t/--type is required",
                                             stderr),
                        "'argument -t/--type is required' is not in errorput")

        self.log('info', 'Issue create command with invalid syntax '
                         '" create /test "')
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "/test", "create")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("invalid choice: '/test'",
                                             stderr),
                        "'invalid choice: '/test'' is not in errorput")

        self.log('info', 'Issue create command with invalid syntax '
                         '" create -p / "')
        cmd = "{0} {1} {2} {3}".format(self.cli.litp_path, "create", "-p", "/")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("argument -t/--type is required",
                                             stderr),
                        "'argument -t/--type is required' is not in errorput")

        self.log('info', 'Issue create command with invalid syntax '
                         '"create --path / --type collections --options none"')
        cmd = "{0} {1} {2} {3} {4} {5} {6} {7}".format(self.cli.litp_path,
                                                       "create", "--path",
                                                       "/", "--type",
                                                       "collections",
                                                       "--options", "none")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("litp create: error: argument "
                                             "-o/--options: invalid option",
                                             stderr),
                        "'litp create: error: argument -o/--options: "
                        "invalid option' is not in errorput")

        self.log('info', 'Issue create command with invalid syntax '
                         '" create -p -o /deployments "')
        cmd = "{0} {1} {2} {3} {4}".format(self.cli.litp_path, "create", "-p",
                                           "-o", "/deployments")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("argument -p/--path: expected "
                                             "one argument", stderr),
                        "'argument -p/--path: expected one argument' "
                        "is not in errorput")

        self.log('info', 'Issue create command with invalid syntax '
                         '" create -p /deployments -t cluster"')
        cmd = "{0} {1} {2} {3} {4} {5}".format(self.cli.litp_path, "create",
                                               "-p", "/deployments",
                                               "-t", "cluster")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertFalse(self.is_text_in_list("//deployment", stderr),
                         "//deployment is not a correct path")
        self.assertTrue(self.is_text_in_list("ItemExistsError", stderr),
                        "ItemExistsError is not in errorput")
        self.assertTrue(self.is_text_in_list("Item already exists in model",
                                             stderr),
                        "'Item already exists in model' is not in errorput")

        self.log('info', 'Issue create command with invalid syntax '
                         '" create -p /deployments/ -t cluster "')
        cmd = "{0} {1} {2} {3} {4} {5}".format(self.cli.litp_path, "create",
                                               "-p", "/deployments/",
                                               "-t", "cluster")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("ItemExistsError", stderr),
                        "ItemExistsError is not in errorput")
        self.assertTrue(self.is_text_in_list("Item already exists in model",
                                             stderr),
                        "'Item already exists in model' is not in errorput")

    @attr('all', 'revert', 'story245', 'story245_tc11')
    def test_11_p_cli_create_help(self):
        """
        @tms_id: litpcds_245_tc11
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create help
        @tms_description: Verify litp create with option '-h' or
                          '--help'
        @tms_test_steps:
        @step: Run " litp --help
        @result: create command is displayed within help output
        @step: Run " litp -h
        @result: create command is displayed within help output
        @step: Run " litp create--help
        @result: Help content for create command is displayed
        @step: Run " litp create -h
        @result:Help content for create command is displayed
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Run " litp --help')
        cmd = "{0} {1}".format(self.cli.litp_path, "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        self.assertTrue(self.is_text_in_list("create", stdout),
                        "create command is not in litp help")

        self.log('info', 'Run " litp -h')
        cmd = "{0} {1}".format(self.cli.litp_path, "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        self.assertTrue(self.is_text_in_list("create", stdout),
                        "create command is not in litp help")

        self.log('info', 'Run " litp create --h')
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "create", "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd,
                                                       add_to_cleanup=False)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK CREATE COMMAND OPTIONS
        self.assertTrue(self.is_text_in_list("-t TYPE", stdout),
                        "-t option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--type TYPE", stdout),
                        "--type option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-p PATH", stdout),
                        "-p option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--path PATH", stdout),
                        "--path option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-j,", stdout),
                        "-j option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--json", stdout),
                        "--json option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-o PROPERTIES", stdout),
                        "-o option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--options PROPERTIES", stdout),
                        "--options option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-h,", stdout),
                        "-h option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--help", stdout),
                        "--help option is not in litp create help")

        self.log('info', 'Run " litp create --help')
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "create", "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd,
                                                       add_to_cleanup=False)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK CREATE COMMAND OPTIONS
        self.assertTrue(self.is_text_in_list("-t TYPE", stdout),
                        "-t option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--type TYPE", stdout),
                        "--type option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-p PATH", stdout),
                        "-p option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--path PATH", stdout),
                        "--path option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-j,", stdout),
                        "-j option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--json", stdout),
                        "--json option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-o PROPERTIES", stdout),
                        "-o option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--options PROPERTIES", stdout),
                        "--options option is not in litp create help")
        self.assertTrue(self.is_text_in_list("-h,", stdout),
                        "-h option is not in litp create help")
        self.assertTrue(self.is_text_in_list("--help", stdout),
                        "--help option is not in litp create help")

    @attr('all', 'revert')
    def obsolete_12_p_cli_link(self):
        """
        Description:
            This test ensures user can create a link points to an item
            in litp tree, cli return code is 0, stdout and stderr are empty
            --json output is in json format

        Actions:
            1. link item with CLI
            2. Check command return code is 0, stdout and stderr are empty
            3. Check test item properties with CLI show command
            4. Check command stdout is the same as REST read command output

        Result:
            CLI return code is 0
            Payload is in json format
            stderr is empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026:Story4026.test_01_p_cli_inherit_command
        """
        pass

    @attr('all', 'revert')
    def obsolete_13_n_cli_link_duplicate(self):
        """
        Description:
            This test ensures user can not link an item two times
            in litp tree, cli return code is not 0, stderr has
            ItemExistsError
            and 'Item already exists in model' content
            --json output is in json format

        Actions:
            1. link item with CLI
            2. Check command return code is 0, stdout and stderr are empty
            3. Check test item properties with CLI show command
            4. Check command stdout is the same as REST read command output

        Result:
            CLI return code is 0
            Payload is in json format
            stderr is empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026:Story4026.\
            test_03_n_cli_inherit_command_reference_exists
        """
        pass

    @attr('all', 'revert')
    def obsolete_15_n_cli_link_invalid_property_name(self):
        """
        Description:
            This test ensures user can not link the an item with invalid
            property name in litp tree, cli return code is not 0 in this
            case,
            stderr has PropertyNotAllowedError
            and 'is not an allowed property on this ItemType' content

        Actions:
            1. link test item with invalid property name
            2. Check command return code is not 0, stdout is empty,
            stderr has PropertyNotAllowedError
            and 'is not an allowed property on this ItemType' content

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026:
             Story4026.test_04_n_cli_inherit_command_invalid_vpath
        """
        pass

    @attr('all', 'revert')
    def obsolete_16_n_cli_link_incorrect_path(self):
        """
        Description:
            This test ensures user can not link the an item with wrong path
            in litp tree, cli return code is not 0
            in this case, stderr is not empty

        Actions:
            1. link test item with wrong path
            2. Check command return code is not 0, stdout is empty,
               stderr has InvalidLocationError and 'Path not found' content

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026:
            Story4026.test_04_n_cli_inherit_command_invalid_vpath
        """
        pass

    @attr('all', 'revert')
    def obsolete_17_n_cli_link_nonexisting_type(self):
        """
        Description:
            This test ensures user can not link the an item with
            non-existing
            type in litp tree, cli return code is not 0
            in this case, stderr is not empty

        Actions:
            1. link test item with non-existing type
            2. Check command return code is not 0, stdout is empty,
               stderr has InvalidTypeError
               and 'Item type not registered' content

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        TC N/A - types are a create issue now, not an inherit issue
        """
        pass

    @attr('all', 'revert')
    def obsolete_18_n_cli_link_incorrect_type(self):
        """
        Description:
            This test ensures user can not link the an item with incorrect
            type in litp tree, cli return code is not 0
            in this case, stderr is not empty

        Actions:
            1. Create test item with non-existing type
            2. Check command return code is not 0, stdout is empty,
               stderr has InvalidChildTypeError
               and 'is not an allowed type for child' content

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        TC N/A - types are a create issue now, not an inherit issue
        """
        pass

    @attr('all', 'revert')
    def obsolete_19_n_cli_link_option(self):
        """
        Description:
            This test ensures user can not link items with invalid options
            like -i or --invalid.
            cli return code is not 0, stderr is not empty and has
            'unrecognized arguments' error message

        Actions:
            1. Create test item with invalid options
            2. Check command return code is not 0,
               stdout is empty, 'unrecognized arguments' is in stderr

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        TC N/A no reason to tests invalid options and help outputs; they are
        much faster as manual tests, since they are used often, and less
        hassle
        to maintain if error messages are changed
        """
        pass

    @attr('all', 'revert')
    def obsolete_20_n_cli_link_command_style(self):
        """
        Description:
            This test ensures user can not link items with wrong order of
            command, arguments and options, in other words user has to
            follow
            link help to execute correct commands. In other case link gives
            a clear error message, cli return code is not 0

        Actions:
            1. link test item with wrong order of command, arguments,
               options
            2. Check command return code is not 0,
               stdout is empty, stderr is not empty

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        TC N/A no reason to tests invalid options and help outputs; they are
        much faster as manual tests, since they are used often, and less
        hassle
        to maintain if error messages are changed
        """
        pass

    @attr('all', 'revert')
    def obsolete_21_p_cli_link_help(self):
        """
        Description:
            This test ensures litp commands, all arguments and options are
            documented in litp help and litp link help

        Actions:
            1. Run litp help command and check output
            2. Run litp help on link command and check output

        Result:
            litp command help shows link command options: path, options,
            verbose, json

        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        TC N/A no reason to test the help output, it is faster to test
        manually
        by simply typing -h
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc22', 'cdb_priority1')
    def test_22_p_cli_update_item(self):
        """
        @tms_id: litpcds_245_tc22
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli updated item with '-j' , '--json' option and
                    through REST
        @tms_description: Verify updating an item can be done with the -j and
                          --json option as well as through REST
        @tms_test_steps:
        @step: Create os profile item
        @result: OS profile item is created
        @step: Update item properties with -j option argument
        @result: command executes successfully
        @step: Update item properties with -json option argument
        @result: command executes successfully
        @step: Update item properties REST
        @result: command executes successfully
        @step: Check os profile item updated with -j is equal to os profile
                item updated with --json
        @result: Both outputs are equal
        @step: Check os profile item updated with -j is equal to os profile
                item updated through REST
        @result: Both outputs are equal
        @tms_test_precondition: NA
        @tms_execution_type: Automated

        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_22")

        self.log('info', 'Update items properties \'-j\' option argument ')
        props = "name='test2-profile' version='rhel7'"
        litp_update1, _, _ = self.execute_cli_update_cmd(self.ms_node, \
            profile_url, props, "-j", expect_positive=True)

        self.log('info', 'Update items properties \'--json\' option argument ')
        props = "name='test2-profile' version='rhel7'"
        litp_update2, _, _ = self.execute_cli_update_cmd(self.ms_node, \
            profile_url, props, "--json", expect_positive=True)

        self.log('info', 'Check item properties updated')
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("test2-profile", props["name"])
        self.assertEqual("rhel7", props["version"])

        self.log('info', 'Update items properties with REST ')
        message_data = \
            "{\"properties\":{\"name\":\"test2-profile\"," \
            "\"version\":\"rhel7\"}}"
        stdout, stderr, status = self.rest.put(profile_url,
                                               header=self.rest.HEADER_JSON,
                                               data=message_data)
        self.assertEqual(200, status)
        self.assertEqual("", stderr)

        # CONVERT OUTPUT IN JSON STRUCTURE
        # Replace localhost with ip address in string so comparison with
        # rest output can be made
        update_output = stdout.replace(self.ms_ip_address, "localhost")
        rest_update = self.json.load_json(update_output)

        self.log('info', 'Check os profile item updated with -j is equal to '
                        'os profile item updated with --json')
        self.log('info', 'Check os profile item updated with -j is equal to '
                        'os profile item updated through REST')
        self.assertEqual(litp_update1, litp_update2)
        self.assertEqual(litp_update1, rest_update)

    @attr('all', 'revert')
    def obsolete_23_p_cli_update_link(self):
        """
        Description:
            This test ensures user can update a link properties in litp tree,
            cli return code is 0, stdout and stderr are empty
            --json output is in json format

        Actions:
            1. Create a link with CLI
            1. Update the link with CLI
            2. Check command return code is 0, stdout and stderr are empty
            3. Check test item properties with CLI show command
            4. Check command stdout is the same as REST read command output

        Result:
            CLI return code is 0
            Payload is in json format
            stderr is empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026:Story4026.\
            test_08_p_inherit_cmd_update_reference_item_property_cli
        """
        pass

    @attr('all', 'revert')
    def obsolete_24_p_cli_update_link_properties(self):
        """
        Description:
            This test ensures user can update the link itself in litp tree,
            in other words user can re-link to point to a different item.
            cli return code is 0, stdout and stderr are empty
            --json output is in json format

        Actions:
            1. Create a link with CLI
            1. Re-link to another item with update command
            2. Check command return code is 0, stdout and stderr are empty
            3. Check test item properties with CLI show command
            4. Check command stdout is the same as REST read command output

        Result:
            CLI return code is 0
            Payload is in json format
            stderr is empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026:Story4026.\
            test_08_p_inherit_cmd_update_reference_item_property_cli
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc25')
    def test_25_n_cli_update_item_invalid_property_value(self):
        """
        @tms_id: litpcds_245_tc25
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli update item invalid property value
        @tms_description: Updating a property of an item with an invalid value
                           throws a ValidationError
        @tms_test_steps:
        @step: Create os profile item
        @result: Item is created
        @step: Update property with invalid property value
        @result: Validation error is thrown: ValidationError in property
        @step: Check item has not been updated
        @result: Item has not been updated
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_25")

        self.log('info', 'Update property with invalid property value')
        props = "name='test-profile' version='rhel7' path='@?&$*' " \
            "arch='x86_32' breed='none'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
            profile_url, props, expect_positive=False)

        self.assertTrue(self.is_text_in_list("ValidationError in property",
                                             stderr),
                        "ValidationError is missing from errorput")

        # CHECK ITEM HAS NOT BEEN UPDATED
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("test-profile", props["name"])
        self.assertEqual("rhel7", props["version"])
        self.assertEqual(self.os_path, props["path"])
        self.assertEqual("x86_64", props["arch"])
        self.assertEqual("redhat", props["breed"])

    @attr('all', 'revert')
    def obsolete_26_n_cli_update_link_invalid_property_value(self):
        """
        Description:
            This test ensures user can not update the a link with invalid
            property in litp tree, cli return code is not 0 in this case,
            stderr is not empty

        Actions:
            1. Update link with invalid property value
            2. Check command return code is not 0, stdout is empty,
               stderr has RegexError
               and 'Invalid value' content

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026.py:Story4026.test_01_p_cli_inherit_command
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc27')
    def test_27_n_cli_update_item_invalid_property_name(self):
        """
        @tms_id: litpcds_245_tc27
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli update item invalid property name
        @tms_description: Updating a property of an item with an invalid value
                           throws a PropertyNotAllowedError
        @tms_test_steps:
        @step: Create os profile item
        @result: Item is created
        @step: Update property with invalid property value
        @result: Validation error is thrown: PropertyNotAllowedError
        @step: Check item has not been updated
        @result: Item has not been updated
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_27")

        self.log('info', 'Update property with invalid property value')
        props = "name='test-profile' version='rhel7' path='/test/' " \
            "arch='x86_64' breed='test' invalid='test'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             profile_url, props, expect_positive=False)

        self.assertTrue(
            self.is_text_in_list("PropertyNotAllowedError", stderr),
            "PropertyNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("is not an allowed property of "
                                             "os-profile", stderr),
                        "'is not an allowed property of os-profile' "
                        "is missing from errorput")

        # CHECK ITEM HAS NOT BEEN UPDATED
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("test-profile", props["name"])
        self.assertEqual("rhel7", props["version"])
        self.assertEqual(self.os_path, props["path"])
        self.assertEqual("x86_64", props["arch"])
        self.assertEqual("redhat", props["breed"])

    @attr('all', 'revert')
    def obsolete_28_n_cli_update_link_invalid_property_name(self):
        """
        Description:
            This test ensures user can not update a link with invalid
            property name in litp tree, cli return code is not 0 in this
            case,
            stderr has PropertyNotAllowedError
            and 'is not an allowed property on this ItemType' content

        Actions:
            1. update link with invalid property name
            2. Check command return code is not 0, stdout is empty,
            stderr has PropertyNotAllowedError
            and 'is not an allowed property on this ItemType' content

        Result:
            CLI return code is not 0
            Payload is in json format
            stderr is not empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026.py:Story4026.test_01_p_cli_inherit_command
        testset_story4026.py:Story4026.\
            test_04_n_cli_inherit_command_invalid_vpath
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc29')
    def test_29_n_cli_update_incorrect_path(self):
        """
        @tms_id: litpcds_245_tc29
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli updated incorrect path
        @tms_description:An InvalidLocationError is displayed when updating an
        item with an incorrect path
        @tms_test_steps:
        @step: Update item with invalid path
        @result: Validation error is thrown: InvalidLocationError
        @step: Check item has not been updated
        @result: Item has not been updated
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create invalid os profile item path')
        profile_url = "/invalid_path/os245_29"
        props = "name='test-profile' version='rhel7' path='/test/' " \
            "arch='x86_64' breed='test'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             profile_url, props, expect_positive=False)

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Not found", stderr),
                        "'Not found' is missing from errorput")

        # CHECK ITEM HAS NOT BEEN UPDATED
        _, _, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

    @attr('all', 'revert', 'story245', 'story245_tc30')
    def test_30_n_cli_update_non_property(self):
        """
        @tms_id: litpcds_245_tc30
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli update on invalid property
        @tms_description: A PropertyNotAllowedError is displayed when creating
                         an item with an invalid property name
        @tms_test_steps:
        @step: Create os profile item
        @result: Item is created
        @step: Update property with invalid property name
        @result: Validation error : PropertyNotAllowedError
        @step: Check item has not been updated
        @result: Item has not been updated
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_30")

        self.log('info', 'Update property with invalid property name')
        props = "status=Initial"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             profile_url, props, expect_positive=False)

        self.assertTrue(
            self.is_text_in_list("PropertyNotAllowedError", stderr),
            "PropertyNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("is not an allowed property of "
                                             "os-profile", stderr),
                        "'is not an allowed property of os-profile' "
                        "is missing from errorput")

        # CHECK ITEM HAS NOT BEEN UPDATED
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("test-profile", props["name"])
        self.assertEqual("rhel7", props["version"])
        self.assertEqual(self.os_path, props["path"])
        self.assertEqual("x86_64", props["arch"])
        self.assertEqual("redhat", props["breed"])

    @attr('all', 'revert', 'story245', 'story245_tc31')
    def test_31_n_cli_update_read_only_item(self):
        """
        @tms_id: litpcds_245_tc31
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli update read only item
        @tms_description: A validation error is thrown when updating a
                          read only item
        @tms_test_steps:
        @step: Update property on root path
        @result: Validation error is thrown: PropertyNotAllowedError
        @step: Update property on infrastructure path
        @result: Validation error is thrown: PropertyNotAllowedError
        @step: Update a write-protected item in  property-types
        @result: Validation error is thrown: MethodNotAllowedError
        @step: Update a write-protected item in item-types
        @result: Validation error is thrown: MethodNotAllowedError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Update property on root path')
        props = "name='root'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             "/", props, expect_positive=False)

        self.assertTrue(
            self.is_text_in_list("PropertyNotAllowedError", stderr),
            "PropertyNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("is not an allowed property of "
                                             "root", stderr),
                        "'is not an allowed property of root' "
                        "is missing from errorput")

        self.log('info', 'Update property on infrastructure path')
        props = "name='infrastructure'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             "/infrastructure", props, expect_positive=False)

        self.assertTrue(
            self.is_text_in_list("PropertyNotAllowedError", stderr),
            "PropertyNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("is not an allowed property of "
                                             "infrastructure", stderr),
                        "'is not an allowed property of infrastructure' "
                        "is missing from errorput")

        self.log('info', 'UPDATE A WRITE-PROTECTED ITEM IN property-types')
        props = "name='self'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             "/property-types/basic_string", props, expect_positive=False)

        self.assertTrue(self.is_text_in_list("MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Update method on path not "
                                             "allowed", stderr),
                        "'Update method on path not allowed' "
                        "is missing from errorput")

        self.log('info', 'UPDATE A WRITE-PROTECTED ITEM IN item-types')
        props = "name='self'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             "/item-types/deployment", props, expect_positive=False)

        self.assertTrue(self.is_text_in_list("MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Update method on path not "
                                             "allowed", stderr),
                        "'Update method on path not allowed' "
                        "is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc32')
    def test_32_n_cli_update_option(self):
        """
        Description:
        @tms_id: litpcds_245_tc32
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli update with invalid option
        @tms_description: Updating an items property with an invalid option
                          outputs an "unrecognized arguments" message
        @tms_test_steps:
        @step: Create os profile item
        @result: Item is created
        @step: Update property with invalid option -i
        @result: Message is displayed: unrecognized arguments
        @result: Items have not been updated
        @step: Update property with invalid option -invalid
        @result: Message is displayed: unrecognized arguments
        @result: Items have not been updated
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_30")

        self.log('info', 'Update property with invalid option -i')
        props = "name='sample-profile' version='rhel7'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             profile_url, props, "-i", expect_positive=False)

        self.assertTrue(
            self.is_text_in_list("unrecognized arguments: -i", stderr),
            "'unrecognized arguments: -i' is not in errorput")

        # CHECK ITEM HAS NOT BEEN UPDATED
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("test-profile", props["name"])
        self.assertEqual("rhel7", props["version"])
        self.assertEqual(self.os_path, props["path"])
        self.assertEqual("x86_64", props["arch"])
        self.assertEqual("redhat", props["breed"])

        self.log('info', 'Update property with invalid option -invalid')
        props = "name='sample-profile' version='rhel7'"
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, \
             profile_url, props, "--invalid", expect_positive=False)

        self.assertTrue(\
            self.is_text_in_list("unrecognized arguments: --invalid", stderr),
          "'unrecognized arguments: --invalid' is not in errorput")

        # CHECK ITEM HAS NOT BEEN UPDATED
        props = self.get_props_from_url(self.ms_node, profile_url)
        self.assertEqual("test-profile", props["name"])
        self.assertEqual("rhel7", props["version"])
        self.assertEqual(self.os_path, props["path"])
        self.assertEqual("x86_64", props["arch"])
        self.assertEqual("redhat", props["breed"])

    @attr('all', 'revert', 'story245', 'story245_tc33')
    def test_33_n_cli_update_command_style(self):
        """
        @tms_id: litpcds_245_tc33
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli update with incorrect syntax
        @tms_description: Update commands issued with an invalid syntax will
                         not be successful
        @tms_test_steps:
        @step: Issue update command with invalid syntax: no arguments
        @result: Message is displayed: argument -p/--path is required
        @step: Issue update command with invalid syntax: /test update
               name=test
        @result: Message is displayed: invalid choice: '/test
        @step: Issue update command with invalid syntax: update -p -o
                /deployments
        @result: Message is displayed: argument -p/--path: expected one
                 argument
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # RUN UPDATE COMMAND WITH WRONG STYLE
        cmd = "{0} {1}".format(self.cli.litp_path, "update")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("argument -p/--path is required",
                                             stderr),
                        "'argument -p/--path is required' is not in errorput")

        # RUN UPDATE COMMAND WITH WRONG STYLE
        cmd = "{0} {1} {2} {3}".format(self.cli.litp_path,
                                       "/test", "update", "name=test")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("invalid choice: '/test'",
                                             stderr),
                        "'invalid choice: '/test'' is not in errorput")

        # RUN UPDATE COMMAND WITH WRONG STYLE
        cmd = "{0} {1} {2} {3} {4}".format(self.cli.litp_path, "update", "-p",
                                           "-o", "/deployments")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("argument -p/--path: expected "
                                             "one argument", stderr),
                        "'argument -p/--path: expected one argument' "
                        "is not in errorput")

    @attr('all', 'revert', 'story245', 'story245_tc34')
    def test_34_p_cli_update_help(self):
        """
        @tms_id: litpcds_245_tc34
        @tms_requirements_id: LITPCDS-245
        @tms_title: Verify cli update help
        @tms_description: Verify contents when executing '--help' and '-h'
                          with update command
        @tms_test_steps:
        @step: Execute "litp --help"
        @result: Update is in help command output
        @step: Execute "litp -h"
        @result: Update is in help command output
        @step: Execute "litp update -h"
        @result: All update options are present in output
        @step: Execute "litp update --help"
        @result: All update options are present in output
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # GET LITP HELP WITH --help
        cmd = "{0} {1}".format(self.cli.litp_path, "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK UPDATE COMMAND
        self.assertTrue(self.is_text_in_list("update", stdout),
                        "update command is not in litp help")

        # GET LITP HELP WITH -h
        cmd = "{0} {1}".format(self.cli.litp_path, "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK UPDATE COMMAND
        self.assertTrue(self.is_text_in_list("update", stdout),
                        "update command is not in litp help")

        # GET LITP UPDATE HELP WITH -h
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "update", "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd,
                                                       add_to_cleanup=False)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK UPDATE COMMAND OPTIONS
        self.assertTrue(self.is_text_in_list("-p PATH", stdout),
                        "-p option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--path PATH", stdout),
                        "--path option is not in litp update help")
        self.assertTrue(self.is_text_in_list("-j,", stdout),
                        "-j option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--json", stdout),
                        "--json option is not in litp update help")
        self.assertTrue(self.is_text_in_list("-o PROPERTIES", stdout),
                        "-o option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--options PROPERTIES", stdout),
                        "--options option is not in litp update help")
        self.assertTrue(self.is_text_in_list("-h,", stdout),
                        "-h option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--help", stdout),
                        "--help option is not in litp update help")

        # GET LITP UPDATE HELP WITH --help
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "update", "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd,
                                                       add_to_cleanup=False)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK UPDATE COMMAND OPTIONS
        self.assertTrue(self.is_text_in_list("-p PATH", stdout),
                        "-p option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--path PATH", stdout),
                        "--path option is not in litp update help")
        self.assertTrue(self.is_text_in_list("-j,", stdout),
                        "-j option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--json", stdout),
                        "--json option is not in litp update help")
        self.assertTrue(self.is_text_in_list("-o PROPERTIES", stdout),
                        "-o option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--options PROPERTIES", stdout),
                        "--options option is not in litp update help")
        self.assertTrue(self.is_text_in_list("-h,", stdout),
                        "-h option is not in litp update help")
        self.assertTrue(self.is_text_in_list("--help", stdout),
                        "--help option is not in litp update help")

    @attr('all', 'revert', 'story245', 'story245_tc35', 'cdb_priority1')
    def test_35_p_cli_remove_item(self):
        """
        @tms_id: litpcds_245_tc35
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove item with -j and --json option
        @tms_description: Verify removing an item can be done with the -j and
                          --json option as well as through REST
        @tms_test_steps:
        @step: Create os profile item
        @result: OS profile is created
        @step: Remove os profile item with -j argument
        @result: OS profile item is removed
        @step: Create os profile item
        @result: OS profile is created
        @step: Remove os profile item with --json argument
        @result: OS profile item is removed
        @step: Create os profile item
        @result: OS profile is created
        @step: Remove os profile item through REST
        @result: OS profile item is removed
        @step: Check os profile item updated with -j is equal to os profile
                item updated with --json
        @result: Properties are equal
        @step: Check os profile item updated with -j is equal to os profile
                item updated through REST
        @result: Properties are equal
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_35", False)

        self.log('info', 'Remove os profile item with -j argument')
        litp_remove1, _, _ = self.execute_cli_remove_cmd(self.ms_node, \
                profile_url, "-j")

        self.log('info', 'Check item is removed')
        _, stderr, _ = self.execute_cli_show_cmd(self.ms_node, \
          profile_url, expect_positive=False)

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Not found", stderr),
                        "'Not found' is missing from errorput")

        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_35", False)

        self.log('info', 'Remove os profile item with --json argument')
        litp_remove2, _, _ = self.execute_cli_remove_cmd(self.ms_node, \
                profile_url, "--json")

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Not found", stderr),
                        "'Not found' is missing from errorput")

        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_35", False)

        self.log('info', 'Remove os profile item through REST')
        stdout, stderr, status = self.rest.delete(profile_url)
        self.assertEqual(200, status)
        self.assertEqual("", stderr)

        # CONVERT OUTPUT IN JSON STRUCTURE
        # Replace localhost with ip address in string so comparison with
        # rest output can be made
        remove_output = stdout.replace(self.ms_ip_address, "localhost")
        rest_remove = self.json.load_json(remove_output)

        # COMPARE CLI CREATE AND REST CREATE OUTPUT
        self.assertEqual(litp_remove1, litp_remove2)
        self.assertEqual(litp_remove1, rest_remove)

    @attr('all', 'revert')
    def obsolete_36_p_cli_remove_link(self):
        """
        Description:
            This test ensures user can remove a link from litp tree,
            cli return code is 0, stdout and stderr are empty
            --json output is in json format

        Actions:
            1. Create link with CLI
            2. Remove link with CLI
            3. Check command return code is 0, stdout and stderr are empty
            4. Check test item has been removed with CLI show command
            5. Check command stdout is the same as REST read command output

        Result:
            CLI return code is 0
            Payload is in json format
            stderr is empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026.py:Story4026.\
            test_12_n_inherit_cmd_remove_reference_item
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc37')
    def test_37_n_cli_remove_item_twice(self):
        """
        @tms_id: litpcds_245_tc37
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove item twice
        @tms_description: Verify an InvalidLocationError will be thrown when
                          trying to remove an item that doesn't exist
        @tms_test_steps:
        @step: Create os profile item
        @result: OS profile is created
        @step: Remove os profile item
        @result: OS profile item is removed
        @step: Remove os profile item
        @result: InvalidLocationError is thrown
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_37", False)

        self.log('info', 'Remove os profile item')
        _, _, _ = self.execute_cli_remove_cmd(self.ms_node, \
                profile_url)

        self.log('info', 'Remove os profile item again')
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, \
                profile_url, expect_positive=False)

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Path not found", stderr),
                        "'Path not found' is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc38')
    def test_38_n_cli_remove_incorrect_path(self):
        """
        @tms_id: litpcds_245_tc38
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove invalid path
        @tms_description: Verify an InvalidLocationError will be thrown when
                          executing remove on an invalid path
        @tms_test_steps:
        @step: Executing remove on an invalid path
        @result: Validation error is thrown: InvalidLocationError is thrown
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Executing remove on an invalid path')
        invalid_url = "/invalid_path"
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, \
                invalid_url, expect_positive=False)

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Path not found", stderr),
                        "'Path not found' is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc39')
    def test_39_p_cli_remove_item_parent(self):
        """
        @tms_id: litpcds_245_tc39
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove item parent
        @tms_description: Verify an InvalidLocationError will be thrown when
                          showing a removed items child
        @tms_test_steps:
        @step: Create os profile item
        @result: OS profile is created
        @step: Remove os profile item
        @result: OS profile item is removed
        @step: Check os profile item child path
        @result: Validation error is thrown: InvalidLocationError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info', 'Create os profile item')
        profile_url = self.create_profile("os245_39", False)

        self.log('info', 'Remove os profile item')
        self.execute_cli_remove_cmd(self.ms_node, profile_url)

        self.log('info', 'Check os profile item child path')
        items_url = profile_url + "/items"
        _, stderr, _ = self.execute_cli_show_cmd(self.ms_node, \
          items_url, expect_positive=False)
        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Not found", stderr),
                        "'Not found' is missing from errorput")

    @attr('all', 'revert')
    def obsolete_40_p_cli_remove_link_parent(self):
        """
        Description:
            This test ensures children elements are removed when user
            removes
            parent item from litp tree,
            cli return code is 0, stdout and stderr are empty

        Actions:
            1. Create item with CLI
            2. Create link - the item's child with CLI
            2. Remove item with CLI
            3. Check command return code is 0, stdout and stderr are empty
            4. Check item's child - the link is removed also

        Result:
            CLI return code is 0
            Payload is in json format
            stderr is empty
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026.py:
                Story4026.test_14_n_inherit_cmd_remove_source_item
        testset_story4026.py:Story4026.\
            test_15_p_inherit_cmd_remove_source_item_and_reference_item
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc41')
    def test_41_n_cli_remove_read_only_item(self):
        """
        @tms_id: litpcds_245_tc41
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove read only item
        @tms_description: Verify an MethodNotAllowedError will be thrown when
                          executing remove on a read only path
        @tms_test_steps:
        @step: Remove root path
        @result: MethodNotAllowedError is thrown
        @result: Item has not been removed
        @step: Remove infrastructure path
        @result: MethodNotAllowedError is thrown
        @result: Item has not been removed
        @step: Remove /item-types/deployment path
        @result: MethodNotAllowedError is thrown
        @result: Item has not been removed
        @step: Remove /property-types/basic_string path
        @result: MethodNotAllowedError is thrown
        @result: Item has not been removed
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # REMOVE ROOT ELEMENT
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, "/", \
                expect_positive=False)

        self.assertTrue(self.is_text_in_list(
                        "MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list(
                        "Operation not permitted", stderr),
                        "Expected Message not seen")

        # CHECK ITEM HAS NOT BEEN REMOVED
        self.execute_cli_show_cmd(self.ms_node, "/")

        # REMOVE A COLLECTION
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, \
            "/infrastructure", expect_positive=False)

        self.assertTrue(self.is_text_in_list(
                        "MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list(
                        "Operation not permitted", stderr),
                        "Expected Message not seen")

        # CHECK ITEM HAS NOT BEEN REMOVED
        self.execute_cli_show_cmd(self.ms_node, "/infrastructure")

        # REMOVE AN ITEMTYPE
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, \
            "/item-types/deployment", expect_positive=False)

        self.assertTrue(self.is_text_in_list("MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Remove method on path not "
                                             "allowed", stderr),
                        "'Remove method on path not allowed' "
                        "is missing from errorput")

        # CHECK ITEM HAS NOT BEEN REMOVED
        self.execute_cli_show_cmd(self.ms_node, "/item-types/deployment")

        # REMOVE A PROPRETYTYPE
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, \
            "/property-types/basic_string", expect_positive=False)
        self.assertTrue(self.is_text_in_list("MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Remove method on path not "
                                             "allowed", stderr),
                        "'Remove method on path not allowed' "
                        "is missing from errorput")

        # CHECK ITEM HAS NOT BEEN REMOVED
        self.execute_cli_show_cmd(self.ms_node, "/property-types/basic_string")

    @attr('all', 'revert')
    def obsolete_42_n_cli_remove_linked_resource(self):
        """
        Description:
            This test ensures litp validation fails when user removes linked
            resource from litp tree,
            cli return code is not 0, stdout is empty,
            stderr has UnresolvedLinkError and the link url content.

        Actions:
            1. Create node with CLI
            2. Create os link
            3. Create routes link
            4. Create plan
            5. Check stderr has expected number of UnresolvedLinkError
            6. Check stderr has expected number of MissingRequiredItemError
            7. Check stderr has expected number of CardinalityError

        Result:
            litp validation fails when user removes linked
            resource from litp tree
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026.py:Story4026.\
            test_13_p_inherit_cmd_remove_reference_item
        """
        pass

    @attr('all', 'revert')
    def obsolete_43_n_cli_remove_linked_resource_parent(self):
        """
        Create test node with CLI
        Create os link
        Create route link
        Create plan
        Check stderr has expected number of UnresolvedLinkError
        Check stderr has expected number of MissingRequiredItemError
        Check stderr has expected number of CardinalityError
        Remove the routes link
        Create plan
        Check stderr has expected number of UnresolvedLinkError
        Check stderr has expected number of MissingRequiredItemError
        Check stderr has expected number of CardinalityError
        Removed because linking has been replaced with inherit which is
        tested
        in story LITPCDS-4026
        testset_story4026.py:
            Story4026.test_14_n_inherit_cmd_remove_source_item
        """
        pass

    @attr('all', 'revert', 'story245', 'story245_tc44', 'cdb_tmp')
    def test_44_n_cli_remove_option(self):
        """
        @tms_id: litpcds_245_tc44
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove with invalid optional argument "-i"
        @tms_description: Verify an item is not removed when invalid option
                          argument -i and --invalid is in the remove command
        @tms_test_steps:
        @step: Remove item with invalid option -i
        @result: Message is displayed: unrecognized arguments
        @step: Remove item with invalid option --invalid
        @result: Message is displayed:: unrecognized arguments
        @tms_test_precondition: NA
        @tms_execution_type: Automated

        """
        self.log('info', 'Remove item with invalid option -i')
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, "/", \
                        "-i", expect_positive=False)

        self.log('info', 'Validation error is thrown')
        self.assertTrue(self.is_text_in_list("unrecognized arguments: -i",
                                             stderr),
                        "'unrecognized arguments: -i' is not in errorput")

        self.log('info', 'Remove item with invalid option --invalid')
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node, "/", \
                        "--invalid", expect_positive=False)

        self.assertTrue(self.is_text_in_list("unrecognized arguments: "
                                             "--invalid", stderr),
                        "'unrecognized arguments: --invalid' "
                        "is not in errorput")

    @attr('all', 'revert', 'story245', 'story245_tc45')
    def test_45_n_cli_remove_command_style(self):
        """
        @tms_id: litpcds_245_tc45
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove with incorrect syntax
        @tms_description: Remove commands issued with an invalid syntax will
                         not be successful
        @tms_test_steps:
        @step: Issue remove command with invalid syntax: no arguments
        @result:Message is displayed: argument -p/--path is required
        @step: Issue remove command with invalid syntax: /test update
               name=test
        @result: Message is displayed: invalid choice: '/test
        @step: Issue remove command with invalid syntax: --path / --options
                none
        @result: Message is displayed: unrecognized arguments: --options none
        @step: Issue remove command with invalid syntax: -p -j /deployments
        @result:Message is displayed: argument -p/--path: expected one argument
        @step: Issue remove command with invalid syntax: -p /deployments/*
        @result: Message is displayed: argument -p/--path:  /deployments/*
                is not a valid path argument
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # RUN REMOVE COMMAND WITH WRONG STYLE
        cmd = "{0} {1}".format(self.cli.litp_path, "remove")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("error: argument -p/--path "
                                             "is required", stderr),
                        "'error: argument -p/--path is required' "
                        "is not in errorput")

        # RUN REMOVE COMMAND WITH WRONG STYLE
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "/test", "remove")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("invalid choice: '/test'",
                                             stderr),
                        "'invalid choice: '/test'' is not in errorput")

        # RUN REMOVE COMMAND WITH WRONG STYLE
        cmd = "{0} {1} {2} {3} {4} {5}".format(self.cli.litp_path, "remove",
                                               "--path", "/", "--options",
                                               "none")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("unrecognized arguments: "
                                             "--options none", stderr),
                        "'unrecognized arguments: --options none' "
                        "is not in errorput")

        # RUN REMOVE COMMAND WITH WRONG STYLE
        cmd = "{0} {1} {2} {3} {4}".format(self.cli.litp_path, "remove",
                                           "-p", "-j", "/deployments")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("argument -p/--path: expected "
                                             "one argument", stderr),
                        "'argument -p/--path: expected one argument' "
                        "is not in errorput")

        # RUN REMOVE COMMAND WITH WRONG STYLE
        cmd = "{0} {1} {2} {3}".format(self.cli.litp_path, "remove",
                                       "-p", "/deployments/*")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)
        self.assertNotEqual(0, return_code)
        self.assertEqual([], stdout)
        self.assertTrue(self.is_text_in_list("is not a valid path argument",
                                             stderr),
                        "'is not a valid path argument' is not in errorput")

    @attr('all', 'revert', 'story245', 'story245_tc46')
    def test_46_p_cli_remove_help(self):
        """
        @tms_id: litpcds_245_tc46
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove help
        @tms_description: Verify the litp remove command with option '-h' or
                          '--help'
        @tms_test_steps:
        @step: Run " litp --help
        @result: 'remove' string is in help output
        @step: Run " litp -h
        @result: 'remove' string is in help output
        @step: Run " litp remove--help
        @result: remove command options are in help output
        @step: Run " litp remove -h
        @result: remove command options are in help output
        @tms_test_precondition: NA
        @tms_execution_type: Automated

        """
        self.log('info', 'Run " litp --help')
        cmd = "{0} {1}".format(self.cli.litp_path, "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK REMOVE COMMAND
        self.assertTrue(self.is_text_in_list("remove", stdout),
                        "remove command is not in litp help")

        # GET LITP HELP WITH -h
        cmd = "{0} {1}".format(self.cli.litp_path, "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK REMOVE COMMAND
        self.assertTrue(self.is_text_in_list("remove", stdout),
                        "remove command is not in litp help")

        # GET LITP REMOVE HELP WITH -h
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "remove", "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd,
                                                       add_to_cleanup=False)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK REMOVE COMMAND OPTIONS
        self.assertTrue(self.is_text_in_list("-p PATH", stdout),
                        "-p option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("--path PATH", stdout),
                        "--path option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("-j,", stdout),
                        "-j option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("--json", stdout),
                        "--json option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("-h,", stdout),
                        "-h option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("--help", stdout),
                        "--help option is not in litp remove help")

        # GET LITP REMOVE HELP WITH --help
        cmd = "{0} {1} {2}".format(self.cli.litp_path, "remove", "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd,
                                                       add_to_cleanup=False)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK REMOVE COMMAND OPTIONS
        self.assertTrue(self.is_text_in_list("-p PATH", stdout),
                        "-p option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("--path PATH", stdout),
                        "--path option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("-j,", stdout),
                        "-j option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("--json", stdout),
                        "--json option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("-h,", stdout),
                        "-h option is not in litp remove help")
        self.assertTrue(self.is_text_in_list("--help", stdout),
                        "--help option is not in litp remove help")

    @attr('all', 'revert', 'story245', 'story245_tc47', 'cdb_priority1')
    def test_47_p_cli_create_plan(self):
        """
        @tms_id: litpcds_245_tc47
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create plan
        @tms_description: Verify executing create plan is successful with -j
                          and --json option as well as through REST
        @tms_test_steps:
        @step: Create telnet package
        @result: Telnet package is created
        @step: Inherit telnet package onto node
        @result: Telnet package is inherited onto node
        @step: Create plan with -j option
        @result: Plan is created
        @step: Delete plan
        @result: Plan is deleted
        @step: Create plan with --json option
        @result: Plan is created
        @step: Create plan through Rest
        @result: Plan is created
        @step: Check create plan output with -j is equal to create plan
                with --json
        @result: Both outputs are equal
        @step: Check create plan output with -j is equal to create plan
                through REST
        @result: Both outputs are equal
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # CREATE PACKAGE ITEM
        package_url = self.create_package("telnet")

        # LINK PACKAGE ITEM
        self.inherit_package_item("telnet", package_url)

        # CREATE PLAN WITH SHORT OPTION
        litp_plan1, _, _ = self.execute_cli_createplan_cmd(self.ms_node, "-j")

        # SHOW PLAN FOR DEBUGGING
        self.execute_cli_showplan_cmd(self.ms_node)

        # DELETE PLAN
        self.execute_cli_removeplan_cmd(self.ms_node)

        # CREATE PLAN WITH LONG OPTION
        litp_plan2, _, _ = self.execute_cli_createplan_cmd(self.ms_node,
                                                           "--json")

        # SHOW PLAN FOR DEBUGGING
        self.execute_cli_showplan_cmd(self.ms_node)

        # DELETE PLAN
        self.execute_cli_removeplan_cmd(self.ms_node)

        # CREATE PLAN WITH REST
        message_data = "{\"id\":\"plan\",\"type\":\"plan\"}"
        stdout, stderr, status = self.rest.post("/plans",
                                            header=self.rest.HEADER_JSON,
                                            data=message_data)
        self.assertEqual(201, status)
        self.assertEqual("", stderr)

        # CONVERT OUTPUT IN JSON STRUCTURE
        # Replace localhost with ip address in string so comparison with
        # rest output can be made
        plan_output = stdout.replace(self.ms_ip_address, "localhost")
        rest_plan = self.json.load_json(plan_output)

        # COMPARE CLI CREATE AND REST CREATE OUTPUT
        self.assertEqual(litp_plan2, litp_plan1)
        self.assertEqual(rest_plan, litp_plan1)

        # SHOW PLAN FOR DEBUGGING
        self.execute_cli_showplan_cmd(self.ms_node)

    @attr('all', 'revert', 'story245', 'story245_tc48')
    def test_48_n_cli_create_plan_empty(self):
        """
        @tms_id: litpcds_245_tc48
        @tms_requirements_id: LITPCDS-245
        @tms_title: cli create plan empty
        @tms_description: Executing a remove or create plan when one doesn't
                          exist in the model results in a DoNothingPlanError
        @tms_test_steps:
        @step: Execute remove plan command
        @result: No plan is removed
        @step: Execute create plan command
        @result: No plan is created
        @result: Validation error is thrown: DoNothingPlanError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        self.log('info', 'Execute remove plan command')
        self.execute_cli_removeplan_cmd(self.ms_node, expect_positive=False)

        self.log('info', 'Execute create plan command')
        _, stderr, _ = self.execute_cli_createplan_cmd(self.ms_node, \
                    expect_positive=False)

        # SHOW PLAN FOR DEBUGGING
        self.execute_cli_showplan_cmd(self.ms_node, expect_positive=False)

        self.log('info', 'Check DoNothingPlanError in output')
        self.assertTrue(self.is_text_in_list(
            "DoNothingPlanError", stderr),
            "DoNothingPlanError is missing from errorput")
        self.assertTrue(self.is_text_in_list(
            "Create plan failed: no tasks were generated", stderr),
            "'Create plan failed' is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc49')
    def test_49_n_cli_create_plan_element(self):
        """
        @tms_id: litpcds_245_tc49
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli create plan element
        @tms_description: Create command with invalid path results in a
                          MethodNotAllowedError
        @tms_test_steps:
        @step: Execute create command with invalid path
        @result: Validation error is thrown: MethodNotAllowedError is thrown
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # CREATE AN INVALID PLAN
        profile_url = "/plans/plan/rhel_7_7"
        props = "name='sample-profile' version='rhel7'"
        _, stderr, _ = self.execute_cli_create_cmd(self.ms_node, profile_url, \
                "os-profile", props, expect_positive=False)

        self.assertTrue(self.is_text_in_list("MethodNotAllowedError", stderr),
                        "MethodNotAllowedError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Create method on path not "
                                             "allowed", stderr),
                        "'Create method on path not allowed' "
                        "is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc50', 'cdb_priority1')
    def test_50_p_cli_show_plan(self):
        """
        @tms_id: litpcds_245_tc50
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli show plan
        @tms_description: Verify executing show plan displays task and phases
        @tms_test_steps:
        @step: Create telnet package
        @result: Telnet package is created
        @step: Inherit telnet package onto node
        @result: Telnet package is inherited onto node
        @step: Create plan
        @result: Plan is created
        @step: Show plan
        @result: Plan is displayed
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # CREATE PACKAGE ITEM
        package_url = self.create_package("telnet")

        # LINK PACKAGE ITEM
        self.inherit_package_item("telnet", package_url)

        # CREATE PLAN
        self.execute_cli_createplan_cmd(self.ms_node)

        # SHOW PLAN
        stdout, _, _ = self.execute_cli_showplan_cmd(self.ms_node)
        self.assertFalse(self.is_text_in_list("Phase 0", stdout),
                         "Phase 0 is in show_plan output")
        self.assertTrue(self.is_text_in_list("Phase 1", stdout),
                        "Phase 1 is not in show_plan output")
        self.assertTrue(self.is_text_in_list("Tasks:", stdout),
                        "Tasks is not in show_plan output")
        self.assertTrue(self.is_text_in_list("Initial:", stdout),
                        "Initial is not in show_plan output")
        self.assertTrue(self.is_text_in_list("Running:", stdout),
                        "Running is not in show_plan output")
        self.assertTrue(self.is_text_in_list("Failed:", stdout),
                        "Failed is not in show_plan output")

    @attr('all', 'revert', 'story245', 'story245_tc51')
    def test_51_n_cli_show_plan_empty(self):
        """
        @tms_id: litpcds_245_tc51
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli show empty plan
        @tms_description: Verify executing show plan when plan is empty
                          returns an InvalidLocationError
        @tms_test_steps:
        @step: Remove plan
        @result: No Plan is removed
        @step: Show plan
        @result: Validation error is thrown: InvalidLocationError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # DELETE PLAN
        self.execute_cli_removeplan_cmd(self.ms_node, expect_positive=False)

        # SHOW PLAN
        _, stderr, _ = self.execute_cli_showplan_cmd(self.ms_node, \
                expect_positive=False)

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Plan does not exist", stderr),
                        "'Plan does not exist' is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc52', 'cdb_priority1')
    def test_52_p_cli_run_plan(self):
        """
        @tms_id: litpcds_245_tc52
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli run plan
        @tms_description: Verify executing run plan results in a successful
                          plan
        @tms_test_steps:
        @step: Create telnet package
        @result: Telnet package is created
        @step: Inherit telnet package onto node
        @result: Telnet package is inherited onto node
        @step: Create plan
        @result: Plan is created
        @step: Show plan
        @result: Show plan is successful
        @step: Run plan
        @result: Plan plan is successful
        @result: Plan completes successfully
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # CREATE PACKAGE ITEM
        package_url = self.create_package("telnet")

        # LINK PACKAGE ITEM
        self.inherit_package_item("telnet", package_url)

        # CREATE PLAN
        self.execute_cli_createplan_cmd(self.ms_node)

        # SHOW PLAN FOR DEBUGGING
        self.execute_cli_showplan_cmd(self.ms_node)

        # RUN PLAN
        self.execute_cli_runplan_cmd(self.ms_node)

        is_completed = self.wait_for_plan_state(self.ms_node,
                                                test_constants.PLAN_COMPLETE,
                                                timeout_mins=3)
        self.assertTrue(is_completed, "Plan was not successful")

    @attr('all', 'revert', 'story245', 'story245_tc53')
    def test_53_n_cli_run_plan_empty(self):
        """
        @tms_id: litpcds_245_tc53
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli run empty plan
        @tms_description: Verify executing run plan fails when no create plan
                          is executed first
        @tms_test_steps:
        @step: Execute remove plan
        @result: Remove plan fails
        @step: Run plan
        @result: Run plan fails
        @result: Validation error is thrown: InvalidLocationError
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # DELETE PLAN
        self.execute_cli_removeplan_cmd(self.ms_node, expect_positive=False)

        # RUN PLAN
        _, stderr, _ = self.execute_cli_runplan_cmd(self.ms_node, \
                expect_positive=False)

        self.assertTrue(self.is_text_in_list("InvalidLocationError", stderr),
                        "InvalidLocationError is missing from errorput")
        self.assertTrue(self.is_text_in_list("Plan does not exist", stderr),
                        "'Plan does not exist' is missing from errorput")

    @attr('all', 'revert', 'story245', 'story245_tc54', 'cdb_priority1')
    def test_54_p_cli_stop_plan(self):
        """
        @tms_id: litpcds_245_tc54
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli stop plan
        @tms_description: Verify stop plan succeeds within 3 minutes while
                            plan is running
        @tms_test_steps:
        @step: Create telnet package
        @result: Telnet package is created
        @step: Inherit telnet package onto node
        @result: Telnet package is inherited onto node
        @step: Create plan
        @result: Plan is created
        @step: Run plan
        @result: Plan is running
        @step: Stop plan while plan is running
        @result: Plan stops within 3 minutes
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Create source LITP package item')
        package_url = self.create_package("telnet")

        self.log('info',
        '2. Inherit the created item into node')
        self.inherit_package_item("telnet", package_url)

        self.log('info',
        '3. Create a plan')
        self.execute_cli_createplan_cmd(self.ms_node)
        self.execute_cli_showplan_cmd(self.ms_node)

        self.log('info',
        '4. Run the plan')
        self.execute_cli_runplan_cmd(self.ms_node)

        self.log('info',
        '5. Stop the plan')
        self.execute_cli_stopplan_cmd(self.ms_node)

        self.log('info',
        '6. Verify that plan has stopped')
        is_stopped = self.wait_for_plan_state(self.ms_node,
                                              test_constants.PLAN_STOPPED,
                                              timeout_mins=3)
        self.assertTrue(is_stopped, 'Attempt to stop a running plan failed')

    @attr('all', 'revert', 'story245', 'story245_tc55')
    def test_55_n_cli_stop_plan_empty(self):
        """
        @tms_id: litpcds_245_tc55
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli stop empty plan
        @tms_description: Verify stop plan fails when a plan doesn't exist
        @tms_test_steps:
        @step: If a plan exits remove it
        @result: Plan is removed
        @step: Stop plan
        @result: Validation error is thrown: InvalidLocationError
        @result: Message diplayed: Plan does not exist
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Ensure that there is not plan on system')
        if self.find(self.ms_node, '/plans', 'plan', assert_not_empty=False):
            self.execute_cli_removeplan_cmd(self.ms_node, expect_positive=True)

        self.log('info',
        '2. Attempt to stop a plan')
        _, stderr, _ = self.execute_cli_stopplan_cmd(self.ms_node,
                                                     expect_positive=False)

        self.log('info',
        '3. Verify that correct error message is thrown')
        expected_errors = ['/plans',
                          'InvalidLocationError    Plan does not exist']
        for line in expected_errors:
            self.assertTrue(self.is_text_in_list(line, stderr),
                '\nExpected text "{0}" not found on error message'
                '\nACTUAL ERROR MESSAGE\n{1}'
                .format(line, '\n'.join(stderr)))

    @attr('all', 'revert', 'story245', 'story245_tc56', 'cdb_priority1')
    def test_56_p_cli_remove_plan(self):
        """
        @tms_id: litpcds_245_tc56
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove plan
        @tms_description: Verify an InvalidLocationError is thrown when a
        plan doesn't exist
        @tms_test_steps:
        @step: Create package item
        @result: Package is created
        @step: Inherit package onto node
        @result: Package is inherited on to node
        @step: Create plan
        @result: Plan is created
        @step: Show plan
        @result: Plan is shown
        @step: Remove plan
        @result: Plan is removed
        @step: Show plan
        @result: InvalidLocationError is thrown: Plan does not exist
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Create source package LITP item')
        package_url = self.create_package("telnet")

        self.log('info',
        '2. Inherit package on node')
        self.inherit_package_item("telnet", package_url)

        self.log('info',
        '3. Create plan')
        self.execute_cli_createplan_cmd(self.ms_node)
        self.execute_cli_showplan_cmd(self.ms_node)

        self.log('info',
        '4. Remove plan')
        self.execute_cli_removeplan_cmd(self.ms_node)

        self.log('info',
        '5. Verify that plan does not exists')
        _, stderr, _ = self.execute_cli_showplan_cmd(self.ms_node,
                                                     expect_positive=False)
        expected_errors = ['/plans',
                         'InvalidLocationError    Plan does not exist']
        for line in expected_errors:
            self.assertTrue(self.is_text_in_list(line, stderr),
                '\nExpected text "{0}" not found on error message'
                '\nACTUAL ERROR MESSAGE\n{1}'
                .format(line, '\n'.join(stderr)))

    @attr('all', 'revert', 'story245', 'story245_tc57')
    def test_57_n_cli_remove_plans_item(self):
        """
        @tms_id: litpcds_245_tc57
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli remove plan item
        @tms_description: Cannot remove collection item directly
        @tms_test_steps:
        @step: Execute remove command on '/plans' path
        @result: Validation error is thrown: MethodNotAllowedError
        @result: Message is displayed: Cannot directly delete Collection item
        @step: Check collection item '/plans' is still in the model
        @result: Collection item '/plans' is still in the model
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Attempt to remove "/plans" item')
        _, stderr, _ = self.execute_cli_remove_cmd(self.ms_node,
                                            "/plans", expect_positive=False)

        self.log('info',
        '2. Verify that expected error message is thrown')
        expected_errors = [
            '/plans',
            'MethodNotAllowedError    Cannot directly delete Collection item']
        for line in expected_errors:
            self.assertTrue(self.is_text_in_list(line, stderr),
                '\nExpected text "{0}" not found on error message'
                '\nACTUAL ERROR MESSAGE\n{1}'
                .format(line, '\n'.join(stderr)))
        self.log('info',
        '3. Verify that the item "/plans" is still on model')
        self.execute_cli_show_cmd(self.ms_node, '/plans')

    @attr('all', 'revert', 'story245', 'story245_tc58')
    def test_58_p_cli_plan_help(self):
        """
        @tms_id: litpcds_245_tc58
        @tms_requirements_id: LITPCDS-245
        @tms_title: Cli plan help
        @tms_description: Verify the litp plan command with option '-h' or
                          '--help' displays option information
        @tms_test_steps:
        @step: Run " litp --help
        @result: "create_plan", "show_plan", "run_plan", "stop_plan" and
                 "remove_plan" is displayed
        @step: Run " litp -h
        @result: "create_plan", "show_plan", "run_plan", "stop_plan" and
                 "remove_plan" is displayed
        @step: Run create_plan -h
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run show_plan -h
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run create_plan -h
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run run_plan -h
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run stop_plan -h
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run remove_plan -h
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run create_plan --help
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run show_plan --help
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run create_plan --help
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run run_plan --help
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run stop_plan --help
        @result: "-j", "--json", "-h" and "--help" is displayed
        @step: Run remove_plan --help
        @result: "-j", "--json", "-h" and "--help" is displayed
        @tms_test_precondition: NA
        @tms_execution_type: Automated

        """
        # GET LITP HELP WITH --help
        cmd = "{0} {1}".format(self.cli.litp_path, "--help")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK PLAN COMMANDS
        for command in ["create_plan", "show_plan", "run_plan",
                        "stop_plan", "remove_plan"]:
            self.assertTrue(self.is_text_in_list(command, stdout),
                            "{0} command is not in litp help".format(command))

        # GET LITP HELP WITH -h
        cmd = "{0} {1}".format(self.cli.litp_path, "-h")
        stdout, stderr, return_code = self.run_command(self.ms_node, cmd)

        self.assertEqual(0, return_code)
        self.assertEqual([], stderr)

        # CHECK PLAN COMMANDS
        for command in ["create_plan", "show_plan", "run_plan",
                        "stop_plan", "remove_plan"]:
            self.assertTrue(self.is_text_in_list(command, stdout),
                            "{0} command is not in litp help".format(command))

        # GET LITP PLAN COMMANDS HELP WITH -h
        for command in ["create_plan", "show_plan", "run_plan",
                        "stop_plan", "remove_plan"]:
            cmd = "{0} {1} {2}".format(self.cli.litp_path, command, "-h")
            stdout, stderr, return_code = \
                self.run_command(self.ms_node, cmd, add_to_cleanup=False)

            self.assertEqual(0, return_code)
            self.assertEqual([], stderr)

            # CHECK PLAN COMMAND OPTIONS
            self.assertTrue(self.is_text_in_list("-j,", stdout),
                            "-j option is not in litp {0} help".
                            format(command))
            self.assertTrue(self.is_text_in_list("--json", stdout),
                            "--json option is not in litp {0} help".
                            format(command))
            self.assertTrue(self.is_text_in_list("-h,", stdout),
                            "-h option is not in litp {0} help".
                            format(command))
            self.assertTrue(self.is_text_in_list("--help", stdout),
                            "--help option is not in litp {0} help".
                            format(command))

        # GET LITP REMOVE HELP WITH --help
        for command in ["create_plan", "show_plan", "run_plan",
                        "stop_plan", "remove_plan"]:
            cmd = "{0} {1} {2}".format(self.cli.litp_path, command, "--help")
            stdout, stderr, return_code = \
                self.run_command(self.ms_node, cmd, add_to_cleanup=False)

            self.assertEqual(0, return_code)
            self.assertEqual([], stderr)

            # CHECK PLAN COMMAND OPTIONS
            self.assertTrue(self.is_text_in_list("-j,", stdout),
                            "-j option is not in litp {0} help".
                            format(command))
            self.assertTrue(self.is_text_in_list("--json", stdout),
                            "--json option is not in litp {0} help".
                            format(command))
            self.assertTrue(self.is_text_in_list("-h,", stdout),
                            "-h option is not in litp {0} help".
                            format(command))
            self.assertTrue(self.is_text_in_list("--help", stdout),
                            "--help option is not in litp {0} help".
                            format(command))
