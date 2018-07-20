import argparse
import os

from core_data_modules.traced_data.io import TracedDataJsonIO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans a list of messages, and outputs to formats "
                                                 "suitable for subsequent analysis")
    parser.add_argument("user", help="User launching this program, for use by TracedData Metadata", nargs=1)
    parser.add_argument("json_input_path", metavar="json-input-path",
                        help="Path to the input JSON file, containing a list of serialized TracedData objects",
                        nargs=1)
    parser.add_argument("json_output_path", metavar="json-output-path",
                        help="Path to a JSON file to write processed TracedData messages to", nargs=1)

    args = parser.parse_args()
    user = args.user[0]
    json_input_path = args.json_input_path[0]
    json_output_path = args.json_output_path[0]

    # Load data from JSON file
    with open(json_input_path, "r") as f:
        data = TracedDataJsonIO.import_json_to_traced_data_iterable(f)

    # FIXME: Clean/filter messages

    # Write json output
    if os.path.dirname(json_output_path) is not "" and not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))
    with open(json_output_path, "w") as f:
        TracedDataJsonIO.export_traced_data_iterable_to_json(data, f, pretty_print=True)

    # FIXME: Output to other formats for analysis, using the TracedData exporters in core_data_modules.traced_data.io
