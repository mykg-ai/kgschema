#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Goddy <wuchuansheng@yeah.net> 2019-09-16
# Desc:
#   data: https://github.com/schemaorg/schemaorg/tree/master/data/releases

import csv
import os
import json

_KGS_NAMESPACE = 'http://kgs.mykg.ai'
_SCHEMA_NAMESPACE = 'http://schema.org'
_KGS_FIELD_NAMES = ['category', 'name', 'nameZh', 'nickname',  'description', 'descriptionZh',
                    'super', 'supersededBy', 'range', 'inverseOf', 'schemaUrl']
_KGS_CSV = '/kgs.csv'
_KGS_JSON_CLASS = '/class.json'
_KGS_JSON_LINK = '/link.json'


class Schema:
    def __init__(self, types_path: str, properties_path: str, cnschema_path: str):
        self.types_path = types_path
        self.properties_path = properties_path
        self.cnschema_path = cnschema_path
        self.file_path = None
        self.data_dir = os.path.dirname(__file__) + '/../data/'

    def generate_files(self, version: str):
        file_path = self.data_dir + version + _KGS_CSV
        self.file_path = file_path
        # generate kgs.csv
        # self.to_kgs(version)
        # generate class.json & link.json
        self.to_class_and_link(version)

    def to_kgs(self, version: str):
        if not os.path.exists(self.data_dir+version):
            os.mkdir(self.data_dir + version)
        else:
            raise FileExistsError('version {} has existed!'.format(version))
        self._fill(self.file_path)

    def to_class_and_link(self, version: str):
        if self.file_path is None:
            raise FileNotFoundError('kgSchema file not found!')
        class_list = []
        link_list = []
        with open(self.file_path, 'r') as f:
            for row in csv.DictReader(f):
                if row['category'] == 'class':
                    class_list.append(row)
                elif row['category'] == 'link':
                    link_list.append(row)
        class_result = get_class_result(class_list)

        with open(self.data_dir+version+_KGS_JSON_LINK, 'w') as f:
            json.dump(link_list, f, indent=2, ensure_ascii=False)
        with open(self.data_dir+version+_KGS_JSON_CLASS, 'w') as f:
            json.dump(class_result, f, indent=2, ensure_ascii=False)

    def _fill(self, file_path: str):
        with open(file_path, 'w+') as rf:
            writer = csv.DictWriter(rf, fieldnames=_KGS_FIELD_NAMES)
            writer.writeheader()
            with open(self.types_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    kgs = type2kgs(row)
                    kgs = self._fill_zh(kgs)
                    writer.writerow(kgs)
            with open(self.properties_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    kgs = property2kgs(row)
                    kgs = self._fill_zh(kgs)
                    writer.writerow(kgs)

    def _fill_zh(self, kgs: dict):
        if self.cnschema_path is None:
            return
        with open(self.cnschema_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name'] == kgs['name']:
                    kgs['nameZh'] = row['nameZh']
                    kgs['nickname'] = row['alternateName']
                    kgs['descriptionZh'] = row['descriptionZh']
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


def get_class_result(class_list: []) -> []:
    class_dict = {}
    class_result = []
    without_super = []
    for c in class_list:
        # if c['name'] == 'Thing':
        #     class_result = {'name': c['name'], 'nameZh': c['nameZh']}
        super_name = get_super_name(c['super'])
        if super_name is None:
            without_super.append(c)
            continue
        if super_name in class_dict:
            class_dict[super_name].append(c)
        else:
            class_dict[super_name] = [c]
    for w in without_super:
        for (super_name, c_list) in class_dict.items():
            if super_name == w['name']:
                class_result.append({
                    'name': w['name'],
                    'nameZh': w['nameZh'],
                    'children': [find_lower(class_dict, c) for c in c_list]
                })
                break
    return class_result


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
    schema = Schema(types_path='../data/schema-types-3.9.csv',
                    properties_path='../data/schema-properties-3.9.csv',
                    cnschema_path='../data/cns-core-3.4.csv')
    schema.generate_files('1.0')
