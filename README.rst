Resoluciones UNC
================

Descripción
-----------

A través de su `digesto electrónico <http://www.digesto.unc.edu.ar>`_, la UNC
ofrece acceso público a todas las resoluciones y ordenanzas que emiten los
diferentes órganos de gobierno que la componen.
En estos documentos se encuentran todas las decisiones que se toman, y en
particular se pueden encontrar todos los cambios que ocurren en la planta
docente, como designaciones, licencias y renuncias de profesores.
Toda esta información puede resultar de interés, por ejemplo, para estudiar el
crecimiento de la universidad y sus dependencias, o para encontrar situaciones
de precariedad laboral, como la falta de concursos.


Objetivos
---------

En este proyecto proponemos detectar y procesar aquellas resoluciones de la UNC
que se refieren a cambios en la planta docente, encontrando y etiquetando las
entidades como nombres de personas, números de legajo, cargos, dedicaciones,
fechas, etc.
La información obtenida podrá ser consultada a través de una interfaz web.


Instalación
-----------

Ver `INSTALL.rst`.


Requerimientos Funcionales
--------------------------

  - Scraping de los PDFs de resoluciones del digesto electrónico.
  - Extracción de texto y metadatos de los PDFs e incorporación a la base de datos.
  - Detección de resoluciones que realizan cambios en la planta docente.
  - Etiquetado de personas: nombres, DNIs y legajos.
  - Etiquetado de cargos: jerarquía, dedicación y código interno.
  - Etiquetado de fechas, rangos de fechas y períodos.
  - Etiquetado de eventos: designaciones interinas y por concurso, ceses de
    designaciones, renuncias, licencias con y sin goce de haberes.
