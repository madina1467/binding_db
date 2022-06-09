# Import necessary modules

from django.shortcuts import render,get_object_or_404
from .models import  Book, Booktype, Binding
from django.db.models import Q

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


# Define function to display all books

def binding_list(request):
    book = Book.objects.all()
    return render(request, 'binding_list.html', {'book': book })

    # # 
    # {% for x in book %}
    # <h3> <a href="{{ x.get_binding_details }}">{{x.drug}}</a></h3>
    # <p class="lead">by {{x.author_name}}</p>
    #   <p class="lead">${{x.price}}</p>
    #  <hr>
    # {% endfor %}


# Define function to display the particular book

def binding_detail(request,id):

    book = get_object_or_404(Book, id=id)
    types = Booktype.objects.all()
    t = types.get(id=book.type.id)
    return render(request, 'binding_detail.html', {'book': book, 'type': t.btype})


# Define function to search book

def search(request):

    es = Elasticsearch("http://localhost:9200")

    # results = scan(
    #     es,
    #     query={
    #         "query": {
    #             "bool": {
    #                 "must": {"match_all": {}},
    #                 "must_not": [],
    #             }
    #         }
    #     },
    #     index="binding",
    # )

    if request.method == "GET":
        drug = request.GET.get('drug', '*')
        print('Drug: ', drug)
        if drug == '' or drug==None:
            drug = '*'
        else:
            drug = f'*{drug}*'
        target = request.GET.get('target', '*')
        print('Target: ', target)
        if target == '' or target==None:
            target = '*'
        else:
            target = f'*{target}*'

        
        print('Drug: ', drug)
        print('Target: ', target)

        results = scan(
            es,
            query={
                "query": {
                    "bool": {
                        "must": 
                        [{
                            "query_string": {
                            "default_field": "drug",
                            "query": drug
                            }
                            },{
                            "query_string": {
                            "default_field": "target",
                            "query": target
                            }
                        }],
                        "must_not": [],
                    }
                }
            },
            index="binding",
        )
        if results == '':
            results = 'None'
        # results = Binding.objects.filter(Q(drug__icontains=results) | Q(target__icontains=results) 
        # | Q(gcnnet_bindingdb_ic50__icontains=results) | Q(gcnnet_bdtdc_ic50__icontains=results) 
        # | Q(model__icontains=results) )

    # for result in results:
    #     print(result['_source']['drug'])
    #     # print(result)


    # resp = es.search(index="binding", query={"match_all": {}})
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    # for hit in resp['hits']['hits']:
    #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


    # results = []

    # if request.method == "GET":
    #     query = request.GET.get('search')
    #     if query == '':
    #         query = 'None'
    #     results = Book.objects.filter(Q(binding_name__icontains=query) | Q(author_name__icontains=query) | Q(price__icontains=query) )

    # return render(request, 'search.html', {'query': query, 'results': results})
    return render(request, 'search.html', {'drug': drug, 'target': target, 'results': results})