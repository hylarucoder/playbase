title: ElasticSearch CheatSheet
date: 2018-02-10 10:25:39
categories:
 - 后台组件
tags:
 - ElasticSearch
 - CheatSheet
 - 搜索排序
 - 搜索引擎

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 ElasticSearch 相关和命令。

不定期更新。

最早使用 ElasticSearch 是两年前了。最近准备用 Django 写一个全栈式的应用，借用强大的 ES 来做搜索。这是我在写程序之余写这篇文章的原因。

官网介绍 ElasticSearch 不仅仅是全文搜索，也可以结构化搜索（这里用结构化查询会更准确一些），分析，处理人类语言，地理位置，以及关系。

然而，我在项目使用过程中还是主要用到了全文搜索以及推荐。

不用其他的主要原因是因为 ES 尺有所短寸有所长：

1. geo 处理方面 postgis 完全就是神一般的存在。为什么还要用 ES 呢？
2. 关系型数据库的核心不就是处理关系？复杂的关系肯定还是放在关系数据库里面。

highlighted search snippets, and search-as-you-type and did-you-mean suggestions.

我对 ElasticSearch 在后台组件里的作用在于搜索与推荐：

1. 整站的搜索功能
  - 全文搜索
2. 推荐
  - 依据某几个维度的数据进行排序

<!-- more -->

## 0x01 安装，配置，基本 shell 命令

### 1. 安装

```
# 执行如下的命令
curl 'http://localhost:9200/?pretty'
# 输出结果
{
  "name" : "XOGvo8a",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "fAwp341bQzalzBxRFyD1YA",
  "version" : {
    "number" : "6.2.1",
    "build_hash" : "7299dc3",
    "build_date" : "2018-02-07T19:34:26.990113Z",
    "build_snapshot" : false,
    "lucene_version" : "7.2.1",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

### 2. 配置

### 3. 插件

ES 的插件有很多，比这使用现在最新的版本是 6.2.1 版本。

> PS: 两年前我用的还是 2.3.3 版本。新版本有很多插件配置起来已经有所不同了。比如说 head 现在已经被独立出来作为一个单纯的网页，chrome 商店可以直接下载。

## 0x02 ElasticSearch 配套工具

建议使用 Head 插件来进行简单的查询与调试。

## 0x03 ElasticSearch 基础概念

### 3.1 Elasticsearch CRUDE 以及基本操作

ES 使用的是 RESTFUL API 接口

这也就意味着：

- PUT 创建记录
- GET 获取记录
- POST 更新记录
- DELETE 删除记录
- HEAD 是否存在

## 0x04 全文搜索的基本概念

### 4.1 全文搜索遇到的挑战

在最初开源搜索引擎技术还不是很成熟的时候，我们一般都会使用 RDBMS 进行简单搜索。

简单搜索，也就是我们常常使用的 like 查询（当然，有的数据库可以使用正则表达式）

这种方式是简单暴力的查询方式，优点是实现起来简单暴力。缺点是在这个场景下性能和准确度很差。

举例：

- 假如站点里文章数量比较大，并且文章内容比较长，则进行一次全表查询，效率可想而知。当然，做好分库分表读写分离也是能用的。
- 如果我要对搜索到的词语进行高亮，则实现方式就只能是把查询到的文章放在应用层里面进行批量替换。
- RDBMS 似乎完全不懂各种语言之间的区别。
  - 『停止词 / 常用词』有的字我是不需要的，比如南京的狗，其实我想搜的是南京狗，这里的『的』就不是我需要的。
  - 『同义词』有的字我需要的是他的同义词，比如日本黄狗，其实我想搜的是柴犬。
  - 『附加符号』假如说我们搜索一个声调 [nǐ], 总不能让用户打出 [nǐ] 进行搜索吧？总归要转为 ni 才能方便搜索
  - 『词根形式』对于一个单词，假如是动词可能有时态上的区分，如果是名词，可能有单复数的区分。假如我搜 mice, 其实同样的 mouse 也应该被搜索出来。但有事用这种方式也会矫枉过正，比如 organizations 的 原型其实并不是 organization 而是，organ. （当然，overstemming 和 understemming 也是两个不可忽视的问题）
    - Number: fox, foxes
    - Tense: pay, paid, paying
    - Gender: waiter, waitress
    - Person: hear, hears
    - Case: I, me, my
    - Aspect: ate, eaten
    - Mood: so be it, were it so
    - PS: 万幸的是，中文处理中木词根这个概念。我也就不深入这块了。
  - 『拼写问题』 周杰棍与周杰伦
  - 『分词 / 识别词』中文不像英文，词和词之间是完全没有空格的，也就是说，中文天然要比英文多一个关于分词的步骤。

### 4.2 全文搜索的索引时与查询时

- 索引时，指的是 ElasticSearch 在存储文档的阶段。
- 查询时，指的是 ElasticSearch 在查询文档的阶段。

#### 1. 索引时 ES 做了什么？

> 这里我们略过定义 index,type,document 仅仅指某个 field 被赋值 document 被保存的时候针对这个被赋值的 text 类型 field 的处理。

- 第一步：**文本经过 analyzer 处理**
- 第二步：**形成倒排索引**

先看第一步：

通常在定义 field 的时候显式指定 analyzer（分析器）.

这个 analyzer 一般的作用如下：

- STEP 1: 令牌化文本为独立的词
- STEP 2: 词语转小写
- STEP 3: 去除常见的停止词
- STEP 4: 获取词的词根的原型

不同的 analyzer 作用大同小异，拿我们常用的 https://github.com/medcl/elasticsearch-analysis-ik 的话，则也是类似的步骤（下面步骤是我猜测的，没看源码）

1. 令牌化文本为独立的词语 - 分词，并且令牌化文本为独立的词汇
2. 除去常见的停止词
3. 匹配同义词
4. ....

可以定义字段的时候可以指定 analyzer（索引时） 与 search_analyzer（查询时）

先看经过第一步之后，就可以进入第二步形成倒排索引了，此时，倒排索引之于 ElasticSearch 可以类比于 btree 之于 MySQL 或者 Gist 之于 PostgreSQL.

那么，倒排索引包含哪些东西呢？

- **Terms dictionary**
  - 已排序完毕的 terms, 以及包含这些 terms 的 documents 的数量。
- **Postings List**
  - 哪些 document 包含这些词
- **Terms frequency**
  - 每个 term 在这些文章的频率
- **Position**
  - 每个 term 在每个 document 的位置，这是为了便于 phrase query 和 proximity query
  - 高频词的 phrase query 可能导致 上 G 的数据被读取。虽然有 cache, 但是远远不够。
- **Offsets**
  - 每个 term 在每个 document 的开始和结束，便于高亮
- **Norms**
  - 用于给短 field 更多权重的因素.(TODO: 啥玩意）

减少停止词仅仅可以减少少部分 terms dictionary 和 postings list , 但是 positions 和 offsets data 对 index 的影响则是非常大的。

#### 2. 查询时 ES 做了什么？

- 第一步：**文本经过 analyzer 处理**
- 第二步：**查询倒排索引**

#### 3. 全文搜索调优之中文分词

如何扩展分词词典呢？

> TODO: 这个话题可能比较大，先挖坑，以后填

#### 4. 全文搜索调优之停止词

使用停止词是减少索引大小的一种方式（减小索引效果不明显），那么，哪些词语可以呗当做停止词呢？

低频词语：低频词语具备高权重
高频词语：高频词语具备低权重

当然，是否是高频词语依据个人经验主要依据两点来判断：

- 具体情况：比如在英文中，and/the 之类的会比较多，但是中文会比较少。同样的，中文里面其他语言的东西会少一些。正文八经的文章出现不正经的词汇的概率会低。在技术问里面，『数据库』属于高频词汇，但是在比如简书之类的，可能梦想 / 鸡汤 / 超级 / 震惊会多一些。掘金的『前端』两个字绝壁是高频词。
- 抽样跑新词发现的程序。社区里多的是新词发现的脚本。对文章内容或者从搜索框记录下来的搜索词跑一下新词发现的程序，然后人工筛选，应该可以发现更多的高频和低频的词汇。

是不是用上停止词就好了呢？并不是。

比如：

- 假如停止词里面包含了 not , 那么 happy 和 not happy 搜索出来的结果则一致。
- 假如停止词里面包含了或，那么，如果有个乐队名字叫做『或或』, 则搜索不出来。
- 假如停止词里面包含了 to / be / not / or , 则莎士比亚的名言 『To be, or not to be』 则搜索不出来。

#### 5. 全文搜索调优之同义词

同义词也有很多种：

1. 平级关系：插、戳、刺、扎
2. 包含关系：成人包含男人和女人
3. 不容易分清楚关系：
  - 炒，煎，贴，烹，炸，溜
　- 汆，涮，煮，炖，煨，焐
　- 蒸，鲊
　- 卤，酱，熏，烤，炝，腌，拌，焗

用法：

> 同义词使用自定义 filter , 并且在新建 analyzer 并指定 filter 即可。

| -        | 索引时                                                                           | 查询时                                 |
|----------|----------------------------------------------------------------------------------|----------------------------------------|
| 索引大小 | 耗时变多，同义词被索引，大小更大                                                 | 耗时几乎不变                           |
| 相关性   | 准确度下降，所有同义词相同 IDF, 则在所有文档的索引记录中，常用词和冷门词权重相同 | 准确度提升，每个同义词的 IDF 将被校正  |
| 性能     | 性能下降，查询需要涨到                                                           | 性能下降，查询被重写，用于查找同义词   |
| 灵活性   | 变差，同义词法则不改变已存在记录，需重新索引                                     | 不变，同义词法则可被更新，无需重新索引 |

由此可见，大部分场景下的索引时如果没有特别的需求，慎用同义词。

#### 6. 全文搜索调优之拼写错误

有的时候，用户也会输入错误：

- 口误，把『周杰伦』拼成『周杰棍』

这个时候，搜索引擎应该提示一下，您搜索的是不是『周杰伦』呢？

这里面就遇到了一个问题，我们显然知道周杰棍和周杰伦是是相似的，为什么呢？或者说，直观上感知的详细，能用数学方式表达出来吗？

有人说，正则匹配 / 通配符匹配呗。这是一个思路。

Vladimir Levenshtein 和 frederic damerau 给出了一种相似度算法 https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

一个词组通过转换到另一个词的步数就是其距离：

- 替换：『周杰伦』到『周杰棍』
- 插入：『周杰』到『周杰棍』
- 删除：『周杰伦』到『周杰』
- 相邻字符转换：『周伦杰』和『周杰伦』 , 但是『周杰棍的双节伦』到『周杰伦的双节棍』 并不是相邻字符转换

用法：

> 指定 "fuzziness": step 即可

当 step >=2 的时候，由于每次查询都会遍历 terms 字典，则如果大于 2 的时候遍历 terms 的数量则非常惊人了。

- 方法一：设置 prefix_length, 单词的前面一定长度不进行 fuzzy 匹配。一般设置为 3 （估计这是属于英文的匹配，中文环境做不了参考）;
- 方法二：设置 max_expansins, 类似于 RDBMS 的 limit, 查询到一定记录之后停止查询。

fuzzy match query 也是支持的，比如说，假如你指定 "fuzziness" 为 1, 搜索周杰棍，则将周杰伦，周杰全搜索出来了。似乎搜索的很全面呀，但是问题来了：

> 依据 TF/IDF 的高频低权重，低频高权重的计算方式，**周杰棍由于出现次数极少，反而获得了极高的权重。**

所以，一般情况下还是建议做为下面两个问题的解决方案：

- Search as you type : completion suggester
- Did you mean : phrase suggester

#### 7. 全文搜索调优之相关性

我们在接触 RDBMS 的时候系统是没有相关性的说法的，比如说，2017 年 12 月份 xxx 用户的订单，就是直接 select 出来这些订单。因为 where 语句后面包含了界限明确的条件，而全文搜索则不然。

全文搜索不仅仅找到匹配的 documents, 并且按照相关性进行排序（其实就是打分 score)。

为什么需要打分呢？从相亲角度来说，上海内环有房肯定是个超级大加分项。同样是录入信息，在上海内环有房的权重值可是设置的高一些。

Elasticsearch 中使用的计算 score 的公式叫做 practical scoring function, 这个公式借鉴于 TF/TDF 以及 矢量空间模型，但有更多的特征比如，条件罂粟，字段长度正态化，term / query clause boosting

##### 索引时三因素

先看前两个因素 TF/IDF

- tf(t in d) = sqrt(frequency)
- idf(t) = 1 + log (numDocs / (docFreq + 1))

再看后一个因素 Field-Length norm

标题越短，这个词对这个 field 的代表性越强

- norm(d) = 1 / sqrt(numTerms)

##### 查询时

几个词 -> 几维度 -> 寻求最佳匹配以及近似匹配

 - 最佳匹配应该是通过计算长度（应该是，但不确定）
 - 近似匹配，计算距离最近的 cos 值。

##### 计算公式

这个公式调优的时候需要用到

```bash
score(q,d)  = queryNorm(q)
                ·coord(q,d)
                ·∑(tf(t in d)·idf(t)²·t.getBoost()·norm(t,d)) (t in q)
```

## 0x05 搜索语法

Single document APIs

 - Index API
 - Get API
 - Delete API
 - Update API
 - Multi-document APIs

Multi Get API

 - Bulk API
 - Delete By Query API
 - Update By Query API
 - Reindex API

> TODO: 全文搜索 RDBMS like 的效率问题。

全文搜索包含两个重要方面：

- 相关性：通过 TF/IDF , 距离 , 模糊相似度，以及其他算法

- Term-Based : term or fuzzy
- Full-Text : match or query_string

TERM 查找->精确查找

> 加上 constant_score 和 filter 的话，就成了常亮？麻痹的，这两个又是啥

 inverted index

## 0x05 调试

查看 analyzer 的效果
```bash
GET /my_index/_analyze
{
  "analyzer" : "my_synonyms",
  "text" : "Elizabeth is the English queen"
}
```

## 0x06 Python SDK

官方提供了两个 SDK 方便我们进行日常的开发：

- elasticsearch
- elasticsearch_dsl

### 6.1 与 Python 集成

前者偏底层一些，后者偏高层一些，高底层关系的有点类似于 sqlalchemy core 和 sqlalchemy orm 之间的关系。

### 6.2 与 Django 集成

#### elasticsearch-analysis-ik 的配置

## 0x07 踩坑集

- 序列问题

## 0xEE 参考链接

- https://www.zhihu.com/question/19645541

---
ChangeLog:
 - **2018-02-15** 重修文字
