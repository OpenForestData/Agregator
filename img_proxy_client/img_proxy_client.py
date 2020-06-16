import base64
import hashlib
import hmac
import textwrap

from agregator_ofd.settings.common import IMG_PROXY_SALT, IMG_PROXY_KEY, IMG_PROXY_AVAILABLE_PARAMS, IMG_PROXY_URL


class ImgProxyClient:
    """
    Static class responsible for handling all communication
    with img proxy server
    """

    @staticmethod
    def create_thumbnail_url(base_url: str, width=300, height=300, resize='fit', extension='webp'):
        key = bytes.fromhex(IMG_PROXY_KEY)
        salt = bytes.fromhex(IMG_PROXY_SALT)

        # TODO: smth to do with these ifs
        if extension not in IMG_PROXY_AVAILABLE_PARAMS['extensions']:
            extension = 'webp'
        if resize not in IMG_PROXY_AVAILABLE_PARAMS['resize']:
            resize = 'fit'

        url = str.encode(base_url)
        encoded_url = base64.urlsafe_b64encode(url).rstrip(b"=").decode()
        # You can trim padding spaces to get good-looking url
        encoded_url = '/'.join(textwrap.wrap(encoded_url, 16))

        path = f"/{resize}/{width}/{height}/no/0/{encoded_url}.{extension}".encode()
        digest = hmac.new(key, msg=salt + path, digestmod=hashlib.sha256).digest()

        protection = base64.urlsafe_b64encode(digest).rstrip(b"=")

        url = b'/%s%s' % (
            protection,
            path,
        )

        return IMG_PROXY_URL + url.decode()
