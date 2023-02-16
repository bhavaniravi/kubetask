import inspect
import logging

def get_object_params(obj):
    attributes = {}
    for attribute, value in obj.__dict__.items():
        if attribute[:2] != '__':
            if not callable(value):
                attributes[attribute] = value
    return attributes
    
