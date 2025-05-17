import pytest
from pydantic import ValidationError
from zendata.tasks.base import BaseTask, TaskStatus


def test_base_task_creation():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    assert task.name == "Test Task"
    assert task.status == TaskStatus.STARTED
    assert 0.0 <= task.percentage <= 1.0
    assert task.input is str
    assert task.output is dict
    assert task.error is None
    assert isinstance(task.id, str)
    assert isinstance(task.created_at, int)
    assert isinstance(task.updated_at, int)
    assert task.extras == {}


def test_percentage_bounds():
    with pytest.raises(ValidationError):
        BaseTask(percentage=-0.1)
    with pytest.raises(ValidationError):
        BaseTask(percentage=1.1)


def test_input_output_type_validation():
    # input/output must be a type or None
    with pytest.raises(ValidationError):
        BaseTask(name="test", input="not_a_type", output=str)
    with pytest.raises(TypeError):
        BaseTask(name="test", intput=str, output=123)


def test_updated_at_is_set_and_refreshed():
    task1 = BaseTask(name="test", input=str, output=str)
    old_updated = task1.updated_at

    # simulate a small delay then re-validate
    import time

    time.sleep(1)
    task2 = BaseTask.model_validate(task1.model_dump())
    assert task2.updated_at > old_updated


def test_serialization_of_input_output():
    task = BaseTask(input=str, output=dict)
    dumped = task.model_dump()
    assert dumped["input"] == "builtins.str"
    assert dumped["output"] == "builtins.dict"


def test_error_field():
    task = BaseTask(error="Something went wrong")
    assert task.error == "Something went wrong"
