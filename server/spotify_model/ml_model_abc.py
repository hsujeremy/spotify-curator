#!/usr/bin/env python3
from abc import ABC
from abc import abstractmethod


class MLModel(ABC):
    """Abstract base class for ML model prediction code. Original code by Brian Schmidt"""
    @property
    @abstractmethod
    def input_schema(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def output_schema(self):
        raise NotImplementedError()

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, data):
        self.input_schema.validate(data)

class MLModelException(Exception):
    """Exception type for MLModel derived classes"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
