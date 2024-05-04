from pydantic import BaseModel


class BaseEntityProperty(BaseModel):
    def create_by_domain_model(self, domain_data: BaseModel):
        data_dict = domain_data.dict(exclude_none=True)

        data = self.parse_obj(data_dict)

        return data
