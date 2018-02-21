title: Vim Cheatsheet
date: 2017-06-23 19:48:00
categories:
 - 编程利器
tags:
 - Vim
 - 效率
 - 工作自动化
 - Cheatsheet

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中 Vim 使用场景。

不定期更新。

<!-- more -->

 - 配置
 - 基本使用技巧
 - 原生 Tips & Hacks
 - Vim 必备插件

## 0x01 配置

原先使用 k-vim 进行日常的编辑，然后依据自己的一些需求进行微调为 c-vim 。

https://github.com/twocucao/c-vim

## 0x02 基本使用技巧

### 2.1 Insert Mode

 - c-w 向后删除一个 word
 - c-h 向后删除一个 char

### 2.2 Normal Mode

- gi 返回上次修改地点
- d% 剪切包含括号的括号内部内容
- U 恢复单个句子
- 在命令状态下按 c-d 可以查看所有命令，相当于 bash 下面的 tabtab
- hjkl 左下上右
- EasyMotion 使用这个就可以代替乱七八糟的快速移动了。这是一个可以给当前的文字立即用打上 tag, 这样的话在 normal 情况下输入，,w  然后就可以看到很多 tag, 输入其中的 tag 就可以立即跳转到相应的 tag.
- insert 状态进行编辑 c-h c-w 删除一个字，删除一个词。
- normal 状态下进行删除 x dd  ------ 删除一个字，剪切一行。
- . ..  ------ 重复操作
- > <   ------ 缩进 >G <g <G >g
- c-b c-f back forth
- c-n c-p 代码补全，tips, 建议标点符号全部半角花，这样就会吧每段连起来的汉字当成一个单词，这样就可以减少输入代码。
- > indent
- < outdent
- do it (>)
- repeat (.)
- reverse (u)
- f{char}
- repeat ;
- reverse ,

### 2.3 Command Mode

:%s/old/new/gc 可以一行一行查看

### 2.4 Visual Mode

vib - 选框内
vi" - "" 内部
vi' - '' 内部
ggVG

### 2.5 窗口管理

切换窗口：Ctrl+w+hjkl
分割窗口：Ctrl+w+vs
关闭窗口：Ctrl+w+q

## 0x03 原生 Tips & Hacks

### 行处理

#### 行排序
```
行排序
sort r /【.\+】/
sort u
sort n
sort
sort!
g/start/+1,/end/-1 sort n

:%!column -t
:%!sort -k2nr

```
#### 行删除
删除 html 标签

```bash
:%s/<\_.\{-1,\}>//g
```

#### 删除空行
```

:g/^$/d
:g/^\s*$/d
:%s/\n\{3,}/\r\r/e
:g/^[ \t\u3000]*$/d

:g/pattern/d
:g!/pattern/d

:g/pattern/t$
:g/pattern/m$
:s/ \{2,}/ /g
```

Use \r instead of \n

## 0x04 Vim 必备插件

