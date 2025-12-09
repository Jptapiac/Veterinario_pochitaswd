# Configuración Completa de Railway

## 1. VARIABLES DE ENTORNO (Copia exactamente así, SIN comillas)

En Railway → Variables, agrega estas 4 variables:

```
DATABASE_URL=postgresql://postgres:yxYaARzdCLiU2YJG@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres
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

## 2. START COMMAND

En Railway → Settings → Deploy → **Start command**, cambia a:

```
bash start.sh
```

## 3. PRE-DEPLOY COMMAND (Déjalo VACÍO)

En Railway → Settings → Deploy → **Pre-deploy command**, déjalo vacío o elimínalo.

Las migraciones se ejecutarán automáticamente en el start.sh.

## 4. HACER COMMIT Y PUSH

```bash
cd Veterinario_pochitaswd
git add .
git commit -m "Complete Railway configuration"
git push
```

## 5. DESPUÉS DEL DEPLOY

Si todo funciona, el frontend estará en:
- https://veterinariopochitaswd-production.up.railway.app/api/inicio/
- https://veterinariopochitaswd-production.up.railway.app/api/login/

Si hay algún error, revisa los logs en Railway → Deployments → View Logs

