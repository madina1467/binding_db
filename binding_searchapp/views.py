# Import necessary modules

from django.shortcuts import render, get_object_or_404
from .models import Book, Booktype, Binding
from .serializers import BindingSerializer
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import HttpResponseNotModified, HttpResponseBadRequest, HttpResponse
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from elasticsearch_dsl import Q
from binding_searchapp.documents import BindingDocument


# Define function to display all books

def binding_list(request):
    return render(request, 'binding_list.html')


def binding_detail(request, id):
    book = get_object_or_404(Book, id=id)
    types = Booktype.objects.all()
    t = types.get(id=book.type.id)
    return render(request, 'binding_detail.html', {'book': book, 'type': t.btype})


class SearchView(TemplateView):
    http_method_names = ['get']
    template_name = "search.html"
    title = settings.PAGE_TITLE
    drug = '*'
    target = '*'
    model = Binding
    serializer_class = BindingSerializer
    queryset = Binding.objects.all()

    def test(self):
        query = '*Br.*'
        q = Q(
            'bool',
            must=[
                Q('query_string',
                  default_field='drug',
                  query=query
                )
            ],
            must_not=[],
            should=[]
        )
        search = BindingDocument.search().query(q)
        response = search.execute()
        print(response)

        for hit in search:
            print(hit.target)
        return search

    def set_drug_target(self, drug, target):
        if drug != '' and drug != None:
            self.drug = f'*{drug}*'
        if target != '' or target != None:
            self.target = f'*{target}*'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        # context["drug"] = kwargs.GET.get('drug', '*')
        return context

    def es_search(self):
        es = Elasticsearch("http://localhost:9200")
        results = scan(es,
                       query={
                           "query": {
                               "bool": {
                                   "must":
                                       [{
                                           "query_string": {
                                               "default_field": "drug",
                                               "query": self.drug
                                           }
                                       }, {
                                           "query_string": {
                                               "default_field": "target",
                                               "query": self.target
                                           }
                                       }],
                                   "must_not": [],
                               }
                           }
                       },
                       index="binding"
                       )
        if results == '':
            print('results: NOONE')
            results = 'None'
        # self.test()
        # return results
        return self.test()

    def get(self, request, *args, **kwargs):
        drug = request.GET.get('drug', '*')
        target = request.GET.get('target', '*')

        self.set_drug_target(drug, target)
        return render(request, 'search.html', {'drug': self.drug, 'target': self.target, 'results': self.es_search()})

# def search(request):
#     es = Elasticsearch("http://localhost:9200")
#     # results = scan(
#     #     es,
#     #     query={
#     #         "query": {
#     #             "bool": {
#     #                 "must": {"match_all": {}},
#     #                 "must_not": [],
#     #             }
#     #         }
#     #     },
#     #     index="binding",
#     # )
#     if request.method == "GET":
#         drug = request.GET.get('drug', '*')
#         print('Drug: ', drug)
#         if drug == '' or drug==None:
#             drug = '*'
#         else:
#             drug = f'*{drug}*'
#         target = request.GET.get('target', '*')
#         print('Target: ', target)
#         if target == '' or target==None:
#             target = '*'
#         else:
#             target = f'*{target}*'
#
#
#         print('Drug: ', drug)
#         print('Target: ', target)
#
#         results = scan(
#             es,
#             query={
#                 "query": {
#                     "bool": {
#                         "must":
#                         [{
#                             "query_string": {
#                             "default_field": "drug",
#                             "query": drug
#                             }
#                             },{
#                             "query_string": {
#                             "default_field": "target",
#                             "query": target
#                             }
#                         }],
#                         "must_not": [],
#                     }
#                 }
#             },
#             index="binding",
#         )
#         if results == '':
#             print('results: NOONE')
#             results = 'None'
#         # results = Binding.objects.filter(Q(drug__icontains=results) | Q(target__icontains=results)
#         # | Q(gcnnet_bindingdb_ic50__icontains=results) | Q(gcnnet_bdtdc_ic50__icontains=results)
#         # | Q(model__icontains=results) )
#
#     # for result in results:
#     #     print(result['_source']['drug'])
#     #     # print(result)
#
#
#     # resp = es.search(index="binding", query={"match_all": {}})
#     # print("Got %d Hits:" % resp['hits']['total']['value'])
#     # for hit in resp['hits']['hits']:
#     #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
#
#
#     # results = []
#
#     # if request.method == "GET":
#     #     query = request.GET.get('search')
#     #     if query == '':
#     #         query = 'None'
#     #     results = Book.objects.filter(Q(binding_name__icontains=query) | Q(author_name__icontains=query) | Q(price__icontains=query) )
#
#     # return render(request, 'search.html', {'query': query, 'results': results})
#     return render(request, 'search.html', {'drug': drug, 'target': target, 'results': results})
