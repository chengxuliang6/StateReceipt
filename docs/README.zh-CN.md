# StateReceipt（简体中文）

**用于 AI 辅助工作状态的机器可验证、时间点式凭证。**

[English](../README.md) | 简体中文 | [Español](README.es.md)

StateReceipt 是一个开放、厂商中立的规范与 Python 参考 CLI，用于记录某个工作单元的状态声明、显式证据、工件快照、有效性依赖以及确定性的 freshness/staleness 检查。

它要解决的问题很具体：**当 AI 辅助任务被中断、切换会话或交给另一个 agent 后，之前关于“已经完成了什么”的哪些声明仍然被当前工件支持？**

## 为什么需要 StateReceipt？

普通交接说明可以写“测试通过”或“实现已经完成”，但接手者往往无法确定这些结论在文件发生变化后是否仍然成立。StateReceipt 将声明、证据与工件快照显式绑定，并允许验证器确定支持是否已经过期。

```text
Claim ──supported_by──> Evidence ──depends_on──> Artifact digest
  ^                                            |
  |---------------- freshness ----------------|
```

当声明依赖的工件发生变化时，相关证据可能变为 `stale`，声明需要重新评估。**`stale` 不等于 `false`。** 它只表示原先的支持已经不能安全地应用于当前状态。

## 5 分钟快速上手

如果你想马上看到 StateReceipt 的核心效果，可以直接按照 [中文快速上手](QUICKSTART.zh-CN.md) 操作。

它会完整演示：

```text
supported → 修改工件 → stale
```

整个示例不需要任何 LLM API，也可以切换到 [English](QUICKSTART.md) 或 [Español](QUICKSTART.es.md) 版本。

## StateReceipt 不是什么

StateReceipt 不是 AI 长期记忆数据库、RAG / 向量数据库、聊天记录同步格式、agent runtime、多 agent 编排器、任务调度系统、sandbox，也不是 Git 或 CI 的替代品。核心 verifier 不会调用 LLM 去判断自然语言声明“是否为真”；基础验证保持确定性。

## 开发安装

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## CLI

```bash
statereceipt init
statereceipt capture src/app.py tests/test_app.py --work-id AUTH-17 --objective "Implement auth middleware"
statereceipt validate .statereceipt/receipts/receipt.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml --replay --trust-receipt
statereceipt inspect .statereceipt/receipts/receipt.yaml
statereceipt diff old.yaml new.yaml
```

Replay 采用显式信任边界：单独使用 `--replay` 会被拒绝，只有在检查 Receipt 后同时提供 `--trust-receipt` 才允许执行。StateReceipt **不提供 sandbox**，也不验证 Receipt producer 的身份。详见 [中文安全说明](SECURITY.zh-CN.md)。

## v0.1 核心能力

- JSON Schema Draft 2020-12 校验
- 语义与引用完整性校验
- SHA-256 / SHA-512 工件完整性检查
- Git commit 捕获与校验
- 显式 Claim–Evidence 绑定
- 基于工件变化的 staleness 检测
- 确定性 claim evaluation
- 需要显式信任的 command/test replay
- Receipt inspect 与 diff

## Claim 状态的确定性规则

v0.1 按以下顺序评估 Claim：

1. 存在有效的 `contradicted_by` 证据 → `contradicted`
2. 显式 `depends_on` 依赖已 stale / missing / invalid → `stale`
3. 至少一个独立 supporting evidence 仍有效 → `supported`
4. 所有 supporting evidence 都已失效 → `stale`
5. 支持证据中仍有未知状态 → `unknown`
6. 没有 supporting evidence → `unsupported`

该顺序是规范的一部分，独立实现不得自行调整优先级。

## 示例领域

同一套 v0.1 Schema 已用于三个不同领域：Python 软件开发、FPGA / Verilog 工程，以及 MATLAB / 科研仿真。

## 规范与翻译说明

正式规范位于 [`spec/SPEC.md`](../spec/SPEC.md)，机器可读 Schema 位于 [`spec/statereceipt-v0.1.schema.json`](../spec/statereceipt-v0.1.schema.json)。**v0.1 的英文规范是唯一 normative source。** 若翻译与英文规范冲突，以英文规范为准。

## 贡献与安全

提交规范或实现变更前请阅读 [`CONTRIBUTING.md`](../CONTRIBUTING.md)。Replay 前请阅读 [中文安全说明](SECURITY.zh-CN.md)；英文 [`SECURITY.md`](../SECURITY.md) 是正式安全策略。

## 许可证

Apache-2.0，见 [`LICENSE`](../LICENSE)。
