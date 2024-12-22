from src.common.exceptions import ValidationError
from src.common.types import ModelT
from src.infra.unit_of_work import AbstractUnitOfWork


def validate_numeric_value(value: str) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValidationError


def create_model_instance(
    *, uow: AbstractUnitOfWork, model_class: type[ModelT], validated_data: dict
) -> ModelT:
    new_entity = model_class(**validated_data)
    uow.add(new_entity)
    return new_entity


def update_model_instance(
    *, uow: AbstractUnitOfWork, instance: ModelT, validated_data: dict
) -> ModelT:
    for attribute, value in validated_data.items():
        if hasattr(instance, attribute):
            setattr(instance, attribute, value)
    uow.add(instance)
    return instance
