title: Pandas Cheatsheet
date: 2017-06-03 18:41:47
categories:
 - 数据科学
tags:
 - Pandas
 - 效率
 - 工作自动化
 - Cheatsheet

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 Pandas 相关语句。

主要包含：

 - Pandas 中 Series 的一些常见操作和技巧
 - Pandas 中 Dateframe 的一些常见操作和技巧
 - Python 里的可视化技巧
 - Pandas 使用过程中的一些细节

不定期更新。

<!-- more -->

> SQL 是一种面向集合的处理工具 / 语言
> Pandas 是一种面向数组的处理工具

> **而一般处理 pandas 的数据往往以二维表的形式存在。所以，可以类比为更加强大的 SQL 语言。**

而依据 Pandas 的作者之言，牛逼的 Pandas 使用者必须要精通 numpy; 当然，关于 Numpy, 留待之后开一篇文章做笔记好了。

## 0x01 Series 相关

Series 接近于 ndarray 的用法，区别仅仅在于会带上 label 而已

> 关于 ndarray, 请参考 我的另一篇文章 Numpy Cheatsheet

## 0x02 DataFrame 相关

### 2.1 对象创建

```python

# 1. 内存变量转 Dataframe
## 1.1. 通过二位矩阵 , index , columns
dates = pd.date_range('20130101', periods=6)
pd = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
## 1.2. 通过字典 Key 为 Column , Value 为 list,timestamp,np.array,value
df2 = pd.DataFrame({ 'A' : 1.,
                     'B' : pd.Timestamp('20130102'),
                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),
                     'E' : pd.Categorical(["test","train","test","train"]),
                     'F' : 'foo' })
# 长度无需统一，会自动填充

# 2. 从文件中读取
pd.read_excel("./data_set.xlsx",index_col=False) # 关掉 Index

# 3. 合并多个同样的 DataFrame
df_items = [df_item1,df_item2,...]
df = pd.concat(df_items).drop_duplicates()
df.merge(data_set_df, left_on="lno", right_on="rno", how="outer")

# 4.series to dataframe
df = s.to_frame()

```
选择数据
    Getting
    Selection by Label
    Selection by Position
    Boolean Indexing
    Setting
缺失数据
数据操作
    Operations
    Stats
    Apply
    Histogramming
    String Methods
数据合并
    Concat
    Join
    Append
Grouping
Reshaping
    Stack
    Pivot Tables
Time Series
Categoricals
Plotting

### 2.2 浏览数据

```python
# 1. 查看表结构

df.head()
df.tail(3)
df.index
# df.index = ['日期','小时']
df.columns
df.columns = map(str.lower, df.columns)

df.values

df['col'] = df['col'].astype(str).convert_objects(convert_numeric=True)

# 2. 删除 col_name

df.drop(['col_name_1','col_name_2',...,'col_name_N'],inplace=True,axis=1,errors='ignore')

del df['cola']

# 3. 修改元数据
df.rename(columns=lambda x: x.split('.')[-1], inplace=True)
df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
df.rename(columns = {0: 'cola', 1: 'colb', 2: 'colc'}, inplace=True)

# 2.
## 2. 遍历
for index, row in df.iterrows():
    print row["c1"], row["c2"]
for row in df.itertuples(index=True, name='Pandas'):
    print getattr(row, "c1"), getattr(row, "c2")
= IF([@price] < 1, "未知",IF([@price] < 30000, "三万以下", IF([@price] <= 50000, "三万到五万", IF([@price] <= 100000, "五万到十万", IF([@price] <= 10000000, "十万以上", "其他")))))
```

### 2.3 修改表内容

```python
df.drop_duplicates(['col_a','col_b'])
```

### 2.4 查看表内容

```python
# 选择
df['A'] # 列选
df[0:30] # 行选
df['20130102':'20130104'] # 行选
df.loc['20130102':'20130104',['A','B']] # by label
df.loc[condition,['cola','colb']]
df.loc[['ri01','ri02'] , ["cola","colb","colc"]]

df.iloc[1:5, 2:4] # by position
df.iloc[: , 0:7] # 全部列，0-7 索引

df.ix[['ri02', 'ri09']] # 选取行

total_rows=len(df.axes[0])
total_cols=len(df.axes[1])

df.sample(3000) # 随机抽取 3000 行，可以用于快速验证算法

criterion = df2['a'].map(lambda x: x.startswith('t'))
df2[criterion]

df2[[x.startswith('t') for x in df2['a']]]
# select * from df limit 5
df.head()
# select a,b,c from df
df[['a','b','c']].head()
# select a,b,c from df where a = 11 and b = 'xx'
df[ ( df['a'] == 11) & ( df['b'] == 'xx') ][['a','b','c']]
df['a'].value_counts()

# SELECT * FROM df ORDER BY a DESC LIMIT 10 OFFSET 5;
df.nlargest(10+5, columns='a').tail(10)

df.column.str[0:2]
df.column_name.str.len()
two_groups = '(?P<letter>[a-z])(?P<digit>[0-9])'
s.str.extract(two_groups, expand=True)

# 排序

df.sort_index(axis=1, ascending=False)
df.sort_values(by='B')
df = df.sort(['col1','col2','col3'],ascending=[1,1,0])
#

# window function
# SELECT a, b, c, rank() OVER (PARTITION BY a ORDER BY b DESC) as rn FROM df;
# 如果没有这个 window function 的话，可以 groupby 一下，然后生成表和原有表进行 JOIN
tips.assign(rn=tips.sort_values(['b'], ascending=False).groupby(['a']).cumcount() + 1)

# Top N rows per group
# rank 代表等级 如果两人并列第一名，则不存在第二名，直接是第三名 , row_number 代表排名，即即便两个人分数一样，也无法并列第一名

# PostGRESQL's ROW_NUMBER() analytic function
SELECT * FROM (
  SELECT
    t.*,
    ROW_NUMBER() OVER(PARTITION BY day ORDER BY total_bill DESC) AS rn
  FROM tips t
) tt
WHERE rn < 3
ORDER BY day, rn;

(tips.assign(rn=tips.sort_values(['total_bill'], ascending=False)
                    .groupby(['day'])
                    .cumcount() + 1)
     .query('rn < 3')
     .sort_values(['day','rn'])
)

(tips.assign(rnk=tips.groupby(['day'])['total_bill']
                     .rank(method='first', ascending=False))
     .query('rnk < 3')
     .sort_values(['day','rnk'])
)

# PostGRESQL's RANK() analytic function
SELECT * FROM (
  SELECT
    t.*,
    RANK() OVER(PARTITION BY sex ORDER BY tip) AS rnk
  FROM tips t
  WHERE tip < 2
)
WHERE rnk < 3
ORDER BY sex, rnk;

(tips[tips['tip'] < 2]
     .assign(rnk_min=tips.groupby(['sex'])['tip']
                         .rank(method='min'))
     .query('rnk_min < 3')
     .sort_values(['sex','rnk_min'])
)

# where 语句
df['a'].isnull()
df['a'].isin(arr)

# groupby
df.groupby('a').size() # 计算 a
df.groupby('a')['b'].count() # 同上计算 a
df.groupby('a').count() # 计算所有 cols
agg_fun_dict = {'tip': np.mean, 'day': np.size}
agg_fun_dict_new = {'tip': [np.mean, np.size]}
df.groupby('a')[['b','c']].agg(agg_fun_dict)
df.groupby('a')['b'].describe()
df.age.agg(['min', 'max'])
df.applymap(multiply_10_for_every_int) #

calc_groups = df.groupby([date])
calc_groups['id_aa'].nunique().reset_index().to_excel("123.xlsx")

# pivot
pd.pivot_table(data=df,values='value_col', index='A_FROM', columns='B_TO', aggfunc=lambda x: len(x.unique()),margins=True)

# CONCAT
append
# JOIN
pd.merge(df1, df2, on='key', how='outer')

# UPDATE tips SET tip = tip*2 WHERE tip < 2;
tips.loc[tips['tip'] < 2, 'tip'] *= 2

# TODO:
```

### 2.5 表变换

```python
# apply , apply map
DataFrame.apply operates on entire rows or columns at a time.
DataFrame.applymap, Series.apply, and Series.map operate on one element at time.
```

### 2.6 表遍历

```python
df.iterrows()
df.itertuples()
```

## 数据导入导出

### SQL

```python
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'yourusername',
    'password': 'yourpass',
    'database': 'yourdb'
}
# 这里并不建议直接写数据库连接字符串，而是使用 URL 函数，这样可以避免转义字符带来的坑，比如 @ 在数据库连接字符串是 %40
engine = create_engine(URL(**DATABASE))

# 读一整张表
with engine.connect() as conn, conn.begin():
    data = pd.read_sql_table('yourtablehere', conn)
    processyourdata(data)

# 按照 SQL 语句来读
with engine.connect() as conn, conn.begin():
    data = pd.read_sql("""
    yoursqlquery
    """, conn)
    processyourdata(data)
```

### CSV

日常数据处理用 CSV 的比较多，因为这种格式语法简洁，类二维表，读写速度快，而且配合 gzip 压缩解压。

pandas 在 windows 上好像不能读取中文路径？

而且，pandas 读取的时候要注意指定编码。因为在日常导出 CSV 的时往往使用的是 utf-8, 而 windows 默认打开文本文件时候使用的是 gbk

read_csv 有几十个参数，挑几个说一下：

- sep 可以指定分隔符，默认为',', 但有的人导出的数据以 tab 为空格。
- dtype 可以指定某些列的值类型为 int,float 的类型从而减少 object 的创建 , 但是对 str/object 没有什么暖用
- parse_dates 可以指定 date 列
- header 如果 CSV 没有 Header, 可以指定为 None
- usecols 可以指定几列，相当于数据库中的 SELECT a_col,b_col

其中还有一些比较有趣的东西，比如说，iterator=True
值得注意的是，通过

### Excel

Gotchas

## 0x02 可视化技术

```python
# 绘制
df.plot(kind='bar')

plt.xlabel('xlable')
plt.ylabel('ylable')
plt.title('title name')

plt.show()

df['数量'].plot(kind='bar')

# 批量创建图
g = sns.FacetGrid(customers, col="cola")
g.map(plt.scatter, "数量", "单位", alpha=1)
g.add_legend();

ttbill = sns.distplot(tips["总价格"]);
ttbill.set(xlabel = '价值', ylabel = '频率', title = "标题名")
sns.despine()

sns.jointplot(x ="total_bill", y ="tip", data = tips)
# https://github.com/guipsamora/pandas_exercises/blob/master/07_Visualization/Tips/Exercises_with_code_and_solutions.ipynb

plt.pie(
    [100,300],
    labels = ['男', '女'],
    shadow = False,
    colors = ['blue','red'],
    explode = (0.15 , 0),
    startangle = 90,
    autopct = '%1.1f%%'
    )
plt.axis('equal')
plt.title("男女比例")
plt.tight_layout()
plt.show()
```

## 0x03 asd1

## 0x07 Performance Tips

最近遇到了数据量比较大的数据处理，数据条数差不多在 3 千万条。加载到内存中大约 1GB.

### 7.1 精简行列

1. 读入 dataframe 的时候就排除多余的行列。
2. Merge 时候需要精简行列。

```python
df1.merge(df2[list('xab')])
pandas.merge(dataframe1, dataframe2.iloc[:, [0:5]], how='left', on='key')
```

### 7.2 大文件的处理

> 参考我的文章 记一次小机器的 Python 大数据分析

## 0x 踩坑集合

## 0x08 踩坑集合

### 8.1 IO 类

####

### 8.2 IO 类

## 0xEE 参考链接

---
ChangeLog:
 - **2017-06-03** 初始化本文
 - **2018-02-03** 重修文字
