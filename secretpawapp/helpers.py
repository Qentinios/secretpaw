import base64
from django.conf import settings
from hashids import Hashids

hashids = Hashids(salt=settings.PROFILE_URL_ENCODE_SECRET)


def encode_profile_url(userid):
    # encode
    userid_encoded = hashids.encode(userid)
    encoded = base64.b32encode(bytes(userid_encoded, 'utf-8')).decode('utf-8')

    # remove trailing equals and make lower
    profile_url = encoded.strip('=').lower()

    return profile_url


def decode_profile_url(profile_url):
    # pre-fill missing equals and make upper
    equals_count = 8 - len(profile_url) % 8
    encoded = profile_url.upper().ljust(len(profile_url) + equals_count, '=')

    # decode
    decoded = base64.b32decode(encoded).decode('utf-8')
    userid_decoded = hashids.decode(decoded)

    return userid_decoded
