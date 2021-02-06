from dateparser.date import DateDataParser


class DayCounter:
    MONTHS = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]

    def __init__(self, start_year=2017, year_iterator=False):
        self.month = "JAN"
        self.month_cursor = 0
        self.year = start_year

        self.max_month = "DEC"
        self.max_year = 2020
        self.year_iterator = year_iterator

    @property
    def next_date(self):
        start_date = f"1 {self.month}, {self.year}"

        if not self.year_iterator:
            if self.month_cursor + 1 >= len(self.MONTHS):
                self.month_cursor = 0
                self.year += 1
            else:
                self.month_cursor += 1

            self.month = self.MONTHS[self.month_cursor]
        else:
            self.year += 1

        end_date = f"1 {self.month}, {self.year}"

        return start_date, end_date

    @property
    def next_date_datetime(self):
        start_date, end_date = self.next_date
        ddt = DateDataParser(languages=['en'])
        return ddt.get_date_data(start_date).date_obj, ddt.get_date_data(end_date).date_obj

    def next_date_datetime_num_months(self, months: int):
        start_date, _ = self.next_date_datetime
        for _ in range(months - 1):
            self.next_date_datetime
        _, end_date = self.next_date_datetime
        return start_date, end_date


    @property
    def done(self):
        return self.month == self.max_month and self.year == self.max_year
