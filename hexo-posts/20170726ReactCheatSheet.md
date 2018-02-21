title: React CheatSheet
date: 2017-07-26 20:06:05
categories:
 - 前端开发
tags:
 - JavaScript
 - React
 - Ant Design

---

## 0x00. 前言

> 备注：由于目前没有上 React 的打算，本文暂时太监

之前一直使用 VueJS 进行开发，心血来潮想换换口味，于是就借着自己的一个开源的项目尝试一下 ReactJS , 代码分为两部分，如下：

 - 前台系统（支持 SSR) [YaReactBlog](https://github.com/twocucao/YaReactBlog)
 - 后台系统 [YaReactAdmin](https://github.com/twocucao/YaReactAdmin)

```bash

TODO:

```

<!-- more -->

本文目录

 - 前端、单页与 React 开发
 - 官网的 Tutorial / Guide 要点
 - Dva 下使用 React JS 的要点

## 0x00. 前端、单页与 React 开发

### 0.1. 前端

前端开发，是最近几年才出现的独立工种。

在我的印象中，以前的人很少会区分前端和后端，现在的前端的职责往往是由后端的人顺手做掉的。当然，这种界面一般情况下都比较丑。

后来，随着浏览器的功能越来越强大，性能越来越好，用户对于界面要求也就越来越高。甚至到后来，对于用户界面的操作的复杂程度要求也越来越高。 传统的后端渲染 Template + 简单的 Ajax 不能满足要求了。

> 要界面，要交互，要复杂

于是便出现了单页应用。

### 0.2. 单页

单页完全可以当做一个性能不是很强的，运行在浏览器中的，使用 HTML CSS JS 来编写的小型客户端。

写单页和写客户端基本一致的情况下，于是在这种情况下，前端开发在使用单页后，直接可以 Mock 数据，接着编写界面，接着调通页面的状态和操作，最后发布。

### 0.3. ReactJS

为什么选用 ReactJS 呢？

个人认为，框架是用于改善代码组织的一种约束。

不管是 Web 应用开发的早期的 HTML in PHP OR PHP in HTML, 还是中期的 MVC MTV, 还是后来的 富 AJAX 操作，还是现在的 SPA, 出现的各种框架无非就是为了解决代码组织的问题。

对后端而言，后端 WEB 框架的设计，都是为了单个模块职责过重而出现的一种解决方案：

 - HTML IN PHP 拼接代码简单暴力，可是如果拼接太多，每个文件就很职责重，代码阅读性差，不方便调试，就显得很杂乱。
 - PHP in HTML 相比上一个解决方案好很多。可是，嵌入过多 PHP 代码，代码阅读性差，不方便调试，则会显得比较混乱。
 - MVC 与 MTV 把渲染的变量独立出来放到 Controller 中，然后把需要渲染的 HTML 模板放到 Template 中，并且在 Template 中来完成模板的拼接。最后调用 Render 进行渲染。是不是这样问题就解决了呢？不是，如果把业务逻辑放在 Model 层，则 Model 职责过重。那就必须要添加一个 Serivce 层来封装业务逻辑。是不是封装了一个

如果业务逻辑简单到令人发指，HTML IN PHP 可以给人最大的灵活性。

1. 尝试一下新技术。保持对技术的敏感性。
2. React 是 FB 出的一套前端框架。大厂支持，不会轻易太监掉。
3. 写了一段时间 VueJS 换换口味。

当我们讨论一个框架的时候，除了基本的框架之外还必须要有大量的社区资源，那么对 React 而言，除了 ReactJS 之外，还有什么？

```bash

后台系统

 - ant.design

打包构建

 - webpack

路由和状态管理

 - react-router
 - react-router-redux
 - redux
 - redux-saga

为了更好的管理路由和状态，还是使用 dva 来管理比较好。

 - [dva](https://github.com/dvajs/dva)
 - [dva-cli](https://github.com/dvajs/dva-cli)

开发构建工具

 - [roadhog](https://github.com/sorrycc/roadhog)

```

## 0x01. 官网的 Tutorial / Guide

官网的要点

## 0x02. 在 dva 下，编写 React 组件的正确姿势

编写 React 的时候，我选用了 dva 框架配合 ReactJS 来编写单页。

参考 FB 的这篇教程后，梳理了我编写组件的步骤 https://facebook.github.io/react/docs/thinking-in-react.html :

1. 先构思出原型 （或者拿到 UI 图）
2. Mock 出假数据
3. 分解页面 OR 组件为 组件树
4. 编写静态组件树
5. 确定最小表达 UI （加上满足要求的样式）
6. 确定什么时候需要什么状态（网络请求，键盘输入，位置变化等等）
7. 收尾美化
8. 在发现问题的时候进行优化

## 0x03. 在 dva 下，编写 React 组件的正确姿势

---
ChangeLog:
 - **2017-07-17** 重修文字
