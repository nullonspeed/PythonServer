from opcua import ua, Server
import sys
import time
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
#myobj = objects.add_object(idx, "MyObject")
#myvar = myobj.add_variable(idx, "MyVariable", 0)
#var = server.nodes.objects.add_variable(idx, node_id, "MyVariable", 1)
#myvar.set_writable()
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
try:
    count = 0
    while True:
        time.sleep(1)
        count += 0.1
        #myvar.set_value(count)
finally:

    server.stop()


#server.set_security_IDs([
#    ('username', 'password'),
 #   ('certificate', 'private_key.pem', 'certificate.pem')
#])




