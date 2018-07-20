import argparse
import os
from os import path

from core_data_modules.traced_data.io import TracedDataJsonIO, TracedDataCodaIO, TracedDataCodingCSVIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a survey and exports to Coda or a Coding for manual "
                                                 "verification and coding")
    parser.add_argument("user", help="User launching this program, for use by TracedData Metadata", nargs=1)
    parser.add_argument("json_input_path", metavar="json-input-path",
                        help="Path to input file, containing a list of serialized TracedData objects as JSON", nargs=1)
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write processed TracedData messages to", nargs=1)
    parser.add_argument("coding_output_mode", metavar="coding-output-mode",
                        help="File format to export data to for coding."
                             "Accepted values are 'coda' or 'coding-csv'", nargs=1, choices=["coda", "coding-csv"])
    parser.add_argument("coded_output_path", metavar="coding-output-path",
                        help="Directory to write coding files to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    json_input_path = args.json_input_path[0]
    json_output_path = args.json_output_path[0]
    coding_mode = args.coding_output_mode[0]
    coded_output_path = args.coded_output_path[0]

    # Load data from JSON file
    with open(json_input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # FIXME: Clean survey data

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    # Output for manual verification + coding
    if coding_mode == "coda":
        # Write Coda output
        if not os.path.exists(coded_output_path):
            os.makedirs(coded_output_path)

        # FIXME: Set the <example-arguments> to export a particular column e.g. "age", "age_clean", "Age"
        with open(path.join(coded_output_path, "<output-file>.csv"), "w") as f:
            TracedDataCodaIO.export_traced_data_iterable_to_coda_with_scheme(
                data, "<key-of-raw>", "<key-of-coded>", "<name-in-Coda>", f)

        # FIXME: Re-use the above code sample to export other columns which need verifying/coding.
    else:
        assert coding_mode == "coding-csv", "coding_mode was not one of 'coda' or 'coding-csv'"

        # Write Coding CSV output
        if not os.path.exists(coded_output_path):
            os.makedirs(coded_output_path)

        # FIXME: Set the <example-arguments> to export a particular column e.g. "age", "age_clean", "Age"
        with open(path.join(coded_output_path, "<output-file>.csv"), "w") as f:
            TracedDataCodingCSVIO.export_traced_data_iterable_to_coding_csv_with_scheme(
                data, "<key-of-raw>", "<key-of-coded>", f)

        # FIXME: Re-use the above code sample to export other columns which need verifying/coding.
