import json

class fileDict:
    def updatefile(self):
        json.dump(self.dic, open(self.filename, 'w', encoding='utf8'), ensure_ascii=False)

    def __init__(self, initdict, filename = 'inputted_names.json', attempt_load=False):
        if attempt_load:
            try:
                self.dic = json.load(open(filename, 'r', encoding='utf8'))
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
