# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import pymongo
from pymongo import Connection
import bson
import traceback


class Corpus(object):
    
    def __init__(self, address = 'localhost', database = '', collection = ''):

        if len(database) == 0 or len(collection) == 0:
            print('Need specified name database or collection.')
            return
        
        self.connection = Connection('localhost', 27017)
        self.db = self.connection[database]

        self.collection = self.db[collection]


    def __del__(self):
        
        self.connection.disconnect()


    def append(self, record):
        """ ディクショナリ形式でデータを追加, .
        """
        try:
            if self.collection.find(record).count() > 0:
                pass
            else:
                self.collection.insert(record)
        except bson.errors.InvalidStringData as e:
            print(e.message)


    def find(self, query={}):

        return self.collection.find(query)
    
    
    def findsorted(self, query={}, key="", reverse=False, count=1):

        order = pymongo.ASCENDING if reverse else pymongo.DESCENDING
        return self.collection.find(query).sort(key, order).limit(count)


    def update(self, record, new_record):

        try:
            self.collection.update(record, new_record)
        except TypeError as e:
            print('%s #%s\n\tMessage: %s'
                    % (str(self.__class__.__name__), traceback.extract_stack()[-1][2], e.message))


    def exists(self, query):

        for item in self.collection.find(query):
            return True
        return False

    def remove(self, item):
        
        self.collection.remove(item)

    def drop(self):
        self.collection.drop()


if __name__ == '__main__':

    import datetime, copy

    db = Corpus(database = 'temp', collection = 'flickr')

    db.append({ 'user_id': 'aaaa' })

    for item in db.find():

        print(item)

        new_record = copy.deepcopy(item)
        new_record.setdefault('date', {'year': year, 'month': month, 'day': day})

        print(new_record)

        db.update(item, new_record)
        new_item = db.find({'user_id': item['user_id']})
        print(new_item)
        break

