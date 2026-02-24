# Solución para Error de Conexión a Supabase

## Problema
Railway no puede conectarse a Supabase: "Network is unreachable"

## Soluciones

### Opción 1: Usar Supabase Pooler (RECOMENDADO)

Supabase tiene un pooler que es más estable para conexiones desde servicios externos.

1. Ve a Supabase Dashboard → Settings → Database
2. Busca la sección **"Connection Pooling"**
3. Copia la **Connection String** del pooler (tiene `pooler` en la URL)
4. En Railway → Variables, actualiza `DATABASE_URL` con la URL del pooler

Formato del pooler:
```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

### Opción 2: Verificar Firewall de Supabase

1. Ve a Supabase Dashboard → Settings → Database
2. Busca **"Network Restrictions"** o **"Allowed IPs"**
3. Asegúrate de que Railway pueda conectarse (puede que necesites permitir todas las IPs temporalmente)

### Opción 3: Usar Connection String Directa (Actual)

Si ya estás usando la directa, verifica:
- La contraseña es correcta
- El proyecto de Supabase está activo
- No hay restricciones de red

### Opción 4: Quitar Pre-deploy (Temporal)

Si el problema persiste, puedes quitar el pre-deploy y ejecutar migraciones manualmente después:

1. En Railway → Settings → Deploy → **Pre-deploy command**, déjalo vacío
2. Después del deploy exitoso, ejecuta manualmente:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py collectstatic --noinput
   ```

## Verificar Conexión

Para probar la conexión manualmente:
```bash
railway run python manage.py dbshell
```

Si funciona, el problema es solo en el pre-deploy.

