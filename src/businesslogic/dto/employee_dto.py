from pydantic import BaseModel
from src.datamodel.enum.e_contract_type import EContractType
from src.datamodel.enum.e_contribution_relief import EContributionRelief
from src.datamodel.enum.e_fiscal_detraction import EFiscalDetraction

class EmployeeDTO(BaseModel):
    ral: float
    contract_type: EContractType
    contribution_relief: EContributionRelief
    fiscal_detraction: EFiscalDetraction

    def to_json(self) -> str:
        return self.model_dump_json()

    @staticmethod
    def from_json(data: str) -> 'EmployeeDTO':
        return EmployeeDTO.model_validate_json(data)