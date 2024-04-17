from typing import Any

from msgspec.json import Decoder, Encoder

decode = Decoder(dict[str, Any]).decode
encode = Encoder().encode
