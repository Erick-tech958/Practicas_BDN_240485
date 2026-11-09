# Diccionario de datos y modelo EER ? db_test

Aplicaci?n est?tica de una sola p?gina para explorar el diccionario de datos, el dashboard, las relaciones y el diagrama EER del respaldo `backups/240485_27.10.26.sql`. La aplicaci?n se encuentra en `docs/index.html`, comparte un ?nico modelo estructural y no requiere conexi?n a MySQL durante su ejecuci?n.

## An?lisis disponible

El respaldo contiene 25 tablas, 226 columnas, 32 claves for?neas declaradas, 65 ?ndices (incluidas 25 PK), 28 vistas, 72 triggers, 3 procedimientos y 4 funciones. No se agregan relaciones inferidas sin evidencia expl?cita. Las descripciones y clasificaciones conceptuales se identifican como inferencias cuando no est?n declaradas en SQL.

Los conteos por tabla se reconstruyen contando las tuplas `INSERT` en cada bloque de datos del respaldo, sin ejecutar SQL: hay **116,522 registros** en total; seis tablas contienen filas y las otras 19 tienen cero filas declaradas en sus bloques. El ?nico `UPDATE` detectado est? dentro de la definici?n de un procedimiento y no forma parte de la carga del respaldo. El archivo `data/schema.json` contiene metadatos estructurales y conteos agregados; no incluye filas ni credenciales.

## Ejecuci?n local

Requiere Node.js y npm. Desde la ra?z del proyecto:

```bash
npm install
npm run dev
```

Vite sirve la aplicaci?n desde `docs/`. Para compilar los archivos est?ticos:

```bash
npm run build
```

La compilaci?n se genera en `dist/`. Para revisarla localmente:

```bash
npm run preview
```

## Publicaci?n en GitHub Pages con un solo archivo

La aplicaci?n completa est? dentro de `index.html`: incluye estilos, c?digo JavaScript y el esquema con conteos. No necesita cargar archivos locales, dependencias, servidor ni conexi?n a MySQL. Para publicarla en GitHub Pages, sube ?nicamente `index.html` a la ra?z de la rama o carpeta configurada como Pages. No ejecutes `npm run build` para esa publicaci?n de un solo archivo.

El respaldo SQL y los archivos de desarrollo que permanecen en este espacio de trabajo no son necesarios para que el sitio abra. No los incluyas al publicar el documento.

## Actualizar el modelo

`_build_metadata.py` lee el respaldo sin ejecutarlo y genera `data/schema.json`. El ?ndice HTML es una aplicaci?n compilada incluida en el repositorio; despu?s de cambiar el respaldo, la actualizaci?n de esa aplicaci?n requiere regenerar sus datos incrustados desde el modelo. No publiques copias del respaldo ni agregues registros personales al sitio.
