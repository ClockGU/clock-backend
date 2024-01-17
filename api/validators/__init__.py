# Dictonary to save internal String identifier

from .student_employee import StudentEmployeeValidator

VALIDATOR_CLASS_NAMES = (
    ("studEmp", "Studentische Hilfskraft"),
)

VALIDATOR_CLASSES = {
    "studEmp": StudentEmployeeValidator
}
