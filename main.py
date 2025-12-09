import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SERVICE_ACCOUNT_JSON_PATH = "service_account.json"

def main():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_JSON_PATH,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # テスト用の固定行
    row = ["TEST", 111.1, 222.2]
    body = {"values": [row]}

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="data!A1",
        valueInputOption="RAW",
        body=body
    ).execute()

    print("APPEND_RESULT", result)

if __name__ == "__main__":
    main()
