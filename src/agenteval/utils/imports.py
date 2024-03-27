from importlib import import_module


def import_class(module_path: str) -> type:
    name, class_name = module_path.rsplit(".", 1)

    return getattr(import_module(name), class_name)
