'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     March 2015
@author:    Maria Varley
@summary:   Story LITPCDS-8290
                Integration test for allowing update and removal of properties
                in the same update CLI command
            Bug LITPCDS-10072
                To ensure that "-d -o" behaves the same as "-o -d" for
                same property
            Bug LITPCDS-10533
                To ensure that multiple litp update "-d" arguments
                are all processed
'''

from litp_generic_test import GenericTest, attr
from rest_utils import RestUtils
import test_constants


class Story8290(GenericTest):
    '''
    As a LITP user, I want to be able to update and delete
    a property via CLI in the same command
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
        super(Story8290, self).setUp()
        self.ms_node = self.get_management_node_filename()
        self.rest = RestUtils(self.get_node_att(self.ms_node, 'ipv4'))

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
        super(Story8290, self).tearDown()

    def _create_my_repo(self, repo):
        """
        Function which creates a test repo to be used for these tests
        """
        repo_dir = test_constants.PARENT_PKG_REPO_DIR + repo
        command = self.rhc.get_createrepo_cmd(repo_dir, update=False)
        self.assertTrue(
            self.create_dir_on_node(self.ms_node, repo_dir, su_root=True))
        self.run_command(
            self.ms_node, command, su_root=True)
        self._check_yum_repo_is_present(repo_dir)

    def _check_yum_repo_is_present(self, repo_path):
        """
        Check that file /repodata/repomd.xml file exist under repo folder
        """
        repmod_path = repo_path + '/repodata/repomd.xml'
        self.assertTrue(self.remote_path_exists(self.ms_node, repmod_path),
            '<{0}> not found'.format(repmod_path))

    def _create_run_and_wait_for_plan(self, timeout=60,
                                      state=test_constants.PLAN_COMPLETE):
        """
        Description
        Create and run plan and wait for specified plan state

        Args:
        timeout (int): Max amount of time allowed for plan to reach
                       expected state
        state (str): Expected plan state
        """
        self.execute_cli_createplan_cmd(self.ms_node)
        self.execute_cli_runplan_cmd(self.ms_node)
        result = self.wait_for_plan_state(self.ms_node, state,
                                         timeout_mins=timeout)
        self.assertTrue(result,
            "Plan did not complete with expected state {0}".format(state))

    @attr('all', 'revert', 'story8290', 'story8290_tc01')
    def test_01_pn_cli_update_delete_property_one_command(self):
        """
        @tms_id:
            litpcds_8290_tc01
        @tms_requirements_id:
            LITPCDS-8290
        @tms_title:
            Update and remove property via CLI interface in one command
        @tms_description:
            Test that a user can update and delete mandatory/optional, REST
            updatable and not mutually exclusive properties via the CLI
            interface in the same update command

        @tms_test_steps:
            @step: Create a logrotate item with a set properties
            @result: Command completes successfully

            @step: Create and run the plan
            @result: Plan created, run and completed successfully

            @step: Delete one property and update a second one with an
                   invalid value
            @result: ValidationError is thrown
            @result: Properties' value have not changed

            @step: Update and delete same property in one command
            @result: Usage message is displayed
            @result: Property's value has not changed

            @step: Delete and update (flag in reversed order) same property
                   in one command
            @result: Usage message is displayed
            @result: Property's value has not changed

            @step: Delete and update different properties in one command
            @result: Command completed successfully
            @result: Properties have been deleted and updated

            @step: Delete multiple properties in one command
            @result: Command completed successfully
            @result: Properties have been deleted

            @step: Verify that plan can be created and run successfully
            @result: Plan created, run and completed successfully

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        invalid_prop_val = 'False'
        n1_logrotate_config = self.find(
            self.ms_node, "/deployments", "logrotate-rule-config", "True")[0]

        self.log('info', 'Create a new logrotate rule with properties '
                         'on the node1')
        props = ("name='logrotate_rule01' path='/var/log/log8290' "
                 "rotate='5' size='3k' "
                 "copytruncate='true' compress='false' copy='false' "
                 "delaycompress='false'")
        log_rule_path = n1_logrotate_config + "/rules/logrule_rule8290"
        self.execute_cli_create_cmd(
            self.ms_node, log_rule_path, "logrotate-rule", props)

        self.log('info', 'Create, run and wait for plan to complete')
        self._create_run_and_wait_for_plan()

        self.log('info', 'Delete one property and update a second one with an '
                         'invalid value')
        props_before_update = self.get_props_from_url(self.ms_node,
            log_rule_path)
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, log_rule_path,
                                                   "copytruncate={0}".
                                                   format(invalid_prop_val),
                                                   "-d compress -o rotate=20",
                                                   expect_positive=False)
        expected = "ValidationErrorin property:\"{0}\"Invalidvalue'{1}" \
                    "'.".format('copytruncate', invalid_prop_val)\
                   .replace(' ', '')

        self.log('info', 'Verify ValidationError')
        self.assertEqual(expected, ''.join(stderr).replace(' ', ''))
        props_after_update = self.get_props_from_url(self.ms_node,
                                                     log_rule_path)

        self.log('info', 'Checking that properties of {0} have not changed'
                         'after update cmd'
                 .format(log_rule_path))
        self.assertEqual(props_before_update, props_after_update,
                         'Properties before and after failed'
                         ' attempt to update do not match {0} {1}'
                         .format(props_before_update, props_after_update))

        self.log('info', 'Update and delete same property '
                         'in one command')
        props_before_update = self.get_props_from_url(self.ms_node,
                                                      log_rule_path)
        _, stderr, _ = self.execute_cli_update_cmd(
                                        self.ms_node,
                                        log_rule_path,
                                        props="copytruncate='false'",
                                        args="-d copytruncate",
                                        action_del=False,
                                        expect_positive=False)

        props_after_update = self.get_props_from_url(self.ms_node,
                                                     log_rule_path)
        expected = 'Usage: litp update [-h] -p PATH [-o PROPERTIES ' \
                   '[PROPERTIES ...]][-d PROPERTIES [PROPERTIES ...]]' \
                   ' [-j]litp update: error: Updating and deleting ' \
                   '"copytruncate" in the same operation'.replace(' ', '')
        self.assertEqual(expected, ''.join(stderr).replace(' ', ''))

        self.log('info', 'Check that properties of item "{0}" have '
                         'not changed'
        .format(log_rule_path))
        self.assertEqual(props_before_update, props_after_update,
            'Properties before and after failed'
            ' attempt to update do not match {0} {1}'
            .format(props_before_update, props_after_update))

        self.log('info', 'Delete and update (flag in reversed order) same '
                         'property in one command')
        _, stderr, _ = self.execute_cli_update_cmd(
                                        self.ms_node,
                                        log_rule_path,
                                        props="copytruncate",
                                        args="-o copytruncate=false",
                                        action_del=True,
                                        expect_positive=False)
        self.assertEqual(expected, ''.join(stderr).replace(' ', ''))

        self.log('info', 'Check that properties of item "{0}" '
                         'have not changed'.format(log_rule_path))
        self.assertEqual(props_before_update, props_after_update,
            'Properties before and after failed'
            ' attempt to update do not match {0} {1}'
            .format(props_before_update, props_after_update))

        self.log('info', 'Delete and update different properties in '
                         'one command')
        _, stderr, _ = self.execute_cli_update_cmd(self.ms_node, log_rule_path,
                                                   "delaycompress='true'",
                                                   "-d size -o copy='true' ",
                                                   expect_positive=True)

        self.log('info', 'Verify properties have been deleted and updated')
        props_after_update = self.get_props_from_url(self.ms_node,
                                                    log_rule_path)

        expected = None
        found = props_after_update.get('size')
        self.assertEqual(expected, found,
            'Incorrect value for "size" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = 'true'
        found = props_after_update.get('delaycompress')
        self.assertEqual(expected, found,
            'Incorrect value for "delaycompress" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = 'true'
        found = props_after_update.get('copy')
        self.assertEqual(expected, found,
            'Incorrect value for "copy" prop. Expected {0}, found {1}'
            .format(expected, found))

        self.log('info', 'Issue litp update command with multiple "-d" '
                         'parameters')
        self.execute_cli_update_cmd(self.ms_node, log_rule_path,
                                    'copytruncate -d compress -d rotate',
                                    action_del=True)

        self.log('info', 'Verify properties have been deleted and updated')
        props_after_plan = self.get_props_from_url(self.ms_node, log_rule_path)

        expected = None
        found = props_after_plan.get('copytruncate')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = None
        found = props_after_plan.get('compress')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = None
        found = props_after_plan.get('rotate')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = None
        found = props_after_plan.get('size')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = 'logrotate_rule01'
        found = props_after_plan.get('name')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = "/var/log/log8290"
        found = props_after_plan.get('path')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = 'true'
        found = props_after_plan.get('delaycompress')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = 'true'
        found = props_after_plan.get('copy')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))

        self.log('info', 'Verify that plan can be created and run '
                         'successfully')
        self.run_and_check_plan(self.ms_node, test_constants.PLAN_COMPLETE, 10)

    @attr('all', 'revert', 'story8290', 'story8290_tc02')
    def test_02_p_rest_update_delete_property_one_command(self):
        """
        @tms_id:
            litpcds_8290_tc02
        @tms_requirements_id:
            LITPCDS-8290
        @tms_title:
            Update and remove properties via REST interface in one command
        @tms_description:
            Test that a user can update and delete mandatory/optional, REST
            updatable and not mutually exclusive properties via the REST
            interface in the one command

        @tms_test_steps:
            @step: Create a firewall item with several properties
            @result: Command executes successfully

            @step: Create and run the plan
            @result: Plan created, run and completed successfully

            @step: Update and delete properties of the firewall item in
                   one command
            @result: Command executes successfully

            @step: Create and run the plan
            @result: Plan created, run and completed successfully
            @result: Properties have been updated and deleted correctly

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        node2_path = self.find(self.ms_node, "/deployments", "node", True)[1]

        node2_config_path = self.find(
            self.ms_node, node2_path, "firewall-node-config")[0]

        self.log('info', 'Create a firewall item with several properties')
        stdout, stderr, status = \
            self.rest.post(node2_config_path + "/rules",
                           "Content-Type:application/json",
                           "{\"id\":\"test02a\","
                           "\"type\":\"firewall-rule\","
                           "\"properties\":"
                           "{\"name\":\"122 test2a\","
                           "\"source\": \"192.168.1.100-192.168.1.200\","
                           "\"dport\": \"22\","
                           "\"proto\": \"tcp\","
                           "\"provider\": \"iptables\","
                           "\"chain\":\"INPUT\"}}"
                )
        self.assertNotEqual(stdout, "", "POST command output is empty")
        self.assertEqual(201, status)
        self.assertEqual("", stderr)

        self.log('info', 'Create and run the plan')
        self._create_run_and_wait_for_plan()

        self.log('info', 'Update and delete properties in one command')
        stdout, stderr, status = \
            self.rest.put(node2_config_path + "/rules/test02a",
                            "Content-Type:application/json",
                            "{\"id\":\"test02a\","
                            "\"type\":\"firewall-rule\","
                            "\"properties\":"
                            "{\"name\":\"122 test2a\","
                            "\"source\": null,"
                            "\"dport\": null,"
                            "\"proto\": \"tcp\","
                            "\"provider\": \"ip6tables\","
                            "\"chain\":\"OUTPUT\"}}"
                )
        self.assertNotEqual(stdout, "", "PUT command output is empty")
        self.assertEqual(200, status)
        self.assertEqual("", stderr)

        self.log('info', 'Create and run the plan')
        self._create_run_and_wait_for_plan()

        self.log('info', 'Check that properties have been deleted and '
                         'updated correctly')
        props_after_update = self.get_props_from_url(self.ms_node,
            node2_config_path + "/rules/test02a")

        self.log('info', 'Checking "provider" property')
        expected = 'ip6tables'
        self.assertEqual(props_after_update.get('provider'), expected,
            "Expected provider = {0}, found {1} "
            .format(expected, props_after_update.get('provider')))

        self.log('info', 'Checking "source" property')
        expected = None
        self.assertEqual(props_after_update.get('source'), expected,
            "Expected provider = {0}, found {1} "
            .format(expected, props_after_update.get('source')))

    @attr('all', 'revert', 'story8290', 'story8290_tc05')
    def test_05_p_cli_replace_mutually_exclusive_properties(self):
        """
        @tms_id:
            litpcds_8290_tc05
        @tms_requirements_id:
            LITPCDS-8290
        @tms_title:
            Update mandatory mutually exclusive properties in one commnad
        @tms_description:
            Test that mandatory mutually exclusive properties can be
            updated by issuing one single command via CLI interface

        @tms_test_steps:
            @step: Create a yum repo server on MS
            @result: Command completes successfully

            @step: Create source yum repo LITP item with the mandatory
                   property "ms_url_path"
            @result: Command executes successfully

            @step: Inherit yum LITP item into MS
            @result: Command executes successfully

            @step: Create and run the plan
            @result: Plan created, run and completed successfully

            @step: Update and delete the inherited yum repo item to use
                   the property "base_url" instead of "ms_url_path"
            @result: Command executes successfully

            @step: Create and run the plan
            @result: Plan created, run and completed successfully
            @result: Mandatory mutually exclusive property "ms_url_path" has
                     been replaced by "base_url"

        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """

        repo_path = "story8290-test05repo2"
        self.del_file_after_run(self.ms_node,
                                '{0}/{1}.repo'.format(
                                 test_constants.YUM_CONFIG_FILES_DIR,
                                 repo_path))

        sw_items_path = self.find(self.ms_node,
            "/software", "collection-of-software-item")[0]
        ms_items_path = self.find(self.ms_node,
            "/ms", "ref-collection-of-software-item")[0]

        self.log('info',
        'Create yum repo server on MS')
        self._create_my_repo(repo_path)

        self.log('info',
        'Create source yum repo LITP item')
        sw_items_url = sw_items_path + "/" + repo_path
        props = 'name="{0}" ms_url_path="/{1}"'.format(repo_path, repo_path)
        self.execute_cli_create_cmd(self.ms_node,
            sw_items_url, "yum-repository", props)

        self.log('info',
        'Inherit created LITP item into MS')
        ms_items_url = '{0}/{1}'.format(ms_items_path, repo_path)
        self.execute_cli_inherit_cmd(self.ms_node, ms_items_url, sw_items_url)

        self.log('info',
        'Create, run and wait for plan to complete')
        self._create_run_and_wait_for_plan()

        self.log('info',
        'Update the inherited yum repo item to use the property '
            '"base_url" instead of "ms_url_path"')
        self.execute_cli_update_cmd(
            self.ms_node, sw_items_url,
            "base_url='http://{0}'".format(repo_path), "-d ms_url_path")

        self.log('info',
        'Create, run and wait for plan to complete')
        self._create_run_and_wait_for_plan()

        self.log('info',
        'Check that properties have been updated')
        props_after_update = self.get_props_from_url(
            self.ms_node, ms_items_url)

        expected = 'http://{0}'.format(repo_path)
        found = props_after_update.get('base_url')
        self.assertEqual(found, expected,
            'Incorrect value for "base_url" prop. Expected {0}, found {1}'
            .format(expected, found))

        expected = None
        found = props_after_update.get('ms_url_path')
        self.assertEqual(expected, found,
            'Incorrect value for "ms_url_path" prop. Expected {0}, found {1}'
            .format(expected, found))
