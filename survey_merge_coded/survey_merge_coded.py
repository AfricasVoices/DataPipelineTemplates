import argparse
import os
from os import path

from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataCodingCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merges manually cleaned files back into a traced data file.")
    parser.add_argument("user", help="User launching this program, for use by TracedData Metadata")
    parser.add_argument("json_input_path", metavar="json-input-path",
                        help="Path to JSON input file, which contains a list of TracedData objects")
    parser.add_argument("coding_mode", metavar="coding-mode",
                        help="How to interpret the files in the coding-input-directory. "
                             "Accepted values are 'coda' or 'coding-mode'", choices=["coda", "coding-csv"])
    parser.add_argument("coded_input_path", metavar="coded-input-path",
                        help="Directory to read coding files from")
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write merged results to")

    args = parser.parse_args()
    user = args.user
    json_input_path = args.json_input_path
    coding_mode = args.coding_mode
    coded_input_path = args.coded_input_path
    json_output_path = args.json_output_path

    # Load data from JSON file
    with open(json_input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # Merge coded data into the loaded data file
    if coding_mode == "coda":
        # Merge manually coded Coda files into the cleaned dataset
        # FIXME: Set the <example-arguments> to import a particular column e.g. "age", "age_clean", "Age"
        with open(path.join(coded_input_path, "<input-file>.csv"), "r") as f:
            data = list(TracedDataCodaIO.import_coda_to_traced_data_iterable(
                user, data, "<key-of-raw>", "<key-of-coded>", f, True))

        # FIXME: Re-use the above code sample to export other columns which need importing.
    else:
        assert coding_mode == "coding-csv", "coding_mode was not one of 'coda' or 'coding-csv'"

        # Merge manually coded CSV files into the cleaned dataset
        # FIXME: Set the <example-arguments> to import a particular column e.g. "age", "age_clean", "Age"
        with open(path.join(coded_input_path, "<input-file>.csv"), "r") as f:
            data = list(TracedDataCodingCSVIO.import_coding_csv_to_traced_data_iterable(
                user, data, "<key_of_raw_in_data>", "<key_of_coded_in_data>",
                "<key_of_raw_in_f>", "<key_of_coded_in_f>", f, True))

        # FIXME: Re-use the above code sample to export other columns which need importing.

    # Write coded data back out to disk
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)
