import datetime
import sys

class ics_formatter():
    def __init__(self):
        start_datetime = datetime.datetime.now()
        self.input_file_path = "input.txt"
        self.output_file_path = "output.ics"
        self.codecs = 'utf-8'
        self.weekday_dictionry = {
            "月曜日" : "MO",
            "火曜日" : "TU",
            "水曜日" : "WE",
            "木曜日" : "TH",
            "金曜日" : "FR"
            }
        self.weekday_dictionry_integer = {
            "月曜日": 0,
            "火曜日": 1,
            "水曜日": 2,
            "木曜日": 3,
            "金曜日": 4
            }
        self.timeschedule_dictionary = {
            1: datetime.datetime(2021, 4, 5, 8, 50, 00),
            2: datetime.datetime(2021, 4, 5, 10, 30, 00),
            3: datetime.datetime(2021, 4, 5, 13, 00, 00),
            4: datetime.datetime(2021, 4, 5, 14, 40, 00),
            5: datetime.datetime(2021, 4, 5, 16, 15, 00),
            6: datetime.datetime(2021, 4, 5, 17, 55, 00),
            7: datetime.datetime(2021, 4, 5, 19, 35, 00)
            }
        self.input_text_file()
        self.generate_ics()
        self.export_ics_file()
        self.show_elapsed_time(start_datetime, datetime.datetime.now())

    def input_text_file(self):
        # print("> [開講曜日]/[時限]/[講義名]")
        with open(self.input_file_path, encoding=self.codecs, mode='r') as f:
            self.input_text_container = f.readlines()
        print(f"[I N]>>> {self.input_file_path}")

    def export_ics_file(self):
        with open(self.output_file_path, encoding=self.codecs, mode='w') as f:
            f.write(self.lump_ics)
        print(f"[OUT]>>> {self.output_file_path}")

    def generate_ics(self):
        self.lump_ics = "BEGIN:VCALENDAR\n"
        for line in self.input_text_container:
            plan = line.split("/")
            course_name = plan[2].replace('\n', '')
            timedelta_days = self.weekday_dictionry_integer[plan[0]] - self.timeschedule_dictionary[int(plan[1])].weekday()
            initial_start_date = self.timeschedule_dictionary[int(plan[1])]+datetime.timedelta(days=timedelta_days)
            initial_end_date = self.timeschedule_dictionary[int(plan[1])]+datetime.timedelta(days=timedelta_days, hours=1, minutes=30)
            weekday_integer = self.weekday_dictionry[plan[0]]
            self.lump_ics += self.formatting_ics(course_name, initial_start_date, initial_end_date, weekday_integer)
        self.lump_ics += "END:VCALENDAR"
      
    def formatting_ics(self, course_name, initial_start_date, initial_end_date, weekday_integer):
        text_formated_ics = \
            f"BEGIN:VEVENT\n" + \
            f"DTSTART;TZID=Asia/Tokyo:{initial_start_date.strftime('%Y%m%dT%H%M%S')}\n" + \
            f"DTEND;TZID=Asia/Tokyo:{initial_end_date.strftime('%Y%m%dT%H%M%S')}\n" + \
            f"SUMMARY:{course_name}\n" + \
            f"RRULE:FREQ=WEEKLY;BYDAY={weekday_integer};COUNT=16\n" + \
            f"END:VEVENT\n"
        return text_formated_ics

    def show_elapsed_time(self, start_datetime, end_datetime):
        elapsed_tuples = divmod((end_datetime - start_datetime).total_seconds(), 60)
        minutes = str(int(elapsed_tuples[0]))
        seconds = str(elapsed_tuples[1]).split('.')[0]
        microseconds = str(elapsed_tuples[1]).split('.')[1]
        print(f"> {minutes.zfill(2)}:{seconds.zfill(2)}.{microseconds}")


if __name__ == '__main__':
    ics_formatter()
