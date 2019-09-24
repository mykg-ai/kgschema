#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Goddy <wuchuansheng@yeah.net> 2019-09-16
# Desc:
#   data: https://github.com/schemaorg/schemaorg/tree/master/data/releases

import csv
import os
import json
import pickle
import re

_KGS_NAMESPACE = 'http://kgs.mykg.ai'
_SCHEMA_NAMESPACE = 'http://schema.org'
_KGS_FIELD_NAMES = ['category', 'name', 'nameZh', 'nickname',  'description', 'descriptionZh',
                    'super', 'property', 'supersededBy', 'domain', 'range', 'inverseOf', 'schemaUrl']
_KGS_CSV = '/kgs.csv'
# _KGS_JSON_CLASS_LIST = '/class-list.json'
# _KGS_JSON_CLASS_SUPER = '/class-super.json'
# _KGS_JSON_CLASS_ZIP = '/class-zip.json'
# _KGS_JSON_LINK_LIST = '/link-list.json'
_data_dir = os.path.dirname(__file__) + '/../data/'
_PICKLE = '/cache.pkl'


class Schema:
    def __init__(self, version: str, **kwargs):
        self.version = version
        if not os.path.exists(_data_dir + version + _PICKLE):
            if not os.path.exists(_data_dir + version):
                os.mkdir(_data_dir + version)
            if not os.path.exists(_data_dir+self.version+_KGS_CSV):
                self._generate_csv(kwargs['types_path'],
                                   kwargs['properties_path'],
                                   kwargs['cnschema_path'],
                                   kwargs['alter_path'])
            self.class_list, self.class_super, self.class_without_super, self.class_zip, self.link_list \
                = self._generate_lists()
        else:
            with open(_data_dir + version + _PICKLE, 'rb') as f:
                self.class_list = pickle.load(f)
                self.class_super = pickle.load(f)
                self.class_without_super = pickle.load(f)
                self.class_zip = pickle.load(f)
                self.link_list = pickle.load(f)

    def get_class_zip(self):
        return json.dumps(self.class_zip, indent=2, ensure_ascii=False)

    def get_class_super(self):
        return json.dumps(self.class_super, indent=2, ensure_ascii=False)

    def get_class_list(self):
        return json.dumps(self.class_list, indent=2, ensure_ascii=False)

    def get_link_list(self):
        return json.dumps(self.link_list, indent=2, ensure_ascii=False)

    def _generate_csv(self, types_path: str, properties_path: str, cnschema_path: str, alter_path: str):
        with open(_data_dir+self.version+_KGS_CSV, 'w+') as rf:
            writer = csv.DictWriter(rf, fieldnames=_KGS_FIELD_NAMES)
            writer.writeheader()
            with open(_data_dir+types_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    kgs = type2kgs(row)
                    kgs = self._fill_zh(_data_dir+cnschema_path, kgs)
                    kgs = self._alter_kgs(_data_dir+alter_path, kgs)
                    if kgs is not None:
                        writer.writerow(kgs)
            with open(_data_dir+properties_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    kgs = property2kgs(row)
                    kgs = self._fill_zh(_data_dir+cnschema_path, kgs)
                    kgs = self._alter_kgs(_data_dir+alter_path, kgs)
                    if kgs is not None:
                        writer.writerow(kgs)

    def _generate_lists(self) -> ([], [], [], [], []):
        class_list = []
        link_list = []
        with open(_data_dir+self.version+_KGS_CSV, 'r') as f:
            for row in csv.DictReader(f):
                if row['category'] == 'class':
                    class_list.append(row)
                elif row['category'] == 'link':
                    link_list.append(row)
        class_super, without_super = get_class_super(class_list)
        class_zip = get_class_zip(class_super, without_super)
        with open(_data_dir+self.version+_PICKLE, 'wb+') as f:
            pickle.dump(class_list, f)
            pickle.dump(class_super, f)
            pickle.dump(without_super, f)
            pickle.dump(class_zip, f)
            pickle.dump(link_list, f)
        return class_list, class_super, without_super, class_zip, link_list

    @staticmethod
    def _fill_zh(cnschema_path: str, kgs: dict):
        with open(cnschema_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name'] == kgs['name']:
                    kgs['nameZh'] = row['nameZh']
                    kgs['nickname'] = row['alternateName']
                    kgs['descriptionZh'] = row['descriptionZh']
        return kgs

    @staticmethod
    def _alter_kgs(alter_path: str, kgs: dict):
        with open(alter_path, 'r') as f:
            alter = json.load(f)
            if kgs['name'] in alter['delete']:
                return None
            for d in alter['alter']:
                if d['name'] == kgs['name']:
                    for k in d:
                        if k in kgs:
                            kgs[k] = d[k]
            for k in ['super', 'property', 'supersededBy', 'domain', 'range', 'inverseOf']:
                if k in kgs:
                    props = re.split('[ ，,]+', kgs[k])
                    for delete in alter['delete']:
                        for prop in props:
                            if delete in prop:
                                props.remove(prop)
                    kgs[k] = ', '.join(props)
        return kgs


def type2kgs(row: dict) -> dict:
    return {
        'category': 'class',
        'schemaUrl': row['id'],
        'name': row['label'],
        'nameZh': '',
        'nickname': '',
        'description': row['comment'],
        'descriptionZh': '',
        'super': get_super(row),
        'property': replace_namespace(row['properties']),
        'supersededBy': row['supersededBy']
    }


def property2kgs(row: dict) -> dict:
    return {
        'category': 'link',
        'schemaUrl': row['id'],
        'name': row['label'],
        'nameZh': '',
        'nickname': '',
        'description': row['comment'],
        'descriptionZh': '',
        'super': replace_namespace(row['subPropertyOf']),
        'supersededBy': replace_namespace(row['supersededBy']),
        'domain': replace_namespace(row['domainIncludes']),
        'range': replace_namespace(row['rangeIncludes']),
        'inverseOf': replace_namespace(row['inverseOf'])
    }


def get_super(row: dict) -> str:
    if row['label'] in ['Number', 'Time']:
        return _SCHEMA_NAMESPACE+'/DataType'
    elif is_not_blank(row['subTypeOf']):
        return replace_namespace(row['subTypeOf'])
    else:
        return replace_namespace(row['enumerationtype'])


def replace_namespace(input_str: str) -> str:
    return input_str.replace(_SCHEMA_NAMESPACE, _KGS_NAMESPACE)


def is_not_blank(test_str: str) -> bool:
    return test_str is not None and test_str != ''


def get_super_name(super_str: str) -> str or None:
    str_split = super_str.split('/')
    if len(str_split) < 2:
        return None
    return super_str.split('/')[-1]


def get_class_super(class_list: []) -> ({}, []):
    class_dict = {}
    without_super = []
    for c in class_list:
        super_name = get_super_name(c['super'])
        if super_name is None:
            without_super.append(c)
            continue
        if super_name in class_dict:
            class_dict[super_name].append(c)
        else:
            class_dict[super_name] = [c]
    return class_dict, without_super


def get_class_zip(class_dict: {}, without_super: []) -> []:
    class_zip = []
    for w in without_super:
        for (super_name, c_list) in class_dict.items():
            if super_name == w['name']:
                class_zip.append({
                    'name': w['name'],
                    'nameZh': w['nameZh'],
                    'children': [find_lower(class_dict, c) for c in c_list]
                })
                break
    return class_zip


def find_lower(class_dict: dict, c2find: dict) -> dict:
    flag = False
    for (super_name, c_list) in class_dict.items():
        if super_name == c2find['name']:
            flag = True
            return {
                'name': c2find['name'],
                'nameZh': c2find['nameZh'],
                'children': [find_lower(class_dict, c) for c in c_list]
            }
    if not flag:
        return {'name': c2find['name'], 'nameZh': c2find['nameZh']}


if __name__ == '__main__':
    schema = Schema(version='1.1',
                    types_path='schema-types-3.9.csv',
                    properties_path='schema-properties-3.9.csv',
                    cnschema_path='cns-core-3.4.csv',
                    alter_path='alter-1.0.json')
    # schema = Schema(version='1.0')
    # print(schema.get_class_zip())
    print('Done!')
