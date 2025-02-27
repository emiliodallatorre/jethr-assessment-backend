from pydantic import BaseModel

from src.datamodel.enum.e_tax_recipient import ETaxRecipient
from src.datamodel.enum.e_value_format import EValueFormat


class TaxModel(BaseModel):
    name: str

    # Tax value
    value: float
    value_format: EValueFormat  # percentage or fixed

    # Recipient
    recipient: ETaxRecipient  # company or employee

    def __init__(self, name: str, value: float, value_format: EValueFormat, recipient: ETaxRecipient):
        self.name = name
        self.value = value
        self.value_format = value_format
        self.recipient = recipient

        super().__init__()
