# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystone.auth import controllers
from keystone.common import wsgi


class Routers(wsgi.RoutersBase):

    def append_v3_routers(self, mapper, routers):
        auth_controller = controllers.Auth()

        # NOTE(morganfainberg): For policy enforcement reasons, the
        # ``validate_token_head`` method is still used for HEAD requests.
        # The controller method makes the same call as the validate_token
        # call and lets wsgi.render_response remove the body data.
        self._add_resource(
            mapper, auth_controller,
            path='/auth/tokens',
            get_action='validate_token',
            head_action='check_token',
            post_action='authenticate_for_token',
            delete_action='revoke_token')

        self._add_resource(
            mapper, auth_controller,
            path='/auth/tokens/OS-PKI/revoked',
            get_action='revocation_list')
