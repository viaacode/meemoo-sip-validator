from py_commons_ip.sip_validator import EARKSIPValidator
from pathlib import Path

class MeemooSIPValidator:
    def validate(self, unzipped_path: Path) -> tuple[bool, str]: 
        """Validate an unzipped SIP making use of the commons-IP validator

        Args:
            The folder pointing to an unzipped SIP.
            
        Returns:
            tuple: A tuple containing:
              - bool: Whether the SIP is valid.
              - str: The full JSON report in string format.

        """
        validator = EARKSIPValidator()

        return validator.validate(unzipped_path)
    