# Import necessary modules

from django.shortcuts import render, get_object_or_404
from .models import Binding
from .serializers import BindingSerializer
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import HttpResponseNotModified, HttpResponseBadRequest, HttpResponse
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from elasticsearch_dsl import Q
from binding_searchapp.documents import BindingDocument
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView



# Define function to display all books

def binding_list(request):
    return render(request, 'binding_list.html')


def binding_detail(request, id):
    book = get_object_or_404(Book, id=id)
    types = Booktype.objects.all()
    t = types.get(id=book.type.id)
    return render(request, 'binding_detail.html', {'book': book, 'type': t.btype})


class SearchView(APIView, LimitOffsetPagination):
    # entry = Entry()
    http_method_names = ['get']
    template_name = "search.html"
    title = settings.PAGE_TITLE
    drug = '*'
    target = '*'
    count = 5
    offset = 0
    limit = 5
    model = Binding
    serializer_class = BindingSerializer
    document_class = BindingDocument
    queryset = Binding.objects.all()
    BINDING_MODELS = ['m1', 'm2']

    def generate_q_expression(self, model):
        q = Q(
            'bool',
            must=[
                Q('query_string',
                  default_field='drug',
                  query=self.drug),
                Q('query_string',
                  default_field='target',
                  query=self.target),
                Q('query_string',
                  default_field='model',
                  query=model),
            ],
            must_not=[],
            should=[]
        )
        return q

    def set_drug_target(self, drug, target):
        if drug != '' and drug != None:
            self.drug = f'*{drug}*'
        if target != '' or target != None:
            self.target = f'*{target}*'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

    def type_to_string(self, name):
        if name == 'm1':
            return 'GCNNet'
        elif name == 'm2':
            return 'GAT_GCN'

    def get(self, request, *args, **kwargs):
        try:
            drug = request.GET.get('drug', '*')
            target = request.GET.get('target', '*')
            self.set_drug_target(drug, target)

            q = self.generate_q_expression(self.type_to_string('m1'))
            m1 = self.document_class.search().query(q)

            q = self.generate_q_expression(self.type_to_string('m2'))
            m2 = self.document_class.search().query(q)


            return render(request, 'search.html',
                          {'drug': self.drug, 'target': self.target,
                           'm1': m1, 'm2': m2, 'method':self.type_to_string})
        except Exception as e:
            return HttpResponse(e, status=500)
