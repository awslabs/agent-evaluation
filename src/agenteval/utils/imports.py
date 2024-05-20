# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from importlib import import_module
from typing import Optional

_ALLOWED_MODULE_NAME_SUFFIX = ["_hook", "_target"]


def import_class(module_path: str, parent_class: Optional[type] = None) -> type:
    """Import a class from a module path and optionally validate
    that it is a subclass of a given parent class.

    Args:
        module_path (str): The full module path to the class, e.g. "my.module.ClassName".
        parent_class (Optional[type]): A parent class to validate the imported class against.

    Returns:
        type

    Raises:
        ValueError: If the module name does not end with one of the allowed suffixes.
        TypeError: If imported class is not a subclass of the provided parent class.
    """

    name, class_name = module_path.rsplit(".", 1)

    # make sure module name starts with one of the allowed suffixes
    _validate_module_name(name.split(".")[-1])

    module = import_module(name)
    cls = getattr(module, class_name)

    if parent_class:
        # make sure the imported class is a subclass
        _validate_subclass(cls, parent_class)

    return cls


def _validate_module_name(name: str):
    if not any(name.endswith(suffix) for suffix in _ALLOWED_MODULE_NAME_SUFFIX):
        raise ValueError(f"Invalid module name: {name}")


def _validate_subclass(child_class: type, parent_class: type):
    if not issubclass(child_class, parent_class):
        raise TypeError(
            f"{child_class.__name__} is not a {parent_class.__name__} subclass"
        )
