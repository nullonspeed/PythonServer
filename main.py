from datetime import date, datetime

from opcua import ua, Server
import sys
import socket
import json
#def data_change_handler(var, val):
 #   print(f"Variable {var} has changed to {val}")


sys.path.insert(0, "..")
server = Server()
server.set_server_name("DynamicOpcUaServer")
server.set_endpoint("opc.tcp://127.0.0.1:4840/dynamicocp/ua/server")

server.name = "DynamicOPCUAServer"
uri = "https://DynamicOPCUAServer.com"
idx = server.register_namespace(uri)

objects = server.get_objects_node()

server.set_security_policy = [
    ua.SecurityPolicyType.NoSecurity,
    ua.SecurityPolicyType.Basic256_SignAndEncrypt,
    ua.SecurityPolicyType.Basic256Sha256_Sign
]
#print(objects.add_data_type(idx, "String", description=None))
#node_id = "ns=2;i=1;"







myobj = objects.add_object(idx, "MyObject")


#Datentyp Int64 als normale Zahl wird normal verschickt. Datentyp DateTime funktioniert genau so. Datentyp String Direkt auch, Sonderwerte oder z.b.
# hex(0) wird als string verschickt, Double kann auch verschickt werden, aber der Datentyp ändert nur as Attribut des datetyps
#int16= datatype 4 funktioniert, wenn man im UA Expert auf die variablen clickt um den Wert zu ändern und dan Enter drückt
#bool in beiden Datentyp 1, und funktioniert, also im cybernetic config und opc ua
#byte ist 2 im config tool und 3 im UA Expert

#str(0), datatype=12
#myvar = myobj.add_variable_type(idx, "MyVariable", 0.0)
#myvar.set_data_type(ua.VariantType.String)
#var = server.nodes.objects.add_variable(idx, node_id, "MyVariable", 1)



#sub = server.create_subscription(500, data_change_handler)
#handle = sub.subscribe_data_change(myvar)

#var.set_writable()
#server.set_attribute_value(node_id, "MyObject", 14)
#node_id = "ns=58;s=MyVariable"
#server.set_attribute_value(node_id, "MyDataValue", 14)

#var.set_attribute(14, "DynamicOPCVar")
#var.set_attribute(15, "MyVariable")  # DisplayName
#var.set_attribute(16, "This is my variable")  # Description
#var.set_attribute(17, 1)  # WriteMask
#var.set_attribute(27, 2)  # UserWriteMask
#var.set_attribute(10, ua.NodeId(ua.ObjectIds.Int32))  # DataTy
server.start()


#vartest = myobj.add_variable(idx, 'testing', 1)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 484))
server_socket.listen()
client_socket, client_address = server_socket.accept()


class Werteliste():
    def __init__(self,wInterface, variablenname, datentyp):
        self.WInterface = wInterface
        self.Variablenname = variablenname
        self.Datentyp = datentyp

#datentypen dictionary machen mit tobis werte

try:
    while True:
        #server_socket.listen()
        #client_socket, client_address = server_socket.accept()
        recived_data = client_socket.recv(4096)
        if recived_data.decode('utf-8') is not '':
            #print(recived_data)
            temp = recived_data.decode('utf-8')
            #print(temp)
            #temp1 = temp.split(' ')
            jsonstring = json.loads(temp)
            #print(jsonstring)
            #print(jsonstring[0])
            print(jsonstring[0]['VariableName'])
            variablenListe = []
            InterfaceList = []
            for liste in range(len(jsonstring)):
                wInterfaceString = jsonstring[liste]['WorkflowInterfaceName']
                v1 = Werteliste(wInterfaceString, jsonstring[liste]['VariableName'], jsonstring[liste]['PlcVariableType'])
                if not InterfaceList.__contains__(wInterfaceString):
                    InterfaceList.append(wInterfaceString)
                variablenListe.append(v1)


                #vartest = myobj.add_variable(idx, jsonstring[liste]['WorkflowInterfaceName']+"."+jsonstring[liste]['VariableName'], 0)
                #vartest.set_writable()

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
                        #print(wert.Datentyp)

                #print(wert.WInterface+"."+wert.Variablenname)
            #vartest = myobj.add_variable(idx, temp1[1], 0)
            #vartest = myobj.add_variable(idx, 'testing', 1, 1)

            #vartest.set_writable()
            #print(recived_data.decode('utf-8'))
            #client_socket.sendall('funktioniert')
            server_socket.close()
finally:

    server.stop()


#server.set_security_IDs([
#    ('username', 'password'),
 #   ('certificate', 'private_key.pem', 'certificate.pem')
#])




