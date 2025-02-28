from pydantic import BaseModel, field_validator

from src.datamodel.entities.cost_model import CostModel
from src.datamodel.enum.e_cost_recipient import ECostRecipient


class TaxPredictionDTO(BaseModel):
    ral: float

    month_gross_salary: float
    year_gross_salary: float

    month_net_salary: float
    year_net_salary: float

    month_cost: float
    year_cost: float

    costs_by_recipient: dict[ECostRecipient, list[CostModel]] = {}

    @field_validator('month_net_salary', 'year_net_salary', 'month_gross_salary', 'year_gross_salary', 'month_cost',
                     'year_cost', mode='before')
    def round_value(cls, v):
        return round(v, 2)

    def to_json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_json(data: str) -> 'TaxPredictionDTO':
        return TaxPredictionDTO.model_validate_json(data)
