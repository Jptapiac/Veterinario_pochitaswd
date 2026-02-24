# Cómo Ejecutar Comandos en Railway

## Opción 1: Desde la Web de Railway (MÁS FÁCIL)

1. Ve a Railway → Tu Proyecto → **Deployments**
2. Haz clic en el deployment más reciente (el que está activo)
3. Verás una pestaña **"Logs"** y otra **"Metrics"**
4. En la parte superior derecha, busca un botón **"Shell"** o **"Terminal"**
5. Si no aparece, ve a **Settings** → **Deploy** → busca **"Pre-deploy step"** o **"Custom commands"**

### Alternativa: Railway CLI (más avanzado)

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

4. Ejecuta comandos:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py collectstatic --noinput
   railway run python manage.py createsuperuser
   ```

## Opción 2: Pre-deploy Automático (YA CONFIGURADO)

He creado `railway.toml` que ejecuta automáticamente:
- Migraciones
- Collectstatic

Esto se ejecuta **antes de cada deploy**, así que solo necesitas hacer push y esperar.

## Comandos Necesarios (si los haces manualmente):

```bash
# 1. Migraciones
python manage.py migrate --noinput

# 2. Archivos estáticos
python manage.py collectstatic --noinput

# 3. Crear superusuario (solo la primera vez)
python manage.py createsuperuser
```

