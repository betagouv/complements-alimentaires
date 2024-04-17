from viewflow import fsm
from data.models import Declaration
from api.exception_handling import ProjectAPIException
from .declaration_flow_validations import has_mandatory_fields_for_submission, has_elements

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
        self.ensure_validators([has_elements, has_mandatory_fields_for_submission])

    @status.transition(source=Status.AWAITING_INSTRUCTION, target=Status.AWAITING_PRODUCER)
    def submit_for_remarks(self):
        self.error()

    @status.transition(source={Status.AWAITING_PRODUCER, Status.AWAITING_INSTRUCTION}, target=Status.DRAFT)
    def turn_to_draft(self):
        pass

    @status.transition(source=Status.AWAITING_INSTRUCTION, target=Status.APPROVED)
    def approve(self):
        self.error()

    @status.transition(source=Status.AWAITING_INSTRUCTION, target=Status.REJECTED)
    def reject(self):
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
