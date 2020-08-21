import json
import pytest

from backend_cms_repository.backend_cms_client import BackendCmsClient


@pytest.fixture()
def bcc():
    client = BackendCmsClient()
    yield client


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_facet_fields_success(bcc, language, success):
    res = bcc.get_facet_fields(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_facet_fields_data(bcc, language):
    res = bcc.get_facet_fields(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_facet_fields_empty_data(bcc, language):
    res = bcc.get_facet_fields(language)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_menu_success(bcc, language, success):
    res = bcc.get_menu(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_menu_data(bcc, language):
    res = bcc.get_menu(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_menu_empty_data(bcc, language):
    res = bcc.get_menu(language)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'language', ['pl', 'en', 'de', 'ru']
)
def test_get_page_details_slug(bcc, language):
    slug = '/api/v1/media-cms/'
    res_with_lang = bcc.get_page_details('/' + language + slug, language)
    res_without_lang = bcc.get_page_details(slug, language)
    assert res_with_lang.get_data() == res_without_lang.get_data()
    assert res_with_lang.is_success() == res_without_lang.is_success()


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_page_details_success(bcc, language, success):
    res = bcc.get_page_details('/cms-api/v1/get-categories', language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_page_details_data(bcc, language):
    res = bcc.get_page_details('/cms-api/v1/get-categories', language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_page_details_empty_data(bcc, language):
    res = bcc.get_page_details('/cms-api/v1/get-categories', language)
    assert res.get_data() == {}


def test_get_page_details_without_lang(bcc):
    res = bcc.get_page_details('/api/v1/media-cms/', 'pi')
    assert not res.is_success()


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_categories_success(bcc, language, success):
    res = bcc.get_categories(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_categories_data(bcc, language):
    res = bcc.get_categories(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_categories_empty_data(bcc, language):
    res = bcc.get_categories(language)
    assert res.get_data() == {}


def test_populate_valid_categories(bcc):
    categories = {'categories': [{'name': 'test_name', 'friendly_name': 'friendly_test_name', 'id': 101,
                                  'description': 'test_description', 'dvName': 'test_dvName', 'publicationDate': '2020',
                                  'dvAffiliation': 'test_dvAffiliation'},
                                 {'name': 'test_name_2', 'friendly_name': 'friendly_test_name_2', 'id': 102,
                                  'description': 'test_description', 'dvName': 'test_dvName_2',
                                  'publicationDate': '2020', 'dvAffiliation': 'test_dvAffiliation_2'}]}
    res = bcc.populate_categories(json.dumps(categories))
    assert res.is_success()
    assert res.get_data() == {}


def test_populate_invalid_categories(bcc):
    res = bcc.populate_categories("")
    assert not res.is_success()
    assert res.get_data() == {}


def test_register_valid_metadata_blocks(bcc):
    blocks = {'test_1': {'name': 'test_name_1', 'displayName': 'test_1_displayName',
                         'fields': {
                             'test_11': {
                                 'name': 'test_11', 'displayName': 'test_11_displayName', 'title': 'title_11',
                                 'type': 'type_11', 'description': 'description_11'},
                             'test_12': {
                                 'name': 'test_12', 'displayName': 'test_12_displayName', 'title': 'title_12',
                                 'type': 'type_12', 'description': 'description_12'}}},
              'test_2': {'name': 'test_name_2', 'displayName': 'test_2_displayName',
                         'fields': {
                             'test_21': {
                                 'name': 'test_21', 'displayName': 'test_21_displayName', 'title': 'title_21',
                                 'type': 'type_21', 'description': 'description_21'},
                             'test_22': {
                                 'name': 'test_22', 'displayName': 'test_22_displayName', 'title': 'title_22',
                                 'type': 'type_22', 'description': 'description_22'}}}}

    res = bcc.register_metadata_blocks(blocks)
    assert res.is_success()
    assert res.get_data() == {}


def test_register_invalid_metadata_blocks(bcc):
    res = bcc.register_metadata_blocks("")
    assert not res.is_success()
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_blog_index_success(bcc, language, success):
    res = bcc.get_blog_index(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_blog_index_data(bcc, language):
    res = bcc.get_blog_index(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_blog_index_empty_data(bcc, language):
    res = bcc.get_blog_index(language)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_news_index_success(bcc, language, success):
    res = bcc.get_news_index(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_news_index_data(bcc, language):
    res = bcc.get_news_index(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_news_index_empty_data(bcc, language):
    res = bcc.get_news_index(language)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'slug,success', zip(['/api/v1/media-cms/', '/cms-api/v1/get-categories', '/test', '/123'],
                            [True, True, False, False])
)
def test_get_blog_details_success(bcc, slug, success):
    res = bcc.get_blog_details(slug)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'slug', ['/api/v1/media-cms/', '/cms-api/v1/get-categories']
)
def test_get_blog_details_data(bcc, slug):
    res = bcc.get_blog_details(slug)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'slug', ['/test', '/123']
)
def test_get_blog_details_empty_data(bcc, slug):
    res = bcc.get_blog_details(slug)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'slug,success', zip(['/api/v1/media-cms/', '/cms-api/v1/get-categories', '/test', '/123'],
                            [True, True, False, False])
)
def test_get_blog_keyword_list_success(bcc, slug, success):
    res = bcc.get_blog_keyword_list(slug)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'slug', ['/api/v1/media-cms/', '/cms-api/v1/get-categories']
)
def test_get_blog_keyword_list_data(bcc, slug):
    res = bcc.get_blog_keyword_list(slug)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'slug', ['/test', '/123']
)
def test_get_blog_keyword_list_empty_data(bcc, slug):
    res = bcc.get_blog_keyword_list(slug)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_home_success(bcc, language, success):
    res = bcc.get_home(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_home_data(bcc, language):
    res = bcc.get_home(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_home_empty_data(bcc, language):
    res = bcc.get_home(language)
    assert res.get_data() == {}


@pytest.mark.parametrize(
    'language,success', zip(['pl', 'en', 'de', 'ru'], [True, True, False, False])
)
def test_get_faq_success(bcc, language, success):
    res = bcc.get_faq(language)
    assert res.is_success() == success


@pytest.mark.parametrize(
    'language', ['en', 'pl']
)
def test_get_faq_data(bcc, language):
    res = bcc.get_faq(language)
    assert res.get_data() != {}


@pytest.mark.parametrize(
    'language', ['de', 'ru']
)
def test_get_faq_empty_data(bcc, language):
    res = bcc.get_faq(language)
    assert res.get_data() == {}
