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
        
    @property
    def current_spreadsheet(self):
        if self._current_spreadsheet is None:
            name = 'annotate-%s' % (datetime.datetime.now().strftime('%y%m'))
            self._current_spreadsheet = self.open_or_create_spreadsheet(name)
        return self._current_spreadsheet
        
    def open_or_create_spreadsheet(self, name):
        try:
            sheet = self.client.open(name)
        except Exeception:
            sheet = self.client.create(name)
        return sheet
