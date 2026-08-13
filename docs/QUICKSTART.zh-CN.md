# StateReceipt 5 分钟快速上手

[English](QUICKSTART.md) | [Español](QUICKSTART.es.md)

本教程不需要任何 LLM API，用一个最小示例演示 StateReceipt 的核心行为：一个 Claim 起初是 `supported`，当它依赖的工件发生变化后，会变成 `stale`。

## 1. 安装开发版本

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## 2. 创建一个最小工件

下面这条命令可在 Windows、macOS 和 Linux 使用：

```bash
python -c "from pathlib import Path; Path('quickstart-demo.txt').write_text('version 1\n', encoding='utf-8')"
```

## 3. 初始化并生成 Receipt

```bash
statereceipt init
statereceipt capture quickstart-demo.txt --work-id DEMO-1 --objective "Track a tiny artifact"
```

Receipt 默认生成在：

```text
.statereceipt/receipts/receipt.yaml
```

其中包含工件摘要、Artifact Evidence、关于捕获状态的 Claim，以及显式有效性依赖。

## 4. 验证未变化的工件

```bash
statereceipt verify .statereceipt/receipts/receipt.yaml
```

Claim 结果应包含：

```text
claim-capture: supported
```

原因是当前文件仍与 Receipt 中捕获的 digest 一致，因此相关 Evidence 仍然有效。

## 5. 修改工件

```bash
python -c "from pathlib import Path; Path('quickstart-demo.txt').write_text('version 2\n', encoding='utf-8')"
```

现在文件已经不再匹配 Receipt 保存的时间点快照。

## 6. 再次验证

```bash
statereceipt verify .statereceipt/receipts/receipt.yaml
```

这一次 Claim 应变成：

```text
claim-capture: stale
```

`stale` **不等于** Claim 为假。它表示之前捕获的 Evidence 已经不能继续安全地支持当前工件状态。

## 发生了什么？

```text
T0
quickstart-demo.txt digest = A
        ↓
Artifact Evidence 有效
        ↓
claim-capture = supported

T1
quickstart-demo.txt digest = B
        ↓
捕获时依赖失效
        ↓
claim-capture = stale
```

这就是 StateReceipt 的核心：工作状态声明不依赖接手者盲目信任自然语言交接，而是与显式 Evidence 和时间点工件绑定。

## 清理

```bash
python -c "from pathlib import Path; p=Path('quickstart-demo.txt'); p.unlink() if p.exists() else None"
```

演示结束后也可以删除 `.statereceipt/` 目录。
