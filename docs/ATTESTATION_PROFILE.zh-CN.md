# StateReceipt in-toto / DSSE 互操作说明（简体中文）

[English](ATTESTATION_PROFILE.md) | [Español](ATTESTATION_PROFILE.es.md)

**状态：** StateReceipt v0.1 的探索性互操作设计。签名 attestation 不是 StateReceipt core 的强制要求。

## 设计目标

StateReceipt 应复用成熟的 attestation 与签名标准，而不是自创密码学 envelope。

映射采用 in-toto Statement v1：

```text
in-toto Statement
├── _type
├── subject[]
├── predicateType
└── predicate  ← 完整 StateReceipt 文档
```

如果需要签名，则在 Statement 外层使用 DSSE。

## 无损映射

### `subject`

对 `StateReceipt.snapshot.artifacts` 中每个工件生成一个 in-toto subject：

```json
{
  "name": "<artifact.id>",
  "digest": {
    "<artifact.digest.algorithm>": "<artifact.digest.value>"
  }
}
```

StateReceipt v0.1 支持 SHA-256 和 SHA-512，这两种算法都可以直接映射到 in-toto DigestSet。

使用 `artifact.id` 作为 subject name，因为 StateReceipt 要求同一 Receipt 中工件 ID 唯一。原始路径、media type 等信息继续保存在 predicate 内的 StateReceipt 文档中。

`snapshot.repository` 中的 Git commit 保留在 predicate 内；v0.1 不自动把 Git commit 解释成额外的 in-toto subject。

### `predicateType`

在正式发布 interoperable attestation 之前，项目必须分配稳定、带版本的 predicate TypeURI。

当前项目还没有稳定的规范 URI namespace，因此本草案**不会提前冻结 URI**。示例统一使用：

```text
<STATERECEIPT_PREDICATE_TYPE_URI>
```

### `predicate`

in-toto `predicate` 直接保存**完整且未修改的 StateReceipt 文档**。

因此：

```text
statement.predicate
```

本身就可以还原原始 Receipt，映射不会丢失 Claim、Evidence、snapshot、continuation、predecessor 等 StateReceipt 语义。

## subject / predicate 一致性

外层 `subject` 是 `predicate.snapshot.artifacts` 的 digest 投影，因此会有意产生少量冗余。

StateReceipt-aware consumer 应检查：

1. 每个 `predicate.snapshot.artifacts[*].id` 都存在对应 subject；
2. subject 中的 digest algorithm/value 与 predicate 内工件 digest 完全一致；
3. 除非未来 profile 明确定义，否则不能把额外 subject 静默解释成 StateReceipt snapshot 的一部分。

如果两层不一致，应拒绝或明确标记，而不是猜测哪一层“更正确”。

## 可选 DSSE wrapping

需要 authenticity 时，应该对 **in-toto Statement** 做 DSSE wrapping，而不是只签 raw StateReceipt：

```text
StateReceipt
   ↓ mapping
in-toto Statement
   ↓ serialize
DSSE payload
   ↓ external signer
DSSE Envelope
```

对 in-toto JSON Statement，可以使用通用 payload type：

```text
application/vnd.in-toto+json
```

DSSE 负责 pre-authentication encoding 和签名 envelope。StateReceipt 不定义 PAE、签名算法、key ID、PKI、密钥轮换、透明日志或 trust root。

## 三层验证必须分开

1. **StateReceipt conformance**：predicate 是否符合 StateReceipt，并且确定性工作状态验证是否成立；
2. **Attestation consistency**：in-toto subject 是否与 embedded StateReceipt 的 artifact digest 一致；
3. **Authenticity**：外部 DSSE/signature verifier 是否依据调用者的 trust policy 接受该 envelope。

有效签名并不代表 Claim 为真，只代表相应字节在外部签名策略下通过认证。

## Unsigned Receipt 仍然是一等公民

普通 YAML/JSON StateReceipt 不使用 in-toto 或 DSSE 也仍然完全符合 StateReceipt v0.1。

互操作 profile 是可选增强，不能迫使本地用户配置密钥、PKI、透明服务或网络基础设施。

## 明确不做

StateReceipt 不引入：

- 自定义签名格式；
- 自定义 PAE；
- 密钥管理或 PKI；
- in-toto Statement 的替代品；
- DSSE 的替代品；
- “签名即可证明工作正确”的结论。

英文 [`ATTESTATION_PROFILE.md`](ATTESTATION_PROFILE.md) 是本设计说明的正式来源；如果翻译产生歧义，以英文为准。
