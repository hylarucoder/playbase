title: Git CheatSheet
date: 2017-06-15 20:46:00
categories:
 - 编程利器
tags:
 - 数据分析

---

# 如何优雅地使用 Git

## 0x00 前言

Git 是一种分布式版本管理工具。

## 0x01 Git 命令范论

 1. 基础命令 （本地修改类）
 2. 合作命令 （本地与仓库类）
 3. 综合命令
 4. 管理命令

前两种命令是入门 Git 的程序员都必须要会的。

而队伍里的技术管理人员必须要会前三。

### 1.1 基础命令

- git-init(1) to create a new repository.
- git-log(1) to see what happened.
- git-checkout(1) and git-branch(1) to switch branches.
- git-add(1) to manage the index file.
- git-diff(1) and git-status(1) to see what you are in the middle of doing.
- git-commit(1) to advance the current branch.
- git-reset(1) and git-checkout(1) (with pathname parameters) to undo changes.
- git-merge(1) to merge between local branches.
- git-rebase(1) to maintain topic branches.
- git-tag(1) to mark a known point.

```bash
$ tar zxf frotz.tar.gz
$ cd frotz
$ git init
$ git add . (1)
$ git commit -m "import of frotz source tree."
$ git tag v2.43 (2)

$ git checkout -b alsa-audio (1)
$ edit/compile/test
$ git checkout -- curses/ux_audio_oss.c (2) # 恢复文件
$ git add curses/ux_audio_alsa.c (3)
$ edit/compile/test
$ git diff HEAD (4) # 查看提交了哪些修改
$ git commit -a -s (5) # 提交所有
$ edit/compile/test
$ git diff HEAD^ (6) # 查看所有变化，包含之前的 commit
$ git commit -a --amend (7) # 修订前一个 commit, 把所有的新变化提交到
$ git checkout master (8)
$ git merge alsa-audio (9)
$ git log --since='3 days ago' (10)
$ git log v2.43.. curses/ (11)
```

### 1.2 合作命令

-  git-clone(1) from the upstream to prime your local repository.
-  git-pull(1) and git-fetch(1) from "origin" to keep up-to-date with the upstream.
-  git-push(1) to shared repository, if you adopt CVS style shared repository workflow.
-  git-format-patch(1) to prepare e-mail submission, if you adopt Linux kernel-style public forum workflow.
-  git-send-email(1) to send your e-mail submission without corruption by your MUA.
-  git-request-pull(1) to create a summary of changes for your upstream to pull.

```bash
## clone 修改 提交
$ git clone git://git.kernel.org/pub/scm/.../torvalds/linux-2.6 my2.6
$ cd my2.6
$ git checkout -b mine master (1)
$ edit/compile/test; git commit -a -s (2)
$ git format-patch master (3)
$ git send-email --to="person <email@example.com>" 00*.patch (4)
$ git checkout master (5)
$ git pull (6)
$ git log -p ORIG_HEAD.. arch/i386 include/asm-i386 (7) # 查看感兴趣的部分
$ git ls-remote --heads http://git.kernel.org/.../jgarzik/libata-dev.git (8) # 查看分支
$ git pull git://git.kernel.org/pub/.../jgarzik/libata-dev.git ALL (9) # 从一个特地
$ git reset --hard ORIG_HEAD (10) # 撤销 pull
$ git gc (11) # garbage collect leftover objects from reverted pull
# 推送到其他 repo

satellite$ git clone mothership:frotz frotz (1)
satellite$ cd frotz
satellite$ git config --get-regexp '^(remote|branch)\.' (2)
remote.origin.url mothership:frotz
remote.origin.fetch refs/heads/*:refs/remotes/origin/*
branch.master.remote origin
branch.master.merge refs/heads/master
satellite$ git config remote.origin.push \
            +refs/heads/*:refs/remotes/satellite/* (3)
satellite$ edit/compile/test/commit
satellite$ git push origin (4)

mothership$ cd frotz
mothership$ git checkout master
mothership$ git merge satellite/master (5)

           1. mothership machine has a frotz repository under your home directory; clone from it to start a repository on the satellite machine.
           2. clone sets these configuration variables by default. It arranges git pull to fetch and store the branches of mothership machine to local remotes/origin/* remote-tracking
           branches.
           3. arrange git push to push all local branches to their corresponding branch of the mothership machine.
           4. push will stash all our work away on remotes/satellite/* remote-tracking branches on the mothership machine. You could use this as a back-up method. Likewise, you can
           pretend that mothership "fetched" from you (useful when access is one sided).
           5. on mothership machine, merge the work done on the satellite machine into the master branch.

       Branch off of a specific tag.

               $ git checkout -b private2.6.14 v2.6.14 (1)
               $ edit/compile/test; git commit -a
               $ git checkout master
               $ git cherry-pick v2.6.14..private2.6.14 (2)

           1. create a private branch based on a well known (but somewhat behind) tag.
           2. forward port all changes in private2.6.14 branch to master branch without a formal "merging". Or longhand git format-patch -k -m --stdout v2.6.14..private2.6.14 | git am -3
           -k

```

### 1.3 综合个体

### 1.4 仓库管理

安装完毕之后，cmd-s-p shell command install

## 0x02 Git Hacks

```bash
# 搜索代码的变化
git log -S'<a term in the source>'
# 放弃本地修改，与远程同步
git fetch origin && git reset --hard origin/master && git clean -f -d
# 列出所有冲突文件
git diff --name-only --diff-filter=U

# 手贱错误提交，但是没有 push
git commit -m "Something terribly misguided"              (1)
git reset HEAD~                                           (2)
# edit needing changed files
git add needing changed files                             (4)
git commit -c ORIG_HEAD                                   (5)

# Delete all changes in the Git repository, but leave unstaged things
git checkout .
# Delete all changes in the Git repository, including untracked files
git clean -f

```

## 0x03 Git 和 我的 Workflow

一切工具都是为思路服务。

## 0xEE 扩展阅读


