from src.agenteval.utils import imports
import pytest


def test_import_class(mocker):
    mock_import_module = mocker.patch("src.agenteval.utils.imports.import_module")
    mock_validate_subclass = mocker.patch(
        "src.agenteval.utils.imports._validate_subclass"
    )

    imports.import_class("path.to.module_hook.TestHook", object)

    mock_import_module.assert_called_once_with("path.to.module_hook")
    mock_validate_subclass.assert_called_once_with(
        mock_import_module.return_value.TestHook, object
    )


def test_validate_subclass():
    class Parent:
        pass

    class Child(Parent):
        pass

    result = imports._validate_subclass(Child, Parent)

    assert result is None


def test_validate_subclass_error():
    class Parent:
        pass

    class Child:
        pass

    with pytest.raises(TypeError):
        imports._validate_subclass(Child, Parent)
