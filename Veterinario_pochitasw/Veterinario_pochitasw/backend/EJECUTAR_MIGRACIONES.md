# Cómo Ejecutar Migraciones en Railway

## Opción 1: Railway CLI (Recomendado)

1. Instala Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login:
   ```bash
   railway login
   ```

3. Conecta tu proyecto:
   ```bash
   cd Veterinario_pochitasw/Veterinario_pochitasw/backend
   railway link
   ```

4. Ejecuta migraciones:
   ```bash
   railway run python manage.py migrate
   ```

5. Recolecta archivos estáticos:
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

6. Crea superusuario (opcional):
   ```bash
   railway run python manage.py createsuperuser
   ```

## Opción 2: Desde la Web de Railway

1. Ve a Railway → Tu Proyecto → **Deployments**
2. Haz clic en el deployment más reciente (el activo)
3. Busca un botón **"Shell"**, **"Terminal"** o **"Open Shell"** (arriba a la derecha)
4. Si no encuentras el botón, ve a **Settings** → **Deploy** → busca opciones de terminal
5. Ejecuta:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

## Opción 3: Pre-deploy Command (Automático)

En Railway → Settings → Deploy → **Pre-deploy command**, agrega:

```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

Esto ejecutará las migraciones automáticamente antes de cada deploy.

## Verificar Migraciones

Después de ejecutar las migraciones, verifica en Supabase:
1. Ve a Supabase Dashboard → Table Editor
2. Deberías ver tablas como: `clinic_usuario`, `clinic_cliente`, `clinic_mascota`, `clinic_cita`, etc.

