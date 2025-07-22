' VBA Code
Option Explicit

'---------------------------------------------------------------------------------------
' Module:      ModuloRefactorizado
' Author:      Jules
' Date:        22/07/2024
' Purpose:     Refactorizado y optimizado para extraer y procesar datos de producción.
'---------------------------------------------------------------------------------------

'---------------------------------------------------------------------------------------
'                           CONSTANTES Y VARIABLES GLOBALES
'---------------------------------------------------------------------------------------

' --- Rutas y Nombres de Archivos ---
Private Const RUTA_REPORTE As String = "M:\Reporte de Guiones\Datos.xlsx"
Private Const RUTA_AMERICA_OPT As String = "M:\Reporte de Guiones\America Opt.xlsm"
Private Const NOMBRE_HOJA_DATOS As String = "tablas"
Private Const NOMBRE_HOJA_ESTADISTICAS As String = "Estadisticas"

' --- URLs ---
Private Const URL_DESMON As String = "http://mxchihjrz-ap23.aptiv.com:1234/desmon/Dailyprod.aspx"

' --- Identificadores de Elementos Web ---
Private Const ID_CAMPO_DESDE As String = "Content_ASPxFormLayout1_ddeFrom_I"
Private Const ID_CAMPO_HASTA As String = "Content_ASPxFormLayout1_ddeTo_I"
Private Const ID_BOTON_BUSCAR As String = "Content_ASPxFormLayout1_btnIr"
Private Const SELECTOR_TABLA As String = "#Content_ASPxFormLayout1_grvPrc table"

' --- Colores de Formato ---
Private Const COLOR_HOY As Long = 65535 ' Amarillo
Private Const COLOR_SEMANA As Long = 49407 ' Naranja
Private Const COLOR_MES As Long = 5296274 ' Verde
Private Const COLOR_ANIO As Long = 255 ' Rojo
Private Const COLOR_OTRO As Long = 15790320 ' Gris
Private Const COLOR_ENCABEZADO_STATS As Long = 9868950 ' Azul oscuro
Private Const COLOR_FILA_PAR As Long = 15921906 ' Gris claro

'---------------------------------------------------------------------------------------
'                               PUNTO DE ENTRADA PRINCIPAL
'---------------------------------------------------------------------------------------

' Summary:   Punto de entrada principal para ejecutar todo el proceso de búsqueda y
'            generación de estadísticas.
Public Sub EjecutarProcesoCompleto()
    Dim driver As Object ' Late binding para WebDriver
    Dim wbDatos As Workbook
    Dim wsDatos As Worksheet
    Dim wsStats As Worksheet

    On Error GoTo CleanExit

    ' --- Inicialización y Configuración del Entorno ---
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    Set driver = IniciarWebDriver(URL_DESMON)
    If driver Is Nothing Then
        MsgBox "No se pudo iniciar el navegador. El proceso se detendrá.", vbCritical, "Error de WebDriver"
        Exit Sub
    End If

    Set wbDatos = AbrirLibro(RUTA_REPORTE)
    If wbDatos Is Nothing Then Exit Sub

    Set wsDatos = ObtenerOPrepararHoja(wbDatos, NOMBRE_HOJA_DATOS)
    If wsDatos Is Nothing Then Exit Sub ' El usuario canceló la operación

    ' --- Procesamiento de Tablas ---
    ProcesarTodasLasTablas wsDatos, driver

    ' --- Generación de Estadísticas ---
    Set wsStats = ObtenerOPrepararHoja(wbDatos, NOMBRE_HOJA_ESTADISTICAS, True)
    GenerarEstadisticasDiseñadores wsDatos, wsStats

    ' --- Limpieza y Finalización ---
    wsDatos.Columns.AutoFit
    wbDatos.Save
    MsgBox "Proceso completado exitosamente.", vbInformation, "Proceso Finalizado"

CleanExit:
    If Err.Number <> 0 Then
        MsgBox "Ocurrió un error inesperado: " & vbCrLf & Err.Description, vbCritical, "Error en Ejecución"
    End If

    ' Restaurar configuración de Excel y cerrar recursos
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    If Not driver Is Nothing Then driver.Quit
    ' No cerramos el libro de datos para que el usuario pueda verlo
End Sub

'---------------------------------------------------------------------------------------
'                           SECCIÓN DE INICIALIZACIÓN Y CONFIGURACIÓN
'---------------------------------------------------------------------------------------

' Summary:   Inicia el WebDriver y navega a la URL especificada.
' Param url: La URL a la que se debe navegar.
' Returns:   Un objeto WebDriver si tiene éxito, de lo contrario Nothing.
Private Function IniciarWebDriver(ByVal url As String) As Object
    Dim driver As Object
    On Error Resume Next
    Set driver = CreateObject("Selenium.WebDriver") ' Usando CreateObject para late binding
    If driver Is Nothing Then
        MsgBox "Asegúrese de que SeleniumBasic está instalado.", vbCritical, "Error de Selenium"
        Exit Function
    End If
    On Error GoTo 0

    driver.Start "edge"
    driver.Get url
    driver.Wait 1000
    Set IniciarWebDriver = driver
End Function

' Summary:   Abre un libro de trabajo de Excel desde una ruta específica.
' Param ruta: La ruta completa del archivo a abrir.
' Returns:   Un objeto Workbook si tiene éxito, de lo contrario Nothing.
Private Function AbrirLibro(ByVal ruta As String) As Workbook
    On Error Resume Next
    Set AbrirLibro = Workbooks.Open(ruta)
    If Err.Number <> 0 Then
        MsgBox "No se pudo abrir el archivo: " & ruta & vbCrLf & "Verifique que la ruta sea correcta y que tenga permisos.", vbCritical, "Error al Abrir Archivo"
        Set AbrirLibro = Nothing
    End If
    On Error GoTo 0
End Function

' Summary:   Obtiene una hoja de trabajo por su nombre. Si no existe, la crea.
'            Si la hoja tiene contenido, pregunta al usuario si desea limpiarla.
' Param wb:  El libro de trabajo donde se encuentra o se creará la hoja.
' Param nombreHoja: El nombre de la hoja a obtener o crear.
' Param limpiarSinPreguntar: (Opcional) Si es True, limpia la hoja sin preguntar.
' Returns:   Un objeto Worksheet o Nothing si el usuario decide no continuar.
Private Function ObtenerOPrepararHoja(ByVal wb As Workbook, ByVal nombreHoja As String, Optional ByVal limpiarSinPreguntar As Boolean = False) As Worksheet
    Dim ws As Worksheet
    Dim respuesta As VbMsgBoxResult

    On Error Resume Next
    Set ws = wb.Sheets(nombreHoja)
    On Error GoTo 0

    If ws Is Nothing Then
        Set ws = wb.Sheets.Add(After:=wb.Sheets(wb.Sheets.Count))
        ws.Name = nombreHoja
    Else
        If Not limpiarSinPreguntar Then
            If Application.WorksheetFunction.CountA(ws.Cells) > 0 Then
                respuesta = MsgBox("La hoja '" & nombreHoja & "' contiene datos. ¿Desea borrar el contenido?", vbYesNo + vbQuestion, "Confirmar Borrado")
                If respuesta = vbNo Then Exit Function ' Retorna Nothing
            End If
        End If
        ws.Cells.Clear
    End If

    Set ObtenerOPrepararHoja = ws
End Function

'---------------------------------------------------------------------------------------
'                               PROCESAMIENTO DE TABLAS
'---------------------------------------------------------------------------------------

' Summary:   Coordina la extracción y copiado de todas las tablas de datos.
' Param ws:  La hoja de cálculo de destino para los datos.
' Param driver: La instancia del WebDriver.
Private Sub ProcesarTodasLasTablas(ByVal ws As Worksheet, ByVal driver As Object)
    Dim currentRow As Long, currentCol As Long

    ws.Range("A1").Value = "Última actualización: " & Format(Now, "dd/mm/yyyy HH:MM")

    ' --- Tablas por Período de Tiempo ---
    currentRow = 3
    currentCol = 2
    ProcesarTablasPorPeriodo ws, driver, currentRow, currentCol

    ' --- Tablas de Semanas Pasadas ---
    currentRow = ws.UsedRange.Rows.Count + 4
    currentCol = 2
    ProcesarSemanasPasadas ws, driver, currentRow, currentCol

    ' --- Tablas del Mes Pasado ---
    currentRow = ws.UsedRange.Rows.Count + 4
    currentCol = 2
    ProcesarSemanasMesPasado ws, driver, currentRow, currentCol

    ' --- Tablas de Meses Anteriores ---
    currentRow = ws.UsedRange.Rows.Count + 4
    currentCol = 2
    ProcesarMesesAnteriores ws, driver, currentRow, currentCol
End Sub

' Summary:   Procesa las tablas para "Hoy", "Semana Actual", "Mes Actual" y "Año Actual".
Private Sub ProcesarTablasPorPeriodo(ByVal ws As Worksheet, ByVal driver As Object, ByRef row As Long, ByRef col As Long)
    Dim periodos(1 To 4) As String
    Dim fechas(1 To 2) As Date
    Dim i As Long

    periodos(1) = "Hoy"
    periodos(2) = "Semana Actual"
    periodos(3) = "Mes Actual"
    periodos(4) = "Año Actual"

    For i = 1 To 4
        fechas(1) = ObtenerFechaDesde(periodos(i))
        fechas(2) = ObtenerFechaHasta(periodos(i))

        ObtenerYCopiarTabla ws, driver, fechas(1), fechas(2), row, col, periodos(i)
        col = ws.Cells(row, ws.Columns.Count).End(xlToLeft).Column + 2
    Next i
End Sub

' Summary:   Procesa las tablas para los últimos 6 días de la semana pasada.
Private Sub ProcesarSemanasPasadas(ByVal ws As Worksheet, ByVal driver As Object, ByRef row As Long, ByRef col As Long)
    Dim i As Long
    Dim fecha As Date
    Dim primerDiaSemanaPasada As Date

    primerDiaSemanaPasada = Date - Weekday(Date, vbMonday) - 6

    For i = 0 To 5 ' Lunes a Sábado
        fecha = primerDiaSemanaPasada + i
        ObtenerYCopiarTabla ws, driver, fecha, fecha, row, col, "Semana Pasada: " & Format(fecha, "dddd, m/d/yyyy")
        col = ws.Cells(row, ws.Columns.Count).End(xlToLeft).Column + 2
    Next i
End Sub

' Summary:   Procesa las tablas por semanas del mes pasado.
Private Sub ProcesarSemanasMesPasado(ByVal ws As Worksheet, ByVal driver As Object, ByRef row As Long, ByRef col As Long)
    Dim primerDiaMesPasado As Date
    Dim ultimoDiaMesPasado As Date
    Dim inicioSemana As Date
    Dim finSemana As Date
    Dim semanaIndex As Long

    primerDiaMesPasado = DateSerial(Year(DateAdd("m", -1, Date)), Month(DateAdd("m", -1, Date)), 1)
    ultimoDiaMesPasado = Application.WorksheetFunction.EoMonth(primerDiaMesPasado, 0)

    ' Encontrar el primer lunes anterior o igual al primer día del mes
    inicioSemana = primerDiaMesPasado - (Weekday(primerDiaMesPasado, vbMonday) - 1)

    semanaIndex = 1
    Do While inicioSemana <= ultimoDiaMesPasado
        finSemana = inicioSemana + 6

        Dim fechaDesdeSemana As Date, fechaHastaSemana As Date
        fechaDesdeSemana = IIf(inicioSemana < primerDiaMesPasado, primerDiaMesPasado, inicioSemana)
        fechaHastaSemana = IIf(finSemana > ultimoDiaMesPasado, ultimoDiaMesPasado, finSemana)

        If fechaDesdeSemana <= fechaHastaSemana Then
            Dim tituloTabla As String
            tituloTabla = "Mes Pasado - Semana " & semanaIndex & " (" & Format(fechaDesdeSemana, "m/d") & " - " & Format(fechaHastaSemana, "m/d") & ")"
            ObtenerYCopiarTabla ws, driver, fechaDesdeSemana, fechaHastaSemana, row, col, tituloTabla
            col = ws.Cells(row, ws.Columns.Count).End(xlToLeft).Column + 2
            semanaIndex = semanaIndex + 1
        End If

        inicioSemana = inicioSemana + 7
    Loop
End Sub

' Summary:   Procesa las tablas de los últimos 6 meses anteriores.
Private Sub ProcesarMesesAnteriores(ByVal ws As Worksheet, ByVal driver As Object, ByRef row As Long, ByRef col As Long)
    Dim i As Long
    Dim fechaMes As Date
    Dim fechaDesde As Date, fechaHasta As Date

    For i = 1 To 6
        fechaMes = DateAdd("m", -i, Date)
        fechaDesde = DateSerial(Year(fechaMes), Month(fechaMes), 1)
        fechaHasta = Application.WorksheetFunction.EoMonth(fechaMes, 0)

        ObtenerYCopiarTabla ws, driver, fechaDesde, fechaHasta, row, col, "Mes Pasado - " & Format(fechaDesde, "MMMM YYYY")
        col = ws.Cells(row, ws.Columns.Count).End(xlToLeft).Column + 2
    Next i
End Sub

'---------------------------------------------------------------------------------------
'                               OBTENCIÓN Y PARSEO DE DATOS WEB
'---------------------------------------------------------------------------------------

' Summary:   Obtiene los datos de una tabla de la web y los copia a la hoja de Excel.
'            Esta es una función clave que necesita ser robusta.
Public Sub ObtenerYCopiarTabla(ByVal ws As Worksheet, ByVal driver As Object, ByVal fechaDesde As Date, ByVal fechaHasta As Date, ByVal filaInicio As Long, ByVal colInicio As Long, ByVal tipoTabla As String)
    On Error GoTo ErrorHandler

    ' --- Navegación y Obtención de HTML ---
    NavegarAFechas driver, fechaDesde, fechaHasta
    Dim tablaHtml As String
    tablaHtml = driver.ExecuteScript("return document.querySelector('" & SELECTOR_TABLA & "').outerHTML;")

    If tablaHtml = "" Or InStr(1, tablaHtml, "No data to display", vbTextCompare) > 0 Then
        ws.Cells(filaInicio, colInicio).Value = tipoTabla & " (Sin Datos)"
        Exit Sub
    End If

    ' --- Parseo de HTML y Volcado a Excel ---
    Dim datosTabla As Variant
    datosTabla = ParsearTablaHtml(tablaHtml)

    If Not IsEmpty(datosTabla) Then
        Dim numRows As Long, numCols As Long
        numRows = UBound(datosTabla, 1)
        numCols = UBound(datosTabla, 2)

        ' Volcar los datos del array a la hoja de una sola vez
        ws.Cells(filaInicio, colInicio).Value = tipoTabla
        ws.Range(ws.Cells(filaInicio + 1, colInicio), ws.Cells(filaInicio + numRows, colInicio + numCols - 1)).Value = datosTabla

        AplicarFormatoTabla ws, filaInicio, colInicio, filaInicio + numRows, colInicio + numCols - 1, tipoTabla
    Else
        ws.Cells(filaInicio, colInicio).Value = tipoTabla & " (Vacío)"
    End If

    Exit Sub
ErrorHandler:
    ws.Cells(filaInicio, colInicio).Value = tipoTabla & " (Error)"
End Sub

' Summary:   Navega a un rango de fechas específico en la página web.
Private Sub NavegarAFechas(ByVal driver As Object, ByVal fechaDesde As Date, ByVal fechaHasta As Date)
    With driver
        .FindElementById(ID_CAMPO_DESDE).Clear
        .FindElementById(ID_CAMPO_DESDE).SendKeys Format(fechaDesde, "m/d/yyyy")
        .FindElementById(ID_CAMPO_HASTA).Clear
        .FindElementById(ID_CAMPO_HASTA).SendKeys Format(fechaHasta, "m/d/yyyy")
        .FindElementById(ID_BOTON_BUSCAR).Click
        .Wait 1500 ' Espera para que la tabla se cargue
    End With
End Sub

' Summary:   Parsea una tabla HTML y la convierte en un array 2D de VBA.
'            Excluye la columna que contiene la palabra "complex" en el encabezado.
' Param tablaHtml: El string que contiene el HTML de la tabla.
' Returns:   Un array 2D con los datos de la tabla.
Private Function ParsearTablaHtml(ByVal tablaHtml As String) As Variant
    Dim htmlDoc As Object
    Set htmlDoc = CreateObject("htmlfile")
    htmlDoc.body.innerHTML = tablaHtml

    Dim tabla As Object
    Set tabla = htmlDoc.getElementsByTagName("table")(0)
    If tabla Is Nothing Then Exit Function

    Dim numRows As Long
    numRows = tabla.Rows.Length
    If numRows = 0 Then Exit Function

    ' --- Encontrar la columna a excluir ---
    Dim colToExclude As Long
    colToExclude = -1
    Dim headerCell As Object
    Dim c As Long
    If tabla.Rows(0).Cells.Length > 0 Then
        For c = 0 To tabla.Rows(0).Cells.Length - 1
            Set headerCell = tabla.Rows(0).Cells(c)
            If InStr(1, headerCell.innerText, "complex", vbTextCompare) > 0 Then
                colToExclude = c
                Exit For
            End If
        Next c
    End If

    ' --- Determinar el tamaño del array de salida ---
    Dim numCols As Long
    numCols = tabla.Rows(0).Cells.Length
    If colToExclude <> -1 Then numCols = numCols - 1
    If numCols <= 0 Then Exit Function

    Dim datos() As Variant
    ReDim datos(1 To numRows, 1 To numCols)

    ' --- Llenar el array con los datos ---
    Dim r As Long, out_c As Long
    For r = 0 To numRows - 1
        out_c = 1
        For c = 0 To tabla.Rows(r).Cells.Length - 1
            If c <> colToExclude Then
                datos(r + 1, out_c) = Trim(tabla.Rows(r).Cells(c).innerText)
                out_c = out_c + 1
            End If
        Next c
    Next r

    ParsearTablaHtml = datos
End Function


'---------------------------------------------------------------------------------------
'                               GENERACIÓN DE ESTADÍSTICAS
'---------------------------------------------------------------------------------------

' Summary:   Genera una hoja de estadísticas de desempeño por diseñador.
Sub GenerarEstadisticasDiseñadores(ByVal wstablas As Worksheet, ByVal wsStats As Worksheet)
    Dim datos As Variant
    datos = wstablas.UsedRange.Value

    Dim designerData As Object
    Set designerData = CreateObject("Scripting.Dictionary")

    Dim r As Long, c As Long
    Dim currentHeader As String
    Dim productionColIndex As Long

    ' --- Recopilar Datos ---
    For r = 1 To UBound(datos, 1)
        ' Identificar una fila de encabezado de tabla
        If Not IsEmpty(datos(r, 2)) And InStr(1, datos(r, 2), "Semana") > 0 Or InStr(1, datos(r, 2), "Mes") > 0 Or InStr(1, datos(r, 2), "Hoy") > 0 Or InStr(1, datos(r, 2), "Año") > 0 Then
            currentHeader = datos(r, 2)
            productionColIndex = -1
            ' Encontrar la columna de producción para esta tabla
            For c = 2 To UBound(datos, 2)
                If IsEmpty(datos(r + 1, c)) Then Exit For
                If InStr(1, LCase(datos(r + 1, c)), "total") > 0 Or InStr(1, LCase(datos(r + 1, c)), "prod") > 0 Then
                    productionColIndex = c
                    Exit For
                End If
            Next c
        End If

        ' Procesar filas de datos si estamos dentro de una tabla válida
        If productionColIndex <> -1 And r > 1 And Not IsEmpty(datos(r, 2)) Then
            Dim designerName As String
            designerName = Trim(datos(r, 2))

            If Not IsNumeric(designerName) And designerName <> "" Then
                If Not designerData.Exists(designerName) Then
                    ' Inicializar estadísticas para un nuevo diseñador
                    designerData.Add designerName, CreateObject("Scripting.Dictionary")
                    designerData(designerName)("TotalProduced") = 0
                    designerData(designerName)("DailyRecords") = CreateObject("System.Collections.ArrayList")
                    designerData(designerName)("DaysActive") = 0
                    designerData(designerName)("WeeklyProdCurrent") = 0
                    designerData(designerName)("MonthlyProdCurrent") = 0
                End If

                ' Acumular estadísticas
                Dim value As Double
                If IsNumeric(datos(r, productionColIndex)) Then
                    value = CDbl(datos(r, productionColIndex))
                    designerData(designerName)("TotalProduced") = designerData(designerName)("TotalProduced") + value

                    If InStr(1, currentHeader, "Hoy", vbTextCompare) > 0 Or InStr(1, currentHeader, "Semana Pasada", vbTextCompare) > 0 Then
                        designerData(designerName)("DailyRecords").Add value
                        designerData(designerName)("DaysActive") = designerData(designerName)("DaysActive") + 1
                    End If
                    If InStr(1, currentHeader, "Semana Actual", vbTextCompare) > 0 Then
                        designerData(designerName)("WeeklyProdCurrent") = designerData(designerName)("WeeklyProdCurrent") + value
                    End If
                    If InStr(1, currentHeader, "Mes Actual", vbTextCompare) > 0 Then
                        designerData(designerName)("MonthlyProdCurrent") = designerData(designerName)("MonthlyProdCurrent") + value
                    End If
                End If
            End If
        End If
    Next r

    ' --- Escribir Resultados en la Hoja de Estadísticas ---
    EscribirResultadosEstadisticas wsStats, designerData
End Sub

' Summary: Escribe los datos de estadísticas procesados en la hoja de destino.
Private Sub EscribirResultadosEstadisticas(ByVal ws As Worksheet, ByVal data As Object)
    ws.Cells.Clear

    ' --- Encabezados ---
    ws.Cells(1, 1).Value = "Estadísticas de Desempeño por Diseñador"
    With ws.Cells(1, 1).Font: .Bold = True: .Size = 16: End With

    Dim headers As Variant
    headers = Array("Diseñador", "Total Producido (General)", "Promedio Diario", "Mayor Producción (Día)", "Menor Producción (Día)", "Días Activos", "Productividad Semanal (Actual)", "Productividad Mensual (Actual)")
    ws.Range("A3").Resize(1, UBound(headers) + 1).Value = headers

    ' --- Escribir Datos ---
    Dim outputRow As Long: outputRow = 4
    Dim k As Variant, stats As Object, dailyRecs As Object

    If data.Count = 0 Then
        ws.Cells(outputRow, 1).Value = "No se encontraron datos de diseñadores."
        Exit Sub
    End If

    For Each k In data.Keys
        Set stats = data(k)
        Set dailyRecs = stats("DailyRecords")

        ws.Cells(outputRow, 1).Value = k
        ws.Cells(outputRow, 2).Value = stats("TotalProduced")

        If stats("DaysActive") > 0 Then
            ws.Cells(outputRow, 3).Value = stats("TotalProduced") / stats("DaysActive")
        Else
            ws.Cells(outputRow, 3).Value = 0
        End If

        If dailyRecs.Count > 0 Then
            ws.Cells(outputRow, 4).Value = Application.WorksheetFunction.Max(dailyRecs.toarray())
            ws.Cells(outputRow, 5).Value = Application.WorksheetFunction.Min(dailyRecs.toarray())
        Else
            ws.Cells(outputRow, 4).Value = 0
            ws.Cells(outputRow, 5).Value = 0
        End If

        ws.Cells(outputRow, 6).Value = stats("DaysActive")
        ws.Cells(outputRow, 7).Value = stats("WeeklyProdCurrent")
        ws.Cells(outputRow, 8).Value = stats("MonthlyProdCurrent")

        outputRow = outputRow + 1
    Next k

    ' --- Formato ---
    With ws.Range("A3").Resize(1, UBound(headers) + 1)
        .Interior.Color = COLOR_ENCABEZADO_STATS
        .Font.Color = vbWhite
        .Font.Bold = True
    End With
    ws.UsedRange.Columns.AutoFit
    ws.Range("B:E,G:H").NumberFormat = "#,##0.00"
End Sub


'---------------------------------------------------------------------------------------
'                           FORMATO Y ESTILOS DE EXCEL
'---------------------------------------------------------------------------------------

' Summary:   Aplica formato a una tabla recién copiada en la hoja.
Private Sub AplicarFormatoTabla(ws As Worksheet, f1 As Long, c1 As Long, f2 As Long, c2 As Long, tipo As String)
    Dim rangoTabla As Range
    Set rangoTabla = ws.Range(ws.Cells(f1, c1), ws.Cells(f2, c2))

    ' --- Autoajuste de Columnas ---
    rangoTabla.Columns.AutoFit

    ' --- Coloreado del Encabezado ---
    Dim colorFondo As Long
    Select Case tipo
        Case "Hoy": colorFondo = COLOR_HOY
        Case "Semana Actual": colorFondo = COLOR_SEMANA
        Case "Mes Actual": colorFondo = COLOR_MES
        Case "Año Actual": colorFondo = COLOR_ANIO
        Case Else: colorFondo = COLOR_OTRO
    End Select

    With ws.Range(ws.Cells(f1, c1), ws.Cells(f1, c2))
        .Interior.Color = colorFondo
        .Font.Color = vbWhite
        .Font.Bold = True
        .Font.Size = 12
    End With

    ' --- Coloreado Alterno de Filas ---
    Dim i As Long
    For i = f1 + 1 To f2
        If (i - (f1 + 1)) Mod 2 = 0 Then
            ws.Range(ws.Cells(i, c1), ws.Cells(i, c2)).Interior.Color = COLOR_FILA_PAR
        Else
            ws.Range(ws.Cells(i, c1), ws.Cells(i, c2)).Interior.ColorIndex = xlNone
        End If
    Next i

    ' --- Aplicación de Bordes ---
    With rangoTabla.Borders
        .LineStyle = xlContinuous
        .Weight = xlThin
        .Color = RGB(200, 200, 200)
    End With

    With rangoTabla.Borders(xlEdgeTop)
        .Weight = xlMedium
        .Color = RGB(47, 84, 150)
    End With
    With rangoTabla.Borders(xlEdgeBottom)
        .Weight = xlMedium
        .Color = RGB(47, 84, 150)
    End With
    With rangoTabla.Borders(xlEdgeLeft)
        .Weight = xlMedium
        .Color = RGB(47, 84, 150)
    End With
    With rangoTabla.Borders(xlEdgeRight)
        .Weight = xlMedium
        .Color = RGB(47, 84, 150)
    End With

    ' --- Limitación de Ancho de Columnas ---
    Dim col As Long
    For col = c1 To c2
        If ws.Columns(col).ColumnWidth > 35 Then ws.Columns(col).ColumnWidth = 35
        If ws.Columns(col).ColumnWidth < 10 Then ws.Columns(col).ColumnWidth = 10
    Next col
End Sub


'---------------------------------------------------------------------------------------
'                           FUNCIONES DE FECHAS Y AUXILIARES
'---------------------------------------------------------------------------------------

' Summary:   Obtiene la fecha de inicio para un período de tiempo dado.
Private Function ObtenerFechaDesde(ByVal periodo As String) As Date
    Select Case periodo
        Case "Hoy": ObtenerFechaDesde = Date
        Case "Semana Actual": ObtenerFechaDesde = Date - Weekday(Date, vbMonday) + 1
        Case "Mes Actual": ObtenerFechaDesde = DateSerial(Year(Date), Month(Date), 1)
        Case "Año Actual": ObtenerFechaDesde = DateSerial(Year(Date), 1, 1)
    End Select
End Function

' Summary:   Obtiene la fecha de fin para un período de tiempo dado.
Private Function ObtenerFechaHasta(ByVal periodo As String) As Date
    Select Case periodo
        Case "Hoy", "Semana Actual", "Mes Actual", "Año Actual": ObtenerFechaHasta = Date
    End Select
End Function

'---------------------------------------------------------------------------------------
'                           MANEJO DE USERFORMS (Ejemplo)
'---------------------------------------------------------------------------------------

' Summary:   Maneja el evento Change del ComboBox de categorías.
'            (Asumiendo que existe un UserForm con cmbCategorias y listProblemas)
Public Sub CargarProblemasPorCategoria(ByVal categoria As String, ByVal listBox As Object)
    listBox.Clear
    Select Case categoria
        Case "Problemas de Sujeción"
            listBox.List = Array("No asegura cover cerrado", "No asegura TPA cerrado", "No asegura candado cerrado", "Lever no sujeta componente", "Se pierde PC de CPA", "Se pierde PC de clip", "Se pierde PC de corbata", "Se suelta terminales", "Componente ajustado / no entra", "Palanca no desliza / no sujeta")
        Case "Falta de Componentes"
            listBox.List = Array("Hace PC de cover sin traerlo", "Hace PC de PLR sin traerlo", "Hace PC de TPA sin traerlo", "Falta foco LED", "Falta slot en cover para cable eslaider", "Falta hoja de capacidad", "Falta diagrama de componente", "Falta PC en cover de arriba", "Falta aditamento para sujeción push button")
        Case "Problemas de Documentación"
            listBox.List = Array("Hoja de capacidad mal redactada", "Hoja de capacidad sin set-up", "No pasa VN", "No pasa vacío", "No es error proof contra sí mismo", "Doble sujeción", "Intermitencia")
        Case "Problemas de Diseño"
            listBox.List = Array("Pernos de expulsión ineficientes", "Tornillo tapa barreno de vacío", "Dimensiones no concuerdan", "Cavidad daña el clap", "Barrenos desalineados", "Componente se atora al salir")
        Case "Otros Problemas"
            listBox.List = Array("Se pierden PCS", "Componente no entra / no sujeta / se suelta", "Problemas con el lever", "Se quiebran pernos", "Palanca golpea en mano")
    End Select
End Sub

'---------------------------------------------------------------------------------------
'                               UTILIDADES ADICIONALES
'---------------------------------------------------------------------------------------

' Summary:   Copia la hoja "tablas" del libro de datos al libro principal de la macro,
'            actualizando o creando la hoja según sea necesario.
Public Sub SincronizarHojaDeDatos()
    Dim wbOrigen As Workbook
    Dim wsOrigen As Worksheet
    Dim wbDestino As Workbook
    Dim wsDestino As Worksheet

    On Error GoTo ErrorHandler

    ' --- Abrir Libros ---
    Set wbDestino = ThisWorkbook ' Asume que esta macro se ejecuta desde "America Opt.xlsm"
    Set wbOrigen = Workbooks.Open(RUTA_REPORTE)

    If wbOrigen Is Nothing Then
        MsgBox "No se pudo abrir el libro de origen en: " & RUTA_REPORTE, vbCritical
        Exit Sub
    End If

    On Error Resume Next
    Set wsOrigen = wbOrigen.Sheets(NOMBRE_HOJA_DATOS)
    If wsOrigen Is Nothing Then
        MsgBox "La hoja '" & NOMBRE_HOJA_DATOS & "' no existe en el libro de origen.", vbCritical
        wbOrigen.Close SaveChanges:=False
        Exit Sub
    End If
    On Error GoTo ErrorHandler

    ' --- Verificar y Copiar ---
    On Error Resume Next
    Set wsDestino = wbDestino.Sheets(NOMBRE_HOJA_DATOS)
    On Error GoTo 0 ' Desactivar Resume Next lo antes posible

    If wsDestino Is Nothing Then
        ' La hoja no existe, la copiamos
        wsOrigen.Copy After:=wbDestino.Sheets(wbDestino.Sheets.Count)
        MsgBox "La hoja '" & NOMBRE_HOJA_DATOS & "' ha sido creada y actualizada.", vbInformation
    Else
        ' La hoja ya existe, la limpiamos y copiamos los datos
        wsDestino.Cells.Clear
        wsOrigen.UsedRange.Copy Destination:=wsDestino.Range("A1")
        MsgBox "La hoja '" & NOMBRE_HOJA_DATOS & "' ha sido actualizada con los datos más recientes.", vbInformation
    End If

    wbOrigen.Close SaveChanges:=False
    Exit Sub

ErrorHandler:
    MsgBox "Ocurrió un error durante la sincronización: " & Err.Description, vbExclamation
    If Not wbOrigen Is Nothing Then wbOrigen.Close SaveChanges:=False
End Sub
