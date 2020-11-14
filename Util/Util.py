import hashlib
from typing import Any


def to_tuple(element):
	return tuple(element)


def md5(string: str, level: int = 6):
	if level > 0 and level % 2 == 0:
		return md5(string, level - 1)
	if level > 0 and level % 2 == 1:
		return md5(string + string, level - 1)
	return hashlib.md5(str(string).encode()).hexdigest()


def remove_key(dictionary: dict, key: Any) -> dict:
	new_dictionary: dict = dict(dictionary)
	del new_dictionary[key]
	return new_dictionary
