# 输入与输出

[English](INPUT.md) | 简体中文 · [教程](tutorial.zh-CN.md)

对应 **v0.2.1**。输入为 UTF-8 JSON 对象，最大 10 MiB。支持 --input 文件路径与 --input -；拒绝重复 JSON 键和非有限常量。

| 字段 | 约定 |
| --- | --- |
| endpoint | HTTP(S) 地址，输出移除账号、查询和片段。 |
| budget_seconds / elapsed_seconds | 非负数，分别为总预算与已用秒数。 |
| replay_safe | 布尔值，依据真实操作是否允许重放来确定。 |
| attempts | 非空数组。每项使用唯一 id；status 可选，整数 100–599；error_kind 为 dns、tls、timeout、connection、context、quota 或 none；retry_after_seconds 可选。余额或硬额度耗尽用 quota。 |

## 样例

```json
{
  "endpoint": "https://api.example.com/v1/chat/completions",
  "budget_seconds": 30,
  "elapsed_seconds": 4,
  "replay_safe": true,
  "attempts": [
    {
      "id": "1",
      "status": 503,
      "error_kind": "none",
      "retry_after_seconds": 2
    }
  ]
}
```

[完整预期结果](../examples/expected.json)。JSON 键名保留英文以匹配程序接口；字符串内容使用你的实际记录。退出码 0 代表处理完成，不代表所报告问题已经通过。

## 错误与副作用

工具不联网，不执行提交的命令。只读取输入及约定中明确指出的本地路径；默认向终端输出，只在明确 --output 时写入新文件。无效输入退出码为 2，已有结果文件不覆盖。写入失败可能留下不完整新文件，应先检查。安装是独立的明确操作。
