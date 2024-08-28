
==========================================================================
Story 4026
==========================================================================
obsoleted test cases:
    testset_story4026.py test_07_p_inherit_cmd_update_model_item_check_referenc
    e_cli

Description:
    """
        Description:
            After creating a reference to a created model item, using the new
            CLI inherit command, if the property of a model item is updated,
            then that update will be reflected on the reference also.

        Actions:
            1.  Execute the cli create command for a package-list in the model
            2.  Execute the cli create command for a package item child of the
                created package-list
            3.  Execute the new cli inherit command for the package-list to
                create a reference item on a node
            4.  Execute the cli create_plan command
            5.  Execute the cli run_plan command
            6.  Wait for the plan to complete successfully
            7.  Execute the cli update command on a property of the
                package-list model item
            8.  Execute the cli show command and check the property is also
                changed on the reference item
            9.  Execute the cli show command and check the item state is set to
                Updated

        Result:
            The property that is updated on the model item must also reflect
            the update
        """

Reason why obsoleted:
To shorten KGB run-time this testcase was combined into:
test_14_p_inherit_cmd_remove_source_item so only one plan is ran once a package
is installed in the model.
As this testcase only verifies that the reference is updated and property values
have been propagated down after a create plan once the states of
both the source and reference package items are in state Applied it can be
combined into test_14 once the source and reference paths are in state Applied.
This test is covered steps 28 and 29

Gerrit review to obsolete test case(s):

-------------------------------------------------------------------------

obsoleted test cases:
    testset_story4026.py test_09_p_inherit_cmd_update_model_item_property_cli

Description:
    """
        Description:
            After creating a reference to a created model item, using the new
            CLI inherit command, if the property of a model item is updated,
            then that update will be reflected on the reference also.

        Actions:
            1.  Execute the cli create command for a package-list in the model
            2.  Execute the cli create command for a package item child of the
                created package-list
            3.  Execute the new cli inherit command for the package-list to
                create a reference item on a node
            4.  Execute the cli create_plan command
            5.  Execute the cli run_plan command
            6.  Wait for the plan to complete successfully
            7.  Execute the cli update command on a property of the
                package-list model item
            8.  Execute the cli show command and check the property is also
                changed on the reference item
            9.  Execute the cli show command and check the item state is set to
                Updated

        Result:
            The property that is updated on the model item must also reflect
            the update on its reference
        """

Reason why obsoleted:
To shorten KGB run-time this testcase was combined into:
test_14_p_inherit_cmd_remove_source_item so only one plan is ran once a package is
installed in the model.
As this testcase only verifies that the reference is updated and property value
'name' has been propagated down after a create plan once the states of
both source and reference package-list are in Applied it can be combined into
test_14 once the source and reference paths are in state Applied
This test is cover in steps 24 and 25
Gerrit review to obsolete test case(s):

-------------------------------------------------------------------------

obsoleted test cases:
    testset_story4026.py test_13_p_inherit_cmd_remove_reference_item

Description:
    """
        Description:
            After creating a reference to a created model item, using the new
            CLI inherit command, if the user attempts to remove the reference,
            then the reference will be set for removal.

        Actions:
            1.  Execute the cli create command for a package-list in the model
            2.  Execute the cli create command for a package item child of the
                created package-list
            3.  Execute the new cli inherit command for the package-list to
                create a reference item on a node
            4.  Execute the new cli inherit command for the package-list to
                create a reference item on a second node
            5.  Execute the remove command to attempt to remove the reference
            6.  Check the item is removed from the model

        Result:
            Removing a reference is allowed
        """

Reason why obsoleted:
To shorten KGB run-time this testcase was combined into:
test_14_p_inherit_cmd_remove_source_item so only one plan is ran once a package
is installed in the model.
This testscase verifies states when the model is updated before and after the
create plan to install a package. This has been included in test_14, the create
plan to verify the reference path is removed is done as a last step in test_14.
This test is split in two parts and are covers in steps 14 to 17 and 32 to 41
Gerrit review to obsolete test case(s):

-------------------------------------------------------------------------

obsoleted test cases:
    testset_story4026.py test_15_p_inherit_cmd_remove_source_item_and_reference_item

Description:
    """
        Description:
            After creating a reference to a created model item, using the new
            CLI inherit command, if the user removes all the references and
            then the source path, then all the items will be marked for
            removal. Execute a successful plan will remove them

        Actions:
            1.  Execute the cli create command for a package-list in the model
            2.  Execute the cli create command for a package item child of the
                created package-list
            3.  Execute the new cli inherit command for the package-list to
                create a reference item on a node
            4.  Execute the create_plan command
            5.  Execute the run_plan command and wait for successful plan
                execution
            6.  Execute the remove command on the reference path
            7.  Check the reference is marked as ForRemoval
            8.  Execute the remove command on the source path
            9.  Check the reference is marked as ForRemoval
            10. Execute the create_plan command
            11. Execute the run_plan command and wait for plan completion
            12. Check reference and source paths are removed from model

        Result:
            Removing a reference is allowed
        """

Reason why obsoleted:
This testcase is redundant as the procedure to remove a reference is covered in
test_13_p_inherit_cmd_remove_reference_item which is now part of test_14
The comment "execute remove command on source path; should succeed now that
reference has been removed" is redundant as of LITPCDS-12018 where a user can
remove the source path without having to remove the reference path first
Gerrit review to obsolete test case(s):

-------------------------------------------------------------------------

obsoleted test cases:
    testset_story4026.py test__12_p_inherit_cmd_remove_reference_item_child

Description:
    """
        Description:
            After creating a reference to a created model item, using the new
            CLI inherit command, if the user attempts to remove a child of the
            reference item, the remove request will succeed

        Actions:
            1.  Execute the cli create command for a package-list in the model
            2.  Execute the cli create command for a package item child of the
                created package-list
            3.  Execute the new cli inherit command for the package-list to
                create a reference item on a node
            4.  Execute the new cli inherit command for the package-list to
                create a reference item on a second node
            5.  Execute the remove command to attempt to remove a child of the
                reference item
            6.  Check for error
            7.  Execute the create_plan command
            8.  Execute the run_plan command and wait for successful plan
                completion
            9.  Execute the remove command again on the same child

        Result:
            Removing a child item from an inherited path will succeed
            if attempted from the reference
        """

Reason why obsoleted:
This testcase doesn't verify any changes made to the model. This check is
now being done.The testcase description is now being verifed in test_14 in
steps 10 and 11


Gerrit review to obsolete test case(s):

------------------------------------------------------------------------------

Obsoleted testcase:
    cli.testset_story4026.test_02_n_inherit_link_already_exists

Description:
    We assert that it is not possible to create an inherit
    path where a link already exists
Actions:
    1. create a new package under /software + link it under /ms
    3. attempt to create an inherit path where a link exists
Result:
    Correct behaviour for attempting to create an inherit path
    where a link already exists is validated

Removed because no longer relevant. Linking has been replaced with inherit


==========================================================================
Story 8290
==========================================================================
obsoleted test cases:
test_03_n_cli_add_remove_property_fails

Description:
        Test that when a command to update and remove properties
        in the same CLI command fails, no changes are made to the model item

        Actions:
         1  Find the logrotate-rule-config already on node1
         2. Define logrotate rules on nodeX
         3. Create a new logrotate rule with certain  properties on the node
         4. Create plan
         5. Run plan
         6. Wait for plan to complete
         7. Attempt to upate and remove the yum repository property,
           cache_metadata in the same cli update command

         Result
             Ensure that no updates have taken place.
        """

Reason why obsoleted:
Now merged into test_01 at step 4 to 6

Gerrit review to obsolete test case(s): https://gerrit.ericsson.se/1299232

-------------------------------------------------------------------------

obsoleted test cases:
test_04_n_cli_update_remove_same_property

Description:
        Verify that validation error returned when an attempt is made
        to update and remove same property in one command

        Actions:
        1. Determine paths to be used during test
        2. Create the repo
        3. Create a LITP source yum repo item on model
        4. Inherit LITP yum repo item into MS
        5. Create and run the plan
        6. Attempt to update and delete same property in one command
        7. Check that properties of item "{0}" have not changed
        8. Attempt to update and delete same property in one command
           with "-d" "-o" flag in inverted order
        9. Check that properties of item "{0}" have not changed
        """

Reason why obsoleted:
Now merged into test_01 at step 7 to 10

Gerrit review to obsolete test case(s): https://gerrit.ericsson.se/1299232

-------------------------------------------------------------------------

obsoleted test cases:
test_06_p_cli_update_with_multiple_delete_flags

Description:
            This test verifies that all instances of "-d" parameters
            passed to the litp update command are processed
            Ref: Bug LITPCDS-10533

        Actions:
            1. Determine items to use during test
            2. Issue litp update command with multiple "-d" parameters
            3. Verify that relevant properties have been deleted
            4. Verify that plan can be created and run successfully
        """
Reason why obsoleted:
Now merged into test_01 at step 12 to 13

Gerrit review to obsolete test case(s): https://gerrit.ericsson.se/1299232

-------------------------------------------------------------------------

Renamed test case:
    test_01_p_cli_add_remove_property
to:
    test_01_pn_cli_update_delete_property_one_command

-------------------------------------------------------------------------

Renamed test case:
    test_02_p_rest_add_remove_property
to:
    test_02_p_rest_update_delete_property_one_command


==========================================================================
Story 5164
==========================================================================
obsoleted test cases:
 test_06_p_remove_property_help_command(self):
        """
        Description:
        Check that the help command has been updated to include the
        "update" command

        Note: extended cases to cover AC specified on story8290

        Actions:
        1. Verify the 'litp --help' command
        2. Verify the 'litp -h' command
        3. Verify the 'litp update --help' command
        4. Verify the 'litp update -h' command
        For each command check that the -d option is explained

        Result:
        The help command has been updated

Reason why obsoleted:
Duplicate of test_35 in testset_story245.py

Gerrit review to obsolete test case(s):https://gerrit.ericsson.se/#/c/1327592/

-------------------------------------------------------------------------
obsoleted test cases:
  obsolete_05_n_remove_property_option_mutually_exclusive(self):
        """
        Description:
        Delete cannot be combined with the "option" parameter,
        they are mutually exclusive

        Note: story8290 made this functionality available

        Actions:
        1. Find the path to the item whos property is to be updated
        2. Attempt to execute update command with -o and -d options
        3. Check returned error message
        4. Attempt to execute update command with -d and -o options
        5. Check returned error message

        Result:
        Appropriate error message is returned


Reason why obsoleted:
Previously marked as obsolete
Expected error message strings are no longer returned when commands are
executed

Gerrit review to obsolete test case(s):https://gerrit.ericsson.se/#/c/1327592/
