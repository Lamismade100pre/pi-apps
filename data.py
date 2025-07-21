import pandas as pd
from io import StringIO

csv_data = """
Última actualización: 21/07/2025 11:25,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Hoy,Hoy,Hoy,Semana Actual,Semana Actual,Semana Actual,Mes Actual,Mes Actual,Mes Actual,Año Actual,Año Actual,Año Actual,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Alan Gaytan,1,0,Alan Gaytan,1,0,Adrian Mireles,18,6,Adrian Mireles,113,52,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Alejandra Rodriguez,1,0,Alejandra Rodriguez,1,0,Alan Gaytan,17,12,Alan Gaytan,97,57,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
David Martinez,0,1,David Martinez,0,1,ALANA LOPEZ,12,3,ALANA LOPEZ,93,35,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Donato Andrade,0,1,Donato Andrade,0,1,Alejandra Rodriguez,19,4,Aldair Torres Rios,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Hector Eduardo Isais,0,1,Hector Eduardo Isais,0,1,America Vivanco,0,3,Alejandra Rodriguez,122,44,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Josue Salazar,0,1,Josue Salazar,0,1,Carlos Mendoza,17,7,America Vivanco,46,33,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Pedro de Jesus Rodriguez,0,1,Pedro de Jesus Rodriguez,0,1,Carlos Ortiz,27,3,Araceli Silva,4,4,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Victor Moreno,1,2,Victor Moreno,1,2,DANIEL ESQUIVEL,19,3,Arturo Garcia Villalobos,3,4,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,Total: 3,Total: 7,,Total: 3,Total: 7,David Martinez,11,11,Carlos Eleazar Avila,4,2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Donato Andrade,9,10,Carlos Humberto Arroyo M.,2,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Ernesto Lazos,8,14,Carlos Mendoza,179,69,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Francisco Jose Ramos,10,4,Carlos Ortiz,176,71,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Hector Eduardo Isais,11,18,Cristina Torres,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Ignacio Valles,20,4,DANIEL ESQUIVEL,112,42,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Jesus Gomez,2,7,David Martinez,107,73,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Josue Salazar,6,11,Donato Andrade,91,63,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Luis Garza,1,5,Ernesto Lazos,87,70,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Luz Elena,0,1,Francisco Jose Ramos,98,40,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Marco Antonio Hernandez,13,15,Gustavo Vieyra,9,9,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Mayra Garcia,0,3,Hector Eduardo Isais,86,91,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Miguel Canez,13,9,Ignacio Ramos,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Oscar Martinez,10,14,Ignacio Valles,144,29,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Pedro de Jesus Rodriguez,13,11,Javier Parras,0,3,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Rafael Cabrales,8,11,Jesus Gomez,81,55,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Ramon Gilberto Corral,22,1,Jorge Arturo Aguilar,4,12,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Ruben Vazquez,15,2,Josue Salazar,34,15,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Tomas Corral,0,1,Leonel Ulloa,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Ulises Ontiveros,9,4,Libertad Granados,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Victor Moreno,55,18,Luis Garza,60,44,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,Total: 365,Total: 215,Luis Mendoza,33,16,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Luis Ortiz Yanez,5,2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Luz Elena,20,7,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Manuel Banda,4,14,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Manuel Sanchez,29,38,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Marco Alfonso Quintanar,9,7,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Marco Antonio Hernandez,89,58,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Mauricio Ramirez,11,5,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Mayra Garcia,1,9,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Miguel Canez,126,60,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Obdulia Laureano,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Olga Lopez,4,4,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Oscar Martinez,139,77,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Pedro de Jesus Rodriguez,103,74,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Pedro Rodriguez,1,1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Rafael Cabrales,114,43,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Rafael Sanchez,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Ramon Gilberto Corral,98,19,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Ricardo Reyes,25,15,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Ruben Vazquez,142,26,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Sandra Jimenez,1,0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Tomas Corral,1,2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Ulises Ontiveros,113,42,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Victor Moreno,336,142,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,Total: 3163,Total: 1580,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Semana Pasada: Monday, 7/14/2025,Semana Pasada: Monday, 7/14/2025,Semana Pasada: Monday, 7/14/2025,Semana Pasada: Tuesday, 7/15/2025,Semana Pasada: Tuesday, 7/15/2025,Semana Pasada: Tuesday, 7/15/2025,Semana Pasada: Wednesday, 7/16/2025,Semana Pasada: Wednesday, 7/16/2025,Semana Pasada: Wednesday, 7/16/2025,Semana Pasada: Thursday, 7/17/2025,Semana Pasada: Thursday, 7/17/2025,Semana Pasada: Thursday, 7/17/2025,Semana Pasada: Friday, 7/18/2025,Semana Pasada: Friday, 7/18/2025,Semana Pasada: Friday, 7/18/2025,Semana Pasada: Saturday, 7/19/2025,Semana Pasada: Saturday, 7/19/2025,Semana Pasada: Saturday, 7/19/2025
Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones
Adrian Mireles,1,2,Adrian Mireles,1,0,Adrian Mireles,1,0,Adrian Mireles,1,1,Adrian Mireles,0,1,Adrian Mireles,2,0
Alan Gaytan,2,1,Alan Gaytan,2,0,Alan Gaytan,1,1,Alan Gaytan,1,1,Alan Gaytan,3,0,Alejandra Rodriguez,1,0
ALANA LOPEZ,1,0,ALANA LOPEZ,1,0,ALANA LOPEZ,0,1,Alejandra Rodriguez,1,0,ALANA LOPEZ,2,0,DANIEL ESQUIVEL,3,0
Alejandra Rodriguez,1,0,Alejandra Rodriguez,2,0,Alejandra Rodriguez,1,1,Carlos Mendoza,0,1,Alejandra Rodriguez,1,0,David Martinez,1,0
Carlos Mendoza,1,0,Carlos Mendoza,1,0,Carlos Mendoza,1,0,Carlos Ortiz,2,0,Carlos Mendoza,1,2,Ernesto Lazos,1,1
Carlos Ortiz,2,1,Carlos Ortiz,1,0,Carlos Ortiz,2,0,DANIEL ESQUIVEL,1,1,Carlos Ortiz,3,0,Hector Eduardo Isais,1,1
DANIEL ESQUIVEL,3,0,DANIEL ESQUIVEL,2,0,DANIEL ESQUIVEL,2,0,David Martinez,1,2,DANIEL ESQUIVEL,2,1,Marco Antonio Hernandez,1,0
David Martinez,0,2,David Martinez,1,0,David Martinez,0,1,Donato Andrade,1,0,David Martinez,1,0,Miguel Canez,1,0
Ernesto Lazos,1,1,Donato Andrade,1,2,Donato Andrade,1,0,Ernesto Lazos,0,1,Donato Andrade,1,0,Oscar Martinez,1,1
Francisco Jose Ramos,1,0,Ernesto Lazos,1,1,Ernesto Lazos,1,1,Francisco Jose Ramos,2,0,Ernesto Lazos,1,1,Pedro de Jesus Rodriguez,1,1
Hector Eduardo Isais,0,2,Francisco Jose Ramos,1,0,Francisco Jose Ramos,1,0,Hector Eduardo Isais,0,1,Francisco Jose Ramos,1,0,Rafael Cabrales,0,1
Ignacio Valles,1,1,Hector Eduardo Isais,1,0,Hector Eduardo Isais,1,0,Ignacio Valles,1,1,Hector Eduardo Isais,0,1,Ramon Gilberto Corral,3,1
Josue Salazar,0,1,Ignacio Valles,2,0,Ignacio Valles,1,0,Josue Salazar,0,1,Ignacio Valles,1,0,Victor Moreno,4,0
Marco Antonio Hernandez,1,1,Josue Salazar,0,1,Marco Antonio Hernandez,0,1,Marco Antonio Hernandez,1,0,Jesus Gomez,0,1,,Total: 20,Total: 6
Miguel Canez,1,0,Luis Garza,0,1,Miguel Canez,0,1,Miguel Canez,0,2,Josue Salazar,1,0,,,
Oscar Martinez,0,1,Marco Antonio Hernandez,1,1,Oscar Martinez,1,0,Oscar Martinez,1,0,Marco Antonio Hernandez,1,0,,,
Pedro de Jesus Rodriguez,1,0,Miguel Canez,1,1,Pedro de Jesus Rodriguez,1,1,Pedro de Jesus Rodriguez,1,0,Miguel Canez,1,1,,,
Rafael Cabrales,0,1,Oscar Martinez,0,1,Rafael Cabrales,0,1,Rafael Cabrales,1,0,Oscar Martinez,1,0,,,
Ramon Gilberto Corral,1,0,Pedro de Jesus Rodriguez,0,1,Ramon Gilberto Corral,2,0,Ramon Gilberto Corral,2,0,Pedro de Jesus Rodriguez,1,0,,,
Ruben Vazquez,0,1,Rafael Cabrales,1,2,Ruben Vazquez,0,1,Ruben Vazquez,2,0,Rafael Cabrales,0,1,,,
Victor Moreno,4,0,Ramon Gilberto Corral,3,0,Victor Moreno,3,1,Victor Moreno,4,1,Ramon Gilberto Corral,1,0,,,
,Total: 22,Total: 15,Victor Moreno,3,3,,Total: 20,Total: 11,,Total: 23,Total: 13,Ruben Vazquez,1,0,,,
,,,,,Total: 26,Total: 14,,,,,,,,,Ulises Ontiveros,0,1,,,
,,,,,,,,,,,,,,,Victor Moreno,4,0,,,
,,,,,,,,,,,,,,,,,Total: 28,Total: 10,,,
,,,,,,,,,,,,,,,,,,,,,,,,
Mes Pasado - Semana 1 (6/1 - 6/1) (Sin Datos),,,Mes Pasado - Semana 2 (6/2 - 6/8),Mes Pasado - Semana 2 (6/2 - 6/8),Mes Pasado - Semana 2 (6/2 - 6/8),Mes Pasado - Semana 3 (6/9 - 6/15),Mes Pasado - Semana 3 (6/9 - 6/15),Mes Pasado - Semana 3 (6/9 - 6/15),Mes Pasado - Semana 4 (6/16 - 6/22),Mes Pasado - Semana 4 (6/16 - 6/22),Mes Pasado - Semana 4 (6/16 - 6/22),Mes Pasado - Semana 5 (6/23 - 6/29),Mes Pasado - Semana 5 (6/23 - 6/29),Mes Pasado - Semana 5 (6/23 - 6/29),Mes Pasado - Semana 6 (6/30 - 6/30),Mes Pasado - Semana 6 (6/30 - 6/30),Mes Pasado - Semana 6 (6/30 - 6/30)
N/A,,,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones
,,,Adrian Mireles,7,2,Adrian Mireles,7,2,Adrian Mireles,5,7,Adrian Mireles,3,10,Adrian Mireles,1,2
,,,Alan Gaytan,9,7,Alan Gaytan,5,2,Alan Gaytan,4,5,Alan Gaytan,4,4,Alan Gaytan,1,1
,,,ALANA LOPEZ,4,3,ALANA LOPEZ,6,2,ALANA LOPEZ,3,3,ALANA LOPEZ,4,2,ALANA LOPEZ,1,0
,,,Alejandra Rodriguez,3,0,Alejandra Rodriguez,4,0,Alejandra Rodriguez,3,3,Alejandra Rodriguez,2,1,Carlos Mendoza,2,1
,,,America Vivanco,2,4,America Vivanco,0,2,America Vivanco,3,1,America Vivanco,0,2,Carlos Ortiz,1,0
,,,Carlos Eleazar Avila,2,1,Arturo Garcia Villalobos,2,0,Arturo Garcia Villalobos,0,1,Arturo Garcia Villalobos,0,2,David Martinez,0,1
,,,Carlos Mendoza,13,4,Carlos Eleazar Avila,0,1,Carlos Mendoza,4,3,Carlos Mendoza,4,2,Donato Andrade,1,0
,,,Carlos Ortiz,11,1,Carlos Mendoza,4,7,Carlos Ortiz,5,6,Carlos Ortiz,5,5,Ernesto Lazos,0,3
,,,DANIEL ESQUIVEL,5,5,Carlos Ortiz,6,6,DANIEL ESQUIVEL,2,1,DANIEL ESQUIVEL,4,0,Francisco Jose Ramos,1,0
,,,David Martinez,3,2,DANIEL ESQUIVEL,2,1,David Martinez,4,2,David Martinez,3,4,Hector Eduardo Isais,0,2
,,,Donato Andrade,3,2,David Martinez,5,1,Donato Andrade,1,2,Donato Andrade,1,4,Ignacio Valles,1,0
,,,Ernesto Lazos,3,4,Donato Andrade,6,1,Ernesto Lazos,4,4,Ernesto Lazos,0,3,Josue Salazar,1,0
,,,Francisco Jose Ramos,6,1,Ernesto Lazos,7,2,Francisco Jose Ramos,2,3,Francisco Jose Ramos,4,1,Luis Garza,1,1
,,,Hector Eduardo Isais,4,1,Francisco Jose Ramos,5,0,Hector Eduardo Isais,2,7,Hector Eduardo Isais,2,12,Miguel Canez,1,0
,,,Ignacio Valles,9,1,Hector Eduardo Isais,2,3,Ignacio Valles,6,0,Ignacio Valles,4,1,Oscar Martinez,1,1
,,,Jesus Gomez,1,2,Ignacio Valles,5,1,Jesus Gomez,0,7,Jesus Gomez,2,2,Rafael Cabrales,1,0
,,,Josue Salazar,3,1,Jesus Gomez,2,4,Josue Salazar,0,1,Josue Salazar,4,0,Victor Moreno,0,1
,,,Luis Garza,7,2,Josue Salazar,5,2,Leonel Ulloa,1,0,Luis Garza,4,3,,Total: 14,Total: 13
,,,Luis Ortiz Yanez,1,1,Luis Garza,3,5,Luis Garza,4,6,Luz Elena,0,1,,,
,,,Luz Elena,3,0,Luis Ortiz Yanez,0,1,Luz Elena,3,0,Marco Antonio Hernandez,2,5,,,
,,,Marco Antonio Hernandez,4,2,Marco Antonio Hernandez,4,2,Marco Antonio Hernandez,4,1,Mayra Garcia,0,1,,,
,,,Miguel Canez,9,0,Miguel Canez,4,2,Miguel Canez,3,4,Miguel Canez,3,6,,,
,,,Oscar Martinez,6,4,Oscar Martinez,4,0,Oscar Martinez,6,3,Oscar Martinez,4,3,,,
,,,Pedro de Jesus Rodriguez,5,3,Pedro de Jesus Rodriguez,2,5,Pedro de Jesus Rodriguez,0,4,Pedro de Jesus Rodriguez,2,4,,,
,,,Pedro Rodriguez,0,1,Rafael Cabrales,4,2,Rafael Cabrales,4,0,Rafael Cabrales,5,0,,,
,,,Rafael Cabrales,5,1,Ramon Gilberto Corral,4,2,Ramon Gilberto Corral,2,2,Ramon Gilberto Corral,0,1,,,
,,,Ramon Gilberto Corral,8,0,Ruben Vazquez,5,1,Ruben Vazquez,4,1,Ruben Vazquez,3,1,,,
,,,Ricardo Reyes,2,0,Tomas Corral,1,0,Ulises Ontiveros,4,1,Tomas Corral,0,1,,,
,,,Ruben Vazquez,15,1,Ulises Ontiveros,2,0,Victor Moreno,18,4,Ulises Ontiveros,4,2,,,
,,,Ulises Ontiveros,8,5,Victor Moreno,19,7,,Total: 101,Total: 82,Victor Moreno,0,6,,,
,,,Victor Moreno,12,6,,Total: 125,Total: 64,,,,Total: 73,Total: 89,,,
,,,,Total: 173,Total: 67,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,
Mes Pasado - June 2025,Mes Pasado - June 2025,Mes Pasado - June 2025,Mes Pasado - May 2025,Mes Pasado - May 2025,Mes Pasado - May 2025,Mes Pasado - April 2025,Mes Pasado - April 2025,Mes Pasado - April 2025,Mes Pasado - March 2025,Mes Pasado - March 2025,Mes Pasado - March 2025,Mes Pasado - February 2025,Mes Pasado - February 2025,Mes Pasado - February 2025,Mes Pasado - January 2025,Mes Pasado - January 2025,Mes Pasado - January 2025
Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones,Diseñador,Nuevo,Guiones
Adrian Mireles,23,23,Adrian Mireles,24,15,Adrian Mireles,19,2,Adrian Mireles,18,6,Adrian Mireles,11,0,Alan Gaytan,12,4
Alan Gaytan,23,19,Alan Gaytan,17,10,Alan Gaytan,16,7,Alan Gaytan,12,1,Alan Gaytan,0,4,ALANA LOPEZ,3,2
ALANA LOPEZ,18,10,ALANA LOPEZ,18,8,ALANA LOPEZ,13,6,ALANA LOPEZ,13,4,ALANA LOPEZ,16,2,Alejandra Rodriguez,23,1
Alejandra Rodriguez,12,4,Aldair Torres Rios,0,1,Aldair Torres Rios,1,0,Alejandra Rodriguez,24,19,Alejandra Rodriguez,20,10,America Vivanco,2,0
America Vivanco,5,9,Alejandra Rodriguez,7,4,Alejandra Rodriguez,17,2,America Vivanco,4,0,America Vivanco,7,2,Araceli Silva,2,2
Arturo Garcia Villalobos,2,3,America Vivanco,15,9,America Vivanco,13,10,Carlos Mendoza,28,6,Araceli Silva,2,2,Carlos Mendoza,20,10
Carlos Eleazar Avila,2,2,Carlos Eleazar Avila,2,0,Arturo Garcia Villalobos,1,1,Carlos Ortiz,31,7,Carlos Humberto Arroyo M.,2,0,Carlos Ortiz,29,10
Carlos Mendoza,27,17,Carlos Mendoza,34,9,Carlos Mendoza,24,10,DANIEL ESQUIVEL,13,4,Carlos Mendoza,29,10,DANIEL ESQUIVEL,9,2
Carlos Ortiz,28,18,Carlos Ortiz,12,7,Carlos Ortiz,22,9,David Martinez,18,9,Carlos Ortiz,27,17,David Martinez,16,7
DANIEL ESQUIVEL,13,7,DANIEL ESQUIVEL,21,15,DANIEL ESQUIVEL,16,7,Donato Andrade,13,5,Cristina Torres,1,0,Donato Andrade,10,6
David Martinez,15,10,David Martinez,15,18,David Martinez,19,7,Ernesto Lazos,14,13,DANIEL ESQUIVEL,21,4,Francisco Jose Ramos,13,7
Donato Andrade,12,9,Donato Andrade,17,15,Donato Andrade,13,10,Francisco Jose Ramos,14,5,David Martinez,13,11,Gustavo Vieyra,8,6
Ernesto Lazos,14,16,Ernesto Lazos,26,10,Ernesto Lazos,14,16,Hector Eduardo Isais,12,10,Donato Andrade,17,8,Hector Eduardo Isais,12,7
Francisco Jose Ramos,18,5,Francisco Jose Ramos,18,9,Francisco Jose Ramos,18,7,Ignacio Valles,20,0,Ernesto Lazos,11,1,Ignacio Valles,19,4
Hector Eduardo Isais,10,25,Hector Eduardo Isais,15,12,Hector Eduardo Isais,17,13,Jesus Gomez,18,3,Francisco Jose Ramos,7,3,Jesus Gomez,19,6
Ignacio Valles,25,3,Ignacio Ramos,1,0,Ignacio Valles,19,2,Luis Garza,15,2,Gustavo Vieyra,1,3,Jorge Arturo Aguilar,1,11
Jesus Gomez,5,15,Ignacio Valles,17,11,Javier Parras,0,3,Luis Mendoza,12,4,Hector Eduardo Isais,9,6,Luis Mendoza,4,0
Josue Salazar,13,4,Jesus Gomez,16,11,Jesus Gomez,13,6,Manuel Banda,0,2,Ignacio Valles,24,5,Luis Ortiz Yanez,1,0
Leonel Ulloa,1,0,Jorge Arturo Aguilar,2,0,Jorge Arturo Aguilar,1,0,Manuel Sanchez,0,4,Jesus Gomez,8,7,Manuel Banda,3,9
Luis Garza,19,17,Josue Salazar,15,0,Luis Garza,10,7,Marco Alfonso Quintanar,0,1,Jorge Arturo Aguilar,0,1,Manuel Sanchez,18,17
Luis Ortiz Yanez,1,2,Libertad Granados,1,0,Luis Mendoza,3,5,Marco Antonio Hernandez,4,4,Luis Garza,2,0,Marco Alfonso Quintanar,4,2
Luz Elena,6,1,Luis Garza,13,13,Luis Ortiz Yanez,1,0,Miguel Canez,15,5,Luis Mendoza,14,7,Marco Antonio Hernandez,6,0
Marco Antonio Hernandez,14,10,Luis Ortiz Yanez,2,0,Luz Elena,10,3,Oscar Martinez,21,3,Manuel Banda,0,3,Miguel Canez,19,9
Mayra Garcia,0,1,Luz Elena,4,2,Manuel Sanchez,1,0,Pedro de Jesus Rodriguez,18,7,Manuel Sanchez,10,17,Oscar Martinez,22,6
Miguel Canez,20,12,Manuel Banda,1,0,Marco Alfonso Quintanar,0,1,Rafael Cabrales,21,5,Marco Alfonso Quintanar,2,2,Pedro de Jesus Rodriguez,9,0
Oscar Martinez,21,11,Marco Alfonso Quintanar,3,1,Marco Antonio Hernandez,17,2,Ramon Gilberto Corral,10,6,Marco Antonio Hernandez,12,17,Rafael Cabrales,15,5
Pedro de Jesus Rodriguez,9,16,Marco Antonio Hernandez,23,10,Mayra Garcia,1,0,Ricardo Reyes,3,1,Mauricio Ramirez,9,5,Rafael Sanchez,1,0
Pedro Rodriguez,0,1,Mauricio Ramirez,2,0,Miguel Canez,17,8,Ruben Vazquez,20,3,Miguel Canez,24,6,Ramon Gilberto Corral,7,2
Rafael Cabrales,19,3,Mayra Garcia,0,5,Oscar Martinez,20,10,Sandra Jimenez,1,0,Oscar Martinez,20,20,Ruben Vazquez,25,7
Ramon Gilberto Corral,14,5,Miguel Canez,18,11,Pedro de Jesus Rodriguez,10,7,Ulises Ontiveros,21,2,Pedro de Jesus Rodriguez,14,19,Ulises Ontiveros,20,11
Ricardo Reyes,2,0,Obdulia Laureano,1,1,Rafael Cabrales,15,5,Victor Moreno,49,23,Rafael Cabrales,14,5,Victor Moreno,51,21
Ruben Vazquez,27,4,Olga Lopez,4,4,Ramon Gilberto Corral,12,1,Total: 462,Total: 164,Ramon Gilberto Corral,14,0,Total: 403,Total: 174
Tomas Corral,1,1,Oscar Martinez,25,13,Ricardo Reyes,10,4,,,,,Ricardo Reyes,7,6,,
Ulises Ontiveros,18,8,Pedro de Jesus Rodriguez,30,14,Ruben Vazquez,19,2,,,,,Ruben Vazquez,20,3,,
Victor Moreno,49,24,Pedro Rodriguez,1,0,Ulises Ontiveros,6,3,,,,,Ulises Ontiveros,19,7,,
Total: 486,Total: 315,Rafael Cabrales,22,9,Victor Moreno,30,17,,,,,Victor Moreno,61,20,,
,Rafael Cabrales,19,4,Total: 438,Total: 193,,,,,,Total: 468,Total: 233,,
,Ramon Gilberto Corral,19,4,,,,,,,,,,,,
,Ricardo Reyes,3,4,,,,,,,,,,,,
,Ruben Vazquez,16,5,,,,,,,,,,,,
,Ulises Ontiveros,20,7,,,,,,,,,,,,
,Victor Moreno,41,19,,,,,,,,,,,,
,Total: 541,Total: 286,,,,,,,,,,,,
"""

# Process the data
data = StringIO(csv_data)
df = pd.read_csv(data, header=None)

# Function to find the start of each table
def find_table_start(df, keyword):
    for i, row in df.iterrows():
        for j, cell in row.items():
            if isinstance(cell, str) and keyword in cell:
                return i, j
    return None, None

# Extracting data for each period
def extract_data(df, start_row, start_col, rows_to_skip, cols_to_take=3):
    if start_row is None:
        return pd.DataFrame(columns=['Diseñador', 'Nuevo', 'Guiones'])

    end_row = start_row + rows_to_skip
    # Adjust end_row logic to be more robust
    for i in range(start_row + 2, len(df)):
        cell_value = df.iloc[i, start_col]
        if cell_value is None or (isinstance(cell_value, str) and "Total" in cell_value):
            end_row = i
            break
    else:
        end_row = len(df)

    table = df.iloc[start_row+2:end_row, start_col:start_col+cols_to_take]
    table.columns = ['Diseñador', 'Nuevo', 'Guiones']
    table = table.dropna(subset=['Diseñador'])
    table = table[~table['Diseñador'].str.contains("Total", na=False)]
    # Convert to numeric, coercing errors
    table['Nuevo'] = pd.to_numeric(table['Nuevo'], errors='coerce').fillna(0).astype(int)
    table['Guiones'] = pd.to_numeric(table['Guiones'], errors='coerce').fillna(0).astype(int)
    return table

# Find and extract all tables
hoy_row, hoy_col = find_table_start(df, 'Hoy')
df_hoy = extract_data(df, hoy_row, hoy_col, 10)

semana_actual_row, semana_actual_col = find_table_start(df, 'Semana Actual')
df_semana_actual = extract_data(df, semana_actual_row, semana_actual_col, 10)

mes_actual_row, mes_actual_col = find_table_start(df, 'Mes Actual')
df_mes_actual = extract_data(df, mes_actual_row, mes_actual_col, 30)

año_actual_row, año_actual_col = find_table_start(df, 'Año Actual')
df_año_actual = extract_data(df, año_actual_row, año_actual_col, 50)

# Weekly data
semana_pasada_lunes_row, semana_pasada_lunes_col = find_table_start(df, 'Semana Pasada: Monday')
df_semana_pasada_lunes = extract_data(df, semana_pasada_lunes_row, semana_pasada_lunes_col, 25)

semana_pasada_martes_row, semana_pasada_martes_col = find_table_start(df, 'Semana Pasada: Tuesday')
df_semana_pasada_martes = extract_data(df, semana_pasada_martes_row, semana_pasada_martes_col, 25)

semana_pasada_miercoles_row, semana_pasada_miercoles_col = find_table_start(df, 'Semana Pasada: Wednesday')
df_semana_pasada_miercoles = extract_data(df, semana_pasada_miercoles_row, semana_pasada_miercoles_col, 25)

semana_pasada_jueves_row, semana_pasada_jueves_col = find_table_start(df, 'Semana Pasada: Thursday')
df_semana_pasada_jueves = extract_data(df, semana_pasada_jueves_row, semana_pasada_jueves_col, 25)

semana_pasada_viernes_row, semana_pasada_viernes_col = find_table_start(df, 'Semana Pasada: Friday')
df_semana_pasada_viernes = extract_data(df, semana_pasada_viernes_row, semana_pasada_viernes_col, 25)

semana_pasada_sabado_row, semana_pasada_sabado_col = find_table_start(df, 'Semana Pasada: Saturday')
df_semana_pasada_sabado = extract_data(df, semana_pasada_sabado_row, semana_pasada_sabado_col, 25)

# Monthly data
mes_pasado_junio_row, mes_pasado_junio_col = find_table_start(df, 'Mes Pasado - June 2025')
df_mes_pasado_junio = extract_data(df, mes_pasado_junio_row, mes_pasado_junio_col, 40)

mes_pasado_mayo_row, mes_pasado_mayo_col = find_table_start(df, 'Mes Pasado - May 2025')
df_mes_pasado_mayo = extract_data(df, mes_pasado_mayo_row, mes_pasado_mayo_col, 40)

mes_pasado_abril_row, mes_pasado_abril_col = find_table_start(df, 'Mes Pasado - April 2025')
df_mes_pasado_abril = extract_data(df, mes_pasado_abril_row, mes_pasado_abril_col, 40)

mes_pasado_marzo_row, mes_pasado_marzo_col = find_table_start(df, 'Mes Pasado - March 2025')
df_mes_pasado_marzo = extract_data(df, mes_pasado_marzo_row, mes_pasado_marzo_col, 40)

mes_pasado_febrero_row, mes_pasado_febrero_col = find_table_start(df, 'Mes Pasado - February 2025')
df_mes_pasado_febrero = extract_data(df, mes_pasado_febrero_row, mes_pasado_febrero_col, 40)

mes_pasado_enero_row, mes_pasado_enero_col = find_table_start(df, 'Mes Pasado - January 2025')
df_mes_pasado_enero = extract_data(df, mes_pasado_enero_row, mes_pasado_enero_col, 40)
