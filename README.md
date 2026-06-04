# Gestor de Gastos e Ingresos CLI 💰

Una aplicación de consola interactiva desarrollada en **Python 3** y **SQLite3** que permite llevar un control ordenado de tus finanzas personales mediante un sistema CRUD completo y la generación de reportes en múltiples formatos (TXT, CSV, JSON).

## 🚀 Características

* **Persistencia de Datos:** Creación automática y gestión de una base de datos local robusta utilizando SQLite3.
* **Operaciones CRUD Completas:**
    * **Crear:** Registro inteligente de ingresos y gastos de forma simultánea o independiente con validación de entradas numéricas.
    * **Leer:** Historial completo ordenado de manera descendente (los más recientes primero) con cálculo automático del saldo total acumulado en tiempo real.
    * **Actualizar:** Modificación de descripción y monto de cualquier movimiento mediante su ID único.
    * **Eliminar:** Borrado seguro de registros específicos por ID con validación de existencia previa.
* **Exportación de Reportes Dinámicos:**
    * **TXT:** Reporte visual estructurado en columnas tabuladas y estéticas.
    * **CSV:** Archivo plano compatible con Microsoft Excel, Google Sheets y softwares contables.
    * **JSON:** Estructura jerárquica con metadatos del reporte ideal para integraciones o desarrollos web futuros.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Base de Datos:** SQLite3 (Librería nativa `sqlite3`)
* **Formatos de Intercambio:** `csv`, `json`
* **Manejo de Fechas:** `datetime`

---