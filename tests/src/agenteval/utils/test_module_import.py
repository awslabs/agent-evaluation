from src.agenteval.utils import imports


def test_import_class(mocker):

    mock_import_module = mocker.patch("src.agenteval.utils.imports.import_module")

    test_class = imports.import_class("path.to.module.TestClass")

    mock_import_module.assert_called_once_with("path.to.module")
    assert test_class == mock_import_module.return_value.TestClass
