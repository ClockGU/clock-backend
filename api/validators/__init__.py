# Dictonary to save internal String identifier

from .student_employee import StudentEmployeeValidator

VALIDATOR_CLASSES_CHOICES = {
    "studEmp": "Studentische Hilfskraft"
}

VALIDATOR_CLASSES = {
    "studEmp": StudentEmployeeValidator
}
