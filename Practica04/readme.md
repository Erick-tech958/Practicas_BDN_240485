# Práctica 04 - Base de Datos

Repositorio correspondiente a la **Práctica 04** de la asignatura de Base de Datos. Este proyecto cuenta con una aplicación web desarrollada con Vite y TypeScript, scripts SQL para la creación y siembra de la base de datos, respaldos de seguridad y su despliegue activo en **GitHub Pages**.

🌐 **Enlace al proyecto publicado (GitHub Pages):**  
👉 [https://Erick-tech958.github.io/Practicas_BDN_240485/Practica03/](https://erick-tech958.github.io/Practicas_BDN_240485/)

---

## 📁 Estructura del Proyecto

```text
Practica03/
├── backups/           # Copias de seguridad y respaldos de la base de datos (.sql)
├── data/              # Archivos de datos e información del proyecto
├── docs/              # Archivos compilados para la publicación en GitHub Pages
├── queries/           # Consultas SQL utilizadas en la práctica
├── scripts/           # Scripts de automatización y utilidad
├── seeds/             # Datos de prueba (semillas) para la base de datos
├── .gitignore         # Archivos y carpetas excluidos de Git
├── _build_metadata.py # Script auxiliar de metadatos para la compilación
├── index.html         # Punto de entrada de la aplicación web
├── package.json       # Dependencias y scripts del proyecto (Node.js)
├── package-lock.json  # Control de versiones exactas de dependencias
├── vite.config.ts     # Configuración del empaquetador Vite
└── readme.md          # Documentación general de la práctica
```

---

## 🛠️ Tecnologías Utilizadas

* **Base de Datos:** SQL (Consultas estructuradas, respaldos `.sql` y scripts de semillas).
* **Frontend:** HTML5, TypeScript.
* **Empaquetador y Build:** [Vite](https://vitejs.dev/).
* **Despliegue & DevOps:** GitHub Pages, Python (scripting de metadatos).
* **Control de Versiones:** Git & GitHub.

---

## 🚀 Instalación y Ejecución Local

Para ejecutar este proyecto de manera local en tu equipo, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Erick-tech958/Practicas_BDN_240485.git
   ```

2. **Navegar a la carpeta de la práctica:**
   ```bash
   cd Practicas_BDN_240485/Practica03
   ```

3. **Instalar dependencias:**
   ```bash
   npm install
   ```

4. **Ejecutar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```

5. Abre tu navegador e ingresa a la dirección indicada en la terminal (por defecto `http://localhost:5173`).

---

## 🗄️ Gestión de la Base de Datos

* **Respaldos:** Los archivos `.sql` generados se ubican en la carpeta `backups/`.
* **Consultas:** Las peticiones SQL requeridas en la práctica están almacenadas en `queries/`.
* **Semillas (Seeds):** Los archivos de carga de datos iniciales están en `seeds/`.

---

## ⚙️ Compilación y Despliegue

Para actualizar los archivos de producción desplegados en GitHub Pages:

1. **Generar la compilación en la carpeta `docs/`:**
   ```bash
   npm run build
   ```

2. **Subir los cambios a GitHub:**
   ```bash
   git add .
   git commit -m "Actualización de build para GitHub Pages"
   git push origin master
   ```

---

