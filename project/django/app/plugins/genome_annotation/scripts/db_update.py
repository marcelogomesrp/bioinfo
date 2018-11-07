# coding: utf-8
import sys, os
from os import path as os_path
from os.path import abspath, dirname
#sys.path.insert(0, dirname(dirname(abspath(__file__))))
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.db.utils import IntegrityError
from plugins.genome_annotation.models import Tissue, TissueKind, Contig

DATA_FOLDER = os_path.join(os_path.abspath(os_path.split(__file__)[0]), 'hcgp_est') + '/%s'

TISSUE_DICT = {'B': u'Mama',
               'C': u'Cólon',
               'E': u'Pulmão',
               'F': u'Próstata',
               'H': u'Cabeça e pescoço',
               'N': u'Sistema nervoso',
               'S': u'Estômago',
               'T': u'Testículo'}

FILE_NAME_TEMPLATE = '%s.insert.cap.contigs.info'

def load_data():    
    def process_line(tissue, line):
        line = line.split()
        sequence = line[2]

        Contig.objects.create(tissue=tissue, name=line[0], base_qty=len(sequence), est_qty=int(line[1]), sequence=sequence)
        
    for tissue_code, t_file, n_file in [(l, 
                            open(DATA_FOLDER % FILE_NAME_TEMPLATE % (l + 'T')), 
                            open(DATA_FOLDER % FILE_NAME_TEMPLATE % (l + 'N'))) for l in TISSUE_DICT.keys()]:
        
        tissue_n, _ = Tissue.objects.get_or_create(symbol=tissue_code + 'N', type='n', name=TISSUE_DICT[tissue_code], kind=TissueKind.objects.get(code=tissue_code))
        tissue_t, _ = Tissue.objects.get_or_create(symbol=tissue_code + 'T', type='t', name=TISSUE_DICT[tissue_code], kind=TissueKind.objects.get(code=tissue_code))
        
        for line in n_file:
            process_line(tissue_n, line)
        
        for line in t_file:
            process_line(tissue_t, line)
        

def update_info():
    last_tissue_symbol = ''
    for line in open(DATA_FOLDER % 'all_tissues.contigs.info'):
        tissue_symbol, contig_qty, est_qty, contig_est_qty, singlet_qty, contig_id, base_qty, frequency = line.split('\t')
        if tissue_symbol <> last_tissue_symbol:
            try:
                t = Tissue.objects.get(symbol=tissue_symbol)
            except Tissue.DoesNotExist:
                continue
                
            t.est_qty = est_qty
            t.singlet_qty = singlet_qty
            t.contig_qty = contig_qty
            t.save()
            last_tissue_symbol = tissue_symbol
            print 'Tissue %s OK' % tissue_symbol
            
        try:
            c = Contig.objects.get(name=contig_id)
            c.frequency = frequency
            c.save()
        except Contig.DoesNotExist:
            print contig_id
            pass

if __name__ == '__main__':
    for k,v in TISSUE_DICT.items():
        try:
            TissueKind.objects.create(code=k, name=v)
        except:
            pass
        
    load_data()
    update_info()