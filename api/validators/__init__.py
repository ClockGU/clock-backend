# Dictonary to save internal String identifier

from .student_employee import StudentEmployeeValidator

VALIDATOR_CLASS_NAMES = (
    ("studEmp", "Studentische Hilfskraft"),
    ("regEmp", "Regulär*er Angestelt*er"),
    ("civilSer", "Beamt*in")
)

FTE_WEEKYL_MINUTES = {
    "regEmp": 2400,  # 40h per week
    "civilSer": 2460,  # 41h per week
}
VALIDATOR_CLASSES = {
    "studEmp": StudentEmployeeValidator
}
