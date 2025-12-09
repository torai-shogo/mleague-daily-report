import os
import datetime as dt
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# GitHub Actions の Secrets から受け取る
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SERVICE_ACCOUNT_JSON_PATH = "service_account.json"

# --- 仮想チーム定義（ここはあなたのチーム構成） ---
TEAMS = {
    "Team_A": ["醍醐大", "鈴木優", "鈴木たろう", "鈴木大介", "内川幸太郎", "中田花奈"],
    "Team_B": ["仲林圭", "白鳥翔", "佐々木寿人", "伊達朱里紗", "竹内元太", "黒沢咲"]
}
TEAM_NAMES = ["Team_A", "Team_B"]  # 列順固定用


# --- ① 前日の成績を取る（まずは空の処理） ---
def fetch_daily_player_points(target_date):
    """
    本来はスクレイピングで {選手名: 当日ポイント} を返す。
    まずは動作テストのために、すべて 0.0 にする。
    """
    return {}  # TODO: あとで実装する


# --- ② チームポイント集計 ---
def calc_team_points(daily_player_points):
    team_points = {}
    for team, members in TEAMS.items():
        total = 0.0
        for p in members:
            total += daily_player_points.get(p, 0.0)
        team_points[team] = total
    return team_points


# --- ③ Google Sheets の data シートに 1 行追加 ---
def append_to_sheet(date_str, team_points):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_JSON_PATH,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # [date, Team_A, Team_B] の形で出力
    row = [date_str] + [team_points.get(name, 0.0) for name in TEAM_NAMES]
    body = {"values": [row]}

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="data!A1",
        valueInputOption="RAW",
        body=body
    ).execute()


# --- メイン処理 ---
def main():
    # JST で前日の日付を計算
    today_jst = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    target_date = (today_jst - dt.timedelta(days=1)).date()
    date_str = target_date.strfti
