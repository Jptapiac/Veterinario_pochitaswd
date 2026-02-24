# Configuración Railway - Paso a Paso

## 1. Root Directory (CRÍTICO)
En Railway > Settings > Source:
- **Add Root Directory**: `Veterinario_pochitasw/Veterinario_pochitasw/backend`

## 2. Variables de Entorno

Agrega estas variables en Railway > Variables:

```
DATABASE_URL=postgresql://postgres:yxYaARzdCLiU2YJGD@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres
DJANGO_SECRET_KEY=2qW-Xa5EuShNsg-fuROQoLxfxlyOu0TVCkJQMEQ2DeUN5ieDQK2MNp1bYu8Ge1LrAyY
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

**Notas importantes:**
- `ALLOWED_HOSTS` usa `*.railway.app` para aceptar cualquier subdominio de Railway
- `DEBUG=False` (sin comillas)
- Después del primer deploy, Railway te dará una URL tipo `tu-app.up.railway.app`
- Actualiza `CORS_ALLOWED_ORIGINS` con la URL real de tu frontend cuando lo despliegues

## 3. Start Command (ya configurado en Procfile)
Railway debería detectar automáticamente:
```
gunicorn pochita_project.wsgi --log-file -
```

## 4. Después del Deploy
1. Ve a Railway > Deployments > View Logs
2. Ejecuta migraciones: `railway run python manage.py migrate`
3. Crea superusuario: `railway run python manage.py createsuperuser`

