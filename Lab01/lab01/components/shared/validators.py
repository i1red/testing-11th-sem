import string
from typing import Final

from lab01.utility.validators import optional, validate_string


UKR_LOWERCASE: Final[str] = "абвгґдеєєжжззииіїйклмнопрстуфхцчшщьюя"
UKR_UPPERCASE: Final[str] = UKR_LOWERCASE.upper()


validate_filename = optional(
    validate_string(
        max_len=5,
        allowed_characters=UKR_LOWERCASE + UKR_UPPERCASE + string.ascii_letters + string.digits
    )
)