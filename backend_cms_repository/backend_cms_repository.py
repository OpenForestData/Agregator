from backend_cms_repository.backend_cms_client import BackendCmsClient
from cache_manager.cache_manager import cached


class BackendCmsRepository:
    # TODO add loggers
    """
    Class responsible for communication with backend cms
    and obtaining all informations
    """

    def __init__(self):
        self.__client = BackendCmsClient()

    @cached
    def get_facet_fields_list(self, language: str) -> (dict, dict):
        """
        Method responsible for obtaining facet fields names
        """
        facet_list = self.__client.get_facet_fields(language).get_data()
        advanced_search_list = {}
        basic_filters = {}
        if 'advanced_search_filters' in facet_list:
            advanced_search_list = facet_list['advanced_search_filters']

        if 'basic_filters' in facet_list:
            basic_filters = facet_list['basic_filters']
        return advanced_search_list, basic_filters

    def get_global_data(self, language: str) -> dict:
        """
        Method responsible for obtaining data that are repeated in
        each view of a agregator (menus, analytics, etc)
        """
        menu = self.get_menu(language)
        return {'menu': menu}

    @cached
    def get_menu(self, language: str) -> dict:
        """
        Method responsible for getting menu structure
        """
        menu_response = self.__client.get_menu(language)
        if menu_response.is_success():
            return menu_response.get_data()
        return {}

    def populate_categories(self, categories_json: str) -> bool:
        """
        Method responsible for populating categories and obtain
        actual categories sets
        """
        response = self.__client.populate_categories(categories_json)
        return response.is_success()

    @cached
    def get_categories(self, language: str):
        categories = self.__client.get_categories(language)
        if categories.is_success():
            return categories.get_data()
        return {}

    @cached
    def get_categories_descriptions(self, language: str):
        categories = self.__client.get_categories(language)
        return categories.get_categories_descriptions()

    def register_metadata_blocks(self, metadata_blocks_list) -> bool:
        """
        Method responsible for registering metadata blocks in backend cms
        """
        return self.__client.register_metadata_blocks(metadata_blocks_list).is_success()

    def get_page_details(self, slug: str):
        page_details = self.__client.get_page_details(slug)
        return page_details.get_data() if page_details.is_success() else None

    def get_blog_details(self, slug: str):
        page_details = self.__client.get_page_details(slug)
        return page_details.get_data() if page_details.is_success() else None

    def get_blog_list(self, language, page, limit, keywords_slug):
        page_details = self.__client.get_blog_index(language, page, limit, keywords_slug)
        return page_details.get_data() if page_details.is_success() else None

    def get_home(self, language: str):
        home = self.__client.get_home(language)
        return home.parse() if home.is_success() else None

    def get_news_list(self, language, page, limit):
        page_details = self.__client.get_news_index(language, page, limit)
        return page_details.get_data() if page_details.is_success() else None

    def get_faq(self, language: str):
        response = self.__client.get_faq(language)
        return response.get_data() if response.is_success() else None
