---
title: "CS Knowledge Tree"
category: "项目说明"
type: "总览"
status: "整理中"
tags:
  - "知识树"
  - "计算机科学"
aliases:
  - README
  - "CS知识树"
整理日期: 2026-06-17
---

# CS Knowledge Tree

这是一个总知识仓库，用来把已有课程笔记组织成技术栈和知识树。

## 入口

- [知识树首页](index.md)
- [学习路线图](roadmap.md)
- [计算机系统知识树](maps/computer-systems.md)
- [计算机网络知识树](maps/networking.md)
- [密码学与安全知识树](maps/cybersecurity.md)
- [编程与工程能力树](maps/programming.md)

## 已接入知识库

- [计算机网络](subjects/computer-networking/index.md)
- [操作系统](subjects/operating-system/README.md)
- [密码学引论](subjects/cryptography/README.md)
- [计算机系统原理](subjects/computer-systems/README.md)

## 使用方式

这个仓库负责总览、路线图和跨课程连接。具体课程内容仍在 `subjects/` 下的各子仓库中维护。

更新子模块：

```bash
git submodule update --remote --merge
```

克隆本仓库后拉取子模块：

```bash
git submodule update --init --recursive
```
