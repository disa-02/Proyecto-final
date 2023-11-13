# Amdo

Herramienta que permite identificar y agrupar multiples documentaciones YAML(.yml) correspondientes a microservicios.
 
# Configuracion
El archivo entries.txt permite configurar la herramienta de diferentes formas. Todos los atributos de este archivo deben estar descriptos por mas que no se utilicen.

## General
- generate: Indica si se deben generar descripciones o no con el ChatGpt
  - 0:No generar
  - 1:Generar
- importDocs: Indica si se van a importar nuevos documentos o se trabajara con una version anterior
  - 0: Version anterior
  - 1: Importar nuevos documentos
## ChatGpt
- chunks:  Cantidad de caracteres que se reconocen en una consulta al ChatGpt
- openApiKey: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
- language: Lenguaje que se esta utilizando en las documentaciones OpenApi

## Spacy - Procesamiento de descripciones
- model: Modelo de lenguaje que utiliza Spacy(ejemplo: en_core_web_lg)
- numberSentences: Numero de oraciones que se formaran al procesar una descripcion
- commonWords: Cantidad de palabras maximas que conformaran una descripcion procesada

## Clustering final
- k: Numero de clusters a formar
- nInit: Cantidad de iteraciones para formar los clusters
- finalClustering: Metodo de clustering a utilizar
  - 0: K-means
  - 1: Jerarquico

## Agrupamiento intermedio 
- metodo: Metodo que se utiliza para agrupar
  - 0: ChatGpt
  - 1: ChatGpt de forma asistida
  - 2: K-Means
  - 3: Jerarquico
  - 4: Agrupacion semantica
    - umbral: valor entre 0 y 1 que indica que tanto se tienen que parecer las descripciones

## Clustering intermedio
- k: Numero de clusters a formar
- nInit: Cantidad de iteraciones para formar los clusters

# Carpetas
Para el funcionamiento correcto todas las carpetas se deben encontrar en el directorio de ejecucion

## openApiDescriptions
Carpeta donde se insertan todas las descripciones que se quieren agrupar.

## outs
Carpeta donde se almacenan todas las salidas de la herramienta.
 - Errores: Carpeta donde se almacenan errores que se pueden generar en la herramienta.
 - Prompts: En caso de usar ChatGpt como metodo de agrupamiento, cada prompt se guardara en esta carpeta.
 - Responses: Almacena las respuestas de las prompt generadas.
 - AgrupacionDeDescripciones.json: Indica en formato json las agrupaciones de las descripciones
 - DescripcionesGeneradas.txt: En caso de que se hayan generado descripciones, se muestran en este archivo.
 - DescripcionesProcesadas.txt: Muestra todas las descripciones procesadas
 - FilesDescription.json: Almacena todas las descripciones de todos los documentos.
 - Vectorization.txt: Indica el resultado final de vectorizar cada documento.
 - FinalOut.txt: Salida general de la herramienta. Muestra los microservicios agrupados junto con informacion de tiempo de ejecucion y metricas de clustering

# Ejecucion
Se debe ejecutar el archivo main.py.
Si se quiere probar diferentes configuraciones para un mismo caso de estudio la herramienta permite utilizar las descripciones ya generadas y procesadas en una ejecucion previa.
Para esto se debe configurar el "importDocs" con valor 0 y de esta forma utilizara los datos que estan en los documentos "filesDescription.json" y "openApiDescriptions". Es decir que no se volveran a importar los documentos.

