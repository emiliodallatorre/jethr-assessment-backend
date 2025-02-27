from pydantic import BaseModel

from src.datamodel.entities.tax_model import TaxModel
from src.datamodel.enum.e_tax_recipient import ETaxRecipient


class TaxPredictionDTO(BaseModel):
    ral: float

    month_net_salary: float
    year_net_salary: float

    month_gross_salary: float
    year_gross_salary: float

    taxes_by_recipient: dict[ETaxRecipient, list[TaxModel]] = {}

    def to_json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_json(data: str) -> 'TaxPredictionDTO':
        return TaxPredictionDTO.model_validate_json(data)
