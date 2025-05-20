from typing import Optional
import pytest
from pydantic import ValidationError, BaseModel
from zendata.data.tasks.base import BaseTask, TaskStatus

class DummyBaseModel(BaseModel):
    test: Optional[str] = None

def test_base_task_creation():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    assert task.name == "Test Task"
    assert task.status == TaskStatus.STARTED
    assert 0.0 <= task.percentage <= 1.0
    assert isinstance(task.input, BaseModel)
    assert isinstance(task.output, BaseModel)
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
    with pytest.raises(ValidationError):
        BaseTask(name="test", intput=str, output=123)


def test_updated_at_is_set_and_refreshed():
    task1 = BaseTask(name="test", input=DummyBaseModel(), output=DummyBaseModel())
    old_updated = task1.updated_at

    # simulate a small delay then re-validate
    import time

    time.sleep(1)
    task2 = BaseTask.model_validate(task1.model_dump())
    assert task2.updated_at > old_updated



def test_error_field():
    task = BaseTask(error="Something went wrong")
    assert task.error == "Something went wrong"



def test_set_status():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status(status=TaskStatus.COMPLETED.value)
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.COMPLETED.value


def test_set_status_to_created():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_created()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.CREATED.value


def test_set_status_to_started():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_started()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.STARTED.value


def test_set_status_to_in_progress():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_in_progress()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.IN_PROGRESS.value


def test_set_status_to_completed():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_completed()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.COMPLETED.value


def test_set_status_to_failed():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_failed(error="test")
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.FAILED.value
    assert task.error == "test"


def test_set_status_to_retrying():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_retrying()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.RETRYING.value


def test_set_status_to_canceled():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_canceled(error="test")
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.CANCELED.value
    assert task.error == "test"


def test_set_status_to_timeout():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=DummyBaseModel(),
        output=DummyBaseModel(),
    )
    actual_updated_at = task.updated_at
    task.set_status_to_timeout(error="test")
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.TIMEOUT.value
    assert task.error == "test"
