def dicts_to_class(class_name, dicts_to_mapper, key_id=None):
    if dicts_to_mapper is None:
        return []

    new_classes = []

    for dict_to_mapper in dicts_to_mapper:
        new_class = dict_to_class(class_name, dict_to_mapper, key_id)
        new_classes.append(new_class)

    return new_classes

# rename dict_to_entity
def dict_to_class(class_name, data:dict, key_id:str =None):
    new_id = 'None'

    if isinstance(data, class_name):
        return data

    if not isinstance(data, dict):
        data = class_to_dict(data)
    
    if key_id:
        new_id = data[key_id]
        data.pop(key_id, None)
    else:
        if '_id' in data:
            new_id = data.pop('_id', None)
        elif 'id' in data:
            new_id = data.pop('id', None)

    new_class = class_name(**dict(data, id=str(new_id)))
    return new_class

def dicts_to_entity(class_name, dicts_to_mapper):
    if dicts_to_mapper is None:
        return []

    new_classes = []

    for dict_to_mapper in dicts_to_mapper:
        new_class = dict_to_entity(class_name, dict_to_mapper)
        new_classes.append(new_class)

    return new_classes

def dict_to_entity(entity_class_name, data:dict):
    if isinstance(data, entity_class_name):
        return data

    if not isinstance(data, dict):
        data = class_to_dict(data)

    # if key_id:
    #     new_id = data[key_id]
    #     data.pop(key_id, None)
    # else:
    #     if '_id' in data:
    #         new_id = data.pop('_id', None)
    #     elif 'id' in data:
    #         new_id = data.pop('id', None)
    new_id = data.pop('_id', None)
    data["id"] = new_id

    new_class = entity_class_name(**dict(data))
    return new_class

def dicts_to_objects(class_name, dicts_to_mapper, key_id=None):
    if dicts_to_mapper is None:
        return []

    new_classes = []

    for dict_to_mapper in dicts_to_mapper:
        new_class = dict_to_object(class_name, dict_to_mapper, key_id)
        new_classes.append(new_class)

    return new_classes

def dict_to_object(class_name, data:dict, key_id:str =None):
    new_id = 'None'

    if isinstance(data, class_name):
        return data

    if not isinstance(data, dict):
        data = class_to_dict(data)

    if key_id:
        new_id = data[key_id]
        data.pop(key_id, None)
    else:
        if '_id' in data:
            new_id = data.pop('_id', None)
        elif 'id' in data:
            new_id = data.pop('id', None)

    new_class = class_name(**dict(data, id=str(new_id)))
    return new_class

def class_to_dict(class_data):
    # Si el objeto es una instancia de dict, simplemente lo devolvemos
    if isinstance(class_data, dict):
        return class_data

    # Si el objeto es una instancia de una clase personalizada, convertimos sus atributos
    if hasattr(class_data, '__dict__'):
        obj_dict = vars(class_data)

        # Convertir recursivamente los atributos que también sean objetos
        for key, value in obj_dict.items():
            if isinstance(value, (list, tuple)):
                obj_dict[key] = [class_to_dict(item) if hasattr(item, '__dict__') else item for item in value]
            elif hasattr(value, '__dict__'):
                obj_dict[key] = value.to_dict

        return obj_dict

    # Si el objeto no es una instancia de una clase personalizada, simplemente lo devolvemos
    return class_data

def class_model_to_entity(entity_class_name, class_model_data:any):
    if isinstance(class_model_data, entity_class_name):
        return class_model_data

    class_model_data = class_to_dict(class_model_data)

    new_id = class_model_data.pop('id', None)
    class_model_data["id"] = new_id

    new_entity = entity_class_name(**dict(class_model_data))

    return new_entity
