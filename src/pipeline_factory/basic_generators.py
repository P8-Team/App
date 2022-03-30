import csv
import io
import json


def json_generator(generator):
    for item in generator:
        yield json.dumps(item)


def output_to_console_generator(generator):
    for item in generator:
        print(item)
        yield item


def output_to_file_generator(generator, file_path, mode='a', encoding='utf-8', newline='\n'):
    with open(file_path, mode, encoding=encoding, newline=newline) as f:
        for item in generator:
            f.write(item)
            f.write(newline)
            yield item


def csv_row_generator(generator, delimiter=';'):
    for item in generator:
        output = io.StringIO()
        csv.writer(output, delimiter=delimiter).writerow(item)
        yield output.getvalue()
