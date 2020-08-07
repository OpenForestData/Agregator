API Views
=======

Datatable
---------
.. autoclass:: core.views.datatable.DatatableViewSet
    :members:

DatatableAction
---------------
.. autoclass:: core.views.datatable_action.DatatableActionViewSet
    :members: revert

    .. method:: list(self, request, *args, **kwargs)

        Returns list of all DatatablesActions

        .. http:get:: /datatable/actions/

            :query offset: offset number. default is 0
            :query limit: limit number. default is 100
            :reqheader Authorization: optional Bearer (JWT) token to authenticate
            :statuscode 200: no error
            :statuscode 401: user unauthorized
            :statuscode 403: user lacks permissions for this action