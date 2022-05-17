from peewee import *
import os
import re
import json

__dir__ = os.path.dirname(os.path.abspath(__file__))
sqlite_db = SqliteDatabase(os.path.join(__dir__, 'TissueSpecific.db'))


class BaseDB(Model):
    class Meta:
        database = sqlite_db


class ExpValueInTissue(BaseDB):
    Blood = FloatField()
    Bladder = FloatField()
    Brain = FloatField()
    Breast = FloatField()
    Cervix = FloatField()
    Colorectal = FloatField()
    Kidney = FloatField()
    Liver = FloatField()
    Lung = FloatField()
    Pancreas = FloatField()
    Prostate = FloatField()
    Skin = FloatField()
    Uterus = FloatField()


# Pan miRNA
class PanmiRNAGene(BaseDB):
    Gene_name = TextField()
    Expression = FloatField()
    Tissues = TextField()
    Types = TextField()
    miR_Family = TextField()
    TSI = FloatField()
    DataBase = FloatField()
    
    class Meta:
        db_table = 'PanmiRNAGene'
        order_by = ('Gene_name',)


class PanmiRNALocation(BaseDB):
    premiRNA = TextField()
    miRNA = TextField()
    Types = TextField()
    TFBS = TextField()
    
    class Meta:
        db_table = 'PanmiRNALocation'
        order_by = ('premiRNA',)


class PanmiRNAMessages(BaseDB):
    miRNA = TextField()
    Types = TextField()
    CancerORNormal = TextField()
    GainORLost = TextField()
    Expression = FloatField()
    TSI = FloatField()
    CoefficientOfVariation = FloatField()
    
    class Meta:
        db_table = 'PanmiRNAMessages'
        order_by = ('miRNA',)


class PanmiRNARegulation(BaseDB):
    miRNA = TextField()
    TrancriptionFactor = TextField()
    Gene = TextField()
    Types = TextField()
    Tissues = TextField()
    CancerORNormal = TextField()
    
    class Meta:
        db_table = 'PanmiRNARegulation'
        order_by = ('miRNA',)


class PanmiRNATFBS(BaseDB):
    TF_name = TextField()
    Expression = FloatField()
    Tissues = TextField()
    Types = TextField()
    TFBS = TextField()
    TSI = FloatField()
    
    class Meta:
        db_table = 'PanmiRNATFBS'
        order_by = ('TF_name',)


# TS miRNA
class TSmiRNAGene(BaseDB):
    Gene_name = TextField()
    Expression = FloatField()
    Tissues = TextField()
    Types = TextField()
    miR_Family = TextField()
    TSI = FloatField()
    DataBase = FloatField()
    
    class Meta:
        db_table = 'TSmiRNAGene'
        order_by = ('Gene_name',)


class TSmiRNALocation(BaseDB):
    premiRNA = TextField()
    miRNA = TextField()
    Types = TextField()
    TFBS = TextField()
    
    class Meta:
        db_table = 'TSmiRNALocation'
        order_by = ('premiRNA',)


class TSmiRNAMessages(BaseDB):
    miRNA = TextField()
    Types = TextField()
    CancerORNormal = TextField()
    GainORLost = TextField()
    Expression = FloatField()
    TSI = FloatField()
    CoefficientOfVariation = FloatField()
    
    class Meta:
        db_table = 'TSmiRNAMessages'
        order_by = ('miRNA',)


class TSmiRNARegulation(BaseDB):
    miRNA = TextField()
    TrancriptionFactor = TextField()
    Gene = TextField()
    Types = TextField()
    Tissues = TextField()
    CancerORNormal = TextField()
    
    class Meta:
        db_table = 'TSmiRNARegulation'
        order_by = ('miRNA',)


class TSmiRNATFBS(BaseDB):
    TF_name = TextField()
    Expression = FloatField()
    Tissues = TextField()
    Types = TextField()
    TFBS = TextField()
    TSI = FloatField()
    
    class Meta:
        db_table = 'TSmiRNATFBS'
        order_by = ('TF_name',)


# Tissue miRNA
class TissuemiRNAGene(BaseDB):
    Gene_name = TextField()
    Expression = FloatField()
    Tissues = TextField()
    Types = TextField()
    miR_Family = TextField()
    TSI = FloatField()
    DataBase = FloatField()
    
    class Meta:
        db_table = 'TissuemiRNAGene'
        order_by = ('Gene_name',)


class TissuemiRNALocation(BaseDB):
    premiRNA = TextField()
    miRNA = TextField()
    Types = TextField()
    TFBS = TextField()
    
    class Meta:
        db_table = 'TissuemiRNALocation'
        order_by = ('premiRNA',)


class TissuemiRNAMessages(BaseDB):
    miRNA = TextField()
    Types = TextField()
    CancerORNormal = TextField()
    GainORLost = TextField()
    Expression = FloatField()
    TSI = FloatField()
    CoefficientOfVariation = FloatField()
    
    class Meta:
        db_table = 'TissuemiRNAMessages'
        order_by = ('miRNA',)


class TissuemiRNARegulation(BaseDB):
    miRNA = TextField()
    TrancriptionFactor = TextField()
    Gene = TextField()
    Types = TextField()
    Tissues = TextField()
    CancerORNormal = TextField()
    
    class Meta:
        db_table = 'TissuemiRNARegulation'
        order_by = ('miRNA',)


class TissuemiRNATFBS(BaseDB):
    TF_name = TextField()
    Expression = FloatField()
    Tissues = TextField()
    Types = TextField()
    TFBS = TextField()
    TSI = FloatField()
    
    class Meta:
        db_table = 'TissuemiRNATFBS'
        order_by = ('TF_name',)


# Expression Value
# Tissue tf expression
class Tissuetf_cancer_exp(ExpValueInTissue):
    TF_name = TextField()
    
    class Meta:
        db_table = 'Tissue_TFCancerExp'
        order_by = ('TF_name',)


class Tissuetf_normal_exp(ExpValueInTissue):
    TF_name = TextField()
    
    class Meta:
        db_table = 'Tissue_TFNormalExp'
        order_by = ('TF_name',)


# Tissue gene expression
class Tissuegene_cancer_exp(ExpValueInTissue):
    Gene_name = TextField()
    
    class Meta:
        db_table = 'Tissue_GeneCancerExp'
        order_by = ('Gene_name',)


class Tissuegene_normal_exp(ExpValueInTissue):
    Gene_name = TextField()
    
    class Meta:
        db_table = 'Tissue_GeneNormalExp'
        order_by = ('Gene_name',)


# Tissue miRNA expression
class TissuemiRNA_cancer_exp(ExpValueInTissue):
    miRNA_name = TextField()
    
    class Meta:
        db_table = 'Tissue_miRNACancerExp'
        order_by = ('miRNA_name',)


class TissuemiRNA_normal_exp(ExpValueInTissue):
    miRNA_name = TextField()
    
    class Meta:
        db_table = 'Tissue_miRNANormalExp'
        order_by = ('miRNA_name',)


# TS
# TS tf expression
class TStf_cancer_exp(ExpValueInTissue):
    TF_name = TextField()
    
    class Meta:
        db_table = 'TS_TFCancerExp'
        order_by = ('TF_name',)


class TStf_normal_exp(ExpValueInTissue):
    TF_name = TextField()
    
    class Meta:
        db_table = 'TS_TFNormalExp'
        order_by = ('TF_name',)


# TS  gene expression
class TSgene_cancer_exp(ExpValueInTissue):
    Gene_name = TextField()
    
    class Meta:
        db_table = 'TS_GeneCancerExp'
        order_by = ('Gene_name',)


class TSgene_normal_exp(ExpValueInTissue):
    Gene_name = TextField()
    
    class Meta:
        db_table = 'TS_GeneNormalExp'
        order_by = ('Gene_name',)


# TS  miRNA expression
class TSmiRNA_cancer_exp(ExpValueInTissue):
    miRNA_name = TextField()
    
    class Meta:
        db_table = 'TS_miRNACancerExp'
        order_by = ('miRNA_name',)


class TSmiRNA_normal_exp(ExpValueInTissue):
    miRNA_name = TextField()
    
    class Meta:
        db_table = 'TS_miRNANormalExp'
        order_by = ('miRNA_name',)


# pan
# Pan tf expression
class Pantf_cancer_exp(ExpValueInTissue):
    TF_name = TextField()
    
    class Meta:
        db_table = 'Pan_TFCancerExp'
        order_by = ('TF_name',)


class Pantf_normal_exp(ExpValueInTissue):
    TF_name = TextField()
    
    class Meta:
        db_table = 'Pan_TFNormalExp'
        order_by = ('TF_name',)


# Pan  gene expression
class Pangene_cancer_exp(ExpValueInTissue):
    Gene_name = TextField()
    
    class Meta:
        db_table = 'Pan_GeneCancerExp'
        order_by = ('Gene_name',)


class Pangene_normal_exp(ExpValueInTissue):
    Gene_name = TextField()
    
    class Meta:
        db_table = 'Pan_GeneNormalExp'
        order_by = ('Gene_name',)


# Pan  miRNA expression
class PanmiRNA_cancer_exp(ExpValueInTissue):
    miRNA_name = TextField()
    
    class Meta:
        db_table = 'Pan_miRNACancerExp'
        order_by = ('miRNA_name',)


class PanmiRNA_normal_exp(ExpValueInTissue):
    miRNA_name = TextField()
    
    class Meta:
        db_table = 'Pan_miRNANormalExp'
        order_by = ('miRNA_name',)
