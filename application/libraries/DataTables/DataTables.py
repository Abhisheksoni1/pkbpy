from django.http import JsonResponse, HttpResponse
from django.db.models import Q


class DataTables:
    MODEL = None
    COLUMN_SEARCH = []
    METHOD = "POST"
    REQUEST = None
    SELECT_LIST_ARGS = []
    SELECT_LIST_KWARGS = {}

    QUERYSET = None
    RECORDSFILTERED = 0

    def __init__(self, request, Model):
        self.REQUEST = request
        self.MODEL = Model
        if self.REQUEST.method == 'GET':
            self.METHOD = "GET"

    def get_method(self):
        if self.METHOD == "GET":

            return self.REQUEST.GET
        else:
            return self.REQUEST.POST

    def select(self, *args, **kwargs):
        self.SELECT_LIST_ARGS, self.SELECT_LIST_KWARGS = args, kwargs
        # print(self.SELECT_LIST)

    def _get_select(self):
        # if self.SELECT_LIST  is not None and :
        self.QUERYSET = self.QUERYSET.values(*self.SELECT_LIST_ARGS, **self.SELECT_LIST_KWARGS)

    # else:
    #     self.QUERYSET = self.QUERYSET.values()

    def set_queryset(self, queryset):
        self.QUERYSET = queryset

    def _get_queryset(self):
        if self.QUERYSET is None:
            self.QUERYSET = self.MODEL.objects.all()
        self._set_search()

    def _set_search(self):
        q_objects = Q()

        for COLUMN in self.COLUMN_SEARCH:
            q_objects.add(Q(**{"{0}__icontains".format(COLUMN): self.get_method().get("search[value]")}), Q.OR)

        self.QUERYSET = self.QUERYSET.filter(q_objects)

    def _set_order(self):
        order_index = self.get_method().get("order[0][column]")


        if order_index:
            order_dir = "" if (self.get_method().get("order[0][dir]") == "asc") else "-"
            order_col = self.get_method().get("columns[" + order_index + "][data]")
            #order_col = 'id' if (order_col=='') else order_col

        else:
            order_index = 1
            order_dir='-'
            order_col = 'id'

        self.QUERYSET = self.QUERYSET.order_by(order_dir + order_col)

    def _get_data(self):
        self.RECORDSFILTERED = self.QUERYSET.count()
        limit = int(self.get_method().get("length"))
        offset = int(self.get_method().get("start"))
        return list(self.QUERYSET)[offset:offset + limit]

    def _get_total(self):
        return self.MODEL.objects.count()

    def response(self, return_list=False):
        draw = int(self.get_method().get('draw', 1))
        self._get_queryset()
        self._get_select()
        self._set_order()
        if not return_list:
            return JsonResponse(
                {'data': self._get_data(), 'draw': draw, 'recordsTotal': self._get_total(),
                 'recordsFiltered': self.RECORDSFILTERED})
        else:
            return {'data': self._get_data(), 'draw': draw, 'recordsTotal': self._get_total(),
                    'recordsFiltered': self.RECORDSFILTERED}


