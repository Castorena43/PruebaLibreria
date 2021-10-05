## Instalacion
```python
cd libraryApi
pip install -r requirements.txt
```

## Migraciones 

Creacion de migraciones y exportacion de datos.

```bash
python manage.py migrate
python manage.py loaddata initial_data.json
```

## Usage
Levantar server
```bash
python manage.py runserver
```