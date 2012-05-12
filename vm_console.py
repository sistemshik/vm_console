import cherrypy
from xen.util.xmlrpcclient import ServerProxy
import re

server = ServerProxy('httpu:///var/run/xend/xmlrpc.sock')
domains = server.xend.domains_with_state(True, 'all', 1)
#map(PrettyPrint.prettyprint, doms)

class xen():
    """Communicates with xen via rpc"""
    @staticmethod
    def get_domains():
        """Gets a dictionary with 'Domain Name':'VNC host:port' structure"""
        domain_list = {}
        for first_level in domains:                             # iterate through first level parameters
            for second_level in first_level:                    # iterate through second level parameters
                if second_level[0] == "name" and second_level[1] != "Domain-0":
                    domain_list_current = second_level[1]
                if second_level[0] == "device":
                    for third_level in second_level[1]:         # iterate through third level subparameters
                        if third_level[0] == "location" and re.match("\d+\.\d+\.\d+\.\d+\:\d\d\d\d", third_level[1]):
                            domain_list[domain_list_current] = str(third_level[1])
        return domain_list

    @staticmethod
    def create_domain_table():
        """Creates table from domain list"""        
        table = """<table id='mytable' cellspacing='0'><caption>List of active domUs</caption>
                   <th scope="col" class="nobg">domU</th>
                   <th scope="col">VNC host:port</th>
            """
        domain_list = xen.get_domains()
        for k, v in domain_list.iteritems():
            link = v.split(':', 1)[1]
            table += """
                <tr>
                <th class="spec" scope="row">%s</th>
                <td><a href="javascript:vnc_console('/vnc/%s')" target='_blank'>%s</a></td>
                </tr>
                """ % (k, link, v)

        table += "</table>"
        return table

class listvm(object):
    def index(self, port=None):
        """Just a stub"""
        return """<h1><a href="/vnc/">vnc</a></h1>"""
    index.exposed = True
    def vnc(self, port=None):
        """Show running vm's or open vnc applet"""
        if port:
            template = open("static/vnc.htm", 'r').read() 
            return template % port 
        else:
            template = open("static/table.htm", 'r').read()
            return template % xen.create_domain_table()
            
    vnc.exposed = True

server_config = {
                  'server.socket_host': '127.0.0.1',
                  'server.socket_port': 80,
                  'tools.staticdir.root': "/root/bin/vm_console",
                  'tools.staticdir.debug': True,
                }
cherrypy.config.update(server_config)

listvm_config = {
                '/static':
                    {'tools.staticdir.on': True,
                     'tools.staticdir.dir': "static",
                    }
                }
cherrypy.tree.mount(listvm(), '/', config=listvm_config)

cherrypy.engine.start()
cherrypy.engine.block()

