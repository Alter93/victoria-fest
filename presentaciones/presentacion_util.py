import datetime
import hashlib
import hmac
import base64

from django.utils import timezone

from presentaciones.models import Conferencia, Conferencista

class ConferenciaZoom:
    API_KEY = 'LgZGayuuTmm070LUrKr_2w'
    API_SECRET = 'Vl1G119NpLs0Kdv6kgCvL923t8QjaCHKzlKc'

    def __init__(self, lugar = 'todo', conf = None):
        self.conferencia = self.obtener_conferencia(lugar = lugar, conf = conf)

        if (self.conferencia != None):
            self.data = {
                'apiKey': ConferenciaZoom.API_KEY,
                'apiSecret': ConferenciaZoom.API_SECRET,
                'meetingNumber': self.conferencia.zoom_id,
                'role': 0
            }
            self.signature = self.generateSignature(self.data)

    def obtener_conferencia(self, lugar='todo', conf = None):
        fecha = timezone.now()
        if conf != None:
            conferencia = Conferencia.objects.get(
                uuid=conf
            )
        else:
            if lugar == 'todo':
                conferencias = Conferencia.objects.filter(
                    fecha_hora__lte=fecha
                )

            else:
                conferencias = Conferencia.objects.filter(
                        lugar=lugar
                    ).filter(
                        fecha_hora__lte=fecha
                    )
                conferencias_filtradas = []
            for conferencia in conferencias:
                if (conferencia.fecha_hora + conferencia.duracion > fecha):
                    conferencias_filtradas.append(conferencia)

            if len(conferencias_filtradas) > 0:
                conferencia = conferencias_filtradas[0]
            else:
                conferencia = None

        return conferencia

    def generateSignature(self, data):
        ts = int(round(timezone.now().timestamp() * 1000)) - 30000;
        msg = data['apiKey'] + str(data['meetingNumber']) + str(ts) + str(data['role']);
        message = base64.b64encode(bytes(msg, 'utf-8'));
        # message = message.decode("utf-8");
        secret = bytes(data['apiSecret'], 'utf-8')
        hash = hmac.new(secret, message, hashlib.sha256);
        hash =  base64.b64encode(hash.digest());
        hash = hash.decode("utf-8");
        tmpString = "%s.%s.%s.%s.%s" % (data['apiKey'], str(data['meetingNumber']), str(ts), str(data['role']), hash);
        signature = base64.b64encode(bytes(tmpString, "utf-8"));
        signature = signature.decode("utf-8");
        return signature.rstrip("=");
