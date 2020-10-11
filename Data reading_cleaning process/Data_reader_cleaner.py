import pandas as pd
import re


class Cleaner():

    """
    class: Reads file, cleans and return data in pandas Dataframe
    instance variable 1: data_path -> the path or name of importing data
    staticmethod 1: clean_from_symbols -> cleans each column of data from unnecessary symbols
    method 1: reading_data -> reads data row by row and returns data in the pandas dataframe
    method 2: cleaning_data -> cleans data through column by column through staticmethod(clean_from_symbols). Returns cleaned pandas DataFrame
    """

    def __init__(self, data_path):
        self.__data_path = data_path

    @staticmethod
    def clean_from_symbols(column, list_of_cleaned_values):

        """
        Function for cleaning values of column from symbols in dataframe
        :param column: column of pandas dataFrame
        :param list_of_cleaned_values: list type variable for keeping cleand values
        :return: list_of_cleaned_values
        """

        symbols = [',', '-', '.', ' ', ';', ':', '!', "*"]

        for value in column:
            value = ''.join(i for i in value if i not in symbols)
            if value.isnumeric():
                list_of_cleaned_values.append(int(value))
            else:
                list_of_cleaned_values.append(value)

        return list_of_cleaned_values

    def reading_data(self):
        column_list = []
        with open(self.__data_path, 'r') as out:
            reader = out.readlines()
            for row in reader:
                row = re.split('\s+', row)
                column_list.append(row)
        pandas_dataframe = pd.DataFrame(column_list)

        return pandas_dataframe

    def cleaning_data(self):
        data = self.reading_data()

        for column in data.columns:
            list_of_cleaned_values = []
            Cleaner.clean_from_symbols(data[column], list_of_cleaned_values)
            data[column] = list_of_cleaned_values

        return data
