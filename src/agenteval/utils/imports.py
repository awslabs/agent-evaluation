from importlib import import_module


def import_class(module_path: str) -> type:
    name, class_name = module_path.rsplit(".", 1)

    return getattr(import_module(name), class_name)


def validate_subclass(child_class: type, parent_class: type) -> None:

    if not issubclass(child_class, parent_class):
        raise TypeError(
            f"{child_class.__name__} is not a {parent_class.__name__} subclass"
        )
