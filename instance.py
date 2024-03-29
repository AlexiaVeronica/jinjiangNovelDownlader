import json
import os
import re


class Config:
    file_path = None
    dir_path = None
    data = None

    def __init__(self, file_path, dir_path):
        self.file_path = file_path
        self.dir_path = dir_path
        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path)
        if '.txt' in file_path:
            open(self.file_path, 'w').close()
        self.data = {}

    def load(self):
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                self.data = json.load(f) or {}
        except FileNotFoundError:
            try:
                open(self.file_path, 'w', encoding="utf-8").close()
            except Exception as e:
                print('[错误]', e)
                print('创建配置文件时出错')
        except Exception as e:
            print('[错误]', e)
            print('读取配置文件时出错')

    def save(self):
        try:
            with open(self.file_path, 'w', encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print('[错误]', e)
            print('保存配置文件时出错')


class File:
    @staticmethod
    def write(text_path: str = "", text_content: str = "", mode: str = "a") -> [str, None]:
        try:
            with open(text_path, mode, encoding="utf-8") as file:
                file.write(text_content)
        except Exception as error:
            print("[error] text_file.write:", error)

    @staticmethod
    def read(text_path: str = "", split_list: bool = False) -> [str, None]:
        try:
            with open(text_path, "r", encoding="utf-8") as file:
                if split_list:
                    return file.read().splitlines()
                return file.read()
        except Exception as error:
            print("[error] text_file.read:", error)


class Vars:
    cfg = Config(os.getcwd() + '/config.json', os.getcwd())
    current_command = None
    current_book = None


def set_config():
    Vars.cfg.load()
    save_config: bool = False
    if not isinstance(Vars.cfg.data.get("user_info"), dict):
        Vars.cfg.data['user_info'] = {}
        save_config = True
    if not isinstance(Vars.cfg.data.get("versionCode"), int):
        Vars.cfg.data['versionCode'] = 206
        save_config = True
    if Vars.cfg.data.get("downloaded_book_id_list") is None:
        Vars.cfg.data['downloaded_book_id_list'] = []
        save_config = True
    if Vars.cfg.data.get("config_path") is None or Vars.cfg.data.get("config_path") == "":
        Vars.cfg.data['config_path'] = "configs"
        save_config = True

    if save_config:
        Vars.cfg.save()


def makedir_config(file_path, dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    if '.txt' in file_path:
        open(file_path, 'w').close()


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default
