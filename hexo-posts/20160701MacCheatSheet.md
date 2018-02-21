title: Mac Cheatsheet
date: 2016-07-01 18:41:47
categories:
 - 善用佳软
tags:
 - CheatSheet
 - macOS

---

## 0x00. 前言

> 好的工匠懂得挑选合适的工具。

做软件行业之间长了，见多了各种操作系统孰优孰劣 / 编程语言哪家强的论战，也就渐渐懂得了这个异常朴素的道理。也懒得去争论。有争论的时间，不如好好的编写代码，多看些技术书籍。以及熟悉自己的工具。

如果说，你现在问我到底是哪个 OS 好，我只能说：

> 好的工匠懂得挑选合适的工具。而不是炫耀自己的工具。

BTW : **大约在 2015 年 12 月份有了第一台 MAC, 如今更加喜爱。**

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 Mac 快捷键和工具。

不定期更新。

<!-- more -->

## 0x01. 必备软件

### 1.1. 常见应用

**非技术流**
 - 启动器 Alfred 3
 - 浏览器 Chrome Firefox
 - 输入法 搜狗输入法
 - 系统清理 AppCleaner
 - 系统增强 Caffeine / PopClip / BetterZip / Amphetamine
 - 手机管理工具 HandShaker / AirDroid
 - 邮件客户端 Airmail 2
 - 录屏截图 Annotate / Camtasia 2 /  Snagit / ScreenFlow
 - 下载工具 Aria2GUI / 迅雷
 - 影音处理 Adobe PhotoShop CC , Adobe PhotoShop , Adobe LightingRoom , Final Cut Pro
 - 影音浏览 MPlayerX, QuickTime , IQIYI , NeteaseMusic , iina
 - 远程协助 TeamViewer
 - 办公软件 Wiznote , PDF Expert , Office（虚拟机内部）OmniFocus , OmniGraffle , EuDic , MacTex : Latex
 - 云存储 iCloud , 百度云
 - 手机管理 HandShaker

**技术流**
 - 终端：iTerm2
 - GIS 相关 QGIS , PostgreSQL + PostGIS
 - IDE 选择 JetBrain 家的软件 PyCharm, IntellijIDEA
 - 编辑器 MacVim （主力）, 配合 [C-VIM](https://github.com/twocucao/c-vim) 作为日常编写文字的利器。
 - 数据库 MySQL , PostgreSQL（主力） , Redis , MongoDB
 - 数据管理 Navicat,Datagrip,RoboMongo,rdm
 - 文档查看 Dash
 - 网络工具 SS QT 不解释
 - 网络抓包 Charles, Wireshark, Chrome
 - 代码仓库 Github SourceTree
 - 数据分析 Tableau
 - 虚拟机 Vmware Fusion
 - 抓包工具 Wireshark

**mac 独有命令行**
 - open
 - pbcopy
 - pbpaste
 - screencapture
 - launchctl
 - mdfind（还是 linux 的 find 好用）
 - sip （还是比较推荐 imagemagic)

### 1.2. Homebrew 和 iTerm2

[iterm2 下载](http://www.iterm2.com/)

```bash
# homebrew 安装
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

另起终端

```bash
# aerial 屏保
# https://github.com/JohnCoates/Aerial
brew cask install aerial
# https://github.com/sindresorhus/quick-look-plugins
brew cask install qlcolorcode qlstephen qlmarkdown quicklook-json qlprettypatch quicklook-csv betterzipql qlimagesize webpquicklook suspicious-package quicklookase qlvideo
# Install some other useful utilities like `sponge`.
brew install moreutils
# Install GNU `find`, `locate`, `updatedb`, and `xargs`, `g`-prefixed.
brew install findutils
# Install GNU `sed`, overwriting the built-in `sed`.
brew install gnu-sed --with-default-names

brew install bash zsh
brew install wget --with-iri

# Install Python
brew install python
brew install python3

brew tap bramstein/webfonttools
brew install sfnt2woff
brew install sfnt2woff-zopfli
brew install woff2

# Install other useful binaries.
brew install ack
brew install dark-mode
#brew install exiv2
brew install git
brew install git-lfs
brew install git-flow
brew install git-extras
brew install hub
brew install imagemagick --with-webp
brew install lua
brew install lynx
brew install p7zip
brew install pigz
brew install pv
brew install rename
brew install rhino
brew install speedtest_cli
brew install ssh-copy-id
brew install tree
brew install webkit2png
brew install zopfli
brew install pkg-config libffi
brew install pandoc

# Lxml and Libxslt
brew install libxml2
brew install libxslt
brew link libxml2 --force
brew link libxslt --force

brew cleanup
# 如果需要升级
brew update && brew upgrade --all && brew cleanup && brew prune
```

有时候 /usr/local 的可能会存在权限问题，建议如果可能出现问题，则需要执行下面的命令修复权限。

```bash
sudo chown -R $(whoami):admin /usr/local/
```

## 0x02. 开发者必备

### 2.0. Shell

>  注意：MAC 使用的大多命令来自于 FreeBSD , 并不是来自 GNU , 所以很多命令会与常规的 linux 命令不太一样。
>  所以，Shell 命令请在安装完 Gnu 的工具集之后，可以到我的文章 Shell CheatSheat 查看语法。

关于 shell 脚本，请参考我的另一篇文章。

[Shell CheatSheat](/2015/04/18/ShellCheatSheet/)

### 2.1. Python

> 笔者虽然也接触过很多语言，都是粗浅一过，但无一精通，唯一可以稍微谈谈的就是 Python 语言。

> 当然，安装完毕自然是可以参考一下我的 Python 武器库啦 [Python 工程师的武器库](http://www.url.com)

#### 2.1.1. Python 安装

```bash
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

# 接着另开终端
# 不喜写兼容代码，所有代码均向 3.5+ 靠拢
v=3.5.2|wget http://mirrors.sohu.com/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v
v=3.6.0|wget http://mirrors.sohu.com/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v
v=2.7.11|wget http://mirrors.sohu.com/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v
# 可以先用迅雷把 官网的 Anaconda3-4.4.0-MacOSX-x86_64.sh 下载下来，然后
mv Anaconda3-4.4.0-MacOSX-x86_64.sh ~/.pyenv/cache/ && pyenv install anaconda3-4.4.0

# 设置 Global Python 为 2.7.11, 备注：尽量不要把 Py3 设置为全局，否则由于 Homebrew 本身有一些依赖是依赖于 Py2 的，这样容易出现一些奇怪的问题。
pyenv global 2.7.11
pip install -i https://pypi.doubanio.com/simple requests
# 下面这个是用于安装基本的代码补全功能
pip install -i https://pypi.doubanio.com/simple --upgrade "jedi>=0.9.0" "json-rpc>=1.8.1" "service_factory>=0.1.5" flake8 pytest autoflake hy

# 创建最常用 Py3 虚拟环境
pyenv virtualenv 3.5.2 py3-daily
pyenv activate py3-daily
pip install -i https://pypi.doubanio.com/simple requests
pip install -i https://pypi.doubanio.com/simple beatutifulsoup4
pip install -i https://pypi.doubanio.com/simple ipython[notebook]
pip install -i https://pypi.doubanio.com/simple jupyter
# 下面这个是用于安装基本的代码补全功能
pip install -i https://pypi.doubanio.com/simple --upgrade "jedi>=0.9.0" "json-rpc>=1.8.1" "service_factory>=0.1.5" flake8 pytest autoflake hy

# 创建 Anaconda 的数据科学 AI 环境
pyenv virtualenv anaconda3-4.4.0 py3-ai
pyenv activate anaconda3-4.4.0/envs/py3-ai
pyenv deactivate
```

#### 2.1.2 Python 环境的坑

##### Homebrew 的 Python 问题

如果本机安装了 Homebrew 如果后面使用 PyEnv 或者 Anaconda 设置当前环境为默认 Python 为 Python3（不建议这么搞）, 但是如果偏偏要把默认的 Python 版本换成 Python3, 会弹出一些 pythonpath 的问题，执行下面命令即可暂时屏蔽这个问题，但是后没有隐患则不清楚。
mv /usr/local/lib/python2.7/site-packages/sitecustomize.py /usr/local/lib/python2.7/site-packages/sitecustomize.py.back

##### 网络问题

在 Python 中执行下面的代码的时候总是报错：

```python
ip = socket.gethostbyname(socket.gethostname())
# socket.gaierror: [Errno 8] nodename nor servname provided, or not known
```

最后发现是因为设置主机名没有设置好

```bash
sudo scutil --set ComputerName "newname"
sudo scutil --set LocalHostName "newname"
sudo scutil --set HostName "newname"
dscacheutil -flushcache
# 然后重启电脑即可
```

## 0x03. 高效率软件 && 专业软件

### 3.1. OmniFocus
### 3.2. OmniGraffle
### 3.3. Final Cut Pro
### 3.4. Keynote

## 0xDD. 参考链接

 - https://github.com/donnemartin/dev-setup

## 0xEE. 扩展阅读

 - [关于 Mac 我的回答](https://www.zhihu.com/question/30816866/answer/59415036)
 - [关于 Ubuntu 我的回答](https://www.zhihu.com/question/30816866/answer/59415036)
 - [关于 Win10 我的回答](https://www.zhihu.com/question/32129337/answer/59379401)

---
ChangeLog:
 - **2017-06-28** Python 环境 和 Homebrew 安装环境
