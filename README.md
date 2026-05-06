<p align="center" >
  <img width="200px" src="app/static/assets/wns-logo.png" />
</p>
<h1 align="center">WNS Challenge :: Meal Calculator</h1>


### Resumen
La aplicación es un **calculador de precios de platos** que permite cargar información de platos e ingredientes mediante la importación masiva de archivos. Posteriormente, posibilita consultar el costo total de cualquier plato según una fecha determinada, mostrando el listado de ingredientes con sus cantidades y el costo total tanto en pesos argentinos como en dólares.

### Implementación
La solución se implementó con una arquitectura de tres capas: 
- Un backend en Python Flask que gestiona las rutas API y la lógica de negocio mediante controladores y casos de uso.
- Una base de datos SQLite que almacena información de platos, ingredientes y precios. 
- Un frontend en JavaScript con HTML/CSS que proporciona una interfaz interactiva para consultar datos y calcular costos.

### Modo de uso
A continuación, se detallan los pasos para la utilización de la interfaz:

**Carga de datos**
1. Acceder a la sección de carga de archivos.
2. Preparar los archivos con los datos de platos, ingredientes y precios.
3. Seleccionar los archivos haciendo clic para cargar los tres archivos.
4. Verificar la carga comprobando que se muestre “3 archivos cargados - listo para procesar”.
5. Presionar el botón “Procesar”.
6. Confirmar la carga verificando que, al finalizar, se redirija a la sección de consulta.

**Consulta de precios de platos**
1. Seleccionar un plato en el selector "Plato", eligiendo el que se desea consultar.
2. Elegir una fecha en el campo "Fecha", seleccionando una fecha válida (máximo 30 días atrás).
3. Presionar "Consultar" para cargar los datos del plato.
4. Revisar los resultados
    - Ingredientes: ver la lista completa con pesos en gramos.
    - Receta: visualizar la descripción del plato.
    - Resumen de costos: consultar el total en pesos y en dólares.


### Consideraciones

   
##### Fortalezas
La solución se destaca por una arquitectura limpia, con una clara separación entre controladores, repositorios y casos de uso, lo que facilita el mantenimiento y las pruebas. Además, incorpora procesamiento asincrónico para la carga de archivos, evitando bloquear la interfaz y mejorando la experiencia del usuario. La interfaz es intuitiva, con funcionalidades como drag-and-drop, modales personalizados para errores y validaciones visuales que simplifican la interacción. A su vez, cuenta con validaciones robustas tanto en los datos de entrada como en las reglas de negocio, y medidas de seguridad que previenen inyecciones mediante consultas parametrizadas. Finalmente, su diseño contempla la escalabilidad, permitiendo migrar a motores de base de datos más potentes

##### Debilidades
La lectura de los documentos que contienen información sobre ingredientes, precios y recetas se realiza de manera estática, por lo tanto, ante cualquier variación, los archivos podrían no procesarse correctamente. Se podría evaluar la creación de un sistema de lectura más robusto, basado en plantillas, para evitar depender de formatos rígidos en la extracción de datos.
Actualmente, la base de datos se elimina por completo cada vez que se vuelven a procesar los archivos. Sería conveniente implementar una solución que actualice únicamente los registros modificados y conserve aquellos que no hayan cambiado, optimizando así el uso de recursos cuando no existan variaciones. Además, en cada inicio de la aplicación se requieren los tres archivos de entrada. Este flujo podría mejorarse haciendo opcional su carga desde la pantalla donde se realizan las consultas sobre los platos. 

##### Despliegue 
Para desplegar la solución más allá del entorno local, se debería implementar un motor de base de datos más escalable y robusto, capaz de soportar concurrencia de consultas, mejorar la seguridad y garantizar un mejor rendimiento. También sería recomendable incorporar un sistema de caché para aquellos datos que no cambian con frecuencia, evitando así llamadas repetitivas a la base de datos. Por otro lado, sería necesario implementar un sistema de monitoreo que permita supervisar errores, latencia y disponibilidad, junto con alertas configurables.

