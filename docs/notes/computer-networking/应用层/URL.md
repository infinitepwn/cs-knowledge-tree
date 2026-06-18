# URL

> 来源：`计算机网络 / 应用层/URL.md`

URL（Uniform Resource Locator，统一资源定位符）用于指出互联网上某个资源的位置以及访问该资源的方法。

## 基本格式

```text
协议://主机:端口/路径
```

例如：

```text
http://www.example.com:80/index.html
```

- 协议：说明使用什么应用层协议，例如 HTTP、HTTPS、FTP。
- 主机：资源所在服务器的域名或 IP 地址。
- 端口：服务器应用进程使用的端口号，省略时使用协议默认端口。
- 路径：服务器上的具体资源位置。

## URL 与 URI

URI 是统一资源标识符，范围更大；URL 是 URI 的一种，强调资源的位置和访问方式。

## 相关笔记
- [万维网](万维网.md)
- [HTTP](HTTP.md)
- [DNS](DNS.md)
