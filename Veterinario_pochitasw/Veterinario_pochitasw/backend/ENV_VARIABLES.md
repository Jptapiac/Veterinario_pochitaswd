# Variables de Entorno para Railway

Copia estas variables en Railway > Variables:

```
DATABASE_URL=postgresql://postgres:TU_PASSWORD_AQUI@db.fnlncegdxgdybyxznxij.supabase.co:5432/postgres
DJANGO_SECRET_KEY=genera-uno-con-el-script-en-scripts/generate_secret_key.py
DEBUG=False
ALLOWED_HOSTS=tu-app.railway.app
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

**Importante:**
- Reemplaza `TU_PASSWORD_AQUI` con tu contraseña real de Supabase
- Genera `DJANGO_SECRET_KEY` ejecutando: `python scripts/generate_secret_key.py`
- Actualiza `ALLOWED_HOSTS` con la URL que Railway te asigne
- Actualiza `CORS_ALLOWED_ORIGINS` con la URL de tu frontend en Vercel

