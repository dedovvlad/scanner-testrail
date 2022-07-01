import os
import re

import yaml


class FileHelper:
    @staticmethod
    def parse_yaml(filepath):
        """
        Parse any yaml and return it as dict.

        :param filepath: full path+filename to the yaml
        :return: loaded yaml as dict
        """
        with open(os.path.abspath(filepath), encoding="utf-8") as file:
            return yaml.unsafe_load(file)

    @staticmethod
    def string_processing(raw_str: str):
        """
        Функция для обработки кастомных полей тестрейла.
        т.к. приходят в виде строки

        :param raw_str: "1\n Needed, 2\n Ready"
        :return: [{"id": 1, "name": "needed"}, {"id": 2, "name": "ready"},]
        """

        _structure = []

        re_raw: list = (
            re.sub("[^A-Za-z0-9_]", " ", raw_str.replace(" ", "_").lower())
        ).split()

        if len(re_raw) > 1:
            for i in range(len(re_raw)):
                if i % 2 == 0:
                    _structure.append({"id": int(re_raw[i])})
                else:
                    _structure[-1].update({"name": re_raw[i][1::]})
        else:
            raise IndexError("List is not complete enough")

        return _structure
