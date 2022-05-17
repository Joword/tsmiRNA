import os
import re
from math import log10
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import url_for
from flask import jsonify
from flask import request
# from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect
from src.api import api
from src.lib.browseAPI import Ajax, get_parameter
from src.db.TissueSpecificTable import *

# from src.lib.browseAPI import query_


__dir__ = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=os.path.join(__dir__, 'static'))
print(app)
# app.debug = True

app.config['SECRET_KEY'] = 'lcbb.swjtu.edu.cn'

csrf = CSRFProtect(app)
csrf.init_app(app)

app.register_blueprint(api, url_prefix='/api')


class PrefixMiddleware(object):
	u"""
	thanks to @su27 at: https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes
	"""
	
	def __init__(self, app, prefix=''):
		self.app = app
		self.prefix = prefix
	
	def __call__(self, environ, start_response):
		
		if environ['PATH_INFO'].startswith(self.prefix):
			environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
			print
			environ['SCRIPT_NAME'] = self.prefix
			return self.app(environ, start_response)
		else:
			start_response('404', [('Content-Type', 'text/plain')])
			return ["This url does not belong to the app.".encode()]


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/TSmiRNA')


# 静态css,js文件的的存放位置
@app.route('/static/<path:filename>')
def sTaTic(filename):
	staticDirectory = os.path.join(__dir__, 'static')
	return send_from_directory(directory=staticDirectory, filename=filename)


@app.route('/SearchStatic/<path:filename>')
def Seastatic(filename):
	SearchstaticDirectory = os.path.join(__dir__, 'SearchStatic')
	return send_from_directory(directory=SearchstaticDirectory, filename=filename)


@app.route('/')
def index():
	return render_template('home.html', page='homepage')  # render_template()加载home.html模板，并把homepage参数传给模板


@app.route('/help/')
def helppage():
	return render_template('help.html', page='help')


@app.route('/download/')
def download():
	download_dir = 'static/files'
	files = []
	for x in sorted(os.listdir(os.path.join(__dir__, download_dir))):
		files.append(
			{
				'name': re.sub('_', ' ', x),
				'path': os.path.join('files', x)
			}
		)
	
	return render_template('download.html', page='download', files=files)


@app.route('/contact/')
def contact():
	return render_template('contact.html', page='contact')


@app.route('/reference/')
def reference():
	return render_template('reference.html', page='reference')


# TSmiRNA regulation  table
@app.route('/TSmiRNAreg/')
def TSmiRNAreg():
	miRNA_Name = get_parameter('tsmiRNA')
	ts_miRNA = miRNA_Name
	if not ts_miRNA or TSmiRNARegulation.select().where(TSmiRNARegulation.miRNA == ts_miRNA).count() == 0:
		return render_template("error.html", error="TS miRNA not available in tissue specific Dabase.")
	
	headers = ['miRNA name', 'TF', 'Gene', 'Types', 'Tissue', 'Cancer/Normal']
	return render_template('TSmiRNAreg.html', page='', tsmiRNA_name=ts_miRNA, header=headers)


@app.route('/PanmiRNAreg/')
def PanmiRNAreg():
	miRNA_Name = get_parameter('panmiRNA')
	pan_miRNA = miRNA_Name
	if not pan_miRNA or PanmiRNARegulation.select().where(PanmiRNARegulation.miRNA == pan_miRNA).count() == 0:
		return render_template("error.html", error="Pan miRNA not available in tissue specific Dabase.")
	
	headers = ['miRNA name', 'TF', 'Gene', 'Types', 'Tissue', 'Cancer/Normal']
	return render_template('PanmiRNAreg.html', page='', panmiRNA_name=pan_miRNA, header=headers)


@app.route('/TissuemiRNAreg/')
def TissuemiRNAreg():
	miRNA_Name = get_parameter('tissue')
	tissue_miRNA = miRNA_Name
	if not tissue_miRNA or TissuemiRNARegulation.select().where(
			TissuemiRNARegulation.Tissues == tissue_miRNA).count() == 0:
		return render_template("error.html", error="Tissue miRNA not available in tissue specific Dabase.")
	
	headers = ['Tissues', 'miRNA', 'TrancriptionFactor', 'Gene', 'Types', 'Cancer/Normal']
	return render_template('tissuemiRNAreg.html', page='', tissuemiRNA_name=tissue_miRNA, header=headers)


# TSmiRNA messages  table
@app.route('/TSmiRNAmessage/')
def TSmiRNAmessage():
	ts = get_parameter('TSmiRNA')
	ts_miRNA = ts
	if not ts_miRNA or TSmiRNAMessages.select().where(TSmiRNAMessages.miRNA == ts_miRNA).count() == 0:
		return render_template("error.html", error=" TS miRNA not available in tissue specific Dabase.")
	
	headers = ['miRNA name', 'Types', 'Cancer/Normal', 'Gain/Lost', 'Expression', 'TSI', 'CoefficientOfVariation']
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = TSmiRNA_normal_exp.select().where(TSmiRNA_normal_exp.miRNA_name == ts_miRNA).dicts()
	Cancertf_Query = TSmiRNA_cancer_exp.select().where(TSmiRNA_cancer_exp.miRNA_name == ts_miRNA).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('TSmiRNAmessage.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   tsmiRNA_name=ts_miRNA, header=headers)


# PanmiRNA messages  table
@app.route('/PanmiRNAmessage/')
def PanmiRNAmessage():
	pan = get_parameter('panmiRNA')
	pan_miRNA = pan
	if not pan_miRNA or PanmiRNAMessages.select().where(PanmiRNAMessages.miRNA == pan_miRNA).count() == 0:
		return render_template("error.html", error="Pan miRNA not available in tissue specific Dabase.")
	
	headers = ['miRNA name', 'Types', 'Cancer/Normal', 'Gain/Lost', 'Expression', 'TSI', 'CoefficientOfVariation']
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = PanmiRNA_normal_exp.select().where(PanmiRNA_normal_exp.miRNA_name == pan_miRNA).dicts()
	Cancertf_Query = PanmiRNA_cancer_exp.select().where(PanmiRNA_cancer_exp.miRNA_name == pan_miRNA).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('PanmiRNAmessage.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   panmiRNA_name=pan_miRNA, header=headers)


# TissuemiRNA messages  table
@app.route('/tissuemiRNAmessage/')
def tissuemiRNAmessage():
	tissue = get_parameter('tissuemiRNA')
	tissue_miRNA = tissue
	if not tissue_miRNA or TissuemiRNAMessages.select().where(TissuemiRNAMessages.miRNA == tissue_miRNA).count() == 0:
		return render_template("error.html", error="tissue miRNA not available in tissue specific Dabase.")
	
	headers = ['miRNA name', 'Types', 'Cancer/Normal', 'Gain/Lost', 'Expression', 'TSI', 'CoefficientOfVariation']
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = TissuemiRNA_normal_exp.select().where(TissuemiRNA_normal_exp.miRNA_name == tissue_miRNA).dicts()
	Cancertf_Query = TissuemiRNA_cancer_exp.select().where(TissuemiRNA_cancer_exp.miRNA_name == tissue_miRNA).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('TissuemiRNAmessage.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   tissuemiRNA_name=tissue_miRNA, header=headers)


# TSmiRNA tf  table
@app.route('/TStfmessage/')
def TStfmessage():
	tf = get_parameter('TStf')
	ts_tf = tf
	if not ts_tf or TSmiRNATFBS.select().where(TSmiRNATFBS.TF_name == ts_tf).count() == 0:
		return render_template("error.html",
							   error="TS miRNA TrancriptionFactor not available in tissue specific Dabase.")
	headers = ['TF name', 'TFBS', 'Types', 'Tissue', 'Expression', 'TSI']
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = TStf_normal_exp.select().where(TStf_normal_exp.TF_name == ts_tf).dicts()
	Cancertf_Query = TStf_cancer_exp.select().where(TStf_cancer_exp.TF_name == ts_tf).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('TSmiRNAtf.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal, tsmiRNAtf_name=ts_tf,
						   header=headers)


# pan miRNA tf  table
@app.route('/Pantfmessage/')
def Pantfmessage():
	tf = get_parameter('pantf')
	pan_tf = tf
	if not pan_tf or PanmiRNATFBS.select().where(PanmiRNATFBS.TF_name == pan_tf).count() == 0:
		return render_template("error.html",
							   error="Pan miRNA TrancriptionFactor not available in tissue specific Dabase.")
	
	headers = ['TF name', 'TFBS', 'Types', 'Tissue', 'Expression', 'TSI']
	
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = Pantf_normal_exp.select().where(Pantf_normal_exp.TF_name == pan_tf).dicts()
	Cancertf_Query = Pantf_cancer_exp.select().where(Pantf_cancer_exp.TF_name == pan_tf).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('PanmiRNAtf.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal, panmiRNAtf_name=pan_tf,
						   header=headers)


# tissue miRNA tf  table
@app.route('/tissuetfmessage/')
def tissuetfmessage():
	tissue = get_parameter('tissuetf')
	tissue_tf = tissue
	if not tissue_tf or TissuemiRNATFBS.select().where(TissuemiRNATFBS.TF_name == tissue_tf).count() == 0:
		return render_template("error.html",
							   error="Tissue miRNA TrancriptionFactor not available in tissue specific Dabase.")
	
	headers = ['TF name', 'TFBS', 'Types', 'Tissue', 'Expression', 'TSI']
	
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = Tissuetf_normal_exp.select().where(Tissuetf_normal_exp.TF_name == tissue_tf).dicts()
	Cancertf_Query = Tissuetf_cancer_exp.select().where(Tissuetf_cancer_exp.TF_name == tissue_tf).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('TissuemiRNAtf.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   tissuemiRNAtf_name=tissue_tf, header=headers)


# TSmiRNA gene  table
@app.route('/TSgenemessage/')
def TSgenemessage():
	gene = get_parameter('TSgene')
	ts_gene = gene
	if not gene or TSmiRNAGene.select().where(TSmiRNAGene.Gene_name == ts_gene).count() == 0:
		return render_template("error.html", error="TS Gene not available in tissue specific Dabase.")
	
	headers = ['Gene name', 'Types', 'Tissue', 'Expression', 'TSI', 'miRNA Family']
	
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = TSgene_normal_exp.select().where(TSgene_normal_exp.Gene_name == ts_gene).dicts()
	Cancertf_Query = TSgene_cancer_exp.select().where(TSgene_cancer_exp.Gene_name == ts_gene).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('TSmiRNAgene.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   tsmiRNAgene_name=ts_gene, header=headers)


# Pan miRNA gene  table
@app.route('/Pangenemessage/')
def Pangenemessage():
	gene = get_parameter('pangene')
	pan_gene = gene
	if not gene or PanmiRNAGene.select().where(PanmiRNAGene.Gene_name == pan_gene).count() == 0:
		return render_template("error.html", error="Pan Gene not available in tissue specific Dabase.")
	
	headers = ['Gene name', 'Types', 'Tissue', 'Expression', 'TSI', 'miRNA Family']  # ',DataBase'
	
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = Pangene_normal_exp.select().where(Pangene_normal_exp.Gene_name == pan_gene).dicts()
	Cancertf_Query = Pangene_cancer_exp.select().where(Pangene_cancer_exp.Gene_name == pan_gene).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('PanmiRNAgene.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   panmiRNAgene_name=pan_gene, header=headers)


# Tissue miRNA gene  table
@app.route('/tissuegenemessage/')
def tissuegenemessage():
	gene = get_parameter('tissuegene')
	tissue_gene = gene
	if not gene or TissuemiRNAGene.select().where(TissuemiRNAGene.Gene_name == tissue_gene).count() == 0:
		return render_template("error.html", error="Tissue Gene not available in tissue specific Dabase.")
	
	headers = ['Gene name', 'Types', 'Tissue', 'Expression', 'TSI', 'miRNA Family']
	
	tf_normal = {
		'xAxis': [],
		'yAxis': []
	}
	tf_cancer = {
		'xAxis': [],
		'yAxis': []
	}
	
	TissueList = ['Prostate', 'Brain', 'Breast', 'Kidney', 'Colorectal', 'Skin',
				  'Liver', 'Lung', 'Blood', 'Pancreas', 'Uterus', 'Cervix', 'Bladder']
	
	Normaltf_Query = Tissuegene_normal_exp.select().where(Tissuegene_normal_exp.Gene_name == tissue_gene).dicts()
	Cancertf_Query = Tissuegene_cancer_exp.select().where(Tissuegene_cancer_exp.Gene_name == tissue_gene).dicts()
	
	for rel in [[Normaltf_Query, tf_normal, 'tf_normal'], [Cancertf_Query, tf_cancer, 'tf_cancer']]:
		query = rel[0]
		dic = rel[1]
		for j in query:
			for i in TissueList:
				if float(j[i]) <= 0.0 and rel[2] == 'tf_cancer':
					continue
				else:
					dic['xAxis'].append(i)
					dic['yAxis'].append(float(j[i]))
	return render_template('TissuemiRNAgene.html', page='', tf_cancer=tf_cancer, tf_normal=tf_normal,
						   tissuemiRNAgene_name=tissue_gene, header=headers)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, threaded=True)
	pass
