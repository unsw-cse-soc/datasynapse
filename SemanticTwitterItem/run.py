import config.config as config_module
import os
import Twitter.ModifyDataTwitter as modify_tweet
if __name__ == '__main__':
    dir_path = config_module.config_file('dir', 'path')
    lst_json_file = [files for files in os.listdir(dir_path) if files.endswith('.json')]
    plus_ins = modify_tweet.ReadFile()
    for json in lst_json_file:
        get_dict_data = plus_ins.readJsonFile(dir_path+json)
        get_dict_file_values = plus_ins.sendRestRequest(get_dict_data)
        plus_ins.createJsonFile(get_dict_file_values, dir_path + 'enriched' + json)

