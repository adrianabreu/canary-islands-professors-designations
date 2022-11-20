# Canary Islands Professor Designations

Just avoiding some friend to every single day to the designations web (https://www.gobiernodecanarias.org/educacion/web/personal/docente/oferta/interinos-sustitutos/nombramientos_diarios/otros_cuerpos/) and dig through a pdf if somebody was called for Biology and thus his position in queue moved.

Using py2pdf + a simple regex for counting the biology calls per island and publishing the result to a telegram group.


# Build steps for lambda

```
poetry build
poetry run pip install --upgrade -t package dist/*.whl
cd package ; zip -r ../artifact.zip . -x '*.pyc'
zip -g artifact.zip lambda_handler.py 
```
