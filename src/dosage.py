class DosageError(Exception):
    """Raised when a calculated dosage is outside the safe range."""
    pass


def calc_dosage(weight_kg, mg_per_kg, max_safe_mg):
    """
    Calculate drug dosage based on patient weight.
    Raises DosageError if the result exceeds the max safe dosage.
    """
    if weight_kg <= 0:
        raise ValueError("Patient weight must be positive")

    dosage = weight_kg * mg_per_kg

    if dosage > max_safe_mg:
        raise DosageError(
            f"Calculated dosage {dosage}mg exceeds max safe dosage {max_safe_mg}mg"
        )

    return dosage