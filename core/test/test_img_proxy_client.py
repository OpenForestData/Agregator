import pytest

from img_proxy_client.img_proxy_client import ImgProxyClient


@pytest.mark.parametrize(
    'param,extension', zip(['jpg', 'png', 'webp', 'gif', 'bmp'], ['jpg', 'png', 'webp', 'webp', 'webp'])
)
def test_thumbnail_extension(param, extension):
    """
    Tests extension of created thumbnail url
    """
    thumbnail = ImgProxyClient.create_thumbnail_url('test', extension=param)
    assert thumbnail.endswith(extension)


@pytest.mark.parametrize(
    'param,resize', zip(['fit', 'fill', 'crop', 'force', 'dwindle', 'enlarge'],
                        ['fit', 'fill', 'crop', 'force', 'fit', 'fit'])
)
def test_thumbnail_resize(param, resize):
    """
    Tests resize type of created thumbnail url
    """
    thumbnail = ImgProxyClient.create_thumbnail_url('test', resize=param)
    assert thumbnail.split('/')[-6] == resize


@pytest.mark.parametrize(
    'size', [-5, 0, 2, 202, 0.33]
)
def test_thumbnail_size(size):
    """
    Tests size of created thumbnail url
    """
    thumbnail = ImgProxyClient.create_thumbnail_url('test', width=size, height=size)
    assert thumbnail.split('/')[-5] == str(size)
    assert thumbnail.split('/')[-4] == str(size)
