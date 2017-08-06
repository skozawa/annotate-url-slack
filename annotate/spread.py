import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from annotate.config import config


class Gspread(object):
    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            config.GSPREAD_KEY_JSON,
            [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        self.client = gspread.authorize(credentials)
        today = datetime.date.today()
        self.year = today.year
        self.month = today.month
        self._current_spreadsheet = None
        self._current_worksheet = None
        self.columns = ['URL', 'Time', 'Title', 'Annotator'] + config.METRICS
        
    @property
    def current_spreadsheet(self):
        if self._current_spreadsheet is None:
            name = 'annotate-quality-%04d%02d' % (self.year, self.month)
            self._current_spreadsheet = self.open_or_create_spreadsheet(name)
        return self._current_spreadsheet
        
    def open_or_create_spreadsheet(self, name):
        try:
            sheet = self.client.open(name)
        except Exception:
            sheet = self.client.create(name)
            self.initialize_sheet(sheet)
        return sheet

    def initialize_sheet(self, sheet):
        current_worksheets = sheet.worksheets()
        for ws_index in range(12):
            ws = sheet.add_worksheet(title='%02d' % (ws_index + 1), rows=1, cols=len(self.columns))
            for (i, value) in enumerate(columns):
                ws.update_cell(1, i+1, value)
        for worksheet in current_worksheets:
            sheet.del_worksheet(worksheet)

    @property
    def current_worksheet(self):
        if self._current_worksheet is None:
            self._current_worksheet = self.current_spreadsheet.get_worksheet(self.month - 1)
        return self._current_worksheet

    def find_data_by_url(self, url):
        try:
            cell = self.current_worksheet.find(url)
            values = self.current_worksheet.row_values(cell.row)
            return dict(zip(self.columns, values))
        except Exception:
            return {}

    def add_url(self, url, time, title, annotator):
        self.current_worksheet.append_row([url, time, title, annotator])

