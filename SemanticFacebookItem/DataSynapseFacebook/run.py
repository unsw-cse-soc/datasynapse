import config.config as config_module
import os
import FB.ModifyDataFB as modify_fb
if __name__=='__main__':
    dir_path = config_module.config_file('dir','path')
    lst_json_file = [files for files in os.listdir(dir_path) if files.endswith('.json')]
    fb_ins = modify_fb.ReadFile()
    for json in lst_json_file:
        get_dict_data = fb_ins.readJsonFile(dir_path+json)
        get_dict_file_values = fb_ins.sendRestRequest(get_dict_data)
        fb_ins.createJsonFile(get_dict_file_values,dir_path+'enriched'+json)
