def dicts_to_class(class_name, dicts_to_mapper):
    new_classes = []

    for dict_to_mapper in dicts_to_mapper:
        new_class = dict_to_class(class_name, dict_to_mapper)
        new_classes.append(new_class)

    return new_classes

def dict_to_class(class_name, dict_to_mapper):
    new_class = class_name(*dict_to_mapper.values())
    return new_class
