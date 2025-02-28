from src.businesslogic.dto.employee_dto import EmployeeDTO
from src.businesslogic.dto.tax_prediction_dto import TaxPredictionDTO
from src.datamodel.entities.cost_model import CostModel
from src.datamodel.enum.e_contribution_relief import EContributionRelief
from src.datamodel.enum.e_cost_recipient import ECostRecipient
from src.datamodel.enum.e_value_format import EValueFormat


def calculate_taxes(employee: EmployeeDTO) -> TaxPredictionDTO:
    costs_for_employer: list[CostModel] = [
        *calculate_tfr(employee),
        *calculate_inps_contributions_for_employer(employee),
        *calculate_inail_for_employer(employee),
    ]
    costs_for_employee: list[CostModel] = [
        *calculate_inps_contributions_for_employee(employee),
        *calculate_irpef_for_employee(employee),
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


def calculate_tfr(employee: EmployeeDTO) -> list[CostModel]:
    value: float = employee.ral / 13.5

    return [CostModel(
        name="TFR",
        description="Il TFR è il trattamento di fine rapporto, corrisponde a circa un mese di stipendio lordo, e viene accantonato gradualmente dal datore di lavoro.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )]


def calculate_inps_contributions_for_employee(employee: EmployeeDTO) -> list[CostModel]:
    value: float = employee.ral * 0.0919

    return [
        CostModel(
            name="INPS",
            description="L'INPS è l'Istituto Nazionale della Previdenza Sociale, che si occupa della previdenza e dell'assistenza sociale in Italia.",
            value=value,
            value_format=EValueFormat.PERCENT,
            recipient=ECostRecipient.EMPLOYER,
        ),
    ]


def calculate_inps_contributions_for_employer(employee: EmployeeDTO) -> list[CostModel]:
    costs: list[CostModel] = []

    value: float = employee.ral * 0.281

    costs.append(
        CostModel(
            name="INPS",
            description="L'INPS è l'Istituto Nazionale della Previdenza Sociale, che si occupa della previdenza e dell'assistenza sociale in Italia.",
            value=value,
            value_format=EValueFormat.PERCENT,
            recipient=ECostRecipient.EMPLOYER,
        ),
    )

    if employee.contribution_relief == EContributionRelief.UNDER_30:  # https://www.anpal.gov.it/documents/552016/586426/Naz-25-Incentivo-strutturale-giovani.pdf/53fb682b-14df-b17f-52ea-c22142cf5584?t=1585229083122
        reduction_value: float = min(value * 0.5, 3000)
        reduction: CostModel = CostModel(
            name="Riduzione contributi INPS",
            description="Riduzione contributiva per i lavoratori under 30.",
            value=-reduction_value,
            value_format=EValueFormat.PERCENT,
            recipient=ECostRecipient.EMPLOYER,
        )

        costs.append(reduction)
    elif employee.contribution_relief == EContributionRelief.OVER_50:  # https://business.infojobs.it/incentivi-alloccupazione-le-agevolazioni-per-gli-over-50.html#:~:text=Sgravi%20contributivi%20del%2050%25%20per,disoccupati%20da%20almeno%2012%20mesi.
        reduction_value: float = min(value * 0.5, 6000)
        reduction: CostModel = CostModel(
            name="Riduzione contributi INPS",
            description="Riduzione contributiva per i lavoratori over 50.",
            value=-reduction_value,
            value_format=EValueFormat.PERCENT,
            recipient=ECostRecipient.EMPLOYER,
        )

        costs.append(reduction)
    elif employee.contribution_relief == EContributionRelief.WOMEN:  # https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2023.06.esonero-per-assunzioni-di-donne-lavoratrici-nel-2023-le-istruzioni.html#:~:text=La%20legge%20di%20bilancio%202021,2023%20ha%20confermato%20l'esonero
        reduction_value: float = min(value * 0.5, 8000)
        reduction: CostModel = CostModel(
            name="Riduzione contributi INPS",
            description="Riduzione contributiva per le donne lavoratrici.",
            value=-reduction_value,
            value_format=EValueFormat.PERCENT,
            recipient=ECostRecipient.EMPLOYER,
        )

        costs.append(reduction)

    return costs


def calculate_irpef_for_employee(employee: EmployeeDTO) -> list[CostModel]:
    aliquote = [
        (28000, 0.23),
        (50000, 0.35),
        (float('inf'), 0.43)
    ]

    total = 0.0
    ral = employee.ral - calculate_inps_contributions_for_employee(employee)[0].value

    for chunck, aliquota in aliquote:
        if ral > chunck:
            total += chunck * aliquota
            ral -= chunck
        else:
            total += ral * aliquota
            break

    return [CostModel(
        name="IRPEF",
        description="L'IRPEF è l'imposta sul reddito delle persone fisiche, è calcolata in base al reddito complessivo del contribuente.",
        value=total,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYEE,
    )]


def calculate_inail_for_employer(employee: EmployeeDTO) -> list[CostModel]:
    value: float = employee.ral * 0.005

    return [CostModel(
        name="INAIL",
        description="L'INAIL è l'Istituto Nazionale per l'Assicurazione contro gli Infortuni sul Lavoro, che si occupa della tutela degli infortuni sul lavoro e delle malattie professionali.",
        value=value,
        value_format=EValueFormat.PERCENT,
        recipient=ECostRecipient.EMPLOYER,
    )]
