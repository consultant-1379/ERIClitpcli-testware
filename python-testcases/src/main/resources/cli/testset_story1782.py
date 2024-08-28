'''
COPYRIGHT Ericsson 2019
The copyright to the computer program(s) herein is the property of
Ericsson Inc. The programs may be used and/or copied only with written
permission from Ericsson Inc. or in accordance with the terms and
conditions stipulated in the agreement/contract under which the
program(s) have been supplied.

@since:     March 2014
@author:    joe
@summary:   Integration test for litp version commands
            Agile: LITPCDS-1782
'''

import re
from litp_generic_test import GenericTest, attr
import test_constants
from litp_cli_utils import CLIUtils

VERSION_FILE = test_constants.LITP_PATH + ".version"
INSTALL_FILE = test_constants.LITP_PATH + ".upgrade.history"

LITP_GROUP = "LITP2"
VERSION_OPT = "version"


class Story1782(GenericTest):

    '''
    As a LITP User I want to be able to retrieve the version information,
    so that I can provide this info when troubleshooting issues
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
        super(Story1782, self).setUp()
        self.ms_node = self.get_management_node_filename()
        self.cli = CLIUtils()

    def _run_cmd(self, cmd, add_to_cleanup=True, su_root=False,
                 expect_positive=True):
        """
        Run a command asserting success or error (returns: stdout / stderr)
        """
        stdout, stderr, exit_code = self.run_command(
            self.ms_node, cmd, add_to_cleanup=add_to_cleanup, su_root=su_root)
        if expect_positive:
            self.assertNotEqual("", stdout)
            self.assertEqual([], stderr)
            self.assertEqual(0, exit_code)
            result = '\n'.join(stdout)
        else:
            self.assertEqual([], stdout)
            self.assertNotEqual("", stderr)
            self.assertNotEqual(0, exit_code)
            result = '\n'.join(stderr)
        return result

    def _assert_in(self, expected_in, actual):
        """
        Method for check for something that is expected
        """
        self.assertTrue(expected_in in actual,
                        "'%s' not in '%s'" % (expected_in, actual))

    def _assert_not_in(self, not_expected_in, actual):
        """
        Method to check for something that is not expected
        """
        self.assertTrue(not_expected_in not in actual,
                        "'%s' in '%s'" % (not_expected_in, actual))

    def _assert_list_in(self, expected_list, actual):
        """
        Method to assert expected item is in list
        """
        for expected_in in expected_list:
            self._assert_in(expected_in, actual)

    def _get_litp_packages(self):
        """
        Method to get list of installed LITP packages
        """
        litp_pkgs_cmd = (
           "/bin/rpm -qa --qf '%-{name} %-{version}\\n' | sort -k1 | "
           "egrep \"`yum groupinfo " + LITP_GROUP + "| grep CXP | "
           "tr -d ' ' | tr '\\n' '|' | sed 's/|$//g'`\"")
        stdout, _, _ = self.run_command(self.ms_node, litp_pkgs_cmd,
                                        su_root=True, default_asserts=True)
        return '\n'.join(stdout)

    @attr('all', 'revert', 'cdb_priority1')
    def obsolete_01_p_retrieve_iso_version_cli(self):
        """
        Description:
            Retrieves version of LITP ISO installed using CLI

        Actions:
            1. cat LITP version file
            2. Run "litp version" command
            3. Ensure output contains version
            4. Run "litp version -a" command
            5. Run "litp version --all" command
            6. Ensure 'litp --a' output matches 'litp --all'
            7. Ensure output contains version

        Result:
            The version of LITP is displayed
        """
        # 1. cat /opt/ericsson/nms/litp/.version
        version_file = "".join(self.get_file_contents(
            self.ms_node, VERSION_FILE))

        # 2. Run "litp version" command
        litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT])
        litp_version_output = self._run_cmd(litp_version_cmd)

        # 3. Ensure output contains version
        self._assert_in(version_file, litp_version_output)

        # 4. Run "litp version -a" command
        litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT, "-a"])
        litp_version_a_output = self._run_cmd(litp_version_cmd)

        # 5. Run "litp version --all" command
        litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT, "--all"])
        litp_version_release_output = self._run_cmd(litp_version_cmd)

        # 6. Ensure 'litp --a' output matches 'litp --all'
        self.assertEqual(litp_version_a_output, litp_version_release_output)

        # 7. Ensure output contains version
        version_key = VERSION_OPT + ':'
        self._assert_in(version_key, litp_version_a_output)
        self._assert_in(version_file, litp_version_a_output)

    @attr('all', 'revert', 'story1782', 'story1782_tc02')
    def test_02_p_retrieve_litp_packages_cli(self):
        """
        @tms_id: litpcds_1782_tc02
        @tms_requirements_id: LITPCDS-1782
        @tms_title: Verify the output of "litp version -a" command
        @tms_description: Verify that the list of installed LITP rpms
        displayed via the "litp version -a" command matches the
        list of installed LITP rpms obtained via the linux "rpm" utility
        @tms_test_steps:
        @step: Get all the LITP rpms installed via linux "rpm" utility
        @result: List of all LITP rpms installed is obtained and stored for
        later use
        @step: Execute "litp version -a"
        @result: "Add-on packages:" is in output
        @result: The output from  "litp version -a" is equal to the
        list of installed LITP rpms obtained via the linux "rpm" utility
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # 1. Query actual installed LITP packages
        litp_pkgs = self._get_litp_packages()

        # 2. Run "litp version -a" command
        litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT, "-a"])
        stdout, _, _ = self.run_command(self.ms_node, litp_version_cmd,
                                        default_asserts=True)

        # 3. Ensure all litp packages are in output
        self.assertTrue(self.is_text_in_list('Add-on packages:',
                                             stdout))
        for pkg_info in litp_pkgs.split('\n'):
            if pkg_info:
                name, cxp_string, version = re.split('[_ ]', pkg_info)
                ver_format = "{0}: {1} {2}".format(name, version, cxp_string)
                self._assert_in(''.join(ver_format), ''.join(stdout))

    @attr('all', 'revert')
    def obsolete_03_p_retrieve_install_info_cli(self):
        """
        Description:
            Retrieves LITP install info using CLI

        Actions:
            1. cat actual install info
            2. Run "litp version -a" command
            3. Ensure all litp packages are in output

        Result:
            LITP install info is displayed
        """
        # 1. cat actual install info
        install_file = "".join(self.get_file_contents(
            self.ms_node, INSTALL_FILE))

        # 2. Run "litp version -a" command
        litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT, "-a"])
        litp_version_a_output = self._run_cmd(litp_version_cmd)

        # 3. Ensure all litp packages are in output
        install_info_key = "install-info:"
        self._assert_in(install_info_key, litp_version_a_output)
        for line in install_file.split('\n'):
            if line:
                install_info_line = line.strip()
                self._assert_in(install_info_line, litp_version_a_output)

    @attr('all', 'revert', 'story1782', 'story1782_tc04')
    def test_04_p_version_help_cli(self):
        """
        @tms_id: litpcds_1782_tc04
        @tms_requirements_id: LITPCDS-1782
        @tms_title: Verify the help contents for "litp version" command
        @tms_description: Verify the contents of the LITP "version" command
        help output
        @tms_test_steps:
        @step: Execute 'litp --help' command
        @result: "version" action is in output
        @step: Execute "litp version --help"
        @result: "-a .--all" is in output
        @step: Execute 'litp -h' command
        @result: "version" action is in output
        @step: Execute "litp version -h"
        @result: "-a .--all" is in output
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # 1. Run litp help command
        litp_help_cmd = " ".join([self.cli.litp_path, "--help"])
        stdout, _, _ = self.run_command(self.ms_node, litp_help_cmd)

        # 2. Ensure version in 'litp --help' output
        help_options = [VERSION_OPT,
                        "Displays the ERIClitpcore version of LITP."]
        for option in help_options:
            self.assertTrue(self.is_text_in_list(option, stdout))

        # 3. Run 'litp version --help' command
        litp_version_help_output = " ".join([self.cli.litp_path,
                                             VERSION_OPT, "--help"])
        stdout, _, _ = self.run_command(self.ms_node, litp_version_help_output)

        # 4. Ensure [-a .--all] options in 'litp version --help'
        version_help_options = ['-a', '--all',
            "Display installed LITP packages"]
        for option in version_help_options:
            self.assertTrue(self.is_text_in_list(option, stdout))

        # 5. Ensure [-a .--all] options in 'litp version -h'
        litp_h_cmd = " ".join([self.cli.litp_path, "-h"])
        stdout, _, _ = self.run_command(self.ms_node, litp_h_cmd)
        for option in help_options:
            self.assertTrue(self.is_text_in_list(option, stdout))

        # 6. Ensure 'litp version -h' matches --help option
        litp_version_h_cmd = " ".join([self.cli.litp_path, VERSION_OPT, "-h"])
        stdout, _, _ = self.run_command(self.ms_node, litp_version_h_cmd)
        for version in version_help_options:
            self.assertTrue(self.is_text_in_list(version,
                                                 stdout))

    @attr('all', 'revert')
    def obsolete_06_n_retrieve_version_with_no_version_file(self):
        """
        Description:
            Test getting version info with no version file

        Actions:
            1. Move version file to .version.tmp
            2. Restart litpd service
            3. Run "litp version" command
            4. Ensure output contains no version founf
            5. Move version file back

        Result:
            No version found is displayed
        """
        # 1. Move version file to .version.tmp
        temp_location = "/tmp/.version.tmp"
        self.assertTrue(self.mv_file_on_node(self.ms_node, \
            VERSION_FILE, temp_location, su_root=True))

        # 2. Restart litpd service
        self.restart_litpd_service(self.ms_node)

        try:
            # 3. Run "litp version" command
            litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT])
            litp_version_output = self._run_cmd(litp_version_cmd)

            # 4. Ensure output contains no version founf
            self._assert_in("No version found", litp_version_output)

        finally:
            # 5. Move version file back
            self.assertTrue(self.mv_file_on_node(self.ms_node, \
                temp_location, VERSION_FILE, su_root=True))

            # 6. Restart litpd service
            self.restart_litpd_service(self.ms_node)

    @attr('all', 'revert')
    def obsolete_07_n_retrieve_install_info_with_no_install_file(self):
        """
        Description:
            Test getting install info with no install file

        Actions:
            1. Move install file to temp location
            2. Restart litpd service
            3. Run "litp version --all" command
            4. Ensure output contains no install info
            5. Move install file back
            6. Restart litd service

        Result:
            No install info is displayed
        """
        # 1. Move install file to temp location
        temp_location = "/tmp/.upgrade.history.tmp"
        self.assertTrue(self.mv_file_on_node(self.ms_node, \
            INSTALL_FILE, temp_location, su_root=True))

        # 2. Restart litpd service
        self.restart_litpd_service(self.ms_node)

        try:
            # 3. Run "litp version" command
            litp_version_cmd = " ".join([self.cli.litp_path, VERSION_OPT,
                                         "--all"])
            litp_version_output = self._run_cmd(litp_version_cmd)

            # 4. Ensure output contains no version found
            self._assert_not_in("install-info:", litp_version_output)

        finally:
            # 5. Move install file back
            self.assertTrue(self.mv_file_on_node(self.ms_node, \
                temp_location, INSTALL_FILE, su_root=True))

            # 6. Restart litpd service
            self.restart_litpd_service(self.ms_node)

    @attr('all', 'revert', 'story1782', 'story1782_tc08')
    def test_08_n_check_invalid_version_commands(self):
        """
        @tms_id: litpcds_1782_tc08
        @tms_requirements_id: LITPCDS-1782
        @tms_title: Check invalid version commands
        @tms_description: Verify error when running version command with
        invalid options
        @tms_test_steps:
        @step: Execute 'litp version -p /'
        @result: Message displayed: unrecognized arguments
        @step: Execute 'litp version -t'
        @result: Message displayed: unrecognized arguments
        @step: Execute 'litp version -'
        @result: Message displayed: unrecognized arguments
        @step: Execute 'litp version --path'
        @result: Message displayed: unrecognized arguments
        @step: Execute 'litp version --type=invalid'
        @result: Message displayed: unrecognized arguments
        @step: Execute 'litp v'
        @result: Message displayed: unrecognized arguments
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # 1. Run and assert error 'litp version ' with invalid options
        erro_msg = 'litp: error: unrecognized arguments:'
        litp_version_cmds = [" ".join([self.cli.litp_path, VERSION_OPT,
                                      "-p", "/"]),
                             " ".join([self.cli.litp_path, VERSION_OPT, "-t"]),
                             " ".join([self.cli.litp_path, VERSION_OPT, "-"]),
                             " ".join([self.cli.litp_path, VERSION_OPT,
                                      "--path"]),
                             " ".join([self.cli.litp_path, VERSION_OPT,
                                      "--type=invalid"]),
                             " ".join([self.cli.litp_path, VERSION_OPT, "v"])
                             ]
        for litp_version_cmd in litp_version_cmds:
            _, stderr, _ = self.run_command(self.ms_node, litp_version_cmd)
            self.assertTrue(self.is_text_in_list(erro_msg, stderr))

    @attr('all', 'revert', 'story1782', 'story1782_tc09')
    def test_09_p_ensure_litp_show_root_contains_version(self):
        """

        @tms_id: litpcds_1782_tc09
        @tms_requirements_id: LITPCDS-1782
        @tms_title: Litp show root contains version
        @tms_description: Test that the output of "litp show -p /" command
        contains the version of the installed LITP "core" rpm
        @tms_test_steps:
        @step: Execute '/bin/rpm -q ERIClitpcore_CXP9030418'
        @result: Installed core version is displayed
        @step: Execute 'litp show -p /'
        @result: Installed core version is displayed
        @step: Check core version from both commands are the same
        @result: Both versions are the same
        @tms_test_precondition: NA
        @tms_execution_type: Automated
        """
        # 1. Get installed core version.
        cmd = "/bin/rpm -q ERIClitpcore_CXP9030418"
        out, _, _ = self.run_command(self.ms_node, cmd, su_root=True,
                                     default_asserts=True)
        installed_core_ver = out[0]

        # 2. Create expected string in model from installed core version.
        _, cxp_string, version, _ = re.split('[_-]', installed_core_ver)
        expected_ver_format = "{0} {1}".format(version, cxp_string)

        # 3. Get the 'version' attribute of the model root item '/'.
        cmd = self.cli.get_show_data_value_cmd("/", "version")
        model_root_ver = self.run_command(self.ms_node, cmd)[0][0]

        # 4. Verify that the strings match.
        self.assertTrue(expected_ver_format in model_root_ver)
