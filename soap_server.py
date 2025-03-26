from flask import Flask, request, Response
from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

app = Flask(__name__)

class SoapService(ServiceBase):
    @rpc(_returns=String)
    def getContacts(ctx):
        return "John Doe, Jane Smith, Alice Johnson"

    @rpc(_returns=String)
    def getAddresses(ctx):
        return "Jl. Sudirman No.1, Jl. Thamrin No.2, Jl. Merdeka No.3"

soap_app = Application(
    [SoapService],
    tns="http://127.0.0.1:8001/soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)

@app.route("/soap", methods=["POST"])
def soap_endpoint():
    print("SOAP request received!")  # Log request

    from io import BytesIO
    environ = request.environ.copy()
    environ["wsgi.input"] = BytesIO(request.data)

    response_data = wsgi_app(environ, lambda status, headers: None)  # Menggunakan lambda untuk menghindari error

    return Response(response_data, content_type="text/xml; charset=utf-8")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)
