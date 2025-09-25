# Meemoo SIP Validator

> WARNING: This library is not yet finished.
> The [SIP specification](https://developer.meemoo.be/docs/diginstroom/sip/) must always be seen as the source of truth.
> Some messages produced by the validator may to be clear and user friendly.

Library to validate meemoo SIP's.

## Usage

You must have a Java runtime available.

Select a SIP version to validate from the [meemoo developer site](https://developer.meemoo.be/docs/diginstroom/sip/).
Run the validator from the CLI.

```
meemoo-sip-validator "2.1" ~/Downloads/uuid-97bb2a97-f991-46f5-a9a4-b474ab30d4de
```

Alternatively, you can run it in Python.

```py
from meemoo_sip_validator.v2_1 import validate

is_valid, report = validate("path/to/sip")
```

Examples of meemoo SIP's are found in [examples repository](https://github.com/viaacode/sip-examples).

## Release

Bump the version in `pyproject.toml` and add a tag `vX.Y.Z` to the commit to start the CI/CD.
The package will be build and uploaded to the interal registry.