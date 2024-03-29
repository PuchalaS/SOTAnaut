from __future__ import annotations

import re
from typing import List


class LLMParser:
    @staticmethod
    def parse_csv_output(output: str, max_entries: int = 10) -> list[str]:
        """Parses the LLM output assumed to be in a CSV format. Extracts entries from a CSV list,
        handling both formatted and plain list outputs.

        Args:
            output (str): The string output from the LLM.
            max_entries (int): Maximum number of entries to return.

        Returns:
            List[str]: A list of parsed entries.

        Raises:
            ValueError: If the output format is not as expected or if no valid data is found.
        """
        if not output:
            return []

        # Attempt to extract a CSV list from a formatted output
        start_index = output.find(":") + 1 if ":" in output else 0
        end_index = output.rfind(".", 0, output.rfind(",")) if "," in output else len(output)
        csv_part = output[start_index:end_index].strip()

        if not csv_part and "," not in output:
            raise ValueError(
                "Output does not contain a CSV format or is not in the expected format."
            )

        if entries := [entry.strip() for entry in csv_part.split(",") if entry.strip()]:
            return entries[:max_entries]
        else:
            raise ValueError("No valid entries found in the output.")

    @staticmethod
    def parse_enumerated_output(output: str) -> list[str]:
        """Parses the LLM output assumed to be in an enumerated format. Extracts entries from a
        list presented with numbers.

        Args:
            output (str): The string output from the LLM.

        Returns:
            List[str]: A list of parsed entries.

        Raises:
            ValueError: If no valid enumerated data is found.
        """
        if not output:
            return []

        # Regular expression to identify enumerated list items
        pattern = r"\d+[.)] +(.+?)(?=\s*\d+[.)]|\s*$)"
        matches = re.findall(pattern, output, re.DOTALL)

        if not matches:
            raise ValueError("No valid enumerated entries found in the output.")
        cleaned_list = LLMParser.clean_list(matches)
        return cleaned_list

    @staticmethod
    def clean_list(output: list[str]) -> list[str]:
        """Cleans and splits an enumerated output list.

        Args:
            output (List[str]): The output list containing enumerated items.

        Returns:
            List[str]: A list of cleaned and individual enumerated items.

        Raises:
            ValueError: If the output list is empty or not in the expected format.
        """
        if not output or not isinstance(output, list):
            raise ValueError("Output is not a valid list.")

        return [re.sub(r"^\d+[.)]\s*", "", item).strip() for item in output]
