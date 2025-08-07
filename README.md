# Meemoo SIP Validator

Library to validate meemoo SIP's.

## Usage

You must have a Java runtime available.
Select a SIP version to validate from the [meemoo developer site](https://developer.meemoo.be/docs/diginstroom/sip/).

```py
from meemoo_sip_validator.v2_1 import validate

is_valid, report = validate("path/to/sip")
```

Examples of meemoo SIP's are found in [this repository](https://github.com/viaacode/sip-examples).