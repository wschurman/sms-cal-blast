
import httplib2
import StringIO
import csv

from smscalblast.scripts import utils
from smscalblast.modules.submodules import Person

from smscalblast.modules.submodules.message_generator import CARRIERS

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

FIELD_NAMES = ['timestamp', 'email', 'phone', 'unlimited_texts', 'carrier']


class Spreadsheet:

    def __init__(self, config):
        self.get_config(config)
        self.authenticate_service()

    def get_config(self, config):
        self.DEBUG = config.DEBUG()
        self.keyfile = config.cf("SERVICE_ACCOUNT_KEYFILE")
        self.service_account_name = config.cf("SERVICE_ACCOUNT_NAME")
        self.fileId = config.cf("FILE_ID")

    def authenticate_service(self):
        """
        Authenticate with Google APIs using Google Service Accounts.
        """
        f = open(self.keyfile, "rb")
        key = f.read()
        f.close()

        credentials = SignedJwtAssertionCredentials(
            service_account_name=self.service_account_name,
            private_key=key,
            scope='https://www.googleapis.com/auth/drive.readonly',
        )

        self.http = httplib2.Http()
        self.http = credentials.authorize(self.http)

        self.service = build('drive', 'v2', http=self.http)

    def download_file(self, url):
        """
        Download file from Google using authenticated http connection.
        """
        if not url:
            return

        resp, content = self.service._http.request(url)
        if resp.status == 200:
            # print 'Status: %s' % resp
            return content
        else:
            print 'An error occurred: %s' % resp
            return None

    def make_download_link(self, gfile):
        """
        Extract download link from file specification.
        """
        xstr = gfile.get('exportLinks').get('application/pdf')
        return xstr.replace("pdf", "csv")

    def validate_row(self, row):
        """
        Validate the csv row.
        """
        return (row.get('unlimited_texts') == "yes" and
                row.get('carrier') in CARRIERS)

    def parse_csv(self, csv_str):
        """
        Parse csv_str and return a set of Person objects.
        """
        ret = []
        reader = csv.DictReader(StringIO.StringIO(csv_str),
                                fieldnames=FIELD_NAMES)
        for row in reader:
            if self.validate_row(row):
                p = utils.fix_number(row.get('phone'))
                if not p:
                    continue
                row['phone'] = p
                ret.append(Person(row))

        return ret

    def get_people(self):
        """
        Fetch People from spreadsheet via API call.
        """
        gfile = self.service.files().get(
            fileId=self.fileId
        ).execute(http=self.http)

        file_data = self.download_file(self.make_download_link(gfile))
        data = self.parse_csv(file_data)

        if self.DEBUG:
            for p in data:
                print p

        return data
