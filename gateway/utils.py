import json 


class GatewayUtil: 

    services = []
    urls = []
    
    def __init__(self):
        self.services = self.read_services()
        self.urls = self.generate_service_url()
    
    def read_services(self):

        services = []

        f = open('service.json')     
        data = json.load(f) 
        f.close() 

        for service in data["services"]:
            services.append(service)

        return services


    def generate_service_url(self):

        urls = []

        for service in self.services:
            for route in service["route"]:
                url = {
                    "url": "/" + service["gateway_url"] + "/" + route["url"],
                    "service_url": route["baseurl"],
                    "jwt_secure": route["jwt_secure"]
                }
                urls.append(url)
            
        return urls