# StateReceipt Receipt 生命周期（简体中文）

[English](LIFECYCLE.md) | [Español](LIFECYCLE.es.md)

> 正式的生命周期规则以 [`spec/SPEC.md`](../spec/SPEC.md) 为准。本文件用于说明与上手。

StateReceipt 的 Receipt 是不可变的时间点工件。后续工作应生成新的 Receipt，而不是修改已经签发的旧 Receipt。

## 直接 predecessor

后续 Receipt 可以声明一个直接 predecessor：

```yaml
receipt:
  id: SR-B
  predecessor:
    id: SR-A
```

这表示 `SR-B` 直接延续 `SR-A` 所记录的工作状态。

Receipt 不能把自己设为 predecessor。predecessor ID 也可以指向当前本地不存在的 Receipt；StateReceipt v0.1 不定义全局 Receipt 注册表，也不要求网络解析。

## 示例链

```text
SR-A (interrupted)
  ↓
SR-B (in_progress)
  ↓
SR-C (completed)
```

这些 work state 不是由 StateReceipt 控制的有限状态机，只是不同时间点的记录。

## 验证本地链集合

```bash
statereceipt validate-chain sr-a.yaml sr-b.yaml sr-c.yaml
```

该命令会拒绝：

- 当前集合内重复的 Receipt ID；
- predecessor 自引用；
- 在当前集合内可以解析出的 predecessor cycle。

如果 predecessor 不在当前输入文件中，会被报告为 external/unresolved，但仅凭这一点不会判定链无效。

## Diff 不代表一定存在链关系

```bash
statereceipt diff sr-a.yaml sr-b.yaml
```

结果会包含 `lifecycle_relation`：

- `same_receipt`
- `direct_successor`
- `direct_predecessor`
- `not_directly_linked`

`not_directly_linked` 只表示两份输入 Receipt 不是直接相邻关系，并不能证明它们完全无关；它们仍可能是更长链中的非相邻成员。
