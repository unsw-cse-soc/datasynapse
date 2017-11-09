import json
import requests

class ReadFileLinkedIn:
    def __init__(self):
        pass

    def readJsonFile(self,file_name_path):
        with open(file_name_path) as json_file:
            json_data = json.load(json_file)
        dict_data = dict()
        dict_data['item'] = []
        for p in json_data['data']:
            dict_data['item'].append({
                'firstName': p['firstName'],
                'lastName': p['lastName'],
                'headline': p['headline'],
                'url': p['siteStandardProfileRequest']['url'],
                'id': p['id']
            })
        return dict_data

    def sendRestRequest(self, dict_data):
        dict_file_values = dict()
        # dict_file_values['values'] =[]
        dict_file_values['item'] = {}
        dict_file_values['entity'] = []
        dict_file_values['keywords'] = {}
        dict_file_values['postags'] = []
        dict_file_values['synset'] = []
        for item in dict_data['item']:
            dict_file_values['item'] = {'id': item['id'], 'firstName': item['firstName'], 'lastName': item['lastName'],
                                        'headline': item['headline'], 'url': item['url']}
            entity = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/entity/?ent=' +
                                   item['headline']).json()

            for ent in entity:
                dict_file_values['entity'].append({'word': ent['word'],
                                                   'ner': ent['ner']})

            keyword = requests.post(
                'http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/keyword/?sentence=' +
                item['headline']).json()

            dict_file_values['keywords'] = {'keyword': keyword['keyword']}

            postag = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/postag/?tag=' +
                                   item['headline']).json()

            for pos in postag:
                dict_file_values['postags'].append({
                    'wordPart': pos['wordPart'],
                    'pos': pos['tag']
                })

            #for token in keyword['keyword'].split(','):
            #    synset = requests.post(
            #        'http://localhost:8080/ExtractionAPI/rest/synset/?syn=' + token).json()
            #    dict_file_values['synset'].append({
            #        'token': token,
            #        'synonym': synset['value']
            #    })
            str_dict_file_values = str(dict_file_values).replace('\'', '\"')
            # dict_file_values['values'].append({'items':str_dict_file_values})
            # dict_file_values['values'].append({'item': dict_file_values['item'], 'entities': dict_file_values['entity'],
            #                                   'keywords': dict_file_values['keywords']
            #                                      , 'postags': dict_file_values['postags'],
            #                                   'synonyms': get_dict_file_values['synset']})
            print(str_dict_file_values)
        return dict_file_values

    def createJsonFile(self,dict_file_values,file_path):
        with open(file_path,'w') as file_writer:
            json.dump(dict_file_values,file_writer)