# csvtomd

`csvtomd` es un script en **Python 3** que convierte archivos **CSV** en tablas **Markdown**, sin necesidad de librerías externas.  
Ideal para preparar documentación técnica, datos tabulados o transformar información rápidamente para GitHub, Wikis o blogs.

---

## Características

- Convierte uno o varios archivos `.csv` a tablas en formato **Markdown**.
- Detecta automáticamente el número de columnas y ajusta los anchos.
- Permite especificar el **delimitador** (`,` por defecto, `;` u otro).
- Control sobre el **espaciado** de celdas.
- Puede leer desde archivo o desde la **entrada estándar**.
- A partir de esta versión, también **genera un archivo `.md`** con el mismo nombre que el CSV original.

---

## Requisitos

- Python **3.6+**  
- No requiere librerías adicionales

---

## Uso

### 1. Convertir un archivo CSV

```bash
python3 csvtomd.py "my file.csv"
````

Esto:

* Imprime la tabla Markdown en la terminal
* Crea un archivo `my file.md` en la misma carpeta

---

### 2. Especificar delimitador

```bash
python3 csvtomd.py -d ";" datos.csv
```

---

### 3. Ajustar el espaciado

```bash
python3 csvtomd.py -p 1 datos.csv
```

---

### 4. Usar entrada estándar

```bash
cat datos.csv | python3 csvtomd.py
```

En este caso solo imprime la salida en pantalla, no genera archivo `.md`.

---

## 📋 Ejemplo

### CSV de entrada (`ejemplo.csv`):

```csv
lang,code,name
uk,700,2 Ін
uk,710,3 Івана
uk,720,Юда
ru,100,2Цар
en,140,2Chronicles
```

### Markdown generado (`ejemplo.md`):

```markdown
| lang  |  code  |  name        |  
|-------|--------|--------------|
| uk    |  700   |  2 Ін        | 
| uk    |  710   |  3 Івана     | 
| uk    |  720   |  Юда         | 
| ru    |  100   |  2Цар        |  
| en    |  140   |  2Chronicles | 
```

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.
¡Siéntete libre de usarlo, modificarlo y mejorarlo!

---

✍️ Desarrollado con ❤️ en Python
