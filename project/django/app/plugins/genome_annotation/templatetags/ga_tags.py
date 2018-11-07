from django.template import Library, Node, Variable
#TODO: tentar colocar esse import relativo
from plugins.genome_annotation.models import Annotation, Answer

register = Library()


class AnnotationObject(Node):
    def __init__(self, pluginenrollment_id, contig_id):
        self.contig_id = Variable(contig_id)
        self.pluginenrollment_id = Variable(pluginenrollment_id)
        
    def render(self, context):
        pluginenrollment_id = int(self.pluginenrollment_id.resolve(context))
        contig_id = int(self.contig_id.resolve(context))
        try:
            context['annotation'] = Annotation.objects.get(enrollment__id=pluginenrollment_id, contig__id=contig_id)
        except Annotation.DoesNotExist:
            a = Annotation.objects.none()
            a.status = Annotation.PENDING
            context['annotation'] = a
        
        return ''

@register.tag()
def get_annotation(parser, token):
    """
    {% get_annotation pluginenrollment_id contig_id %}
    """
    bits = token.split_contents()
    return AnnotationObject(bits[1], bits[2])
  

class AnswerObject(Node):
    def __init__(self, pluginenrollment_id, question_id):
        self.question_id = Variable(question_id)
        self.pluginenrollment_id = Variable(pluginenrollment_id)

    def render(self, context):
        pluginenrollment_id = int(self.pluginenrollment_id.resolve(context))
        question_id = int(self.question_id.resolve(context))

        try:
            context['answer'] = Answer.objects.get(plugin_enrollment__id=pluginenrollment_id, question__id=question_id)
        except Answer.DoesNotExist:
            context['answer'] = Answer.objects.none()
        return ''

@register.tag()
def get_answer(parser, token):
    """
    {% get_answer pluginenrollment_id question_id %}
    """
    bits = token.split_contents()
    return AnswerObject(bits[1], bits[2])
    
@register.filter()
def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False