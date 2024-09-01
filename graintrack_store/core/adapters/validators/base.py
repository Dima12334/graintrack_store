from typing import List

from pydantic import ValidationError as PydanticValidationError


class BaseValidator:

    def parse_pydantic_validation_error(
        self, exception: PydanticValidationError
    ) -> List[str]:
        errors = []
        for error in exception.errors():
            field = ".".join([str(el) for el in error["loc"]])
            message = error["msg"]
            errors.append(f"{field}: {message}")

        return errors
