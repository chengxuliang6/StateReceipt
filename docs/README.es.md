# StateReceipt (Español)

**Recibos verificables por máquina y asociados a un instante concreto para el estado de trabajo asistido por IA.**

[English](../README.md) | [简体中文](README.zh-CN.md) | Español

StateReceipt es una especificación abierta e independiente del proveedor, junto con una CLI de referencia en Python, para registrar afirmaciones sobre una unidad de trabajo, la evidencia vinculada explícitamente a esas afirmaciones, instantáneas de artefactos, dependencias de validez y comprobaciones deterministas de vigencia (`freshness` / `staleness`).

La pregunta central es deliberadamente concreta: **cuando una tarea asistida por IA se interrumpe, cambia de sesión o pasa a otro agente, ¿qué afirmaciones sobre el trabajo siguen respaldadas por los artefactos actuales?**

## ¿Por qué StateReceipt?

Una nota de traspaso puede decir «las pruebas pasan» o «la implementación está terminada», pero el siguiente desarrollador o agente puede no tener una forma determinista de saber si esa afirmación sigue siendo válida después de que cambien los archivos. StateReceipt representa la afirmación, la evidencia vinculada y la instantánea de artefactos de la que dependía esa evidencia.

```text
Claim ──supported_by──> Evidence ──depends_on──> Artifact digest
  ^                                            |
  |---------------- freshness ----------------|
```

Si cambia un artefacto del que depende una afirmación, la evidencia asociada puede quedar `stale` y la afirmación debe reevaluarse. **`stale` no significa `false`.** Significa que el respaldo anterior ya no puede aplicarse de forma segura al estado actual.

## Inicio rápido en 5 minutos

Para ver el comportamiento central inmediatamente, sigue el [inicio rápido en Español](QUICKSTART.es.md).

El recorrido muestra:

```text
supported → cambio del artefacto → stale
```

No necesita ninguna API de LLM. También están disponibles las versiones [English](QUICKSTART.md) y [简体中文](QUICKSTART.zh-CN.md).

## Lo que StateReceipt no es

StateReceipt no es:

- una base de datos de memoria persistente para IA
- un sistema RAG o base vectorial
- un formato para sincronizar historiales de chat
- un runtime de agentes
- un orquestador multiagente
- un planificador de tareas
- un sustituto de Git o CI

El verificador básico tampoco utiliza un LLM para decidir si una afirmación en lenguaje natural es «verdadera»; la verificación fundamental permanece determinista.

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
statereceipt verify .statereceipt/receipts/receipt.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml --replay
statereceipt inspect .statereceipt/receipts/receipt.yaml
statereceipt diff old.yaml new.yaml
```

## Capacidades de v0.1

- Validación con JSON Schema Draft 2020-12
- Validación semántica y de integridad de referencias
- Comprobaciones SHA-256 / SHA-512 de artefactos
- Captura y comprobación de commits Git
- Vinculación explícita Claim–Evidence
- Detección de `staleness` impulsada por cambios de artefactos
- Evaluación determinista de afirmaciones
- Reejecución opcional de comandos/pruebas reproducibles
- Inspección y comparación de receipts

## Reglas deterministas para el estado de una Claim

v0.1 evalúa cada Claim en este orden:

1. Evidencia válida en `contradicted_by` → `contradicted`
2. Una dependencia explícita en `depends_on` está stale / missing / invalid → `stale`
3. Al menos una evidencia de soporte independiente sigue siendo válida → `supported`
4. Toda la evidencia de soporte ha quedado invalidada → `stale`
5. Parte del soporte permanece en estado desconocido → `unknown`
6. No existen referencias de soporte → `unsupported`

El orden forma parte de la especificación y no debe reordenarse en implementaciones independientes.

## Dominios de ejemplo

La misma Schema v0.1 se prueba en tres flujos de trabajo distintos:

- Desarrollo de software Python: `examples/python-auth.yaml`
- Ingeniería FPGA / Verilog: `examples/fpga-verilog.yaml`
- Simulación MATLAB / investigación: `examples/matlab-qpsk.yaml`

## Especificación y traducciones

La semántica normativa está en [`spec/SPEC.md`](../spec/SPEC.md) y la Schema legible por máquina está en [`spec/statereceipt-v0.1.schema.json`](../spec/statereceipt-v0.1.schema.json).

**La especificación inglesa de v0.1 es la única fuente normativa.** Esta traducción existe para facilitar el acceso. Si existe cualquier conflicto entre la traducción y `spec/SPEC.md`, prevalece el texto normativo en inglés. Esto evita divergencias en términos como MUST / SHOULD / MAY.

## Contribución y seguridad

Consulta [`CONTRIBUTING.md`](../CONTRIBUTING.md) antes de proponer cambios en la especificación o la implementación. Antes de usar `--replay` con receipts de una fuente no confiable, consulta [`SECURITY.md`](../SECURITY.md).

## Licencia

Apache-2.0. Consulta [`LICENSE`](../LICENSE).
