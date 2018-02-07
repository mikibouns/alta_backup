# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
import logging
import time

import log_cfg

log = logging.getLogger('alta_backup')


def log_decorator(func):
    def wrapper(*args, **kwargs):
        log.info('Start {}'.format(func.__name__))
        func_result = func(*args, **kwargs)
        log.info('{} is completed'.format(func.__name__))
        return func_result
    return wrapper


yandex_path = r'\\webdav.yandex.ru@SSL\DavWWWRoot\backup_alta'
local_path = r'C:\alta\backup'


def get_files_list(dir_path, expansion):
    file_list = [os.path.join(dir_path, i) for i in os.listdir(dir_path) if i[len(expansion) * -1:] == expansion]
    return file_list


def get_last_or_first_file(file_list, func):
    if file_list:
        return func(file_list, key=os.path.getatime)


@log_decorator
def create_zip_file(file_path):
    file_name = '{}.zip'.format(os.path.splitext(file_path)[0])
    with zipfile.ZipFile(file_name, 'w') as zip_array:
        zip_array.write(file_path)
    return file_name


@log_decorator
def move_to_backup(copied_file, destination_path):
    try:
        shutil.move(copied_file, destination_path )
    except Exception as e:
        log.error(e)


@log_decorator
def rotation_files(dir_path, expansion):
    while True:
        file_list = get_files_list(dir_path, expansion)
        if len(file_list) > 5:
            first_file = get_last_or_first_file(file_list, min)
            os.remove(first_file)
            log.info('{} is removed'.format(first_file))
        else:
            break


if __name__ == '__main__':
    log.info('!!!Start backup_app!!!')

    yadisk = get_files_list(yandex_path, '.zip')
    local = get_files_list(local_path, '.bak')

    last_local_file = get_last_or_first_file(local, max)
    last_yadisk_file = get_last_or_first_file(yadisk, max)
    if yadisk:
        if os.path.getatime(last_local_file) > os.path.getatime(last_yadisk_file):
            zip_file_path = create_zip_file(last_local_file)
            move_to_backup(zip_file_path, yandex_path)

        rotation_files(yandex_path, '.zip')
    else:
        zip_file_path = create_zip_file(last_local_file)
        move_to_backup(zip_file_path, yandex_path)

    log.info('!!!backup_app is completed!!!')



