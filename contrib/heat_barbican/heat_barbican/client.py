#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from heat.engine.clients import client_plugin


try:
    from barbicanclient import client as barbican_client
except ImportError:
    barbican_client = None


class BarbicanClientPlugin(client_plugin.ClientPlugin):

    def _create(self):
        keystone_client = self.clients.client('keystone').client
        endpoint_type = self._get_client_option('barbican', 'endpoint_type')
        endpoint = self.url_for(service_type='key-manager',
                                endpoint_type=endpoint_type)
        # Remove version if set
        endpoint = endpoint.rsplit("/", 1)[0]
        client = barbican_client.Client(
            session=keystone_client.session, endpoint=endpoint)

        return client
