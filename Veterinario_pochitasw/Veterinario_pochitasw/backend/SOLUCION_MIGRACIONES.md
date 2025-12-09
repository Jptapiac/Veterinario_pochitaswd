# Solución: Ejecutar Migraciones en Railway

## Opción 1: Pre-deploy Command (MÁS FÁCIL)

En Railway → Settings → Deploy → **Pre-deploy command**, agrega:

```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

Luego haz un nuevo deploy (push a GitHub o manualmente).

## Opción 2: Start Command Completo

En Railway → Settings → Deploy → **Start command**, usa:

```bash
mkdir -p staticfiles && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn pochita_project.wsgi --log-file - --timeout 120 --workers 2 --bind 0.0.0.0:${PORT:-8080}
```

## Opción 3: Railway CLI (si funciona)

Si puedes hacer que `railway link` funcione, luego ejecuta:

```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
```

## Verificar en Supabase

Después de ejecutar migraciones, ve a Supabase → Table Editor y deberías ver:
- `clinic_usuario`
- `clinic_cliente`  
- `clinic_veterinario`
- `clinic_mascota`
- `clinic_cita`
- `clinic_atencion`
- `clinic_listaespera`
- `clinic_producto`
- `django_migrations`
- `django_content_type`
- etc.

