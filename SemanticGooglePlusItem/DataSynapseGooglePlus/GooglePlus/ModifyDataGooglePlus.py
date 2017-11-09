import json
import requests
import Parser.HtmlStrip as hStrip
class ReadFile:
    def __init__(self):
        pass

    def readJsonFile(self,file_name_path):
        with open(file_name_path) as json_file:
           json_data= json.load(json_file)
        dict_data =dict()
        dict_data['item'] = []
        dict_data['item'].append({
            'title': json_data['title'],
            'name': json_data['object']['actor']['displayName'],
            'content': json_data['object']['content'],
            'url': json_data['object']['actor']['image']['url']
        })
        return dict_data
    def sendRestRequest(self, dict_data):
        tag_remover =hStrip.MLStripper()
        dict_file_values = dict()
        #dict_file_values['values'] =[]
        dict_file_values['item'] = {}
        dict_file_values['entity'] = []
        dict_file_values['keywords'] = {}
        dict_file_values['postags'] = []
        #dict_file_values['synset'] = []
        for item in dict_data['item']:
            dict_file_values['item'] = {'title': item['title'], 'displayName': item['name'], 'url': item['url']}
            text = tag_remover.strip_tags(item['content'])
            entity = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/entity/?ent=' +
                                   text).json()

            for ent in entity:
                dict_file_values['entity'].append({'word': ent['word'],
                                                   'ner': ent['ner']})
            keyword = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/keyword/?sentence=' +
                text).json()
            dict_file_values['keywords'] = {'keyword': keyword['keyword']}
            postag = requests.post('http://d2dcrc.cse.unsw.edu.au:9091/ExtractionAPI-0.0.1-SNAPSHOT/rest/postag/?tag=' +
                                   text).json()
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
