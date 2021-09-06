#! /usr/bin/python

import datetime
import json
from json2html import *
import pdfkit


class TestRecorder():
    """ Stores the results of a performed test
    """

    def __init__(self, description="", accuracy=None, precision=None, recall=None, f1=None,
                 date=datetime.datetime.now()):
        """ Inits TestRecorder class.

        :param description: str Phrase that serves to distinguish one test from another
        :param accuracy: float Accuracy value of the model
        :param precision: float Precision value of the model
        :param recall: float Recall value of the model
        :param f1: float F1-Score of the model
        :param date: datetime Time when the test was performed
        """

        self.description = description
        self.accuracy = round(accuracy * 100, 1)
        self.precision = round(precision * 100, 1)
        self.recall = round(recall * 100, 1)
        self.f1 = round(f1 * 100, 1)
        self.date = date.strftime("%m/%d/%Y,\n %H:%M:%S")

        self.json = {
            "description": self.description,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "date": self.date,
        }

    def data_to_json(self, file_name="results"):
        data = None
        try:
            with open("data/{}.json".format(file_name)) as json_file:
                data = json.load(json_file)
        except IOError:
            pass
        if data:
            data['test'].append(self.json)
        else:
            data = {'test': []}
            data['test'].append(self.json)

        with open("data/{}.json".format(file_name), "w", encoding='utf-8') as outfile:
            json.dump(data, outfile)


class CustomReport(object):
    """ Generates a pdf from a json file
    """

    def __init__(self, file_name="results"):
        """ Inits TestRecorder class.

        :param file_name: str Name of the pdf file generated
        """

        self.file_name = file_name

    @staticmethod
    def to_html(json_doc):
        """ Converts a json file into a html str
        """

        return json2html.convert(json=json_doc)

    @staticmethod
    def to_pdf(html_str):
        """ Converts a html str into a PDF
        """

        return pdfkit.from_string(html_str, None)


def main():
    try:
        with open("../notebooks/data/{}.json".format("results")) as json_file:
            data = json.load(json_file)
    except IOError:
        pass

    if data:
        pdf_report = CustomReport()
        with open("pdfs/{}.pdf".format(pdf_report.file_name), "wb") as pdf_fl:
            pdf_fl.write(pdf_report.to_pdf(pdf_report.to_html(json.dumps(data))))
    else:
        print("No data available")


if __name__ == '__main__':
    main()
