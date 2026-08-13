# StateReceipt — Ciclo de vida de Receipts (Español)

[English](LIFECYCLE.md) | [简体中文](LIFECYCLE.zh-CN.md)

> Las reglas normativas del ciclo de vida están en [`spec/SPEC.md`](../spec/SPEC.md). Este documento es explicativo.

Los Receipts de StateReceipt son artefactos inmutables asociados a un instante concreto. El trabajo posterior debe producir un nuevo Receipt en lugar de modificar uno ya emitido.

## Predecessor directo

Un Receipt posterior puede identificar un único predecessor directo:

```yaml
receipt:
  id: SR-B
  predecessor:
    id: SR-A
```

Esto significa que `SR-B` continúa directamente el estado de trabajo representado por `SR-A`.

Un Receipt no puede nombrarse a sí mismo como predecessor. Un ID de predecessor puede apuntar a un Receipt que no esté disponible localmente; StateReceipt v0.1 no define un registro global ni exige resolución por red.

## Cadena de ejemplo

```text
SR-A (interrupted)
  ↓
SR-B (in_progress)
  ↓
SR-C (completed)
```

Los estados de trabajo no forman una máquina de estados controlada por StateReceipt. Son instantáneas registradas.

## Validar un conjunto local de cadena

```bash
statereceipt validate-chain sr-a.yaml sr-b.yaml sr-c.yaml
```

El comando rechaza:

- IDs de Receipt duplicados dentro del conjunto suministrado;
- autorreferencias de predecessor;
- ciclos que puedan resolverse dentro del conjunto suministrado.

Si un predecessor no está presente en los archivos suministrados, se informa como external/unresolved, pero eso por sí solo no invalida el conjunto.

## Diff no implica linaje

```bash
statereceipt diff sr-a.yaml sr-b.yaml
```

El resultado incluye `lifecycle_relation` con uno de estos valores:

- `same_receipt`
- `direct_successor`
- `direct_predecessor`
- `not_directly_linked`

`not_directly_linked` solo significa que los dos Receipts suministrados no son vecinos directos. Aún podrían ser miembros no adyacentes de una cadena más larga.
