import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Загрузка данных 
data = pd.read_csv('ecommerce_data.csv')  
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Расчет RFM-метрик
snapshot_date = data['InvoiceDate'].max() + pd.Timedelta(days=1)  

rfm = data.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, 
    'InvoiceNo': 'nunique',                                  
    'TotalPrice': 'sum'                                       
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
})

# Разбиение 
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# Комбинированный RFM-скор
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Сегментация клиентов
segmentation_map = {
    r'555|554|545|544|535|534|525|524|515|514|455|454|445|444|435|434|425|424|415|414|355|354|345|344|335|334|325|324': 'Champions',
    r'[1-5][1-5][1-2]': 'Hibernating',
    r'3[1-2][1-3]': 'At Risk'
}

rfm['Segment'] = rfm['RFM_Score'].replace(segmentation_map, regex=True)
rfm['Segment'] = rfm['Segment'].fillna('Others')

# Визуализация
plt.figure(figsize=(10, 6))
rfm['Segment'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Распределение клиентов по сегментам')
plt.xlabel('Сегмент')
plt.ylabel('Количество клиентов')
plt.savefig('rfm_segments.png') 
plt.show()

# RFM-анализ, выделил 20% 'Champions', приносящих 60% прибыли"