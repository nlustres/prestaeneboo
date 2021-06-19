# -*- coding: utf-8 -*-

from prestapyt import PrestaShopWebService, PrestaShopWebServiceError
import sys, getopt
import ast
import xml.etree.ElementTree as ET
import requests

class PrestaShop:
	url = None
	clave = None
	prestashop = None
	resultado = None
	
	
	def __init__(self, url, clave, debug=False, session=None, verbose=False):
		self.url = url
		self.clave = clave
		
		try:		
			self.prestashop = PrestaShopWebService(self.url, self.clave, debug, session, verbose)						
		except PrestaShopWebServiceError as err:		
			sys.stderr.write(str(err))
			sys.exit()
		
	def get(self, recurso, id_recurso=None):				
		self.resultado = self.prestashop.get(recurso, id_recurso)
			
	def add(self, recurso, id_recurso=None):		
		if id_recurso==None:
			self.resultado = self.prestashop.add(recurso)			
		else:
			self.resultado = self.prestashop.add(recurso, id_recurso)
			
	def delete(self, recurso, id_recurso=None):		
		if id_recurso==None:
			self.resultado = self.prestashop.delete(recurso)			
		else:
			self.resultado = self.prestashop.delete(recurso, id_recurso)
			
	def search(self, recurso, opciones=None):		
		if opciones:
			try:
				opciones = ast.literal_eval(opciones)
			except:
				raise TypeError("Las opciones han de tener la sintaxis de un diccionario Python.")
				
			self.resultado = self.prestashop.search(recurso, options=opciones)			
		else:
			self.resultado = self.prestashop.search(recurso)		
			
	def head(self, recurso, id_recurso=None):		
		if id_recurso==None:
			self.resultado = self.prestashop.head(recurso)			
		else:
			self.resultado = self.prestashop.head(recurso, id_recurso)		
			
	def schema(self, recurso, opciones=None):
		if opciones is not None:
			self.resultado = self.prestashop.get(recurso, options={'schema':'synopsis'})
		else:
			self.resultado = self.prestashop.get(recurso, options={'schema':'blank'})
			
	def version(self):
		r = requests.get(self.url + '/api', auth=(self.clave, ''))	
		self.resultado = r.headers['psws-version']			
	
		
def main(argv):
	url = ''
	clave = ''	
	operacion = ''
	recurso = ''
	id_recurso = ''
	opciones = None
	error = ''
	verbose = False
		
	try:
		opts, args = getopt.getopt(argv, "hvVu:c:o:r:i:O:", ["url=", "clave=", "operacion=", "recurso=", "id_recurso=", "opciones=", "version="])
	except getopt.GetoptError:
		error = getopt.GetoptError;
		print("error opciones")
		

	if error == '':
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print("Uso: prestaeneboo -h -v -u <url> -c <clave> -o <operacion> -r <recurso> -i <id_recurso> -O opciones")		
				print("\r")
				print("\t-h, Ayuda")
				print("\t-v, Modo dicharachero")
				print("\t-u, --url: Dirección de la página principal de la tienda. Ej.: 'http://mitiendaprestashop.com'")
				print("\t-c, --clave: Clave del servicio web")
				print("\t-o, --operacion: Operación a realizar. Valores válidos: 'get', 'add', 'edit', 'delete', 'search'")
				print("\t-r, --recurso: Recurso al que se accede. Ej.: addresses, products, ...")
				print("\t-i, --id_recurso: Parámetros de la operación. Si se omite esta opción, nos devolverá todos los valores del recurso")
				print("\t-O, --opciones: opciones de la operación, tales como 'search', 'display', 'limit', ...")
				print("\t-V, --version: Versión de la API")
				print("\r\r")
				print("Ej.: prestaeneboo -u 'http://mitiendaprestashop.com' -c 'MICLAVEDELWEBSERVICEPRESTASHOP' -r 'addresses' -o 'get' -i '33' -O {'limit':'10'}")
				print("Esto nos devolvería los datos de la dirección con ID = 33")
				sys.exit()
			elif opt in ("-u", "--url"):
				url = arg
			elif opt in ("-c", "--clave"):
				clave = arg
			elif opt in ("-o", "--operacion"):
				operacion = arg
			elif opt in ("-r", "--recurso"):
				recurso = arg
			elif opt in ("-i", "--id_recurso"):
				id_recurso = arg
			elif opt in ("-O", "--opciones"):
				opciones = arg
			elif opt in ("-v", "--verbose"):
				verbose = True
			elif opt in ("-V", "--version"):
				operacion = 'version'			
							
		
		try:		
			tienda = PrestaShop(url, clave, debug=True, session=None, verbose=verbose)
		except PrestaShopWebServiceError as err:
			error = err;
	
	
		if operacion=='get':
			try:
				tienda.get(recurso, id_recurso)			
			except PrestaShopWebServiceError as err:		
				error="Error: " + str(err)
		elif operacion == 'search':
			try:
				tienda.search(recurso, opciones)
			except PrestaShopWebServiceError as err:		
				error="Error: " + str(err)
			except TypeError as err:
				error="Error: " + str(err)
		elif operacion == 'head':
			try:
				tienda.head(recurso, id_recurso)
			except PrestaShopWebServiceError as err:		
				error="Error: " + str(err)
		elif operacion == 'schema':
			try:
				tienda.schema(recurso, opciones)
			except PrestaShopWebServiceError as err:		
				error="Error: " + str(err)
		elif operacion == 'version':
			try:
				tienda.version()
			except:		
				error = "Error accediendo a la API."
							
	if error:		
		sys.stderr.write(str(error))
		resultado = ''
		sys.exit(1)
	else:		
		resultado = tienda.resultado

		
	try:
		xml_str = ET.tostring(resultado, encoding='unicode')
		sys.stdout.write(str(xml_str))		
	except:
		sys.stdout.write(resultado)
			

if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1:])
