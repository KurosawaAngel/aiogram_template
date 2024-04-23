from typing import Any

from msgspec.json import Decoder, Encoder

decode = Decoder(dict[str, Any]).decode
encode_bytes = Encoder().encode


def encode(obj: Any) -> str:
    data: bytes = encode_bytes(obj)
    return data.decode()
