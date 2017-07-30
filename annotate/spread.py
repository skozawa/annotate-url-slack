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
        columns = ['URL', 'Time', 'Title', 'Annotator'] + ['Quality', 'Readability', 'Informativeness', 'Style', 'Topic', 'Sentiment']
        for ws_index in range(12):
            ws = sheet.add_worksheet(title='%02d' % (ws_index + 1), rows=1, cols=len(columns))
            for (i, value) in enumerate(columns):
                ws.update_cell(1, i+1, value)
        for worksheet in current_worksheets:
            sheet.del_worksheet(worksheet)

