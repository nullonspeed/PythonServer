from datetime import date, datetime

from opcua import ua, Server
import sys
import socket
import json


#erstellung des Servers und einrichten des Localhosts
sys.path.insert(0, "..")
server = Server()
server.set_server_name("DynamicOpcUaServer")
server.set_endpoint("opc.tcp://127.0.0.1:4840/dynamicocp/ua/server")
#Konfiguration von eher unwichtigen werten vom server Folgend
server.name = "DynamicOPCUAServer"
uri = "https://DynamicOPCUAServer.com"

#der namespace wird öfter verwendet und ist notwendig für das erstellen von variablen und objekten
idx = server.register_namespace(uri)

#grund objekt
objects = server.get_objects_node()

#security policy für den server wie man den server verwenden kann
server.set_security_policy = [
    ua.SecurityPolicyType.NoSecurity,
    ua.SecurityPolicyType.Basic256_SignAndEncrypt,
    ua.SecurityPolicyType.Basic256Sha256_Sign
]
#den OPC UA Server starten
server.start()
#einrichtung des Server Sockets um verbindung mit dem C# Client herzustellen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 484))
server_socket.listen()
client_socket, client_address = server_socket.accept()


#Objekt das gesendete werte speichern kann in einer später benutzten Liste
class Werteliste():
    def __init__(self,wInterface, variablenname, datentyp):
        self.WInterface = wInterface
        self.Variablenname = variablenname
        self.Datentyp = datentyp


        #serverTry parse
try:
    while True:
        #verbindungsaufbau zum Client bzw die bekommenen daten werden hier limitiert wieviel entgegen genommen werden kann
        recived_data = client_socket.recv(32768)
        if recived_data.decode('utf-8') is not '':
            #decodieren um zu lesen da hier die daten über utf-8 geschickt werden
            temp = recived_data.decode('utf-8')

            jsonstring = json.loads(temp)

            #hier wird eine variablen und Interface liste erstellt um angenehm die werte weiter zu geben und zu speichern die vom Json bereitgestellt werden
            variablenListe = []
            InterfaceList = []
            for liste in range(len(jsonstring)):
                wInterfaceString = jsonstring[liste]['WorkflowInterfaceName']
                v1 = Werteliste(wInterfaceString, jsonstring[liste]['VariableName'], jsonstring[liste]['PlcVariableType'])
                if not InterfaceList.__contains__(wInterfaceString):
                    InterfaceList.append(wInterfaceString)
                variablenListe.append(v1)


            #der Tree wird hier festgelegt, und dadurch das der die einzelnen variablen enthält mit verschiedenen Datentypen
            #wird alles mit if else eingefügt (andere möglichkeit wäre ein Dictionary gewesen, dies wurde nicht gewählt da auch der momentane wert
            # der Daten die Bugfrei angezeigt werden können)
            for interface in InterfaceList:
                tempObject = objects.add_object(idx, interface)
                for wert in variablenListe:
                    if wert.WInterface == interface:
                        if wert.Datentyp == "BYTE":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=3)
                        elif wert.Datentyp == "BOOL":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "" == "", datatype=1)
                        elif wert.Datentyp == "WORD":
                            #Word wird als string eingelesen, da bei ua expert nichts direktes wie ein word ist
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "LWORD":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "DWORD":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "SINT":
                            #SInt ist kleiner als der kleinste wert in UA Expert daher wir Int16 verwendet
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=4)
                        elif wert.Datentyp == "INT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=4)
                        elif wert.Datentyp == "DINT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=6)
                        elif wert.Datentyp == "USINT":
                            #selbes Problem wie bei SInt
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=5)
                        elif wert.Datentyp == "UINT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=5)
                        elif wert.Datentyp == "UDINT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=7)
                        elif wert.Datentyp == "LINT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=8)
                        elif wert.Datentyp == "ULINT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=9)
                        elif wert.Datentyp == "REAL":
                            #für real ist auch kein direkter typ zur verfügung, deswegen wird auch hier string verwendet
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "LREAL":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "S5TIME":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "TIME":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "LTIME":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "CHAR":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "WCHAR":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "STRING":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "WSTRING":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "DATE":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "TOD":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "LTOD":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "DT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "LDT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        elif wert.Datentyp == "DTL":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0, datatype=13)
                        #ab hier sind dummy datentypen. Das ist weil kein passender wert bei UA Expert gefunen wurde
                        elif wert.Datentyp == "POINTER":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "ANY":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)
                        elif wert.Datentyp == "VARIANT":
                            vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, "", datatype=12)

                        vartest.set_writable()

            server_socket.close()
finally:

    server.stop()





