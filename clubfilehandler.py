import csv
import re


class ClubFileHandler:
    def __init__(self, filename, fields):
        self.filename = filename.encode('utf-8')
        self.output_file = open(self.filename, "wb")
        self.fields = fields

    def get_csv_writer(self):
        club_writer = csv.DictWriter(self.output_file, fieldnames=self.fields, delimiter=',')
        return club_writer

    def get_csv_reader(self, csvfile):
        club_reader = csv.DictReader(csvfile)
        return club_reader

    def close_file(self):
        self.output_file.close()

    def format_data(self, value):
        value = value.replace("_", " ")
        value = value.encode('utf-8')
        value = re.sub('.*?\((.*?)\)', '', value, re.DOTALL)
        if "/" in value:
            return value[28:]
        else:
            return value

