from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from binding_searchapp.models import Binding

@registry.register_document
class BindingDocument(Document):
    # drug = fields.TextField()
    # target = fields.TextField()
    #
    # gcnnet_bindingdb_ic50 = fields.FloatField()
    # gcnnet_bdtdc_ic50 = fields.FloatField()
    #
    # model = fields.TextField()
    # type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'binding'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 5,
        }

    class Django:
        model = Binding
        fields = [
            'drug',
            'target',
            'bindingdb_kd', 'bindingdb_ki', 'bindingdb_ic50', 'bdtdc_ic50', 'bdtdc_ki',
            'model',
        ]
