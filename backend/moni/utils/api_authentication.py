"""Override DRF Token authentication"""

from rest_framework.authentication import TokenAuthentication


class APIAuthentication(TokenAuthentication):
    '''
    Simple token based authentication.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with string `Bearer`. For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''

    keyword = 'Bearer'
