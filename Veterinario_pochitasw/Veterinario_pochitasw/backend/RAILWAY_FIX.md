# Correcciones Necesarias en Railway

## 1. ACTUALIZAR START COMMAND (CRÍTICO)

En Railway → Settings → Deploy → **Start Command**, cambia de:
```
gunicorn pochita_project.wsgi --log-file -
```

A:
```
bash start.sh
```

## 2. CORREGIR VARIABLES DE ENTORNO (SIN COMILLAS)

En Railway → Variables, **QUITA las comillas dobles** de todas las variables:

**ANTES (INCORRECTO):**
```
DATABASE_URL="postgresql://..."
DJANGO_SECRET_KEY="2qW-..."
DEBUG="False"
ALLOWED_HOSTS="veterinariopochitaswd-production.up.railway.app,*.railway.app"
```

**DESPUÉS (CORRECTO):**
```
DATABASE_URL=postgresql://postgres:yxYaARzdCLiU2YJGD@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres
DJANGO_SECRET_KEY=2qW-Xa5EuShNsg-fuROQoLxfxlyOu0TVCkJQMEQ2DeUN5ieDQK2MNp1bYu8Ge1LrAyY
DEBUG=False
ALLOWED_HOSTS=veterinariopochitaswd-production.up.railway.app,*.railway.app
```

## 3. HACER COMMIT Y PUSH

Después de hacer estos cambios en Railway, haz commit de los cambios del código:

```bash
cd Veterinario_pochitaswd
git add .
git commit -m "Fix Railway deployment: add start.sh script and fix static files"
git push
```

## 4. VERIFICAR DEPLOYMENT

Después del deploy, verifica los logs. Deberías ver:
- "Running migrations..."
- "Collecting static files..."
- "Starting Gunicorn..."

Si hay errores, comparte los logs.

