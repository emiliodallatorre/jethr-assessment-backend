from pydantic import BaseModel, validator, field_validator

from src.datamodel.enum.e_cost_recipient import ECostRecipient
from src.datamodel.enum.e_value_format import EValueFormat


class CostModel(BaseModel):
    name: str
    description: str

    # Tax value
    value: float
    value_format: EValueFormat  # percentage or fixed

    # Recipient
    recipient: ECostRecipient  # company or employee

    @field_validator('value', mode='before')
    def round_value(cls, v):
        return round(v, 2)

    def __init__(self, name: str, description: str, value: float, value_format: EValueFormat,
                 recipient: ECostRecipient):
        super().__init__(name=name, description=description, value=value, value_format=value_format,
                         recipient=recipient)

    def to_json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_json(data: str) -> 'CostModel':
        return CostModel.model_validate_json(data)
