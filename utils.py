import datetime


class Utils:
    @staticmethod
    def check_empty(d, key_name):
        r = d.get(key_name)
        if r:
            return r
        else:
            raise KeyError('Empty field' + key_name)

    @staticmethod
    def convert_timestamps_to_date(ts):
        date_stamps = []
        for stamp in Utils.check_empty(ts, 'timestamp'):
            date_stamps.append(datetime.datetime.fromtimestamp(stamp).date())
        return date_stamps

    @staticmethod
    def remove_none_in_two_lists(main, second):
        """
        Function for finding and removing None values in two lists
        :param main: Main list, where None values have to be found
        :param second: Minor lists, where responding values have to be removed
        """
        assert len(main) == len(second), "Lists must be the same length"
        for i in range(len(main)-1, 0, -1):
            if not main[i]:
                second.pop(i)
                main.pop(i)
        return main, second
