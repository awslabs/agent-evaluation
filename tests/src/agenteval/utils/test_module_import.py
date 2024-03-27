from src.agenteval.utils import imports
import pytest


def test_import_class(mocker):

    mock_import_module = mocker.patch("src.agenteval.utils.imports.import_module")

    test_class = imports.import_class("path.to.module.TestClass")

    mock_import_module.assert_called_once_with("path.to.module")
    assert test_class == mock_import_module.return_value.TestClass


def test_validate_subclass():

    class Parent:
        pass

    class Child(Parent):
        pass

    result = imports.validate_subclass(Child, Parent)

    assert result is None


def test_validate_subclass_error():

    class Parent:
        pass

    class Child:
        pass

    with pytest.raises(TypeError):
        imports.validate_subclass(Child, Parent)
