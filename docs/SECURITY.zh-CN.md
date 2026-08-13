# StateReceipt 安全说明（简体中文）

> 英文 [`SECURITY.md`](../SECURITY.md) 是安全策略的正式来源。本文件是便于阅读的翻译；若存在冲突，以英文版本为准。

## Replay 信任模型

StateReceipt 的基础验证默认**不会执行** Receipt 中记录的命令。

普通验证：

```bash
statereceipt verify receipt.yaml
```

不会 replay 任何命令。

仅指定：

```bash
statereceipt verify receipt.yaml --replay
```

也不会执行。CLI 会拒绝，并要求调用者额外显式声明：

```bash
--trust-receipt
```

因此真正允许执行 replay 的形式是：

```bash
statereceipt verify receipt.yaml --replay --trust-receipt
```

`--trust-receipt` 只表示调用者已经检查该 Receipt，并接受执行其中 replayable command 的风险。它**不是**密码学认证、签名检查或 producer 身份验证，也不意味着 StateReceipt 已确认该 Receipt 安全。

## StateReceipt 不是 sandbox

StateReceipt **不提供**进程隔离、容器隔离、权限降级、系统调用过滤、文件系统限制或网络隔离。

`evidence[].execution.argv` 应被视为可执行输入。启用 replay 前应：

- 检查 Receipt 以及所有可 replay 的命令；
- 不 replay 未知或不可信来源的 Receipt；
- 对高风险命令使用一次性容器、虚拟机或其他合适的隔离环境；
- 使用完成任务所需的最小权限运行；
- 不要把 JSON Schema validation 当作命令安全审核。

未来版本可能加入策略 hook，但 StateReceipt core 不会声称能让任意命令安全执行。

## Receipt 身份

StateReceipt v0.1 不定义密码学签名或 producer authentication。结构合法的 Receipt 并不能证明作者身份。
