import pytest

from ..main import CacheManager, cached


class Add:
    """
    Helper class
    """
    @cached
    def two(self, x):
        return x + 2

    @cached
    def sum_list(self, x):
        return sum(x)


@pytest.fixture()
def adding():
    obj = Add()
    yield obj
#
#
# @pytest.fixture()
# def cm():
#     cache = CacheManager()
#     yield cache
#
#
# @pytest.mark.parametrize(
#     'name', ['string', 'int', 'float', 'None', 'list', 'dict']
# )
# def test_cache_manager_get_absent(cm, name):
#     """
#     Tests get function on absent names
#     """
#     assert cm.get(name) is None
#
#
# @pytest.mark.parametrize(
#     'name,value',
#     [('string', 'tests'), ('int', -1), ('float', 0.5), ('None', None), ('list', [1, 2, 3]), ('dict', {'tests': 1})]
# )
# def test_cache_manager_get(cm, name, value):
#     """
#     Tests get function on occurring names
#     """
#     res = cm.set(name, value)
#     assert res
#     assert cm.get(name) == value
#
#
# @pytest.mark.parametrize(
#     'name,value',
#     [('rep', 'tests'), ('rep', -1), ('rep', 0.5), ('rep', None), ('rep', [1, 2, 3]), ('rep', {'tests': 1})]
# )
# def test_cache_replace(cm, name, value):
#     """
#     Tests replacement
#     """
#     cm.set(name, value)
#     assert cm.get(name) == value


@pytest.mark.parametrize(
    'x,y', zip(range(10), range(2, 12))
)
def test_cached_int_param(adding, x, y):
    """
    Tests cached wrapper on function with int parameter
    """
    value = adding.two(x)
    assert value == y


@pytest.mark.parametrize(
    'x,y', [(list(range(i)), sum(list(range(i)))) for i in range(1, 10)]
)
def test_cached_list_param(adding, x, y):
    """
    Tests cached wrapper on function with list parameter
    """
    value = adding.sum_list(x)
    assert value == y
