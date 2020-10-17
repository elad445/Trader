import yfinance as yf
import os


class StoreKeeper:
    """
    Stores and fetches data about stocks from yfinance library in files stores in local folder.
    """

    ROOT_FOLDER = 'Store Keepers'
    store_keeper_index = 0

    def __init__(self):
        """
        - Creates local folder
        - Creates meta-data file
        """
        pass

    def _download(self, ticker):
        """
        Stores data on tickers via yfinance library
        """

        PATH = os.getcwd() + os.path.sep
        folder_name = ticker

        name = StoreKeeper.ROOT_FOLDER + str(StoreKeeper.store_keeper_index)
        StoreKeeper.store_keeper_index += 1  # increase folder index for next folder
        os.mkdir(PATH + folder_name)

        for ticker in self.tickers:
            file_name = folder_name + ticker

            # get data from yfinance
            data = yf.download(ticker)

            # store data into file
            with open(file_name, 'w') as data_file:
                data_file.write(data.to_string())

    def get_dictionary_keys(self, file):
        """
        gets dictionary keys from the first row of the data file
        """

        line_list = []
        line = next(file)
        while line:
            line = line.strip()
            string = ''
            for char in line:
                if char == ' ':
                    break
                string += char
                line = line[1:]
            line_list.append(string)

        return line_list

    def _get_data(self, tickers):
        """
        Retrieves data from existing files / newly created with given ticker data combination.
        """

        data = {}

        # open file
        with open(file, 'r') as data_file:

            # initialize keys for dictionary
            data_keys = self.get_dictionary_keys(data_file)
            # data_keys = [next(data_file).strip()] + data_keys
            print('data keys:', data_keys)  # log print

            for key in data_keys:
                data[key] = {}

            next(data_file)

            for line in data_file:  # first two lines are titles

                line_list = line.split(sep='  ')  # list the line into an array

                # insert line numbers into respective slots in the dictionary
                for index in range(len(data_keys)):
                    print('data_keys[index]:', data_keys[index])  # log print
                    print('line_list[0].strip():', line_list[0].strip())  # log print
                    print('line_list[index].strip():', line_list[index].strip())  # log print
                    print('data[data_keys[index]][line_list[0].strip()]:', data[data_keys[index]][line_list[0].strip()])  # log print
                    data[data_keys[index]][line_list[0].strip()] = float(line_list[index + 1].strip())

        return data

    def _update_files(self, files):
        """
        updates all --files to current time
        """
        pass
