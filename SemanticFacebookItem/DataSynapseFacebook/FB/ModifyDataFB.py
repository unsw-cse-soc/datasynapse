import json
import requests
class ReadFile:
    def __init__(self):
        pass

    def readJsonFile(self,file_name_path):
        with open(file_name_path) as json_file:
           json_data= json.load(json_file)
        dict_data =dict()
        dict_data['item'] = []
        for p in json_data['data']:
            dict_data['item'].append({
                'message': p['message'],
                'name': p['from']['name'],
                'id': p['id']
            })
        return dict_data

    def sendRestRequest(self, dict_data):
        dict_file_values = dict()
        #dict_file_values['values'] =[]
        dict_file_values['item'] = {}
        dict_file_values['entity'] = []
        dict_file_values['keywords'] = {}
        dict_file_values['postags'] = []
        #dict_file_values['synset'] = []
        for item in dict_data['item']:
            dict_file_values['item'] = {'id': item['id'], 'message': item['message'], 'user': item['name']}
            entity = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/entity/?ent=' +
                                   item['message']).json()
            for ent in entity:
                dict_file_values['entity'].append({'word': ent['word'],
                                                   'ner': ent['ner']})
            keyword = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/keyword/?sentence=' +
                item['message']).json()
            dict_file_values['keywords'] = {'keyword': keyword['keyword']}
            postag = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/postag/?tag=' +
                                   item['message']).json()
            for pos in postag:
                dict_file_values['postags'].append({
                    'wordPart': pos['wordPart'],
                    'pos': pos['tag']
                })
            #for token in keyword['keyword'].split(','):
                #synset = requests.post(
                #    'http://localhost:8080/ExtractionAPI/rest/synset/?syn=' +token).json()
                #dict_file_values['synset'].append({
                #    'token': token,
                #    'synonym': synset['value']
                #})
            str_dict_file_values = str(dict_file_values).replace('\'', '\"')
            #dict_file_values['values'].append({'items':str_dict_file_values})
            #dict_file_values['values'].append({'item': dict_file_values['item'], 'entities': dict_file_values['entity'],
            #                                   'keywords': dict_file_values['keywords']
            #                                      , 'postags': dict_file_values['postags'],
            #                                   'synonyms': get_dict_file_values['synset']})
            print(str_dict_file_values)
        return dict_file_values

    def createJsonFile(self,dict_file_values,file_path):
        with open(file_path,'w') as file_writer:
            json.dump(dict_file_values,file_writer)
if __name__ == '__main__':
    re = ReadFile()
    get_dict_data = re.readJsonFile()
    get_dict_file_values = re.sendRestRequest(get_dict_data)
    re.createJsonFile(get_dict_file_values)
