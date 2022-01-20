# -*- coding: UTF8 -*-


def replace_dict_key(data, is_list=False, **kwargs):
    """

    :param data:
    :param is_list:
    :param kwargs: old_key=new_key
    :return:
    """
    def __replace(__data: dict, **__kwargs):
        for key in __kwargs:
            __data[kwargs[key]] = __data[key]
            del __data[key]

    if not is_list:
        __replace(data, **kwargs)
    else:
        for i in data:
            __replace(i, **kwargs)
