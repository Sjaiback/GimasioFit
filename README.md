# Control Fit

Backend Django para administracion de gimnasio.

## Primer commit: backend

- Migracion desde Flask a Django.
- Base de datos configurada para PostgreSQL por variables de entorno.
- Apps separadas por dominio: cuentas, socios, membresias, pagos, reportes y notificaciones.
- Endpoints JSON para gestion operativa y dashboard administrativo.
- Login obligatorio y roles operativos: administrador, encargado y recepcion.

## Roles

- Administrador: acceso completo.
- Encargado: gestion operativa, membresias, reportes y verificaciones.
- Recepcion: socios, pagos basicos y asistencia.

## Configuracion local

1. Crear y activar un entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Crear una base PostgreSQL y copiar `.env.example` a `.env`.
4. Ejecutar migraciones:

```bash
python manage.py migrate
```

5. Levantar el servidor:

```bash
python manage.py runserver
```
