## 拓展AbstractUser后创建表格报错

**错误信息如下**
> django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its depend
ency account.0001_initial on database 'default'.

**解决方式**:  
删除auth_user表，重新migrate即可。

**原因:** 
> This is issue due to parent models migrations already in database table.   
SO you have to Delete your database and re-create it.

----

### 触发问题说明
1. 在创建的app account.models.py中自定义一个UserProfile(用户信息类)

```python
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    pass
```

2. 在settings.py中启用这个类为auth_user_model

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account'
]

# 注册用户系统使用哪个模型，注意不需要是account.models.UserProfile
AUTH_USER_MODEL = 'account.UserProfile'
```
