from src.businesslogic.dto.employee_dto import EmployeeDTO
from src.businesslogic.dto.tax_prediction_dto import TaxPredictionDTO
from src.datamodel.entities.cost_model import CostModel
from src.datamodel.enum.e_cost_recipient import ECostRecipient
from src.datamodel.enum.e_value_format import EValueFormat


def calculate_taxes(employee: EmployeeDTO) -> TaxPredictionDTO:
    costs_for_employer: list[CostModel] = [calculate_tfr(employee.ral)]
    costs_for_employee: list[CostModel] = []

    year_cost_for_employer: float = employee.ral + sum(cost.value for cost in costs_for_employer)
    year_profit_for_employee: float = employee.ral - sum(cost.value for cost in costs_for_employee)

    return TaxPredictionDTO(
        ral=employee.ral,
        month_net_salary=year_profit_for_employee / employee.months,
        year_net_salary=year_profit_for_employee,
        month_gross_salary=employee.ral / employee.months,
        year_gross_salary=employee.ral,
        year_cost=year_cost_for_employer,
        month_cost=year_cost_for_employer / employee.months,
        costs_by_recipient={
            ECostRecipient.EMPLOYER: costs_for_employer,
            ECostRecipient.EMPLOYEE: costs_for_employee,
        },
    )


def calculate_tfr(ral: float) -> CostModel:
    value: float = ral / 13.5

    return CostModel(
        name="TFR",
        description="Il TFR è il trattamento di fine rapporto, corrisponde a circa un mese di stipendio lordo, e viene accantonato gradualmente dal datore di lavoro.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )
