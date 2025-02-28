from src.businesslogic.dto.employee_dto import EmployeeDTO
from src.businesslogic.dto.tax_prediction_dto import TaxPredictionDTO
from src.datamodel.entities.cost_model import CostModel
from src.datamodel.enum.e_cost_recipient import ECostRecipient
from src.datamodel.enum.e_value_format import EValueFormat


def calculate_taxes(employee: EmployeeDTO) -> TaxPredictionDTO:
    costs_for_employer: list[CostModel] = [
        calculate_tfr(employee),
        calculate_inps_contributions_for_employer(employee),
        calculate_inail_for_employer(employee),
    ]
    costs_for_employee: list[CostModel] = [
        calculate_inps_contributions_for_employee(employee),
        calculate_irpef_for_employee(employee),
    ]

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


def calculate_tfr(employee: EmployeeDTO) -> CostModel:
    value: float = employee.ral / 13.5

    return CostModel(
        name="TFR",
        description="Il TFR è il trattamento di fine rapporto, corrisponde a circa un mese di stipendio lordo, e viene accantonato gradualmente dal datore di lavoro.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )


def calculate_inps_contributions_for_employee(employee: EmployeeDTO) -> CostModel:
    value: float = employee.ral * 0.0919

    return CostModel(
        name="INPS",
        description="L'INPS è l'Istituto Nazionale della Previdenza Sociale, che si occupa della previdenza e dell'assistenza sociale in Italia.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )

def calculate_inps_contributions_for_employer(employee: EmployeeDTO) -> CostModel:
    value: float = employee.ral * 0.281

    return CostModel(
        name="INPS",
        description="L'INPS è l'Istituto Nazionale della Previdenza Sociale, che si occupa della previdenza e dell'assistenza sociale in Italia.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )

def calculate_irpef_for_employee(employee: EmployeeDTO) -> CostModel:
    aliquote = [
        (28000, 0.23),
        (50000, 0.35),
        (float('inf'), 0.43)
    ]

    total = 0.0
    ral = employee.ral - calculate_inps_contributions_for_employee(employee).value

    for chunck, aliquota in aliquote:
        if ral > chunck:
            total += chunck * aliquota
            ral -= chunck
        else:
            total += ral * aliquota
            break

    return CostModel(
        name="IRPEF",
        description="L'IRPEF è l'imposta sul reddito delle persone fisiche, è calcolata in base al reddito complessivo del contribuente.",
        value=total,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYEE,
    )

def calculate_inail_for_employer(employee: EmployeeDTO) -> CostModel:
    value: float = employee.ral * 0.005

    return CostModel(
        name="INAIL",
        description="L'INAIL è l'Istituto Nazionale per l'Assicurazione contro gli Infortuni sul Lavoro, che si occupa della tutela degli infortuni sul lavoro e delle malattie professionali.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )
