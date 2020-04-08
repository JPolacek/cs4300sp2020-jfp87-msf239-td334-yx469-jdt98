from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Stretches: Find a stretch to help you pain"
net_id = "Jake Polacek:jfp87 Jonathan Tran:jdt98 Matt Frucht:msf239 Teresa Datta:td334 Yifan Xu:yx469"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



