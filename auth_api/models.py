from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, cc, password, email, nombre, **kwargs):
        administrador = False
        manejador_inventario = False
        cajero = False
        punto_venta = None
        empresa = 0

        if 'rol_administrador' in kwargs:
            administrador = kwargs['rol_administrador']
        if 'rol_inventario' in kwargs:
            manejador_inventario = kwargs['rol_inventario']
        if 'rol_cajero' in kwargs:
            cajero = kwargs['rol_cajero']
        if 'punto_venta' in kwargs:
            punto_venta = kwargs['punto_venta']
        elif 'empresa' in kwargs:
            empresa = kwargs['empresa']

        user = self.model(
            cc=cc,
            email=email,
            nombre=nombre,
            rol_administrador=administrador,
            rol_inventario=manejador_inventario,
            rol_cajero=cajero,
            empresa=empresa,
            punto_venta=punto_venta
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cc, email, nombre, password):
        user = self.create_user(
            cc=cc,
            email=email,
            nombre=nombre
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    cc = models.BigIntegerField(unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    punto_venta = models.CharField(max_length=50)

    is_admin = models.BooleanField(default=False)
    rol_administrador = models.BooleanField(default=False)
    rol_inventario = models.BooleanField(default=False)
    rol_cajero = models.BooleanField(default=False)

    USERNAME_FIELD = 'cc'
    REQUIRED_FIELDS = [cc, email, nombre]

    objects = UserManager()
