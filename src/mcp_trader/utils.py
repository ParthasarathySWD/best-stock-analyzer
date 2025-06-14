class DataUtils:
    @staticmethod
    def convert_to_rupees(amount: float) -> str:
        """
        Converts a float amount to a string formatted in Indian Rupees (INR).
        
        Args:
            amount (float): The amount to be converted.
        
        Returns:
            str: The formatted amount in INR without decimal places.
        """
        return f"{int(amount):,}"