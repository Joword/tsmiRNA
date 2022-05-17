import re
from datetime import datetime
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import g
from peewee import Expression
import sqlite3

try:
    from src.db.TissueSpecificTable import *
    from src.lib.browseAPI import get_parameter, Ajax
    # from src.lib.customScripts import *
except ImportError:
    try:
        from db.TissueSpecificTable import *
        from lib.browseAPI import get_parameter, Ajax
        # from lib.customScripts import *
    except ImportError:
        from TissueSpecificTable import *
        from browseAPI import get_parameter, Ajax
        # from customScripts import *

api = Blueprint('api', __name__)


# 在数据库上添加regexp
def regexp(self, pattern, subject):
    reg = re.compile(pattern, re.I)
    return reg.search(subject) is not None


conn = sqlite_db.connect()
conn.create_function('REGEXP', 2, regexp)
conn.execute('DELETE FROM table REGEXP"\m"')
conn.close()


@api.route('/autocomplete/')
def autocomplete():
    subtype = get_parameter('subtype')
    pattern = get_parameter('q')
    table = None
    searchable = None
    
    if subtype == 'tsmiRNA':
        table = TSmiRNAMessages
        searchable = TSmiRNAMessages.miRNA
    elif subtype == 'panmiRNA':
        table = PanmiRNAMessages
        searchable = PanmiRNAMessages.miRNA
    elif subtype == 'tissue':
        table = TissuemiRNARegulation
        searchable = TissuemiRNARegulation.Tissues
    
    data = []
    querys = table.select(searchable).where(
        searchable.regexp(pattern)).paginate(1, 10).tuples()
    tmp = set(x[0] for x in querys)
    if len(tmp) >= 10:
        data += list(tmp)[0:10]
    else:
        data += list(tmp)
    
    if len(data) == 0:
        data = ['No results']
    return jsonify(matching_results=data)


# TS
@api.route('/TSmiRNAreg/')
def TSmiRNAreg():
    TSmiRNA_name = get_parameter('tsmiRNA')
    columns = [TSmiRNARegulation.miRNA, TSmiRNARegulation.Tissues, TSmiRNARegulation.CancerORNormal,
               TSmiRNARegulation.TrancriptionFactor, TSmiRNARegulation.Gene, TSmiRNARegulation.Types]
    condition = (TSmiRNARegulation.miRNA == TSmiRNA_name)
    
    table = Ajax(TSmiRNARegulation, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/TSmiRNAmessage/')
def TSmiRNAmessage():
    TSmiRNA_name = get_parameter('TSmiRNA')
    columns = [TSmiRNAMessages.miRNA, TSmiRNAMessages.Types, TSmiRNAMessages.CancerORNormal,
               TSmiRNAMessages.GainORLost, TSmiRNAMessages.Expression, TSmiRNAMessages.TSI,
               TSmiRNAMessages.CoefficientOfVariation]
    condition = (TSmiRNAMessages.miRNA == TSmiRNA_name)
    
    table = Ajax(TSmiRNAMessages, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/TStfmessage/')
def TStfmessage():
    TStf_name = get_parameter('TStf')
    columns = [TSmiRNATFBS.TF_name, TSmiRNATFBS.TFBS, TSmiRNATFBS.Types,
               TSmiRNATFBS.Tissues, TSmiRNATFBS.Expression, TSmiRNATFBS.TSI]
    condition = (TSmiRNATFBS.TF_name == TStf_name)
    
    table = Ajax(TSmiRNATFBS, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/TSgenemessage/')
def TSgenemessage():
    TSgene_name = get_parameter('TSgene')
    columns = [TSmiRNAGene.Gene_name, TSmiRNAGene.miR_Family, TSmiRNAGene.Types,
               TSmiRNAGene.Tissues, TSmiRNAGene.Expression, TSmiRNAGene.TSI]
    # ,TSmiRNAGene.DataBase
    condition = (TSmiRNAGene.Gene_name == TSgene_name)
    
    table = Ajax(TSmiRNAGene, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


# Pan
@api.route('/PanmiRNAreg/')
def PanmiRNAreg():
    PanmiRNA_name = get_parameter('panmiRNA')
    columns = [PanmiRNARegulation.miRNA, PanmiRNARegulation.Tissues, PanmiRNARegulation.CancerORNormal,
               PanmiRNARegulation.TrancriptionFactor, PanmiRNARegulation.Gene, PanmiRNARegulation.Types]
    condition = (PanmiRNARegulation.miRNA == PanmiRNA_name)
    
    table = Ajax(PanmiRNARegulation, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/PanmiRNAmessage/')
def PanmiRNAmessage():
    panmiRNA_name = get_parameter('panmiRNA')
    columns = [PanmiRNAMessages.miRNA, PanmiRNAMessages.Types, PanmiRNAMessages.CancerORNormal,
               PanmiRNAMessages.GainORLost, PanmiRNAMessages.Expression, PanmiRNAMessages.TSI,
               PanmiRNAMessages.CoefficientOfVariation]
    condition = (PanmiRNAMessages.miRNA == panmiRNA_name)
    
    table = Ajax(PanmiRNAMessages, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('Pantfmessage/')
def Pantfmessage():
    pantf_name = get_parameter('pantf')
    columns = [PanmiRNATFBS.TF_name, PanmiRNATFBS.TFBS, PanmiRNATFBS.Types,
               PanmiRNATFBS.Tissues, PanmiRNATFBS.Expression, PanmiRNATFBS.TSI]
    condition = (PanmiRNATFBS.TF_name == pantf_name)
    
    table = Ajax(PanmiRNATFBS, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/Pangenemessage/')
def Pangenemessage():
    pangene_name = get_parameter('pangene')
    columns = [PanmiRNAGene.Gene_name, PanmiRNAGene.miR_Family, PanmiRNAGene.Types,
               PanmiRNAGene.Tissues, PanmiRNAGene.Expression, PanmiRNAGene.TSI]
    # ,PanmiRNAGene.DataBase
    condition = (PanmiRNAGene.Gene_name == pangene_name)
    
    table = Ajax(PanmiRNAGene, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


# Tissue
@api.route('/tissuemiRNAreg/')
def tissuemiRNAreg():
    TissuemiRNA_name = get_parameter('tissue')
    columns = [TissuemiRNARegulation.miRNA, TissuemiRNARegulation.Tissues, TissuemiRNARegulation.CancerORNormal,
               TissuemiRNARegulation.TrancriptionFactor, TissuemiRNARegulation.Gene, TissuemiRNARegulation.Types]
    condition = (TissuemiRNARegulation.Tissues == TissuemiRNA_name)
    
    table = Ajax(TissuemiRNARegulation, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/tissuemiRNAmessage/')
def tissuemiRNAmessage():
    tissuemiRNA_name = get_parameter('tissuemiRNA')
    columns = [TissuemiRNAMessages.miRNA, TissuemiRNAMessages.Types, TissuemiRNAMessages.CancerORNormal,
               TissuemiRNAMessages.GainORLost, TissuemiRNAMessages.Expression, TissuemiRNAMessages.TSI,
               TissuemiRNAMessages.CoefficientOfVariation]
    condition = (TissuemiRNAMessages.miRNA == tissuemiRNA_name)
    
    table = Ajax(TissuemiRNAMessages, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('tissuetfmessage/')
def tissuetfmessage():
    tissuetf_name = get_parameter('tissuetf')
    columns = [TissuemiRNATFBS.TF_name, TissuemiRNATFBS.TFBS, TissuemiRNATFBS.Types,
               TissuemiRNATFBS.Tissues, TissuemiRNATFBS.Expression, TissuemiRNATFBS.TSI]
    condition = (TissuemiRNATFBS.TF_name == tissuetf_name)
    
    table = Ajax(TissuemiRNATFBS, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)


@api.route('/tissuegenemessage/')
def tissuegenemessage():
    tissuegene_name = get_parameter('tissuegene')
    columns = [TissuemiRNAGene.Gene_name, TissuemiRNAGene.miR_Family, TissuemiRNAGene.Types,
               TissuemiRNAGene.Tissues, TissuemiRNAGene.Expression, TissuemiRNAGene.TSI]
    condition = (TissuemiRNAGene.Gene_name == tissuegene_name)
    # ,TissuemiRNAGene.DataBase
    table = Ajax(TissuemiRNAGene, columns)
    tmpResult = table.query_(condition=condition)
    return jsonify(tmpResult)
