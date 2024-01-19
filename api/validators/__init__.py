# Dictonary to save internal String identifier

from .student_employee import StudentEmployeeValidator

VALIDATOR_CLASS_NAMES = (
    ("studEmp", "Studentische Hilfskraft"),
    ("regEmp", "Regulär*er Angestelt*er"),
    ("civilSer", "Beamt*in")
)

VALIDATOR_CLASSES = {
    "studEmp": StudentEmployeeValidator
}
