# StateReceipt (Español)

**Recibos verificables por máquina y asociados a un instante concreto para el estado de trabajo asistido por IA.**

[English](../README.md) | [简体中文](README.zh-CN.md) | Español

StateReceipt es una especificación abierta e independiente del proveedor, junto con una CLI de referencia en Python, para registrar afirmaciones sobre una unidad de trabajo, evidencia vinculada explícitamente, instantáneas de artefactos, dependencias de validez y comprobaciones deterministas de `freshness` / `staleness`.

La pregunta central es concreta: **cuando una tarea asistida por IA se interrumpe, cambia de sesión o pasa a otro agente, ¿qué afirmaciones sobre el trabajo siguen respaldadas por los artefactos actuales?**

## ¿Por qué StateReceipt?

Una nota de traspaso puede decir «las pruebas pasan» o «la implementación está terminada», pero el siguiente desarrollador o agente puede no tener una forma determinista de saber si esa afirmación sigue siendo válida después de que cambien los archivos. StateReceipt representa la afirmación, la evidencia vinculada y la instantánea de artefactos de la que dependía esa evidencia.

```text
Claim ──supported_by──> Evidence ──depends_on──> Artifact digest
  ^                                            |
  |---------------- freshness ----------------|
```

Si cambia un artefacto del que depende una afirmación, la evidencia asociada puede quedar `stale` y la afirmación debe reevaluarse. **`stale` no significa `false`.**

## Inicio rápido en 5 minutos

Sigue el [inicio rápido en Español](QUICKSTART.es.md) para ver `supported → cambio del artefacto → stale` sin ninguna API de LLM. También están disponibles [English](QUICKSTART.md) y [简体中文](QUICKSTART.zh-CN.md).

## Lo que StateReceipt no es

StateReceipt no es una base de datos de memoria persistente, un sistema RAG, un formato de sincronización de chat, un runtime de agentes, un orquestador, un planificador, un sandbox ni un sustituto de Git/CI. El verificador básico tampoco utiliza un LLM para decidir si una afirmación en lenguaje natural es «verdadera».

## Instalación para desarrollo

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
statereceipt validate-chain receipt-a.yaml receipt-b.yaml receipt-c.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml --replay --trust-receipt
statereceipt inspect .statereceipt/receipts/receipt.yaml
statereceipt diff old.yaml new.yaml
```

Replay utiliza un límite de confianza explícito: `--replay` por sí solo es rechazado. Solo se permite ejecutar comandos si, después de revisar el Receipt, también se proporciona `--trust-receipt`. StateReceipt **no proporciona sandboxing** ni autentica al productor del Receipt. Consulta la [guía de seguridad en Español](SECURITY.es.md).

## Capacidades de v0.1

- Validación con JSON Schema Draft 2020-12
- Integridad semántica y de referencias
- Comprobaciones SHA-256 / SHA-512
- Captura y comprobación de commits Git
- Vinculación explícita Claim–Evidence
- Detección de `staleness` por cambios de artefactos
- Evaluación determinista de Claims
- Replay de comandos/pruebas solo con confianza explícita
- Validación de cadenas predecessor para Receipts inmutables
- Inspección y diff con relación de ciclo de vida

## Guías

- [Inicio rápido en 5 minutos](QUICKSTART.es.md)
- [Ciclo de vida y semántica de predecessor](LIFECYCLE.es.md)
- [Seguridad y modelo de confianza de replay](SECURITY.es.md)
- [Perfil opcional de interoperabilidad in-toto / DSSE](ATTESTATION_PROFILE.es.md)
- [Prior art y límites del proyecto (inglés)](../PRIOR_ART.md)

## Especificación y traducciones

La semántica normativa está en [`spec/SPEC.md`](../spec/SPEC.md) y la Schema en [`spec/statereceipt-v0.1.schema.json`](../spec/statereceipt-v0.1.schema.json). **La especificación inglesa de v0.1 es la única fuente normativa.** Si una traducción entra en conflicto con ella, prevalece el inglés.

## Contribución y seguridad

Consulta [`CONTRIBUTING.md`](../CONTRIBUTING.md) antes de proponer cambios. Antes de replay, consulta la [guía de seguridad en Español](SECURITY.es.md); [`SECURITY.md`](../SECURITY.md) en inglés es la política autoritativa.

## Licencia

Apache-2.0. Consulta [`LICENSE`](../LICENSE).
