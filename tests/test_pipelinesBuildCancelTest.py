# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from azure_devtools.scenario_tests import AllowLargeResponse
from .utilities.helper import DevopsScenarioTest, disable_telemetry, set_authentication, get_test_org_from_env_variable

DEVOPS_CLI_TEST_ORGANIZATION = get_test_org_from_env_variable() or 'Https://dev.azure.com/dhilmathy'

class PipelinesBuildCancelTests(DevopsScenarioTest):
    @AllowLargeResponse(size_kb=3072)
    @disable_telemetry
    @set_authentication
    def test_build_cancel(self):
        self.cmd('az devops configure --defaults organization=' + DEVOPS_CLI_TEST_ORGANIZATION + ' project=buildtests')

        build_definition_name = 'BuildTests Definition1'

        #QueueBuild to get a build ID
        queue_build_command = 'az pipelines build queue --definition-name "' + build_definition_name + '" --detect false --output json'
        queue_build_output = self.cmd(queue_build_command).get_output_in_json()
        queued_build_id = queue_build_output["id"]

        #Cancel the running build
        cancel_running_build_command = 'az pipelines build cancel --id ' + str(queued_build_id) + ' --detect false --output json'
        cancel_running_build_output = self.cmd(cancel_running_build_command).get_output_in_json()
        assert cancel_running_build_output["status"] == "cancelling"