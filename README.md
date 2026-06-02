# 💰 Gestor de Gastos e Ingresos con SQLite

¡Bienvenido! Este es un proyecto interactivo desarrollado en Python que funciona a través de la consola. Está diseñado para ayudar a los usuarios a llevar un control financiero básico, permitiendo registrar movimientos, consultar el historial con saldos acumulados y eliminar registros de forma segura.

Este proyecto demuestra el uso de bases de datos relacionales locales, control de excepciones y validación de datos en entornos interactivos.

---

## 🚀 Características del Proyecto

- **Persistencia de Datos:** Utiliza **SQLite3** para almacenar de forma permanente todos los movimientos en una base de datos local (`Gestor_Gastos.db`).
- **Operaciones CRUD Básicas:** - **Crear:** Registro inteligente de ingresos y gastos de forma independiente.
  - **Leer:** Historial formateado en columnas con cálculo automático de **Saldo Total Acumulado** en tiempo real.
  - **Borrar:** Eliminación selectiva de registros mediante su identificador único (`ID`).
- **Control de Errores Robusto:** Validación de entradas para evitar que el usuario ingrese letras donde van números, montos negativos o IDs inexistentes.
- **Cierre Seguro de Conexiones:** Arquitectura protegida con bloques `try/except/finally` para prevenir corrupciones o bloqueos en la base de datos.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3**
- **SQLite3** (Motor de base de datos integrado)
- **Datetime** (Para el sellado de tiempo automático de cada transacción)