# coding: utf-8
from unipath import Path
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from plugins.genome_annotation.models import Tissue, TissueKind, Contig

TISSUE_DICT = {'B': u'Mama',
               'C': u'Cólon',
               'E': u'Pulmão',
               'F': u'Próstata',
               'H': u'Cabeça e pescoço',
               'N': u'Sistema nervoso',
               'S': u'Estômago',
               'T': u'Testículo'}

FILE_NAME_TEMPLATE = '%s.insert.cap.contigs.info'


class Command(BaseCommand):
    help = "Inclui as ESTs e clusters no banco"

    def handle(self, *args, **options):
        self.data_folder = Path(args[0])
        self.create_tissue_kinds()
        self.load_data()
        self.update_all_tissue_data()
    
    def create_tissue_kinds(self):
        for k,v in TISSUE_DICT.items():
            try:
                TissueKind.objects.create(code=k, name=v)
            except:
                pass
        
    
    def _process_contig_file_line(self, tissue, line):
        line = line.split()
        sequence = line[2]

        Contig.objects.create(tissue=tissue, name=line[0], base_qty=len(sequence), est_qty=int(line[1]), sequence=sequence)
    
    def load_data(self):
        for tissue_code, t_file, n_file in [(l, 
                                open(self.data_folder.child(FILE_NAME_TEMPLATE % (l + 'T'))), 
                                open(self.data_folder.child(FILE_NAME_TEMPLATE % (l + 'N')))) for l in TISSUE_DICT.keys()]:
            print 'Processing %s...' % TISSUE_DICT[tissue_code]
            tissue_n, _ = Tissue.objects.get_or_create(symbol=tissue_code + 'N', type='n', name=TISSUE_DICT[tissue_code], kind=TissueKind.objects.get(code=tissue_code))
            tissue_t, _ = Tissue.objects.get_or_create(symbol=tissue_code + 'T', type='t', name=TISSUE_DICT[tissue_code], kind=TissueKind.objects.get(code=tissue_code))

            for line in n_file:
                self._process_contig_file_line(tissue_n, line)

            for line in t_file:
                self._process_contig_file_line(tissue_t, line)

    def update_all_tissue_data(self):
       last_tissue_symbol = ''
       for line in open(self.data_folder.child('all_tissue_contig.info')):
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

