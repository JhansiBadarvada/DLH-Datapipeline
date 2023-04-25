#!/usr/bin/env python
# coding: utf-8

# In[101]:


import json

class pipeline_settings_single:
    instance = None
    def __new__(cls):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

class pipeline_settings(pipeline_settings_single):
    def load_settings(self,filename=None):
        if filename:
            with open(filename, 'r') as f:
                self._settings = json.load(f)
        else:
            self._settings = {}
    
    def setAttr(self,key, value):
        self._settings[key] = value
        
    def getAttr(self,key):
        if key in self._settings:
            return self._settings[key]
        else:
            return None
    
    def getall(self):
        return self._settings
        
    def saveSettings(self, filename):
        if filename:
            with open(filename, 'w') as f:
                f.write(json.dumps(self._settings))


