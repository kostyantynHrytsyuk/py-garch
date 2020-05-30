import datetime

class Utils:
    @staticmethod
    def check_empty(d, key_name):
        r = d.get(key_name)
        if r:
            return r
        else:
            raise Exception('Empty field' + key_name)

    @staticmethod
    def convert_timestamps_to_date(ts):
        date_stamps = []
        for stamp in Utils.check_empty(ts, 'timestamp'):
            date_stamps.append(datetime.datetime.fromtimestamp(stamp).date())
        return date_stamps
