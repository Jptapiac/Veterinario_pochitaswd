# Guía de Despliegue - Veterinaria Pochita

## Pasos Rápidos

### 1. SUPABASE (Base de Datos) ✅

**Ya configurado:**
- Host: `db.fnlncegdxgdybyxznxij.supabase.co`
- Port: `5432`
- Database: `postgres`
- User: `postgres`

**Solo necesitas:**
1. Ve a tu proyecto en Supabase > Settings > Database
2. Copia tu contraseña (o resetea si no la tienes)
3. Reemplaza `[YOUR_PASSWORD]` en la Connection String:
   ```
   postgresql://postgres:TU_PASSWORD_AQUI@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres
   ```

### 2. RAILWAY (Backend)

1. Ve a https://railway.app y conéctate con GitHub
2. **New Project** > **Deploy from GitHub repo**
3. Selecciona tu repositorio y la carpeta: `Veterinario_pochitasw/Veterinario_pochitasw/backend`
4. En **Variables** agrega:
   - `DATABASE_URL` = `postgresql://postgres:TU_PASSWORD@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres`
     (Reemplaza `TU_PASSWORD` con tu contraseña real de Supabase)
   - `DJANGO_SECRET_KEY` = (genera uno con: `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `tu-app.railway.app,localhost`
   - `CORS_ALLOWED_ORIGINS` = `https://tu-frontend.vercel.app`
5. Railway detectará automáticamente el `Procfile` y desplegará

### 3. VERCEL (Frontend)

**Opción A: Si el frontend está separado (React/Vue/etc)**
1. Ve a https://vercel.com y conéctate con GitHub
2. Importa el proyecto del frontend
3. En **Environment Variables** agrega:
   - `VITE_API_URL` o `REACT_APP_API_URL` = `https://tu-backend.railway.app`

**Opción B: Si el frontend está integrado con Django (templates)**
- El frontend se sirve desde Railway junto con el backend
- Solo necesitas configurar CORS en Railway para permitir tu dominio

### 4. Migraciones

Después del despliegue en Railway, ejecuta migraciones:
1. En Railway, ve a tu servicio > **Deployments** > **View Logs**
2. O usa Railway CLI: `railway run python manage.py migrate`
3. Crea superusuario: `railway run python manage.py createsuperuser`

## Variables de Entorno Necesarias

### Railway (Backend)
```
DATABASE_URL=postgresql://...
DJANGO_SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=tu-app.railway.app
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

### Vercel (Frontend - si está separado)
```
VITE_API_URL=https://tu-backend.railway.app
```

## Notas

- Railway te dará una URL automática tipo: `tu-app.up.railway.app`
- Vercel te dará una URL automática tipo: `tu-app.vercel.app`
- Asegúrate de actualizar `CORS_ALLOWED_ORIGINS` con la URL de Vercel

