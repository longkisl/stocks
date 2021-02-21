## https://www.cnblogs.com/ysging/p/13215072.html
'''
需求：

使用tushare包获取某股票的历史行情数据。
输出该股票所有收盘比开盘上涨3%以上的日期。
输出该股票所有开盘比前日收盘跌幅超过2%的日期。
'''

import tushare as ts
import pandas as pd

# ts.set_token(3d369e6b9ec6f8dc82a475b0cd451a9187abe65f5f035b5bd0d9e18a)

pro=ts.pro_api('3d369e6b9ec6f8dc82a475b0cd451a9187abe65f5f035b5bd0d9e18a')


#1-需求一：使用tushare包获取某股票的历史行情数据。

# 获取行情
df = ts.get_k_data(code="600519",start='2000-01-01')
# 保存到本地
df.to_csv('./maotai.csv')
# 读取本地csv文件数据
df = pd.read_csv('./maotai.csv')
# 删除 Unnamed: 0 这一列，将 date 列转为时间类型，并设置为 index 列
df.drop(labels='Unnamed: 0',axis=1,inplace=True)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date',inplace=True)
print(df.info())    # 查看整个数据集合中各个数据类型
print(df)

#2-需求二：输出该股票所有收盘比开盘上涨3%以上的日期。
# (收盘-开盘)/开盘 > 0.03  返回值为 boolean 值，将 boolean 作为行索引来使用
# 在分析的过程中如果产生了boolean值则下一步马上将布尔值作为源数据的行索引
# 如果布尔值作为df的行索引，则可以取出true对应的行数据，忽略false对应的行数据
# print((df['close'] - df['open'])/df['open'] > 0.03)   # 获取了True对应的行数据（满足需求的行数据）

print(df.loc[(df['close'] - df['open']) / df['open'] > 0.03].index)


#3-需求三：输出该股票所有开盘比前日收盘跌幅超过2%的日期。
# (今日开盘价-昨日收盘价)/昨日收盘价 < -0.02
# print(df['close'].shift(1))    # 使 df['close'] 列整体下移一位
print(df.loc[(df['open'] - df['close'].shift(1)) / df['close'].shift(1) < -0.02].index)


#4-需求四：假如我从2010年1月1日开始，每月第一个交易日买入1手股票，每年最后一个交易日卖出所有股票，到今天为止，我的收益如何？
'''
- 分析：
　　- 时间节点：2010-2020
　　- 一手股票：100支股票
　　- 买：
　　　　- 一个完整的年需要买入1200支股票
　　- 卖：
　　　　- 一个完整的年需要卖出1200支股票
　　-买卖股票的单价：
　　　　- 开盘价
'''

# 买股票：找每个月的第一个交易日对应的行数据（捕获到开盘价）==》每月的第一行数据
# 根据月份从原始数据中提取指定的数据
# 每月第一个交易日对应的行数据

new_df = df['2010-01-01':]
mairu = new_df.resample('M').first()['open'].sum() * 100  # 数据的重新取样，取出每月的第一支股票
maichu = new_df.resample('A').last()['open'][:-1].sum() * 1200  # 取出每年最后一个交易日的收盘价
yu = new_df['close'][-1] * 600  # 剩余股票价值

# print(new_df.resample('M').first()['open']*100)
# print(new_df.resample('A').last()['close'][:-1] * 100)

print(maichu - mairu + yu)