#  Copyright 2011-2012 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from StringIO import StringIO

from parsing import parse
from robomachine.strategies import DepthFirstSearch


def _write_test(name, machine, output, test, values):
    output.write('\n%s\n' % name)
    if values:
        machine.write_variable_setting_step(values, output)
    machine.start_state.write_steps_to(output)
    for action in test:
        action.write_to(output)

def _write_tests(machine, max_tests, max_actions, output):
    i = 1
    for test, values in DepthFirstSearch(machine, max_actions).tests():
        _write_test('Test %d' % i, machine, output, test, values)
        i += 1
        if max_tests is not None and i > max_tests:
            return

def generate_dfs(machine, max_tests=None, max_actions=None, output=None):
    max_actions = -1 if max_actions is None else max_actions
    machine.write_settings_table(output)
    machine.write_variables_table(output)
    output.write('*** Test Cases ***')
    _write_tests(machine, max_tests, max_actions, output)
    machine.write_keywords_table(output)

def transform(text):
    output = StringIO()
    generate_dfs(parse(text), output=output)
    return output.getvalue()
