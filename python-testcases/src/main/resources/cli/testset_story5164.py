'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     June 2014
@author:    Maria Varley
@summary:   Integration test for cli delete property option
            Agile: Story LITPCDS-5164, Story LITPCDS-8290
'''


from litp_generic_test import GenericTest, attr
from rest_utils import RestUtils
import test_constants


class Story5164(GenericTest):

    '''
    As a LITP user I want a CLI option for deleting a property from an
    item so that I can unset/reset a previous value
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
        super(Story5164, self).setUp()
        self.ms_node = self.get_management_node_filename()
        self.ms_ip_address = self.get_node_att(self.ms_node,
                                           test_constants.NODE_ATT_IPV4)
        self.rest = RestUtils(self.ms_ip_address)

    def tearDown(self):
        """
        Description:
            Runs after every single test
        Actions:
            1. Perform Test Cleanup
            2. Call superclass teardown
        Results:
            Items used in the test are cleaned up and the
        """
        self.rest.clean_paths()
        super(Story5164, self).tearDown()

    @attr('all', 'revert', 'story5164', 'story5164_tc01', 'cdb_priority1')
    def test_01_p_remove_optional_property_without_default(self):
        """
         @tms_id: litpcds_5164_tc01
         @tms_requirements_id: LITPCDS-5164
         @tms_title: Remove optional property without default
         @tms_description: Verify the removal of an optional property with
         no default value from source item type and inherited item results in
         a successful execution
         @tms_test_steps:
         @step: Create a package item type with properties under software path
         @result: Item is created under software path
         @step: Inherit item onto ms
         @result: Item is inherited onto ms
         @step: Remove non mandatory, non default value property from source
                item
         @result: Property is removed from source and inherited item
         @step: Update non mandatory, non default value property on inherited
                item
         @result: Property is updated on inherited item
         @result: Property is unchanged on source item
         @step: Remove non mandatory, non default value property from inherited
                item
         @result: Property is returned to original inherited value
         @step: Remove the same non mandatory, non default value property from
                inherited item
         @result: Property is returned to original inherited value
         @step: Remove multiple properties from source item
         @result: Properties removed from source and inherited items
         @tms_test_precondition: NA
         @tms_execution_type: Automated
        """
        # 1. Find the software/items path
        sw_items_path = self.find(
            self.ms_node, "/software", "collection-of-software-item", True)[0]

        # 2. Find the ms/items path
        ms_items_path = self.find(
            self.ms_node, "/ms", "ref-collection-of-software-item", True)[0]

        pkg_path = sw_items_path + "/pkg_5164"
        ms_pkg_path = ms_items_path + "/pkg_5164"

        # 3. Create a package item type with many optional properties
        props = "name='pkg_5164' arch='redhat' config='replace' " \
            "release='1.7.1' repository='/var/lib/story5164' version='1.0.0.1'"
        self.execute_cli_create_cmd(self.ms_node, pkg_path, "package", props)

        # 4. Check the package item type has been created
        self.execute_cli_show_cmd(self.ms_node, pkg_path)

        # 5. Create a subclass
        self.execute_cli_inherit_cmd(self.ms_node, ms_pkg_path, pkg_path)

        # 6. Check the ms package subclass has been created
        self.execute_cli_show_cmd(self.ms_node, ms_pkg_path)

        # 7. Remove an optional property that does not have a default value
        # and is not mandatory
        self.execute_cli_update_cmd(
            self.ms_node, pkg_path, "repository", \
            action_del=True)

        # 8. Check property has been removed from the item type
        # and its subclass
        self.execute_show_data_cmd(
            self.ms_node, pkg_path, "repository", expect_positive=False)

        self.execute_show_data_cmd(
            self.ms_node, ms_pkg_path, "repository", expect_positive=False)

        # 9. Update a property in the subclass item
        self.execute_cli_update_cmd(
            self.ms_node, ms_pkg_path, "arch=os")

        # 10. Check for the updated value in the subclass
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, ms_pkg_path, "arch"), "os")

        # 11. Check it remains unchanged in the parent item
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, pkg_path, "arch"), "redhat")

        # 12. Delete the property in the subclass item
        self.execute_cli_update_cmd(
            self.ms_node, ms_pkg_path, "arch", \
            action_del=True)

        # 13. Attempt to delete the inherited property again
        self.execute_cli_update_cmd(
            self.ms_node, ms_pkg_path, "arch", \
            action_del=True)

        # 14. Check that the property has returned to its inherited value
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, ms_pkg_path, "arch"), "redhat [*]")

        # 15. Remove multiple optional properties
        # that do not have default values
        # and are not mandatory
        self.execute_cli_update_cmd(
            self.ms_node, pkg_path, "config,release,version", \
            action_del=True)

        # 16. Check multiple properties have been deleted from the item type
        # and its subclass
        props_list = ["config", "release", "version"]
        for prop in props_list:
            self.execute_show_data_cmd(
                self.ms_node, pkg_path, prop, expect_positive=False)

            self.execute_show_data_cmd(
                self.ms_node, ms_pkg_path, prop, expect_positive=False)

    @attr('all', 'revert', 'story5164', 'story5164_tc02')
    def test_02_p_remove_property_with_default(self):
        """
         @tms_id: litpcds_5164_tc02
         @tms_requirements_id: LITPCDS-5164
         @tms_title: Remove mandatory property with default value
         @tms_description: Verify that removing an mandatory property with a
         user defined value results in the property being returned and set to
         default value
         @tms_test_steps:
         @step: Create a bridge item type with properties where
         device_name='br_5164', forwarding_delay='5' " \
         "stp='true', ipaddress='10.82.23.131' and network_name='mgmt
         @result: Item is created where properties have non default and
         user defined values
         @step: Remove forwarding_delay and stp properties
         @result: Properties are returned and set to default value
         @step: Remove bridge item
         @result: Bridge item is removed
         @step: Change snap-size value from 100 to 90 on existing root
         file-system
         @result: Snap-size is 90
         @step: Remove snap-size property
         @result: Snap-size is returned to default value
         @tms_test_precondition: NA
         @tms_execution_type: Automated
        """
         # Add a network bridge
        net_interface_path = self.find(
            self.ms_node, "/ms", "collection-of-network-interface", True)[0]
        bridge_path = net_interface_path + "/brStory5164"
        props = "device_name='br_5164' forwarding_delay='5' " \
            "stp='true' ipaddress='10.82.23.131' network_name='mgmt'"
        self.execute_cli_create_cmd(self.ms_node, bridge_path, "bridge", props)

        # Check that properties that have default values have been
        # created with value other than the default value
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, bridge_path, "forwarding_delay"), "5")
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, bridge_path, "stp"), "true")

        # Remove property that has a default value
        self.execute_cli_update_cmd(
            self.ms_node, bridge_path, "forwarding_delay,stp", \
            action_del=True)

        # Check the property is returned to its default value
        # Default property value of fowarding delay is
        # now set between 4 and 30 with default of 4.
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, bridge_path, "forwarding_delay"), "4")
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, bridge_path, "stp"), "false")

        # Remove network bridge
        self.execute_cli_remove_cmd(self.ms_node, bridge_path)

        # Find file system path
        fs_path1 = self.get_storage_profile_paths(self.ms_node,
                                                  profile_driver="lvm")[0]
        fs_path = self.find(
            self.ms_node, fs_path1, "file-system", True)
        for path in fs_path:
            result = self.execute_show_data_cmd(
                self.ms_node, path, "snap_size")
            if result == "100":
                default_fs_path = path
                break

        # Get the current value of the snap_size property(should be default)
        sn_size = self.execute_show_data_cmd(
            self.ms_node, default_fs_path, "snap_size")

        # Test is based on the assumption this property is set
        # to its default value
        self.assertEqual(sn_size, "100")

        # Update property, snap_size that has a default
        self.execute_cli_update_cmd(
            self.ms_node, default_fs_path, "snap_size=90")

        # Check property has been updated to its default
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, default_fs_path, "snap_size"), "90")

        # Check property has been updated
        self.execute_cli_update_cmd(
        self.ms_node, default_fs_path, "snap_size", \
            action_del=True)

        # Check property has been updated
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, default_fs_path, "snap_size"), sn_size)

    @attr('all', 'revert', 'story5164', 'story5164_tc03', 'cdb_priority1')
    def test_03_n_remove_mandatory_property(self):
        """
         @tms_id: litpcds_5164_tc03
         @tms_requirements_id: LITPCDS-5164
         @tms_title: Remove mandatory property
         @tms_description: Verify that removing a mandatory property results
         in a MissingRequiredPropertyError and the value being unchanged
         @tms_test_steps:
         @step: Create a bridge item type with properties where one is
         mandatory
         @result: Item is created
         @step: Remove mandatory property
         @result: Validation error is thrown: MissingRequiredPropertyError
         @result: Property is not removed and the value remains the same
         @step: Create a blade item with three mandatory property
         @result: Item is created
         @step: Remove three mandatory properties
         @result: Validation error is thrown: MissingRequiredPropertyError
         @result: Properties are not removed and the values remain the same
         @tms_test_precondition: NA
         @tms_execution_type: Automated
        """
        # Add a network bridge
        net_interface_path = self.find(
            self.ms_node, "/ms", "collection-of-network-interface", True)[0]
        bridge_path = net_interface_path + "/brStory5164"
        props = "device_name='br_5164' " \
            "ipaddress='10.82.23.131' network_name='mgmt'"
        self.execute_cli_create_cmd(self.ms_node, bridge_path, "bridge", props)

        # Remove the mandatory property, device_name
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, bridge_path, "device_name", \
            expect_positive=False, action_del=True)

        # Check returned error
        self.assertTrue(
            self.is_text_in_list("MissingRequiredPropertyError", stderr),
            "Expected MissingRequiredPropertyError Error message")

        # Check the mandatory property has not been removed
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, bridge_path, "device_name"), "br_5164")

        # Get system path
        system_path = self.find(
            self.ms_node, "/infrastructure", "collection-of-system", True)[0]

        # Create a system
        sys_item_path = system_path + "/sysStory5164"
        props = "system_name='sys_Story5164'"
        self.execute_cli_create_cmd(
            self.ms_node, sys_item_path, "blade", props)

        # Create a disk
        disk_path = self.find(
            self.ms_node, sys_item_path, "disk-base", False)[0]

        disk_item_path = disk_path + "/diskStory5164"
        props = "name='hdStory5164' size='2G' " \
            "uuid='600story5164story5164story516411'"
        self.execute_cli_create_cmd(
            self.ms_node, disk_item_path, "disk", props)

        # Remove multiple mandatory properties
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, disk_item_path, "name,size,uuid", \
            expect_positive=False, action_del=True)

        # Check expected returned errors
        self.assertEqual(
            self.count_text_in_list(
            "MissingRequiredPropertyError", stderr), 3)

        # Check the mandatory properties have not been removed
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, disk_item_path, "name"), \
            "hdStory5164")
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, disk_item_path, "size"), \
            "2G")
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, disk_item_path, "uuid"), \
            "600story5164story5164story516411")

    @attr('all', 'revert', 'story5164', 'story5164_tc04')
    def test_04_n_remove_properties(self):
        """
         @tms_id: litpcds_5164_tc04
         @tms_requirements_id: LITPCDS-5164
         @tms_title: Comma separated removal of mandatory and non existent
         properties
         @tms_description: Verify that validation errors returned when user
         attempts to remove mandatory or non existent properties
         @tms_test_steps:
         @step: Create a network item type
         @result: Item is created
         @step: Create a second network item type
         @result: Item is created
         @step: Remove properties on collection-of-network item
         @result: Validation error is thrown: PropertyNotAllowedError
         @step: Remove properties, one of which is mandatory on first network
         item type
         @result: Validation error is thrown: MissingRequiredPropertyError
         @step: Remove properties, one of which is not mandatory and the other
         has a default value when not user defined
         @result: Non mandatory property is removed
         @result: Property with user defined value is returned to default value
         @step: Remove properties, one mandatory and one non existent
         @result: Validation error is thrown: InvalidRequestError
         @result: Validation error is thrown: MissingRequiredPropertyError
         @step: Remove mandatory and default value property
         @result: Validation error is thrown: MissingRequiredPropertyError
         @step: Remove invalid property type
         @result: Validation error is thrown: InvalidRequestError
         @step: Remove non existent property type
         @result: Validation error is thrown: InvalidRequestError
         @tms_test_precondition: NA
         @tms_execution_type: Automated
        """
        # 1. Get network path
        network_path = self.find(
        self.ms_node, "/infrastructure", "collection-of-network", True)[0]
        net_item_path = network_path + "/net_5164"

        # 2. Create a network
        props = "name='net_5164' " \
        "litp_management='true' subnet='92.168.200.164/24'"
        self.execute_cli_create_cmd(
            self.ms_node, net_item_path, "network", props)

        # 3. Create a second network
        net2_item_path = network_path + "/net2_5164"
        props = "name='net_5164_1' "
        self.execute_cli_create_cmd(
            self.ms_node, net2_item_path, "network", props)

        # 4. Test unable to delete property on collection
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, network_path, "subnet,name", \
            expect_positive=False, action_del=True)

        # 5. Check expected returned PropertyNotAllowedError
        err_msg = "Properties cannot be set on collections"
        self.assertTrue(self.is_text_in_list(
            "PropertyNotAllowedError", stderr), \
            "Expected PropertyNotAllowedError")
        self.assertTrue(self.is_text_in_list(
            err_msg, stderr,), \
            "message has changed")

        # 6. Test the deletion of properties when the comma
        # separated list contains a space - space is ignored
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, net_item_path, "subnet, name", \
            expect_positive=False, action_del=True)

        # 7. Check expected returned error for attemtped
        # removal of a mandatory property
        err_msg1 = \
        'ItemType "network" is required to have a property with name "name"'
        self.assertTrue(self.is_text_in_list(
            "MissingRequiredPropertyError", stderr), \
            "Expected MissingRequiredPropertyError")
        self.assertTrue(self.is_text_in_list(
            err_msg1, stderr), \
            "message has changed")

        # 8. Test the deletion of a property with a default value
        # and a property without a default property in a comma separated list
        self.execute_cli_update_cmd(
            self.ms_node, net_item_path, "litp_management,subnet", \
            action_del=True)

        # 9. Check the property has been returned to its default value
        self.assertEqual(self.execute_show_data_cmd(
            self.ms_node, net_item_path, "litp_management"), \
            "false")

        # 10. Check that the property has been removed
        self.execute_show_data_cmd(
            self.ms_node, net_item_path, "subnet", expect_positive=False)

        # 11.Test the deletion of a property with a mandatory value
        # and a property that has already been deleted in a comma
        # separated list
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, net_item_path, "subnet,name", \
            expect_positive=False, action_del=True)

        # 12. Check expected returned errors
        self.assertTrue(self.is_text_in_list(
            "MissingRequiredPropertyError", stderr), \
           "MissingRequiredPropertyError")
        self.assertTrue(self.is_text_in_list('InvalidRequestError', stderr))

        # 13. Test the deletion of the property with a mandatory value
        # and a property with a default property in a comma separated list
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, net_item_path, "litp_management, name", \
            expect_positive=False, action_del=True)

        # 14. Check expected returned errors
        self.assertTrue(
        self.count_text_in_list(
        "MissingRequiredPropertyError", stderr),)

        # 15. Test the deletion of a property that does exist in that item type
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, net_item_path, "management", \
            expect_positive=False, action_del=True)

        # 16. Check the expected error is returned
        err_msg = "Unable to delete property: management"
        self.assertTrue(self.is_text_in_list(
            "InvalidRequestError", stderr), \
           "Expected InvalidRequestError")
        self.assertTrue(self.is_text_in_list(
            err_msg, stderr), \
            "message has changed")

        # 17. Test the deletion of a property that the item type accepts
        # but that has not been created
        _, stderr, _ = self.execute_cli_update_cmd(
            self.ms_node, net2_item_path, "subnet", \
            expect_positive=False, action_del=True)

        # 18. Check returned error
        self.assertTrue(self.is_text_in_list(
            "InvalidRequestError", stderr), \
           "Expected InvalidRequestError")
