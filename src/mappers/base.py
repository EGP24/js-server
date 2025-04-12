import dataclasses
import datetime
from typing import Any, Dict, Type, TypeVar

import serpyco_rs

T = TypeVar('T')


class EntityMapper:
    def __init__(self, dataclass_type: Type[T]) -> None:
        self.dataclass_type = dataclass_type
        self.serializer = serpyco_rs.Serializer(
            dataclass_type,
            force_default_for_optional=True,
        )

    def map_to(self, instance: T) -> Dict[str, Any]:
        return self.serializer.dump(instance)

    def map_from(self, data: Dict[str, Any]) -> T:
        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                data[key] = datetime.datetime.isoformat(value)
        return self.serializer.load(data)