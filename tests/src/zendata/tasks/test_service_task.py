import pytest
from typing import Any, Type
from zendata.tasks.service import (
    BaserService,
)  # Ajuste ce chemin selon la structure de ton projet


def test_good_service_runs_and_sets_output_data():
    class GoodService(BaserService):
        input: Type[str] = str
        output: Type[int] = int

        def apply(self) -> int:
            # input_data is provided via the field
            return len(self.input_data)

    # correct input_data type
    svc = GoodService(input_data="hello")
    result = svc.run()
    assert result == 5
    # output_data must be set on the instance
    assert svc.output_data == 5
    assert isinstance(svc.output_data, int)


def test_invalid_input_data_type_raises_type_error():
    class StringToIntService(BaserService):
        input: Type[str] = str
        output: Type[int] = int

        def apply(self) -> int:
            return len(self.input_data)

    # wrong type for input_data → TypeError in model_validator
    with pytest.raises(TypeError, match=r"does not match expected input type"):
        StringToIntService(input_data=123).run()


def test_run_raises_when_apply_returns_wrong_type():
    class BadOutputService(BaserService):
        input: Type[str] = str
        output: Type[int] = int

        def apply(self) -> Any:
            # deliberately return a wrong type (float)
            return 3.14

    svc = BadOutputService(input_data="abc")
    # run() should raise TypeError because 3.14 is not an int
    with pytest.raises(TypeError, match=r"does not match expected output type"):
        svc.run()
