# Configuración Completa de Railway - CORREGIDA

## 🔴 PROBLEMA DETECTADO

El Build Command está ejecutando `gunicorn`, lo cual causa que se quede trabado. El Build Command NO debe ejecutar la aplicación.

## ✅ CONFIGURACIÓN CORRECTA

### 1. VARIABLES DE ENTORNO (SIN COMILLAS)

En Railway → Variables, configura estas 4 variables **SIN comillas dobles**:

```
DATABASE_URL=postgresql://postgres:Eco235713.-@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres
```

```
DJANGO_SECRET_KEY=2qW-Xa5EuShNsg-fuROQoLxfxlyOu0TVCkJQMEQ2DeUN5ieDQK2MNp1bYu8Ge1LrAyY
```

```
DEBUG=False
```

```
ALLOWED_HOSTS=veterinariopochitaswd-production.up.railway.app,*.railway.app
```

### 2. BUILD COMMAND (DEBE ESTAR VACÍO)

En Railway → Settings → Build → **Build Command**:
- **DÉJALO VACÍO** o elimínalo completamente
- NO debe tener `gunicorn` ni comandos de inicio

### 3. PRE-DEPLOY COMMAND

En Railway → Settings → Deploy → **Pre-deploy command**:

```
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

### 4. START COMMAND

En Railway → Settings → Deploy → **Start command**:

```
gunicorn pochita_project.wsgi --log-file - --timeout 120 --workers 2 --bind 0.0.0.0:${PORT:-8080}
```

## 📋 RESUMEN DE CAMBIOS NECESARIOS

1. ✅ **Variables**: Actualizar `DATABASE_URL` con nueva contraseña `Eco235713.-` y quitar comillas de todas
2. ✅ **Build Command**: Eliminar completamente (dejar vacío)
3. ✅ **Pre-deploy**: `python manage.py migrate --noinput && python manage.py collectstatic --noinput`
4. ✅ **Start Command**: `gunicorn pochita_project.wsgi --log-file - --timeout 120 --workers 2 --bind 0.0.0.0:${PORT:-8080}`

## 🚀 DESPUÉS DE CONFIGURAR

1. Guarda todos los cambios en Railway
2. Haz un nuevo deploy (push a GitHub o manual)
3. Verifica en Supabase → Table Editor que se crearon las tablas
4. Accede al frontend: https://veterinariopochitaswd-production.up.railway.app/api/inicio/

