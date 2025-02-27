from src.datamodel.enum.e_contract_type import EContractType
from src.datamodel.enum.e_contribution_relief import EContributionRelief
from src.datamodel.enum.e_fiscal_detraction import EFiscalDetraction


class EmployeeModel:
    ral: float
    contract_type: EContractType
    contribution_relief: EContributionRelief
    fiscal_detraction: EFiscalDetraction