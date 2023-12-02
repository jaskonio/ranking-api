class BaseEntity():
    def __init__(self) -> None:
        pass

    def to_dict(self):
        # Si el objeto es una instancia de dict, simplemente lo devolvemos
        if isinstance(self, dict):
            return self

        # Si el objeto es una instancia de una clase personalizada, convertimos sus atributos
        if hasattr(self, '__dict__'):
            obj_dict = vars(self)

            # Convertir recursivamente los atributos que también sean objetos
            for key, value in obj_dict.items():
                if isinstance(value, (list, tuple)):
                    obj_dict[key] = [item.to_dict() if hasattr(item, '__dict__') else item for item in value]
                elif hasattr(value, '__dict__'):
                    obj_dict[key] = value.to_dict

            return obj_dict

        # Si el objeto no es una instancia de una clase personalizada, simplemente lo devolvemos
        return self
