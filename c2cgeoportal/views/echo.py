# Copyright (c) 2012-2014, Camptocamp SA
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

from base64 import b64encode
import json

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config


def json_base64_encode(filename, file):
    """
    Generate a JSON-wrapped base64-encoded string.
    See http://en.wikipedia.org/wiki/Base64
    """
    yield '{"filename":%s,"data":"' % (json.dumps(filename),)
    yield b64encode(file.read())
    yield '","success":true}'


@view_config(route_name='echo')
def echo(request):
    """
    Echo an uploaded file back to the client as an text/html document so it can
    be handled by Ext.

    The response is JSON-wrapped and base64-encoded to ensure that there are no
    special HTML characters or charset problems and so that braindead ext
    doesn't barf on it.

    See:
    http://docs.sencha.com/ext-js/3-4/#!/api/Ext.form.BasicForm-cfg-fileUpload
    """
    if request.method != 'POST':
        return HTTPBadRequest()
    try:
        file = request.POST['file']
    except KeyError:
        return HTTPBadRequest()
    response = Response()
    response.app_iter = json_base64_encode(file.filename, file.file)
    response.content_type = 'text/html'
    response.cache_control.no_cache = True
    return response
