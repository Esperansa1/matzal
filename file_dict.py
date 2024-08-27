import json
from pathlib import Path

"""
This class is supposed to act as a dictionary
    that when updated, also updates a file associated with it.
Essenically a wrapper for a dictionary.
This implementation of saving the statuses was chosen for minimal refactoring.
"""
class FileDict:
    def updatefile(self):
        THIS_FOLDER = Path(__file__).parent.resolve()
        data_file = f"{THIS_FOLDER}/{self.filename}"
        with open(self.filename, 'w', encoding='utf8') as f:
            json.dump(self.dic, f, ensure_ascii=False)

    def __init__(self, initdict, filename = 'json/inputted_names.json', attempt_load=False):
        if attempt_load:
            try:          
                THIS_FOLDER = Path(__file__).parent.resolve()
                data_file = f"{THIS_FOLDER}/{filename}"
                with open(data_file, 'r', encoding='utf8') as f:
                    self.dic = json.load(f)
            except Exception as ex:
                print('Something wrong went with loading inputted_names:', ex)
                self.dic = initdict
        else:
            self.dic = initdict

        self.filename = filename
        self.updatefile()
    
    def __setitem__(self, key, item):
        self.dic[key] = item
        self.updatefile()
    
    def __getitem__(self, key):
        return self.dic.get(key)

    def __len__(self):
        return len(self.dic)

    def __delitem__(self, key):
        del self.dic[key]
        self.updatefile()

    def keys(self):
        return self.dic.keys()

    def values(self):
        return self.dic.values()

    def items(self):
        return self.dic.items()

    def toJSON(self):
        return json.dumps(self.dic)
