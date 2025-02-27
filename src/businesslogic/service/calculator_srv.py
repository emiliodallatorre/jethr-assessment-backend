from src.businesslogic.dto.employee_dto import EmployeeDTO
from src.businesslogic.dto.tax_prediction_dto import TaxPredictionDTO


def calculate_taxes(employee: EmployeeDTO) -> TaxPredictionDTO:
    return TaxPredictionDTO(
        ral=employee.ral,
        month_net_salary=0,
        year_net_salary=0,
        month_gross_salary=round(employee.ral / 12, 2),
        year_gross_salary=0,
        taxes_by_recipient={},
    )
