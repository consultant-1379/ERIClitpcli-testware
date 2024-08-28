'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.


@since:     October 2013
@author:    Ares
@summary:   LITPCDS-4026
            As a LITP Developer I want subclass model items so that I can more
            efficiently create populated items but with their own configurable
            properties
'''

import os
import test_constants as const
from litp_generic_test import GenericTest, attr


class Story4026(GenericTest):
    """As a LITP Developer I want subclass model items so that I can more
       efficiently create populated items but with their own configurable
       properties"""

    def setUp(self):
        """Runs before every test to perform required setup"""
        super(Story4026, self).setUp()
        self.ms1 = self.get_management_node_filename()
        self.ms_ip = self.get_node_att(self.ms1, 'ipv4')
        self.story_id = 'story4026'

    def tearDown(self):
        """Runs after every test to perform required cleanup/teardown"""
        super(Story4026, self).tearDown()

    def get_local_rpm_paths(self, path, story_id):
        """
        given a path (which should contain some RPMs) and a substring
        which is present in the RPM names you want, return a list of
        absolute paths to the RPMS that are local to your test

        Arguments:
            path (str): path where to search for rpm files
            story_id (str): filter to apply to rmp file search
        """
        # get all RPMs in 'path' that contain 'rpm_substring' in their name
        rpm_names = [rpm for rpm in os.listdir(path)
                        if story_id in rpm and 'rpm' in rpm]

        self.assertNotEqual(len(rpm_names), 0,
            'Unable to find any rpm files on MS at {0}'.format(path))

        # return a list of absolute paths to the RPMs found in 'rpm_names'
        return [
            os.path.join(rpath, rpm)
            for rpath, rpm in
            zip([os.path.abspath(path)] * len(rpm_names), rpm_names)
        ]

    def install_rpms(self):
        """
        Check if packages are installed install. If not install
        Note: installed packages will not get removed at end of the test
        """
        local_rpm_paths = self.get_local_rpm_paths(
            os.path.dirname(repr(__file__).strip('\'')), self.story_id)

        for local_rpm_path in local_rpm_paths:
            pkg = os.path.basename(local_rpm_path).strip('.rpm')
            installed = self.check_pkgs_installed(
                                self.ms1, [pkg + "_CXP1234567"], su_root=True)
            if not installed:
                self.assertTrue(self.copy_and_install_rpms(self.ms1,
                                                           [local_rpm_path]))

    def add_package_model_item(self):
        """create a package-list/package in the software model"""

        # software-item collection path
        software_items = self.find(
            self.ms1, '/software', 'software-item', False
        )[0]

        # package-list create path
        package_list = os.path.join(
            software_items, '{0}_packages'.format(self.story_id)
        )

        # create package-list
        self.execute_cli_create_cmd(
            self.ms1, package_list, 'package-list',
            'name=\'{0}_packages\''.format(self.story_id)
        )

        # package create path
        package = os.path.join(
            package_list, 'packages/{0}'.format(self.story_id)
        )

        # create package
        props = "name='finger' config='keep' epoch='0'"
        self.execute_cli_create_cmd(
            self.ms1, package, 'package', props
        )

        return package_list, package

    def create_node(self, test_node_name):
        """wrapper function for creating a node and getting
           necessary information for running inherit commands.
           We return the nodes storage path and the path from
           which this storage profile is linked to"""
        # create a node
        results = self.run_commands(
            self.ms1,
            self.get_create_node_deploy_cmds(
                self.ms1, node_name=test_node_name,
                hostname=test_node_name
            )
        )
        self.assertEquals([], self.get_errors(results))

        # get test node path
        test_node_path = [
            node for node in
            self.find(self.ms1, "/deployments", "node")
            if "4026" in node
        ][0]

        # build test node storage profile path
        node_os_path = os.path.join(test_node_path, "os")

        # get default storage profile that we the node is linked to
        std_out, std_err, rcode = self.run_command(
            self.ms1,
            self.cli.get_show_data_value_cmd(node_os_path, "inherited from")
        )
        self.assertNotEqual([], std_out)
        self.assertEqual([], std_err)
        self.assertEqual(0, rcode)

        # get source path string which we will use as an argument to
        # the inherit command
        source_path = std_out[0]

        # get storage_profile_name from source path
        os_profile_version = self.get_props_from_url(
            self.ms1, source_path, "version",
            show_option=''
        )
        self.assertNotEqual("", os_profile_version)

        return node_os_path, source_path

    @attr('all', 'revert', 'story4026', 'story4026_tc01')
    def test_01_p_cli_inherit_command(self):
        """
        @tms_id:
            litpcds_4026_tc01
        @tms_requirements_id:
            LITPCDS-4026
        @tms_title:
            Test valid usage of the "inherit" command
        @tms_description:
            Test that a user can create an item using the "inherit" command
            both with and/or without overriding property values locally

        @tms_test_steps:
        @step: Create a new node structure in the model which contains an
               inherited "storage_profile" item to use in this test
        @result: The model structure is created successfully
        @result: The structure has one "storage_profile" item
        @result: The "storage_profile" item inherits from a source item
        @result: The "storage_profile" item's parent is known
        @step: Remove the "storage_profile" item
        @result: The command executed successfully
        @step: Inherit "storage_profile" from source again without overriding
               any property value
        @result: The "storage_profile" item is in the model in Initial state
        @result: The "storage_profile" item inherits from correct source
        @result: Properties of "storage_profile" are marked with an
                 asterisk to indicate that they have not been overridden
        @result: The "CLI" and the "JSON" output format of the "show" command
                 against the "storage_profile" item are in agreement
        @step: Create a plan
        @result: A plan is created successfully
        @step: Remove the "storage_profile" item
        @result: The command executed successfully
        @step: Inherit "storage_profile" from source overriding the "breed"
               property
        @result: The property "breed" has been overridden locally
        @result: All other property values are still inheriting from source
        @result: The "CLI" and the "JSON" output format of the "show" command
                 against the "storage_profile" item are in agreement
        @step: Create a plan
        @result: A plan is created successfully

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Create a new node structure in the model which contains an '
            'inherited "storage_profile" item to use in this test')
        node_os_path, source_path = self.create_node("testnode4026")

        self.log('info',
        '2. Remove the inherited "storage_profile" item from the node '
            'structure just created')
        self.execute_cli_remove_cmd(self.ms1, node_os_path)

        self.log('info',
        '3. Inherit "storage_profile" from source again without overriding '
            'any property value')
        self.execute_cli_inherit_cmd(self.ms1, node_os_path, source_path)

        self.log('info',
        '4. Assert that inherited item "storage_profile" is in Initial state')
        self.assertEqual('Initial', self.execute_show_data_cmd(
                                            self.ms1, node_os_path, 'state'))

        self.log('info',
        '5. Assert that we can create a plan successfully')
        self.execute_cli_createplan_cmd(self.ms1)

        self.log('info',
        '6. Assert that "storage_profile" item inherits from correct source')
        inherited_path = self.execute_show_data_cmd(
                                    self.ms1, node_os_path, "inherited from")
        self.assertEqual(source_path, inherited_path)

        self.log('info',
        '7. Assert properties of the inherited "storage_profile" item have '
            'not been overridden locally and that the "CLI" and JSON output '
            'of the "show" command are in agreement')

        # The output of the command "show" in JSON format will list all
        # properties that have been overridden in the "properties-overwritten"
        # list. We expect undefined "properties-overwritten" list here
        props_j, _, _ = self.execute_cli_show_cmd(self.ms1, node_os_path, '-j')
        self.assertEqual(None, props_j.get('properties-overwritten'))

        # The output of the "show" command in CLI format will mark a property
        # value with an asterisk if it is inherited and not overridden
        # We expect all the property values marked as inherited
        props_cli = self.get_props_from_url(self.ms1,
                                            node_os_path, show_option='')

        for prop, value in props_cli.iteritems():
            self.assertTrue('[*]' in value,
                'Property "{0} is not marked as inherited'.format(prop))

        self.assertNotEqual(None, props_cli.get('breed'))

        self.log('info',
        '8. Remove the and re-inherit "storage_profile" overriding property '
            '"breed" locally this time')
        self.execute_cli_remove_cmd(self.ms1, node_os_path)

        self.execute_cli_inherit_cmd(self.ms1,
                            node_os_path, source_path, props="breed=Fuduntu")

        self.log('info',
        '9. Assert that we can create a plan successfully')
        self.execute_cli_removeplan_cmd(self.ms1)
        self.execute_cli_createplan_cmd(self.ms1)

        self.log('info',
        '10. Assert that the property "breed" has been overridden locally '
             'and that CLI and JSON output of the "show" command are in '
             'agreement')
        props_j, _, _ = self.execute_cli_show_cmd(self.ms1, node_os_path, "-j")

        self.assertEqual(['breed'], props_j['properties-overwritten'])

        props_cli = self.get_props_from_url(self.ms1,
                                            node_os_path, show_option='')

        for prop, value in props_cli.iteritems():
            if prop == 'breed':
                self.assertFalse('[*]' in value,
                    'Property "{0} is marked as inherited'.format(prop))
            else:
                self.assertTrue('[*]' in value,
                    'Property "{0} is not marked as inherited'.format(prop))

    @attr('all', 'revert', 'story4026', 'story4026_tc03')
    def test_03_n_cli_inherit_command_reference_exists(self):
        """
        @tms_id:
            litpcds_4026_tc03
        @tms_requirements_id:
            LITPCDS-4026
        @tms_title:
            Test "inherit" command with duplicate path
        @tms_description:
            Test that if a user attempts to inherit an item using a duplicate
            destination path an "ItemExistsError" is thrown

        @tms_test_steps:
        @step: Create a source "software-item" to use in this test
        @result: The command executed successfully
        @step: Inherit the source "software-item" onto the MS
        @result: The command executed successfully
        @step: Inherit the same source item onto the same path again
        @result: A "ItemExistsError" is thrown

        @tms_test_precondition: NA
        @tms_execution_type: Automated

        """
        self.log('info',
        '1. Create a source "software-item" to use in this test')
        sw_software_item_path = self.find(self.ms1,
                                    "/software", "software-item", False)[0]
        sw_pkg_path = os.path.join(sw_software_item_path, "finger")
        self.execute_cli_create_cmd(self.ms1,
                                    sw_pkg_path, "package", "name=finger")

        self.log('info',
        '2. Inherit the source "software-item" onto the MS')
        ms_software_item_path = self.find(self.ms1,
                                          "/ms", "software-item", False)[0]
        ms_pkg_path = os.path.join(ms_software_item_path, "finger")
        self.execute_cli_inherit_cmd(self.ms1, ms_pkg_path, sw_pkg_path)

        self.log('info',
        '3. Inherit the same source item onto the same path again')
        _, stderr, _ = self.execute_cli_inherit_cmd(self.ms1,
                            ms_pkg_path, sw_pkg_path, expect_positive=False)

        expected_errors = [
            {
                'url': '/ms/items/finger',
                'error_type': 'ItemExistsError',
                'msg': '    Item already exists in model: finger'
            }
        ]
        missing, extra = self.check_cli_errors(expected_errors, stderr)
        self.assertEqual([], missing)
        self.assertEqual([], extra)

        self.log('info',
        '4. Remove inherited item to avoid cleanup to fail')
        self.execute_cli_remove_cmd(self.ms1, ms_pkg_path)

    @attr('all', 'revert', 'story4026', 'story4026_tc04')
    def test_04_n_cli_inherit_command_invalid_vpath(self):
        """
        @tms_id:
            litpcds_4026_tc04
        @tms_requirements_id:
            LITPCDS-4026
        @tms_title:
            Test "inherit" command with invalid paths
        @tms_description:
            Test that if a user attempts to inherit using invalid source or
            destination paths an error is thrown

        @tms_test_steps:
        @step: Inherit from a source path that does not exist
        @result: An "InvalidLocationError" is thrown
        @result: Inherited items is not created
        @step: Inherit into a valid destination path and with invalid child
               item type
        @result: A "ChildNotAllowedError" is thrown
        @result: Inherited items is not created
        @step: Inherit into an destination path which contains invalid
               characters
        @result: A "Usage" message is posted
        @result: Inherited items is not created

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Inherit from a source path that does not exist')
        node_storage_path = self.find(self.ms1,
                                      "/deployments", "storage-profile")[0]

        invalid_source_path = "/invalid_path"
        destination_path = '{0}/child_4026_tc04'.format(node_storage_path)

        _, stderr, _ = self.execute_cli_inherit_cmd(self.ms1,
                                                    destination_path,
                                                    invalid_source_path,
                                                    expect_positive=False)

        expected_errors = [
            {
                'url': invalid_source_path,
                'error_type': 'InvalidLocationError',
                'msg': "    Source item /invalid_path doesn't exist"
            }
        ]
        missing, extra = self.check_cli_errors(expected_errors, stderr)
        self.assertEqual([], missing)
        self.assertEqual([], extra)

        self.execute_cli_show_cmd(self.ms1, destination_path,
                                  expect_positive=False)

        self.log('info',
        '2. Inherit into a valid destination path and with invalid child '
            'item type')
        source_storage_path = self.find(self.ms1,
                                    "/infrastructure", "storage-profile")[0]
        invalid_destination_path = '/ms/invalid_path'
        _, stderr, _ = self.execute_cli_inherit_cmd(self.ms1,
                                                     invalid_destination_path,
                                                     source_storage_path,
                                                     expect_positive=False)

        expected_errors = [
            {
                'error_type': 'ChildNotAllowedError',
                'msg': " in property: \"storage-profile\"    'invalid_path' "
                       "(type: 'storage-profile') is not an allowed child of /"
            }
        ]
        missing, extra = self.check_cli_errors(expected_errors, stderr)
        self.assertEqual([], missing)
        self.assertEqual([], extra)

        self.execute_cli_show_cmd(self.ms1, invalid_destination_path,
                                  expect_positive=False)

        self.log('info',
        '3. Inherit into an destination path which contains invalid '
            'characters')
        invalid_destination_path = '/invalid_@_path'
        _, stderr, _ = self.execute_cli_inherit_cmd(self.ms1,
                                                     invalid_destination_path,
                                                     source_storage_path,
                                                     expect_positive=False)

        expected_errors = [
            {'msg': "Usage: litp inherit [-h] -p PATH -s SOURCE_PATH"},
            {'msg': "[-o [PROPERTIES [PROPERTIES ...]]] [-j]"},
            {'msg': "litp inherit: error: argument -p/--path: /invalid_@_path "
                    "is not a valid path argument"}
        ]
        missing, extra = self.check_cli_errors(expected_errors, stderr)
        self.assertEqual([], missing)
        self.assertEqual([], extra)

        self.execute_cli_show_cmd(self.ms1, invalid_destination_path,
                                  expect_positive=False)

    @attr('all', 'revert', 'story4026', 'story4026_tc06')
    def test_06_p_plugin_inherit_command_query_reference_item(self):
        """
        @tms_id:
            litpcds_4026_tc06
        @tms_requirements_id:
            LITPCDS-4026
        @tms_title:
            Test that a plug-in is be able to query an inherit reference item
        @tms_description:
            Verify that a plug-in is be able to query the reference type of
            an inherited item and return tasks
            NOTE: Once a plug-in is installed and registered with the LITP
                  service, it cannot be removed

        @tms_test_steps:
        @step: Install dummy plug-ins to use during test
        @result: The command executed successfully
        @step: Create a source item of type provided by the dummy plug-in
        @result: The command executed successfully
        @step: Inherit from source into a node
        @result: The command executed successfully
        @result: The inherited item has a reference to the source item
        @step: Create the plan
        @result: Plan completed successfully
        @result: Task referred to the dummy item type is in the plan

        @tms_test_precondition:
        Dummy plug-ins and extension types as described in the LITP 2 SDK are
        required.
        The plug-ins must be edited to make use of the new reference type.
        The following are examples of dummy plug-in:
        ERIClitpstory4026api.rpm
        ERIClitpstory4026.rpm

        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Copy and install plug-in rpms to use during test')
        self.install_rpms()

        self.log('info',
        '2. Create a source item of type provided by the dummy plug-in')
        software_item = self.find(self.ms1,
                                  '/software', 'software-item', False)[0]

        source_path = os.path.join(software_item,
                                   '{0}_source'.format(self.story_id))

        props = "name='{0}_source'".format(self.story_id)
        self.execute_cli_create_cmd(self.ms1,
                                    url=source_path,
                                    class_type=self.story_id,
                                    props=props)

        self.log('info',
        '3. Inherit from source into a node')
        node = self.find(self.ms1, '/deployments', 'node')[0]

        destination_path = os.path.join(node,
                                        'items/{0}'.format(self.story_id))

        self.execute_cli_inherit_cmd(self.ms1, destination_path, source_path)
        self.assertEqual(source_path,
            self.execute_show_data_cmd(self.ms1,
                                       destination_path, 'inherited from'))

        self.log('info',
        '4. Assert that a plan can be created')
        self.execute_cli_createplan_cmd(self.ms1)

        self.log('info',
        '5. Assert that the plug-in was able to query the new reference type '
            'by verifying that the relevant task is in the plan')
        stdout, _, _ = self.execute_cli_showplan_cmd(self.ms1)
        self.assertTrue(
            self.is_text_in_list('ConfigTask() {0}'.format(self.story_id),
            stdout))

    @attr('all', 'revert', 'story4026', 'story4026_tc08')
    def test_08_p_inherit_cmd_update_reference_item_property_cli(self):
        """
        @tms_id:
            litpcds_4026_tc08
        @tms_requirements_id:
            LITPCDS-4026
        @tms_title:
            Test property update mechanism with inherited items
        @tms_description:
            Test that with an inheritance structure of one source item and
            two inherited items if a user overrides the value of a property
            on one of the  inherited items, then updating the value of same
            property on the source item will not have effect on it.
            The same property on the other inherited item will be updated.

        @tms_test_steps:
        @step: Create source items type "package-list" and its child "package"
        @result: The item structure is created on the model
        @step: Inherit source "package-list" onto each node
        @result: Inherited items and their descendants are successfully created
        @result: Inherited item reference is pointing to the correct source
        @step: Create the plan
        @result: Plan created successfully
        @step: Update property "name" of inherited "package" item on node1
        @result: "name" property on source and inherited items have different
                 value
        @result: Property "name" of the inherited item is marked as
                 "overridden"
        @result: Plan is now invalid
        @step: Update source package item "name" property value
        @result: Overridden property "name" has not changed
        @result: Not overridden property "name" has changed

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        self.log('info',
        '1. Create source items type "package-list" and its child "package"')
        source_package_list_url, source_package_url = \
                                            self.add_package_model_item()

        self.log('info',
        '2. Inherit source "package-list" onto each node')
        nodes = self.find(self.ms1, '/deployments', 'node')
        inherited_urls = list()
        for node in nodes:
            inherit_url = os.path.join(node, 'items/{0}'.format(self.story_id))
            inherited_urls.append(inherit_url)

            self.execute_cli_inherit_cmd(self.ms1,
                                         url=inherit_url,
                                         source_path=source_package_list_url)

            inherited_from = self.execute_show_data_cmd(self.ms1,
                                            inherit_url, 'inherited from')
            self.assertEqual(source_package_list_url, inherited_from)

            inherit_package_url = \
                    '{0}/packages/{1}'.format(inherit_url, self.story_id)
            item_data, _, _ = self.execute_cli_show_cmd(
                                        self.ms1, inherit_package_url, '-j')
            self.assertFalse(item_data.get('properties-overwritten', False))

        # The model structure of the relevant items now looks like this:
        # /software/items/story4026_packages
        # /software/items/story4026_packages/packages/story4026
        # /deployments/.../nodes/n1/items/story4026/packages/story4026
        # /deployments/.../nodes/n2/items/story4026/packages/story4026

        self.log('info',
        '3. Create the plan')
        self.execute_cli_createplan_cmd(self.ms1)

        self.log('info',
        '4. Update property "name" of inherited package item on node1')
        update_url = os.path.join(inherited_urls[0],
                                   'packages/{0}'.format(self.story_id))

        self.execute_cli_update_cmd(self.ms1, update_url, 'name="firefox"')

        item_data, _, _ = self.execute_cli_show_cmd(self.ms1, update_url, '-j')
        self.assertEqual(['name'], item_data['properties-overwritten'])

        self.assertNotEqual(
            self.execute_show_data_cmd(self.ms1, update_url, 'name'),
            self.execute_show_data_cmd(self.ms1, source_package_url, 'name'))

        self.log('info',
        '5. Check that the plan is now invalid')
        self.assertTrue(self.wait_for_plan_state(self.ms1, const.PLAN_INVALID))

        self.log('info',
        '6. Update source package item "name" property value')
        self.execute_cli_update_cmd(self.ms1,
                            source_package_url, 'name="tftp"')

        self.log('info',
        '7. Check that overridden property "name" of package item on "node1" '
            'has not been updated, while same property of any other item has')
        for inherited_path in inherited_urls:
            inherited_path_child = os.path.join(
                inherited_path, 'packages/{0}'.format(self.story_id))

            if inherited_path_child != update_url:
                self.assertEqual(
                    self.execute_show_data_cmd(self.ms1,
                                source_package_url, 'name'),
                    self.execute_show_data_cmd(self.ms1,
                                inherited_path_child, 'name').strip(' [*]'))

                self.assertNotEqual(
                    self.execute_show_data_cmd(self.ms1,
                                update_url, 'name'),
                    self.execute_show_data_cmd(self.ms1,
                                inherited_path_child, 'name').strip(' [*]'))

    @attr('all', 'revert', 'story4026', 'story4026_tc14')
    def test_14_p_inherit_cmd_remove_source_item(self):
        """
        @tms_id:
            litpcds_4026_tc14
        @tms_requirements_id:
            LITPCDS-4026, LITPCDS-12018
        @tms_title:
            Test the LITP inherit mechanism with the "remove/update" command
        @tms_description:
            Test the LITP inherit mechanism of direct and implicit
            inheritance with the "remove" and or "update" command in the
            following cases:

            1. if a user attempts to remove the source item (in various
            states), without having removed the inherited items beforehand,
            the remove will succeed and apply to the inherited items as well.
            Removing a descendant of the source item will also remove the
            descendants of the inherited items.

            2. if a user attempts to remove the inherited item (in various
            states), the remove will succeed. Removing a descendant of the
            inherited item will also succeed. The source item will remain
            unchanged

            3. if the property of a source item is updated, then that update
            will be reflected on the inherited items also (provided the
            property has not been overridden)

        @tms_test_steps:
        @step: Create source items type "package-list" and its child "package"
        @result: The item structure is created on the model
        @step: Inherit "package-list" into one node
        @result: The command executed successfully
        @step: Remove source "package"
        @result: The command executed successfully
        @result: Source "package" item is removed from model
        @result: Inherited "package" item is removed from model
        @step: Create source "package" again
        @result: The command executed successfully
        @result: The source "package" item is on the model
        @result: The inherited "package" item is on the model
        @step: Remove inherited "package" item
        @result: The command executed successfully
        @result: The inherited "package" item is no longer in the model
        @step: Inherit "package" item again
        @result: The command executed successfully
        @result: The inherited "package" item is in the model and it is in
                 Initial state
        @step: Remove inherited "package-list" item
        @result: The command executed successfully
        @result: Inherited "package-list" item is removed from the model
        @step: Inherit item "package-list" again
        @result: The command executed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in Initial state
        @result: The source "package-list" item is in the model and it is
                 in Initial state
        @step: Create and run the plan
        @result: The plan completed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in Applied state
        @result: The source "package-list" item is in the model and it is
                 in Applied state
        @step: Remove source "package-list" item (allowed by LITPCDS-12018)
        @result: The command executed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in ForRemoval state
        @result: The source "package-list" item is in the model and it is
                 in ForRemoval state
        @step: Update property "name" of source "package-list" item back to
               its original value
        @result: The command executed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in Applied state
        @result: The source "package-list" item is in the model and it is
                 in Applied state
        @step: Update property "name" of source "package-list" with different
               value
        @result: The command executed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in Updated state
        @result: The source "package-list" item is in the model and it is
                 in Updated state
        @result: Both property "name" of both source and inherited
                 "package-list" item have same value
        @step: Update property "name" of source "package-list" item back to
               its original value
        @result: The command executed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in Applied state
        @result: The source "package-list" item is in the model and it is
                 in Applied state
        @step: Update properties "config" and "epoch" of source "package" item
        @result: The command executed successfully
        @result: The inherited "package" item is in the model and it is
                 in Updated state
        @result: Properties "config" and "epoch" of inherited "package" item
                 are set to the new values
        @step: Update property "name" and "epoch" of source "package" item
               back to their original values and delete property "config" to
               set item's state back to Applied
        @result: The command executed successfully
        @result: The command executed successfully
        @result: The source "package-list" item is in the model and it is
                 in Applied state
        @result: The source "package-list" item is in the model and it is
                 in Applied state
        @result: The inherited "package-list" item is in the model and it is
                 in Applied state
        @result: The inherited "package" item is in the model and it is
                 in Applied state
        @step: Update property "epoch" of inherited "package" item
               (LITPCDS-5237)
        @result: The command executed successfully
        @result: The inherited "package" item is in the model and it is
                 in Applied state
        @step: Create the plan
        @result: Plan created successfully
        @step: Update property "config" of inherited "package" item
        @result: The command executed successfully
        @result: The inherited "package" item is in the model and it is
                 in Updated state
        @step: Remove inherited package-list item
        @result: The command executed successfully
        @result: The inherited "package-list" item is in the model and it is
                 in ForRemoval state
        @step: Create and run the plan
        @result: Plan completed successfully
        @result: The inherited "package-list" item is removed from the model
        @step: Remove source "package-list" item
        @result: The command executed successfully
        @step: Create and run the plan
        @result: Plan completed successfully
        @result: The source "package-list" item is removed from the model

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        self.log('info',
        '1. Create source "package-list" and "package" items in the model')
        s_parent, s_child = self.add_package_model_item()

        self.log('info',
        '2. Inherit "package-list" into one node')
        node = self.find(self.ms1, '/deployments', 'node')[0]

        i_parent = os.path.join(node, 'items/{0}'.format(self.story_id))
        i_child = os.path.join(i_parent, 'packages/{0}'.format(self.story_id))

        self.execute_cli_inherit_cmd(self.ms1, i_parent, s_parent)

        # The model structure of the relevant items now looks like this:
        # s_parent (source parent)
        #   /software/items/story4026_packages
        # s_child (source child)
        #   /software/items/story4026_packages/packages/story4026
        # i_parent (inherited parent)
        #   /deployments/.../nodes/n1/items/story4026/
        # i_child (inherited child)
        #   /deployments/.../nodes/n1/items/story4026/packages/story4026
        #
        # Properties original values
        # s_child name='finger'
        # s_child epoch='0'
        # s_child config=undefined

        self.log('info',
        '3. Remove source "package" and check that both source and inherited '
            'items are removed')
        self.execute_cli_remove_cmd(self.ms1, s_child)
        _, stderr, _ = self.execute_cli_show_cmd(self.ms1,
                                                s_child, expect_positive=False)
        self.assertTrue(self.is_text_in_list('InvalidLocationError', stderr))

        _, stderr, _ = self.execute_cli_show_cmd(self.ms1,
                                                i_child, expect_positive=False)
        self.assertTrue(self.is_text_in_list('InvalidLocationError', stderr))

        self.log('info',
        '4. Create source "package" item again')
        self.execute_cli_create_cmd(self.ms1,
                                    s_child, 'package', "name='finger'")

        self.execute_cli_show_cmd(self.ms1, i_child)
        self.assertEqual('Initial',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('Initial',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info',
        '5. Remove inherited "package" item')
        self.execute_cli_remove_cmd(self.ms1, i_child)

        _, stderr, _ = self.execute_cli_show_cmd(self.ms1,
                                                i_child, expect_positive=False)
        self.assertTrue(self.is_text_in_list('InvalidLocationError', stderr))

        self.log('info',
        '6. Inherit "package" item again')
        self.execute_cli_inherit_cmd(self.ms1, i_child, s_child)
        self.assertEqual('Initial',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info',
        '7. Remove inherited "package-list" item')
        self.execute_cli_remove_cmd(self.ms1, i_parent)

        _, stderr, _ = self.execute_cli_show_cmd(self.ms1,
                                            i_parent, expect_positive=False)
        self.assertTrue(self.is_text_in_list('InvalidLocationError', stderr))

        self.log('info',
        '8. Inherit the item "package-list" again')
        self.execute_cli_inherit_cmd(self.ms1, i_parent, s_parent)

        self.assertEqual('Initial',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('Initial',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info',
        '9. Create and run the plan')
        self.run_and_check_plan(self.ms1, const.PLAN_COMPLETE, 10)

        self.assertEqual('Applied',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('Applied',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info', ' LITPCDS-12018 Allows this behaviour and sets '
                         'inherited items to "ForRemoval" state')

        self.log('info',
        '10. Remove source "package-list" item (allowed by LITPCDS-12018)')
        self.execute_cli_remove_cmd(self.ms1, s_parent)

        self.assertEqual('ForRemoval',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('ForRemoval',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info',
        '11. Update property "name" of source "package-list" item back to its '
             ' original value to set item\'s state back to Applied')
        self.execute_cli_update_cmd(self.ms1, s_parent,
                            "name='{0}_packages'".format(self.story_id))

        self.assertEqual('Applied',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('Applied',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info',
        '12. Update property "name" of source "package-list" with different '
             'value')
        self.execute_cli_update_cmd(self.ms1, s_parent, 'name=firefox')

        self.assertEqual('Updated',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('Updated',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))
        self.assertEqual(
            self.execute_show_data_cmd(self.ms1, s_parent, 'name'),
            self.execute_show_data_cmd(self.ms1,
                                       i_parent, 'name').strip(' [*]'))

        self.log('info',
        '13. Update property "name" of source "package-list" item back to its '
             'original value to set item\'s state back to Applied')
        self.execute_cli_update_cmd(self.ms1,
                    s_parent, "name='{0}_packages'".format(self.story_id))

        self.assertEqual('Applied',
                    self.execute_show_data_cmd(self.ms1, i_parent, 'state'))
        self.assertEqual('Applied',
                    self.execute_show_data_cmd(self.ms1, s_parent, 'state'))

        self.log('info',
        '14. Update properties "config" and "epoch" of source "package" item')
        props = "config='replace' epoch='1'"
        self.execute_cli_update_cmd(self.ms1, s_child, props)

        self.assertEqual('replace',
                self.execute_show_data_cmd(self.ms1,
                                           i_child, 'config').strip(' [*]'))
        self.assertEqual('1',
                self.execute_show_data_cmd(self.ms1,
                                           i_child, 'epoch').strip(' [*]'))
        self.assertEqual('Updated',
                self.execute_show_data_cmd(self.ms1, i_child, 'state'))

        self.log('info',
        '15. Update property "name" and "epoch" of source "package" item back '
             'to their original value and delete property "config"')
        props = "name='finger' epoch='0'"
        self.execute_cli_update_cmd(self.ms1, s_child, props)
        self.execute_cli_update_cmd(self.ms1,
                                    s_child, "config", action_del=True)

        self.assertEqual('Applied',
                self.execute_show_data_cmd(self.ms1, s_child, 'state'))
        self.assertEqual('Applied',
                self.execute_show_data_cmd(self.ms1, s_parent, 'state'))
        self.assertEqual('Applied',
                self.execute_show_data_cmd(self.ms1, i_child, 'state'))
        self.assertEqual('Applied',
                self.execute_show_data_cmd(self.ms1, i_parent, 'state'))

        self.log('info',
        '17. Update property "epoch" of inherited "package" item '
             '(LITPCDS-5237)')
        self.execute_cli_update_cmd(self.ms1, i_child, "epoch='0'")

        self.assertEqual('Applied',
                self.execute_show_data_cmd(self.ms1, i_child, 'state'))

        self.log('info',
        '18. Create Plan')
        self.execute_cli_createplan_cmd(self.ms1, expect_positive=False)

        self.log('info',
        '19. Update property "config" of inherited "package" item')
        self.execute_cli_update_cmd(self.ms1, i_child, 'config="replace"')

        self.assertEqual('Updated',
                self.execute_show_data_cmd(self.ms1, i_child, 'state'))

        self.log('info',
        '20. Remove inherited package-list item')
        self.execute_cli_remove_cmd(self.ms1, i_parent)

        self.assertEqual('ForRemoval',
                self.execute_show_data_cmd(self.ms1, i_parent, 'state'))

        self.log('info',
        '21. Create and run the plan')
        self.run_and_check_plan(self.ms1, const.PLAN_COMPLETE, 20)

        _, stderr, _ = self.execute_cli_show_cmd(self.ms1,
                                        i_parent, expect_positive=False)
        self.assertTrue(self.is_text_in_list('InvalidLocationError', stderr))

        self.log('info',
        '22. Remove source "package-list" item')
        self.execute_cli_remove_cmd(self.ms1, s_parent)

        self.log('info',
        '23. Create and run the plan')
        self.run_and_check_plan(self.ms1, const.PLAN_COMPLETE, 20)

        _, stderr, _ = self.execute_cli_show_cmd(self.ms1,
                                    s_parent, expect_positive=False)
        self.assertTrue(self.is_text_in_list('InvalidLocationError', stderr))
