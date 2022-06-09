import pandas as pd
from models.gat import GATNet
from models.gat_gcn import GAT_GCN
from models.gcn import GCNNet
from models.ginconv import GINConvNet
from utils import *

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

def ged_models():
    
    path = '/Users/madina/Documents/research/de novo molecular design/Custom-GraphDTA-with-BindingDB/GraphDTA_Results/'
    
    # md1 = 'Davis/GAT_GCN_Davis/model_GAT_GCN_davis.model'
    # md2 = 'Davis/GATNet_Davis/model_GATNet_davis.model'
    # md3 = 'Davis/GATNet_Davis/model_GATNet_davis2.model'
    # md4 = 'Davis/GCNNet_Davis/model_GCNNet_davis.model'
    # md5 = 'Davis/GINConvNet_Davis/model_GINConvNet_davis.model'
    #
    # md6 = 'KIBA/GAT_GCN_KIBA/model_GAT_GCN_kiba.model'
    # md7 = 'KIBA/GATNet_KIBA/model_GATNet_kiba.model'
    # md8 = 'KIBA/GCNNet_KIBA/model_GCNNet_kiba.model'
    # md9 = 'KIBA/GINConvNet_KIBA/model_GINConvNet_kiba.model'
    #
    # md10 = 'BindingDB/GAT_GCN/model_GAT_GCN_Kd.model'
    # md11 = 'BindingDB/GATNet/model_GATNet_bdtdc_ic50.model'
    # md12 = 'BindingDB/GATNet/model_GATNet_IC50.model'
    # md13 = 'BindingDB/GATNet/model_GATNet_Kd.model'
    #
    # md14 = 'BindingDB/GCNNet/bdtdc_ic50_dec20/model_GCNNet_bdtdc_ic50.model'
    # md15 = 'BindingDB/GCNNet/strange_model_try_to_test/model_GCNNet_Kd.model'
    # md16 = 'BindingDB/GCNNet/model_GCNNet_bdtdc_ic50.model'
    # md17 = 'BindingDB/GCNNet/model_GCNNet_bdtdc_kd.model'
    #
    # md18 = 'BindingDB/GCNNet/model_GCNNet_bdtdc_ki.model'
    # md19 = 'BindingDB/GINConvNet/model_GINConvNet_bindingdb_Kd.model'
    # md20 = 'BindingDB/GINConvNet/model_GINConvNet_IC50.model'
    # md21 = 'BindingDB/GINConvNet/model_GINConvNet_Ki.model'
    #
    # md22 = 'BindingDB/GAT_GCN/model_GAT_GCN_bdtdc_ki.model'
    # md23 = 'BindingDB/GAT_GCN/model_GAT_GCN_bdtdc_ic50.model'
    #
    # md24 = 'BindingDB/GCNNet/model_GCNNet_bindingdb_kd.model'
    # md25 = 'BindingDB/GAT_GCN/model_GAT_GCN_bindingdb_kd.model'
    #
    # md26 = 'BindingDB/GCNNet/model_GCNNet_bindingdb_ki.model'
    # md27 = 'BindingDB/GAT_GCN/model_GAT_GCN_bindingdb_ki.model'
    #
    # md28 = 'BindingDB/GAT_GCN/model_GAT_GCN_bindingdb_ic50.model'
    # md29 = 'BindingDB/GCNNet/model_GCNNet_bindingdb_ic50.model'

    md30 = 'BindingDB/bd_tdc_latest_models/model_GCNNet_bdtdc_ic50.model'
    md31 = 'BindingDB/bd_tdc_latest_models/model_GCNNet_bdtdc_ki.model'

    # models_list = [md1, md2, md3, md4, md5, md6, md7, md8, md9, md10, md11, md12, md13, md14, md15, md16, md17, md18,
    #                md19, md20, md21, md22, md23, md24, md25, md26, md27, md28, md29, md30, md31]
    # models_list = [path + i for i in models_list]
    #
    # model_names = [md1[46:-6], md2[45:-6], 'GATNet_davis2', 'GCNNet_davis', 'GINConvNet_davis', 'GAT_GCN_kiba',
    #                'GATNet_kiba', 'GCNNet_kiba', 'GINConvNet_kiba', 'GAT_GCN_Kd', 'GATNet_bdtdc_ic50', 'GATNet_IC50',
    #                'GATNet_Kd', 'bdtdc_ic50_dec20/model_GCNNet_bdtdc_ic50', 'strange_model_try_to_test/model_GCNNet_Kd',
    #                'GCNNet_bdtdc_ic50', 'GCNNet_bdtdc_kd', 'GCNNet_bdtdc_ki', 'GINConvNet_bindingdb_Kd',
    #                'GINConvNet_IC50', 'GINConvNet_Ki', 'GAT_GCN_bdtdc_ki_latest', 'GAT_GCN_bdtdc_ic50_latest',
    #                'GCNNet_bindingdb_kd_latest', 'GAT_GCN_bindingdb_kd_latest', 'GCNNet_bindingdb_ki_latest',
    #                'GAT_GCN_bindingdb_ki_latest', 'GAT_GCN_bindingdb_ic50_latest', 'GCNNet_bindingdb_ic50_latest',
    #                'GCNNet_bdtdc_ic50_latest_v2', 'GCNNet_bdtdc_ki_latest_v2']
    #
    # model_arch = [GAT_GCN, GATNet, GATNet, GCNNet, GINConvNet, GAT_GCN, GATNet, GCNNet, GINConvNet, GAT_GCN, GATNet,
    #               GATNet, GATNet, GCNNet, GCNNet, GCNNet, GCNNet, GCNNet, GINConvNet, GINConvNet, GINConvNet, GAT_GCN,
    #               GAT_GCN, GCNNet, GAT_GCN, GCNNet, GAT_GCN, GAT_GCN, GCNNet, GCNNet, GCNNet]
    #

    models_list = [md30, md31]
    models_list = [path + i for i in models_list]
    model_names = ['GCNNet_bdtdc_ic50_lv2', 'GCNNet_bdtdc_ki_lv2']
    model_arch = [GCNNet, GCNNet]


    return models_list, model_names, model_arch


def predicting(model, device, loader):
    model.eval()
    total_preds = torch.Tensor()
    print('Make prediction for {} samples...'.format(len(loader.dataset)))
    with torch.no_grad():
        for data in tqdm(loader):
            data = data.to(device)
            output = model(data)
            total_preds = torch.cat((total_preds.to(device), output), 0)
    return total_preds.cpu().numpy().flatten()

def addToDB(df, name):
    es = Elasticsearch("http://localhost:9200")

    new_employee = {
        "name": "George Peterson",
        "sex": "male",
        "age": "34",  # use "" if this is meant to be a text _type
        "years": "10"  # use "" if this is meant to be a text _type
    }

    response = es.index(index='binding', doc_type='person', body=new_employee)

def pred():
    vdr_path = '/Users/madina/Documents/research/de novo molecular design/Custom-GraphDTA-with-BindingDB/data/shrinked/'
    D_vitamind = {}
    for file in os.listdir(vdr_path):
        if '.csv' in file:
            df = pd.read_csv(vdr_path + file)
            name = file.replace('.csv', '')
            D_vitamind[name] = df

    models_list, model_names, model_arch = ged_models()

    for i in range(len(models_list)):
        device = torch.device('cuda:4' if torch.cuda.is_available() else "cpu")
        modeling = model_arch[i]
        model = modeling()
        model.to(device)
        model.load_state_dict(torch.load(models_list[i], map_location='cpu'))

        TEST_BATCH_SIZE = 512

        for k, v in D_vitamind.items():
            test_data = TestbedDataset(root=vdr_path, dataset=str(k))
            test_loader = DataLoader(test_data, batch_size=TEST_BATCH_SIZE, shuffle=False)
            pred = predicting(model, device, test_loader)
            D_vitamind[k][model_names[i]] = pred

    for k, v in D_vitamind.items():
        D_vitamind[k].to_csv(
            '/Users/madina/Documents/research/de novo molecular design/Custom-GraphDTA-with-BindingDB/prediction_for_generated_vitamind_latest/GraphDTA_prediction_shrinked_' + str(
                k) + '.csv', index=False)

if __name__ == '__main__':
    pred()