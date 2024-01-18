from opcua import ua, Server
import sys
import time
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

#node_id = "ns=2;i=1;"
myobj = objects.add_object(idx, "MyObject")
myvar = myobj.add_variable(idx, "MyVariable", 0)
#var = server.nodes.objects.add_variable(idx, node_id, "MyVariable", 1)
myvar.set_writable()


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
    def __init__(self,wInterface, variablenname):
        self.WInterface = wInterface
        self.Variablenname = variablenname


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
                wInterfaceString=jsonstring[liste]['WorkflowInterfaceName']
                v1 = Werteliste(wInterfaceString, jsonstring[liste]['VariableName'])
                if not InterfaceList.__contains__(wInterfaceString):
                    InterfaceList.append(wInterfaceString)
                variablenListe.append(v1)


                #vartest = myobj.add_variable(idx, jsonstring[liste]['WorkflowInterfaceName']+"."+jsonstring[liste]['VariableName'], 0)
                #vartest.set_writable()

            for interface in InterfaceList:
                tempObject = objects.add_object(idx, interface)
                for wert in variablenListe:
                    if wert.WInterface == interface:
                        vartest = tempObject.add_variable(idx, wert.WInterface+'.'+wert.Variablenname, 0)
                        vartest.set_writable()

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




