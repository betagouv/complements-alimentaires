from viewflow import fsm

from api.exception_handling import ProjectAPIException
from data.models import Declaration

from .declaration_flow_validations import validate_mandatory_fields, validate_number_of_elements

Status = Declaration.DeclarationStatus


class DeclarationFlow:
    status = fsm.State(Status, default=Status.DRAFT)

    def __init__(self, declaration):
        self.declaration = declaration

    @status.setter()
    def _set_declaration_state(self, value):
        self.declaration.status = value

    @status.getter()
    def _get_declaration_state(self):
        return self.declaration.status

    @status.transition(source=Status.DRAFT, target=Status.AWAITING_INSTRUCTION)
    def submit_for_instruction(self):
        self.ensure_validators([validate_number_of_elements, validate_mandatory_fields])

    @status.transition(source=Status.AWAITING_INSTRUCTION, target=Status.ONGOING_INSTRUCTION)
    def take_instruction(self):
        self.error()

    @status.transition(source=Status.ONGOING_INSTRUCTION, target=Status.OBSERVATION)
    def observe_no_visa(self):
        self.error()

    @status.transition(source=Status.OBSERVATION, target=Status.ABANDONED)
    def abandon(self):
        self.error()

    @status.transition(source=Status.ONGOING_INSTRUCTION, target=Status.AUTHORIZED)
    def authorize(self):
        self.error()

    def ensure_validators(self, validators):
        field_errors = []
        non_field_errors = []
        for validator in validators:
            (v_field_errors, v_non_field_errors) = validator(self.declaration)
            field_errors += v_field_errors
            non_field_errors += v_non_field_errors
        if len(field_errors) or len(non_field_errors):
            raise ProjectAPIException(field_errors=field_errors, non_field_errors=non_field_errors)
