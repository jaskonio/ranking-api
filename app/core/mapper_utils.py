def dicts_to_class(class_name, dicts_to_mapper, key_id=None):
    if dicts_to_mapper is None:
        return []

    new_classes = []

    for dict_to_mapper in dicts_to_mapper:
        new_class = dict_to_class(class_name, dict_to_mapper, key_id)
        new_classes.append(new_class)

    return new_classes

def dict_to_class(class_name, data:dict, key_id:str =None):
    new_id = 'None'

    if isinstance(data, class_name):
        return data

    if key_id:
        new_id = data[key_id]
        data.pop(key_id, None)
    else:
        if '_id' in data:
            new_id = data.pop('_id', None)
        elif 'id' in data:
            new_id = data.pop('id', None)

    new_class = class_name(**dict(data, id=new_id))
    return new_class
