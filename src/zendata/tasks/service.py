from typing import Any, Type, Optional, get_type_hints
from abc import ABC, abstractmethod
from pydantic import validate_call, model_validator, Field
from .base import BaseTask


class BaserService(BaseTask, ABC):
    """
    Base service that enforces:
      - `input` and `output` class attributes must be set to a type
      - the `apply` method’s signature matches those types
      - runtime checks of input/output in `run`
    """

    input_data: Any = Field(..., description="Data to process")
    output_data: Optional[Any] = Field(None, description="Result of processing")

    @abstractmethod
    def apply(self, *args, **kwargs) -> Any:
        """Process the input_data and return the result."""
        ...

    def run(self, *args, **kwargs) -> Any:
        """
        1. Validates that self.input_data is correct type
        2. Calls apply(...)
        3. Validates that the returned output matches self.output
           and stores it in self.output_data
        """
        # apply() is already wrapped by @validate_call, so its parameters
        # are checked against its signature
        if not isinstance(self.input_data, self.input):
            raise TypeError(
                f"{self.input_data!r} does not match expected input type {self.input}"
            )
        result = self.apply(*args, **kwargs)

        if self.output is not None and not isinstance(result, self.output):
            raise TypeError(
                f"{result!r} (type {type(result)}) does not match "
                f"expected output type {self.output}"
            )

        self.output_data = result
        return result
