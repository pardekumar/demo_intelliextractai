import csv
import io
from typing import Dict, Any, Iterable

def dict_to_csv_stream(data: Dict[str, Any]) -> Iterable[bytes]:
    """
    Converts a dictionary to a CSV stream.
    Yields bytes for StreamingResponse.
    """
    output = io.StringIO()
    writer = None

    # If the dict values are lists of dicts, flatten them
    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        # Assume all lists are of the same length and structure
        for key, rows in data.items():
            if rows and isinstance(rows[0], dict):
                writer = csv.DictWriter(output, fieldnames=rows[0].keys())
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
                break
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    elif isinstance(data, dict):
        writer = csv.DictWriter(output, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    else:
        output.write("Unsupported data format for CSV export.\n")

    yield output.getvalue().encode("utf-8")
    output.close()