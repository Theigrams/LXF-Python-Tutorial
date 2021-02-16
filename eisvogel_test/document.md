---
title: "廖雪峰Python"
author: [张晋]
date: "2017-02-20"
subject: "Markdown"
keywords: [Markdown, Example]
subtitle: "略略略"
titlepage: true,
titlepage-rule-color: "360049"
titlepage-background: "backgrounds/background1.pdf"
header-left: "\\hspace{1cm}"
header-center: "\\leftmark"
header-right: "Page \\thepage"
footer-left: "\\thetitle"
footer-center: "\\thepage"
footer-right: "\\theauthor"
---

## 第一个 Python 程序

在正式编写第一个 Python 程序前，我们先复习一下什么是命令行模式和 Python 交互模式。

JSON 表示的对象就是标准的 JavaScript 语言的对象，JSON 和 Python 内置的数据类型对应如下：

| JSON类型   | Python类型 |
| :--------- | :--------- |
| {}         | dict       |
| []         | list       |
| "string"   | str        |
| 1234.56    | int或float |
| true/false | True/False |
| null       | None       |

Python 内置的`json`模块提供了非常完善的 Python 对象到 JSON 格式的转换。我们先看看如何把 Python 对象变成一个 JSON：