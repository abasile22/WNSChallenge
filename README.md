<p align="center" >  
  <img width="200px" src="app/static/assets/wns-logo.png" />  
</p>  
<h1 align="center">WNS Challenge :: Meal Calculator</h1>  


### Indice
- [Resumen](#resumen)  
- [Implementación](#implementación)  
  - [Arquitectura](#arquitectura)  
  - [Base de datos](#base-de-datos)  
- [Ejecutar la aplicación](#ejecutar-la-aplicación)  
  - [Prerequisitos](#prerequisitos)  
  - [Pasos de ejecución](#pasos-de-ejecución) 
- [Modo de uso](#modo-de-uso)
  - [Carga de datos](#carga-de-datos)  
  - [Consulta de precios de platos](#consulta-de-precios-de-platos)  
- [Consideraciones](#consideraciones)  
  - [Fortalezas](#fortalezas)
  - [Debilidades](#debilidades)
  - [Despliegue](#despliegue)
  - [Limitaciones](#limitaciones)
  - [Uso de IA](#uso-de-ia)

## Resumen  
La aplicación es un **calculador de precios de platos** que permite cargar información de platos e ingredientes mediante la importación masiva de archivos. Posteriormente, posibilita consultar el costo total de cualquier plato según una fecha determinada, mostrando el listado de ingredientes con sus cantidades y el costo total tanto en pesos argentinos como en dólares.  
  
## Implementación  

### Arquitectura
La solución se implementó con una arquitectura de tres capas:   
- Un backend en Python Flask que gestiona las rutas API y la lógica de negocio mediante controladores y casos de uso.  
- Una base de datos SQLite que almacena información de platos, ingredientes y precios.   
- Un frontend en JavaScript con HTML/CSS que proporciona una interfaz interactiva para consultar datos y calcular costos.  

### Base de datos
Se utilizo SQLite como motor de base de datos. Se modelaron cuatro tablas con el fin de almacenar y consultar la información correspondiente:
- Tabla `meals` donde se almacenan todas las posibles comidas.
- Tabla `ingredients` donde se almacenan los ingredientes de las comidas.
- Tabla `recipes` donde se almacenan las recetas de las comidas. 
- Tabla `prices` donde se almacenan los precios de los ingredientes. 

A excepción de la tabla prices*, todas las tablas están interrelacionadas según conveniencia para consultar los datos y todas se encuentran debidamente indexadas para un rápido acceso a los registros. 

\*Al modelar las tablas, no fue posible relacionar directamente la tabla `prices` con la tabla `ingredients`, ya que los ingredientes están asociados a los platos y un mismo ingrediente puede aparecer múltiples veces. Esto impide establecer una relación uno a uno entre cada ingrediente y su precio, dado que el mismo no varía entre platos.
Como mejora, se podría incorporar una tabla padre de ingredientes, donde cada ingrediente exista de manera única y desde allí relacionarlo tanto con sus precios como con los platos que lo utilizan. En este caso, se optó por una solución más simple, dejando como efecto colateral una tabla sin relaciones directas.

## Ejecutar la aplicación  
### Prerequisitos
Se requiere contar con Docker instalado en el sistema.

### Pasos de ejecución
Ejecutar los siguientes comandos desde una terminal:
1. Acceder a la raíz del proyecto:  `cd WNSChallenge/`
2. Construir la imagen: `docker build -t wns-challenge .`
3. Ejecutar el contenedor: `docker run -p 5000:5000 wns-challenge`
4. Acceder a la aplicación: http://localhost:5000

## Modo de uso  
Se detallan los pasos para la utilización de la interfaz:  
  
### Carga de datos 
1. Acceder a la sección de carga de archivos.  
2. Preparar los archivos con los datos de platos, ingredientes y precios.  
3. Seleccionar los archivos haciendo clic para cargar los tres archivos.  
4. Verificar la carga comprobando que se muestre “3 archivos cargados - listo para procesar”.  
5. Presionar el botón “Subir Archivos”.  
6. Confirmar la carga verificando que, al finalizar, se redirija a la sección de consulta.  
  
### Consulta de precios de platos
1. Seleccionar un plato en el selector "Plato", eligiendo el que se desea consultar.  
2. Elegir una fecha en el campo "Fecha", seleccionando una fecha válida (máximo 30 días atrás).  
3. Presionar "Consultar" para cargar los datos del plato.  
4. Revisar los resultados  
   - Ingredientes: ver la lista completa con pesos en gramos.  
   - Receta: visualizar la descripción del plato.  
   - Resumen de costos: consultar el total en pesos y en dólares.  
  
  
## Consideraciones  
### Fortalezas  
La solución se destaca por una arquitectura limpia, con una clara separación entre controladores, repositorios y casos de uso, lo que facilita el mantenimiento y las pruebas. Además, incorpora procesamiento asincrónico para la carga de archivos, evitando bloquear la interfaz y mejorando la experiencia del usuario. La interfaz es intuitiva, con funcionalidades como drag-and-drop, modales personalizados para errores y validaciones visuales que simplifican la interacción. A su vez, cuenta con validaciones robustas tanto en los datos de entrada como en las reglas de negocio, y medidas de seguridad que previenen inyecciones mediante consultas parametrizadas. Finalmente, su diseño contempla la escalabilidad, permitiendo migrar a motores de base de datos más potentes  
  
### Debilidades  
La lectura de los documentos que contienen información sobre ingredientes, precios y recetas se realiza de manera estática, por lo tanto, ante cualquier variación, los archivos podrían no procesarse correctamente. Se podría evaluar la creación de un sistema de lectura más robusto, basado en plantillas, para evitar depender de formatos rígidos en la extracción de datos.  
Actualmente, la base de datos se elimina por completo cada vez que se vuelven a procesar los archivos. Sería conveniente implementar una solución que actualice únicamente los registros modificados y conserve aquellos que no hayan cambiado, optimizando así el uso de recursos cuando no existan variaciones. Además, en cada inicio de la aplicación se requieren los tres archivos de entrada. Este flujo podría mejorarse haciendo opcional su carga desde la pantalla donde se realizan las consultas sobre los platos.   
  
### Despliegue   
Para desplegar la solución más allá del entorno local, se debería implementar un motor de base de datos más escalable y robusto, capaz de soportar concurrencia de consultas, mejorar la seguridad y garantizar un mejor rendimiento. También sería recomendable incorporar un sistema de caché para aquellos datos que no cambian con frecuencia, evitando así llamadas repetitivas a la base de datos y al servicio de cotización de divisas, dado que los valores no cambiaran para una fecha consultada. Por otro lado, sería necesario implementar un sistema de monitoreo que permita supervisar errores, latencia y disponibilidad, junto con alertas configurables.

### Limitaciones
La solución no hace las suficientes validaciones, por lo que frente a cambios menores puede verse afectada la experiencia del usuario. Esto se evidencia al cambiar los archivos de datos donde la interfaz permite avanzar en el flujo pero no muestra ninguna información. 

### Uso de IA
Se utilizaron herramientas de inteligencia artificial como Claude Code y ChatGPT para la resolución de consultas, la estructuración del proyecto, la corrección de errores menores, la optimización de funciones, la generación de tests unitarios de cobertura y la mejora de la documentación.