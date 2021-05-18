import sys
import django

from mipha.utils.sys_info import get_current_os


def get_system_info():
    return {
        "Python Version": sys.version.split()[0],
        "Django Version": django.__version__,
        "服务器操作系统": get_current_os(),
        "文件上传限制": "6M",
        "服务器域名": "http://twocucao.xyz",
        "服务器IP地址": "192.168.1.1",
        "数据库版本": "PostgreSQL",
        "时区设置": "UTC",
    }


RESUME_INFO_JSON_STRING = """
{
  "基本信息": [
    {
      "name": "网名",
      "value": "twocucao"
    },
    {
      "name": "个人网站",
      "value": "http://twocucao.xyz"
    },
    {
      "name": "博客地址",
      "value": "http://twocucao.xyz"
    },
    {
      "name": "电子邮箱",
      "value": "twocucao@gmail.com"
    },
    {
      "name": "毕业院校",
      "value": "常州大学"
    },
    {
      "name": "学历",
      "value": "本科"
    }
  ],
  "教育经历": [
    {
      "时间": "2012年-2016年",
      "专业": "软件工程",
      "简介": "Full Stuff Engineer"
    }
  ],
  "技能树": [
    {
      "name": "编程语言",
      "value": [
        {
          "编号": 1,
          "语言": "Python",
          "评价": 10,
          "涉及领域": [
            "Web开发(DJANGO后端REST API)",
            "数据分析(Pandas)",
            "爬虫( Http 级别的 Requests Headless Browser, MITM, Socket级别)",
          ]
        },
        {
          "编号": 2,
          "语言": "JavaScript",
          "评价": 10
        },
        {
          "编号": 3,
          "语言": "Java",
          "评价": 10
        }
      ]
    },
    {
      "name": "编程框架",
      "value": [
        {
          "编号": 1,
          "语言": "Python",
          "评价": 10,
          "开源库": [
            "Django",
            "Flask",
            "Scrapy",
            "啦啦"
          ]
        },
        {
          "编号": 2,
          "语言": "JavaScript",
          "评价": 10
        },
        {
          "编号": 3,
          "语言": "Java",
          "评价": 10
        }
      ]
    }
  ],
  "工作经历": [
    {
      "时间": "2012年-2014年",
      "公司": "大保健公司",
      "职位": "后端 Python 工程师",
      "职责": "年",
      "项目": [
        {
          "时间": "",
          "开发工具": "",
          "技术栈": "",
          "详细职责": ""
        }
      ]
    }
  ],
  "个人项目": [
    {
      "时间": "",
      "开发工具": "",
      "技术栈": "",
      "Github地址": ""
    }
  ]
}
"""


def get_resume_info():
    import json

    return json.loads(RESUME_INFO_JSON_STRING)
