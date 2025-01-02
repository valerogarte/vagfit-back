class ImagenURLMixin:
    def get_imagen_url(self, obj, imagen_field):
        request = self.context.get('request')
        imagen = getattr(obj, imagen_field)
        if imagen and request:
            scheme = request.scheme
            host = request.get_host()
            port = request.get_port()
            url = f"{scheme}://{host}:{port}{imagen.url}"
            return url
        elif imagen:
            return imagen.url
        return None