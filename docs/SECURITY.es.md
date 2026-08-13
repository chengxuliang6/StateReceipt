# StateReceipt — Seguridad (Español)

> [`SECURITY.md`](../SECURITY.md) en inglés es la política de seguridad autoritativa. Esta traducción existe para facilitar el acceso; si existe un conflicto, prevalece la versión inglesa.

## Modelo de confianza para replay

La verificación básica de StateReceipt **no ejecuta** comandos registrados en un Receipt de forma predeterminada.

Una verificación normal:

```bash
statereceipt verify receipt.yaml
```

no reejecuta ningún comando.

Usar solamente:

```bash
statereceipt verify receipt.yaml --replay
```

tampoco ejecuta comandos. La CLI rechaza la operación y exige una aceptación explícita adicional:

```bash
--trust-receipt
```

La forma que realmente permite replay es:

```bash
statereceipt verify receipt.yaml --replay --trust-receipt
```

`--trust-receipt` significa únicamente que la persona que ejecuta el comando ha revisado el Receipt y acepta el riesgo de ejecutar sus comandos reproducibles. **No** es autenticación criptográfica, verificación de firma ni autenticación del productor, y no significa que StateReceipt haya determinado que el Receipt es seguro.

## StateReceipt no es un sandbox

StateReceipt **no proporciona** aislamiento de procesos, contenedores, reducción de privilegios, filtrado de llamadas al sistema, confinamiento del sistema de archivos ni aislamiento de red.

Los valores `evidence[].execution.argv` deben tratarse como entrada ejecutable. Antes de habilitar replay:

- inspecciona el Receipt y todos los comandos reproducibles;
- no reejecutes Receipts de fuentes desconocidas o no confiables;
- usa un contenedor desechable, una máquina virtual u otro límite de aislamiento apropiado para comandos de mayor riesgo;
- ejecuta con los mínimos privilegios necesarios;
- recuerda que la validación JSON Schema comprueba estructura, no seguridad del comando.

Versiones futuras pueden añadir hooks de política, pero el núcleo de StateReceipt no afirma que pueda hacer seguro un comando arbitrario.

## Identidad del Receipt

StateReceipt v0.1 no define firmas criptográficas ni autenticación del productor. Un Receipt estructuralmente válido no demuestra la identidad de su autor.
