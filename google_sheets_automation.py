import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Авторизация в Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Открытие таблицы и листа
sheet = client.open("Отчеты_аналитика").sheet1

# Загрузка данных из CSV 
data = pd.read_csv('marketing_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data['ROI'] = (data['Revenue'] - data['Cost']) / data['Cost'] * 100

# Расчет ключевых метрик
metrics = {
    'Дата': datetime.now().strftime("%Y-%m-%d"),
    'Общий бюджет': data['Cost'].sum(),
    'Конверсия': (data['Conversions'].sum() / data['Clicks'].sum() * 100).round(2),
    'Средний ROI': data['ROI'].mean().round(2),
    'Лучшая кампания': data.loc[data['ROI'].idxmax()]['Campaign']
}

# Обновление Google-таблицы
rows = [
    list(metrics.keys()),  
    list(metrics.values()) 
]
sheet.clear()  
sheet.update('A1', rows)

print("Отчет успешно обновлен в Google Sheets!")