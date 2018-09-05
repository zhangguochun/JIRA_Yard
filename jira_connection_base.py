import json
from base64 import b64encode
from http.client import HTTPSConnection
from abc import ABC, ABCMeta

class JiraConnection(ABC):

    __metaclass__=ABCMeta

    _body=""
    _header=""
    _userAndPass=b''

    def setUserAndPass(self, userAndPassStr):
        self._userAndPass=b64encode(bytes(userAndPassStr,'ascii')).decode("ascii")
        return self

    def setHeader(self):
        self._headers = { 'Authorization' : 'Basic %s' %  self._userAndPass, 'Content-Type': 'application/json' }
        return self

    def setBody(self,body_json):
        self._body=body_json
        return self

    def sendRequest(self):

        try:
            self.connection=HTTPSConnection("jira.aspiraconnect.com", context=ssl._create_unverified_context())
            self.connection.request('POST', '/rest/api/2/search', headers=self._headers, body=self._body)
            return self.connection.getresponse().read()
        except ConnectionResetError:
            print(error_message='Connection reset')
            return None
        except TimeoutError:
            print(error_message='Timeout....')
            return None

        return None

        



