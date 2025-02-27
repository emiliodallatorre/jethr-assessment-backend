from fastapi import APIRouter

from src.businesslogic.dto.employee_dto import EmployeeDTO
from src.businesslogic.dto.tax_prediction_dto import TaxPredictionDTO
from src.businesslogic.service import calculator_srv

router = APIRouter()
prefix: str = "/calculator"
tags: list[str] = ["Calculator"]


@router.post("/", response_model=TaxPredictionDTO)
def calculate_taxes(employee: EmployeeDTO) -> TaxPredictionDTO:
    return calculator_srv.calculate_taxes(employee)
