# StateReceipt — Perfil de interoperabilidad in-toto / DSSE (Español)

[English](ATTESTATION_PROFILE.md) | [简体中文](ATTESTATION_PROFILE.zh-CN.md)

**Estado:** diseño exploratorio de interoperabilidad para StateReceipt v0.1. Las attestations firmadas no son un requisito del núcleo.

## Objetivo

StateReceipt debe reutilizar estándares existentes de attestation y firma en lugar de inventar un envelope criptográfico propio.

El mapeo usa in-toto Statement v1:

```text
in-toto Statement
├── _type
├── subject[]
├── predicateType
└── predicate  ← documento StateReceipt completo
```

Si se requiere firma, DSSE se aplica por fuera del Statement.

## Mapeo sin pérdida

### `subject`

Por cada elemento de `StateReceipt.snapshot.artifacts`, se genera un subject de in-toto:

```json
{
  "name": "<artifact.id>",
  "digest": {
    "<artifact.digest.algorithm>": "<artifact.digest.value>"
  }
}
```

StateReceipt v0.1 permite SHA-256 y SHA-512, que se pueden representar directamente en DigestSet de in-toto.

Se usa `artifact.id` como nombre porque los IDs de artefacto son únicos dentro de un Receipt. La ruta, media type y demás semántica original permanecen dentro del StateReceipt embebido en el predicate.

El commit Git de `snapshot.repository`, cuando existe, permanece dentro del predicate; v0.1 no lo convierte automáticamente en un subject adicional.

### `predicateType`

Antes de publicar interoperabilidad de producción debe asignarse un TypeURI estable y versionado.

Como el proyecto todavía no tiene un namespace estable de especificación, este borrador **no congela prematuramente un URI**. Los ejemplos usan:

```text
<STATERECEIPT_PREDICATE_TYPE_URI>
```

### `predicate`

El `predicate` de in-toto contiene el documento StateReceipt completo y sin modificaciones.

Por ello:

```text
statement.predicate
```

reconstruye el Receipt original sin perder Claims, Evidence, snapshot, continuation, predecessor u otra semántica de StateReceipt.

## Consistencia entre subject y predicate

El `subject` externo es una proyección de los digests de `predicate.snapshot.artifacts`, por lo que existe redundancia deliberada.

Un consumidor compatible con StateReceipt debería comprobar que:

1. cada `predicate.snapshot.artifacts[*].id` tiene un subject correspondiente;
2. algoritmo y valor del digest coinciden exactamente;
3. ningún subject adicional se interpreta silenciosamente como parte del snapshot salvo que un perfil posterior lo defina.

Si ambas capas no coinciden, el consumidor debe rechazar o señalar explícitamente la discrepancia en vez de adivinar cuál es correcta.

## DSSE opcional

Si se necesita autenticidad, debe envolverse el **in-toto Statement**, no únicamente el StateReceipt crudo:

```text
StateReceipt
   ↓ mapping
in-toto Statement
   ↓ serialize
DSSE payload
   ↓ external signer
DSSE Envelope
```

Para un Statement JSON de in-toto puede usarse el payload type genérico:

```text
application/vnd.in-toto+json
```

DSSE se ocupa de pre-authentication encoding y del envelope de firma. StateReceipt no define PAE, algoritmos de firma, key IDs, PKI, rotación de claves, transparency logs ni trust roots.

## Tres capas de verificación separadas

1. **StateReceipt conformance**: el predicate es un StateReceipt válido y sus comprobaciones deterministas son coherentes;
2. **Attestation consistency**: los subjects de in-toto coinciden con los digests del StateReceipt embebido;
3. **Authenticity**: un verificador externo de DSSE/firma acepta el envelope bajo la política de confianza elegida por el consumidor.

Una firma válida no demuestra que una Claim sea verdadera; autentica bytes bajo una política externa.

## Los Receipts sin firma siguen siendo de primera clase

Un StateReceipt YAML/JSON normal sigue siendo plenamente conforme sin in-toto ni DSSE.

Este perfil es opcional y aditivo. No debe obligar a usuarios locales a configurar claves, PKI, servicios de transparencia ni infraestructura de red.

## No objetivos

StateReceipt no introduce:

- un formato de firma propio;
- un PAE propio;
- gestión de claves o PKI;
- un sustituto de in-toto Statement;
- un sustituto de DSSE;
- la afirmación de que una firma criptográfica prueba la corrección del trabajo.

El archivo inglés [`ATTESTATION_PROFILE.md`](ATTESTATION_PROFILE.md) es la fuente autoritativa de esta nota; si una traducción difiere, prevalece el inglés.
