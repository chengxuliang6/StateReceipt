# StateReceipt — Inicio rápido en 5 minutos

[English](QUICKSTART.md) | [简体中文](QUICKSTART.zh-CN.md)

Este tutorial no necesita ninguna API de LLM. Muestra el comportamiento central de StateReceipt con un ejemplo mínimo: una Claim comienza como `supported` y pasa a `stale` cuando cambia el artefacto del que depende.

## 1. Instalar la versión de desarrollo

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## 2. Crear un artefacto mínimo

El mismo comando funciona en Windows, macOS y Linux:

```bash
python -c "from pathlib import Path; Path('quickstart-demo.txt').write_text('version 1\n', encoding='utf-8')"
```

## 3. Inicializar y capturar un Receipt

```bash
statereceipt init
statereceipt capture quickstart-demo.txt --work-id DEMO-1 --objective "Track a tiny artifact"
```

El Receipt se crea por defecto en:

```text
.statereceipt/receipts/receipt.yaml
```

Incluye el digest del artefacto, Artifact Evidence, una Claim sobre el estado capturado y dependencias explícitas de validez.

## 4. Verificar el artefacto sin cambios

```bash
statereceipt verify .statereceipt/receipts/receipt.yaml
```

El resultado de la Claim debe incluir:

```text
claim-capture: supported
```

Esto ocurre porque el archivo actual sigue coincidiendo con el digest capturado en el Receipt y la Evidence continúa siendo válida.

## 5. Modificar el artefacto

```bash
python -c "from pathlib import Path; Path('quickstart-demo.txt').write_text('version 2\n', encoding='utf-8')"
```

Ahora el archivo ya no coincide con la instantánea puntual almacenada en el Receipt.

## 6. Verificar de nuevo

```bash
statereceipt verify .statereceipt/receipts/receipt.yaml
```

La Claim debe pasar a:

```text
claim-capture: stale
```

`stale` **no significa** que la Claim sea falsa. Significa que la Evidence capturada anteriormente ya no puede respaldar de forma segura el estado actual del artefacto.

## ¿Qué ocurrió?

```text
T0
quickstart-demo.txt digest = A
        ↓
Artifact Evidence válida
        ↓
claim-capture = supported

T1
quickstart-demo.txt digest = B
        ↓
dependencia capturada invalidada
        ↓
claim-capture = stale
```

Esta es la idea central de StateReceipt: las afirmaciones sobre el estado del trabajo se vinculan a Evidence explícita y a artefactos de un instante concreto, en lugar de confiar ciegamente en una nota de traspaso en lenguaje natural.

## Limpieza

```bash
python -c "from pathlib import Path; p=Path('quickstart-demo.txt'); p.unlink() if p.exists() else None"
```

También puedes eliminar `.statereceipt/` después del ejemplo.
