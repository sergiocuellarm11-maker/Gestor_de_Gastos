💰 Gestor de Gastos e Ingresos con SQLite
¡Bienvenido! Este es un proyecto interactivo desarrollado en Python que funciona a través de la consola. Está diseñado para ayudar a los usuarios a llevar un control financiero básico, permitiendo registrar movimientos, consultar el historial con saldos acumulados, modificar registros y eliminarlos de forma segura.

Este proyecto demuestra el uso de bases de datos relacionales locales, control de excepciones y validación de datos en entornos interactivos.

🚀 Características del Proyecto
Persistencia de Datos: Utiliza SQLite3 para almacenar de forma permanente todos los movimientos en una base de datos local (Gestor_Gastos.db).

Operaciones CRUD Completas:

Crear (Create): Registro inteligente de ingresos y gastos de forma independiente con sellado de tiempo automático.

Leer (Read): Historial formateado en columnas legibles con cálculo automático del Saldo Total Acumulado en tiempo real.

Actualizar (Update): Modificación selectiva de la descripción y el monto de cualquier movimiento mediante su identificador único (ID).

Borrar (Delete): Eliminación segura de registros específicos por ID.

Control de Errores Robusto: Validación estricta de entradas para evitar que el usuario ingrese texto en campos numéricos, montos negativos o intente operar con IDs inexistentes.

Cierre Seguro de Conexiones: Arquitectura protegida con bloques try/except/finally que garantizan el cierre de la base de datos incluso si ocurren errores en la ejecución, previniendo corrupciones o bloqueos de archivos.

🛠️ Tecnologías Utilizadas
Python 3

SQLite3 (Motor de base de datos relacional integrado)

Datetime (Para el registro exacto de la fecha y hora de cada transacción)