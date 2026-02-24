# Comandos Post-Deploy en Railway

Después del despliegue exitoso, ejecuta estos comandos:

## 1. Migraciones de Base de Datos
```bash
railway run python manage.py migrate
```

## 2. Recolectar Archivos Estáticos
```bash
railway run python manage.py collectstatic --noinput
```

## 3. Crear Superusuario (Admin)
```bash
railway run python manage.py createsuperuser
```

## Cómo ejecutar en Railway:

### Opción A: Railway CLI
1. Instala Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Conecta tu proyecto: `railway link`
4. Ejecuta los comandos arriba

### Opción B: Desde la Web
1. Ve a Railway > Deployments
2. Haz clic en el deployment más reciente
3. Ve a la pestaña "Logs"
4. Usa el terminal integrado o ejecuta comandos desde Settings > Deploy

## URLs del Frontend (después de generar dominio):

- **Inicio**: `https://tu-dominio.railway.app/api/inicio/`
- **Login**: `https://tu-dominio.railway.app/api/login/`
- **Servicios**: `https://tu-dominio.railway.app/api/servicios/`
- **Admin**: `https://tu-dominio.railway.app/admin/`
- **API Docs**: `https://tu-dominio.railway.app/api/schema/swagger-ui/`

