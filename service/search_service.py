#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Goddy <wuchuansheng@yeah.net> 2019-09-17
# Desc:

from model import Schema
import re
import copy


class SearchService:
    def __init__(self, schema: Schema):
        self.schema = schema

    def autocomplete(self, q: str):
        result = []
        for c in self.schema.class_list:
            if _is_name_contain(q, c):
                result.append(_filter_name(c))
        for l in self.schema.link_list:
            if _is_name_contain(q, l):
                result.append(_filter_name(l))
        return result

    def search(self, q: str):
        result = []
        for c in self.schema.class_list:
            if _is_name_contain(q, c):
                result.append(_filter_intro(c))
        for l in self.schema.link_list:
            if _is_name_contain(q, l):
                result.append(_filter_intro(l))
        return result

    def get_one(self, name: str):
        d = self._find_name(name)
        if d is None:
            return
        d = copy.deepcopy(d)
        split_keys = ['domain', 'range', 'property']
        for split_key in split_keys:
            if split_key in d and d[split_key] != '':
                d[split_key] = re.split('[ ，,]+', d[split_key])
        search_keys = ['domain', 'range', 'property', 'super', 'supersededBy', 'inverseOf']
        search_names = []
        for search_key in search_keys:
            if isinstance(d[search_key], str) and d[search_key] != '':
                search_names.append(_get_super_name(d[search_key]))
            elif isinstance(d[search_key], list):
                search_names.extend(_get_super_name(i) for i in d[search_key])
        names_dict = self._find_names(search_names)
        for search_key in search_keys:
            if isinstance(d[search_key], str) and d[search_key] != '':
                d[search_key] = _filter_intro(names_dict[
                                                  _get_super_name(d[search_key])])
            elif isinstance(d[search_key], list):
                d[search_key] = [_filter_intro(names_dict[
                                                   _get_super_name(i)], range=search_key == 'property')
                                 for i in d[search_key]]
        return d

    def _find_names(self, names: [str]):
        result = {name: None for name in names}
        for c in self.schema.class_list:
            for name in names:
                if c['name'].lower() == name.lower():
                    result[name] = c
                    names.remove(name)
        for l in self.schema.link_list:
            for name in names:
                if l['name'].lower() == name.lower():
                    result[name] = l
                    names.remove(name)
        return result

    def _find_name(self, name: str):
        for c in self.schema.class_list:
            if c['name'].lower() == name.lower():
                return c
        for l in self.schema.link_list:
            if l['name'].lower() == name.lower():
                return l
        return None


def _get_super_name(super_str: str) -> str or None:
    str_split = super_str.split('/')
    if len(str_split) < 2:
        return None
    return super_str.split('/')[-1]


def _filter_name(d: dict):
    return {'name': d['name'], 'nameZh': d['nameZh']}


def _filter_intro(d: dict, **kwargs):
    result = {'name': d['name'], 'nameZh': d['nameZh'],
              'description': d['description'], 'descriptionZh': d['descriptionZh']}
    if 'range' in kwargs and kwargs['range'] is True:
        result['range'] = d['range']
    return result


def _is_name_contain(q: str, d: dict):
    return re.search(q, d['name'], re.IGNORECASE) \
           or re.search(q, d['nameZh'], re.IGNORECASE) \
           or re.search(q, d['nickname'], re.IGNORECASE)
