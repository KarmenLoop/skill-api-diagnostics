# API Diagnostics · API 诊断

[English](README.md) | 简体中文

API 调用失败后，先弄清楚该修哪里。输入已有请求记录、剩余时间和操作是否允许重放，得到故障分类与有边界的重试建议。

[下载 v0.2.1](https://github.com/KarmenLoop/skill-api-diagnostics/releases/tag/v0.2.1) · [完整教程](docs/tutorial.zh-CN.md) · [输入参考（英文）](docs/INPUT.md) · [反馈问题](https://github.com/KarmenLoop/skill-api-diagnostics/issues)

## 能做什么

样例记录一次 503 响应，剩余 26 秒；由于 replay_safe 为 true，结果建议等待 2 秒。

工具只分析记录，不会发起 HTTP 请求；操作能否安全重放，需要由真实接口约定确认。

![API 诊断 0.2.1 版本样例的真实 JSON 输出](docs/images/example-output-v0.2.1.svg)

*图片来自 v0.2.1 的真实本地输出，采用英文键名；[完整结果](examples/expected.json) · [图片来源记录](docs/images/provenance.json)。*

## 开始使用

在发行页下载 `karmen-api-diagnostics-v0.2.1.zip` 与对应 `.sha256` 文件，核对哈希后解压。在解压目录中使用 Python 3.9 或更新版本：

```sh
python3 scripts/run.py --version
python3 scripts/run.py --input examples/input.json
```

预期版本：`karmen-api-diagnostics 0.2.1`。样例记录一次 503 响应，剩余 26 秒；由于 replay_safe 为 true，结果建议等待 2 秒。

如果宿主读取 `~/.agents/skills`，可安装完整技能：

```sh
python3 install.py --host agents
```

目标目录已存在时安装器会拒绝覆盖。宿主发现和调用方式可能不同，见[安装与实践教程](docs/tutorial.zh-CN.md)。不使用 AI 宿主也能直接运行本地工具。

## 用于自己的任务

根据接口真实约定填写 replay_safe，并记录 elapsed_seconds 和服务端 Retry-After；余额耗尽等硬额度限制使用 quota。

分别尝试 401 响应和已耗尽预算，比较 next_action 与 retry_allowed，再决定调用方如何处理。

准备新输入前可查看[字段约定（英文）](docs/INPUT.md)。工具只依赖 Python 标准库，本身不需要模型账号、API 密钥或网络。使用 AI 宿主时，宿主有自己的数据与权限设置。

## 常见问题

**它会重试失败的支付吗？** 不会。工具不发送请求，也不授予重试权限。支付操作是否幂等，需要查看支付服务的约定。

**结果保存在哪里？** 默认向终端输出 JSON；使用 `--output` 时只创建新文件，已有输出文件会保留。工具只读取提交的记录和输入约定中明确列出的本地路径。

## 文档与支持

- [下载、安装、配置、练习、升级与卸载](docs/tutorial.zh-CN.md)
- [输入输出约定](docs/INPUT.md)与[兼容性说明](docs/COMPATIBILITY.md)（英文参考）
- [更新记录](CHANGELOG.md)、[参与贡献](CONTRIBUTING.md)、[支持](SUPPORT.md)和[安全反馈](SECURITY.md)

## 许可证

[MIT](LICENSE)。再分发时保留许可证和[声明](NOTICE.md)。由 [KarmenLoop](https://karmenloop.com) 维护。
