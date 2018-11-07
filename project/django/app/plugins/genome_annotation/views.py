# coding: utf-8
from os import path as os_path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from enrollments.decorators import class_enrollment_required
from plugins.decorators import plugin_enrollment_required
from plugins.util import get_class_enrollment
from forms import AddQuestionForm, AnnotationForm, PluginEnrollmentForm, AddUserFile, SubmissionTitleForm
from models import Annotation, Answer, Contig, PluginEnrollment, Tissue, TissueKind, Project, Submission, Institution

#class_enrollment = get_class_enrollment(request.user, classenrollment_id)

@login_required
@class_enrollment_required
def plugin_enrollment(request, classenrollment_id):
    ''' Associa a matrícula do usuário ao plugin de anotação genômica, 
        setando projeto e tecido '''
    
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    # 
    # if class_enrollment.pluginenrollment_set.count():
    #     return redirect('enrollment_dashboard', classenrollment_id=class_enrollment.id)
    #     
    if request.method == 'POST':
        form = PluginEnrollmentForm(class_enrollment.course_class, request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.enrollment = class_enrollment
            obj.save()

            messages.info(request, _('Enrollment completed'))
            return redirect('enrollment_dashboard', classenrollment_id=class_enrollment.id)
    else:
        form = PluginEnrollmentForm(class_enrollment.course_class)
        
    return render_to_response('genome_annotation/enrollment.html', {
                                'class_enrollment': class_enrollment,
                                'form': form,
                                },
                                context_instance=RequestContext(request))
    
    #o = PluginEnrollment.objects.create(enrollment=class_enrollment, project=Project.objects.order_by('?')[0], tissue=TissueKind.objects.order_by('?')[0])
    #return redirect('enrollment_dashboard', classenrollment_id=class_enrollment.id)


@login_required
@class_enrollment_required
@plugin_enrollment_required
def contig_validation(request, classenrollment_id):
    ''' Redireciona o usuário para validar uma contig (randômica) '''
    #TODO: melhorar isso
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    
    plugin_enrollment = class_enrollment.pluginenrollment_set.all()[0]
    
    return redirect('genome_annotation_validate_contig', classenrollment_id=class_enrollment.id, pluginenrollment_id=plugin_enrollment.id, tissue_symbol=plugin_enrollment.tissue.tissue_set.all()[0].symbol)


@login_required
@class_enrollment_required
@plugin_enrollment_required
def questions(request, classenrollment_id):
    ''' Lista as questões de acordo com o projeto selecionado '''
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = class_enrollment.pluginenrollment_set.all()[0]
    question_list = plugin_enrollment.project.question_set.all()
    
    if request.method == 'POST':
        question = question_list.get(pk=request.POST.get('question_id'))
        answer, __ = Answer.objects.get_or_create(plugin_enrollment=plugin_enrollment, question=question)
        answer.text = request.POST.get('answer_%s' % question.id)
        answer.save()
        
        if request.FILES.get('file'):
            f = AddUserFile(request.POST, request.FILES)
            if f.is_valid():
                obj = f.save(commit=False)
                obj.answer = answer
                obj.save()
            else:
                messages.warning(request, _('File type not allowed'))
                return redirect('genome_annotation_questions', classenrollment_id=classenrollment_id)
        messages.info(request, _('Answer saved'))
        
        return redirect('genome_annotation_questions', classenrollment_id=classenrollment_id)
    
    return render_to_response('genome_annotation/questions.html', {
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                'question_list': question_list,
                                },
                                context_instance=RequestContext(request))


@login_required
def manage_projects(request, class_id):
    ''' Permite ao instrutor gerenciar os projetos do curso '''
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    projects = Project.objects.all()
    
    return render_to_response('genome_annotation/manage_projects.html', {
                                'class': course_class,
                                'projects': projects,
                                },
                                context_instance=RequestContext(request))


@login_required
def manage_questions(request, class_id, project_id):
    ''' Permite ao instrutor gerenciar as perguntas do curso '''
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    project = Project.objects.get(id=project_id)

    return render_to_response('genome_annotation/manage_questions.html', {
                                'class': course_class,
                                'project': project,
                                },
                                context_instance=RequestContext(request))

@login_required
def add_question(request, class_id, project_id):
    ''' Permite ao instrutor adicionar uma nova pergunta, relacionada a um projeto '''
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.project = project
            obj.save()
            
            messages.info(request, _('Question added'))
            
            return redirect('genome_annotation_manage_questions', 
                            class_id=class_id, project_id=project.id)
    else:
        form = AddQuestionForm()

    return render_to_response('genome_annotation/add_question.html', {
                                'class': course_class,
                                'project': project,
                                'form': form,
                                },
                                context_instance=RequestContext(request))

@login_required
def modify_question(request, class_id, project_id, question_id):
    ''' Permite ao instrutor adicionar uma nova pergunta, relacionada a um projeto '''
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    project = Project.objects.get(pk=project_id)
    question = project.question_set.get(pk=question_id)

    if request.method == 'POST':
        form = AddQuestionForm(request.POST, instance=question)

        if form.is_valid():
            form.save()
            
            messages.info(request, _('Question modified'))

            return redirect('genome_annotation_manage_questions', 
                            class_id=class_id, project_id=project.id)
    else:
        form = AddQuestionForm(instance=question)

    return render_to_response('genome_annotation/add_question.html', {
                                'class': course_class,
                                'project': project,
                                'form': form,
                                },
                                context_instance=RequestContext(request))
                                
@login_required
def annotation_stats(request, class_id):
    ''' Permite ao instrutor visualizar o progresso da anotação de 
        cada aluno
    '''
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    plugin_enrollments = PluginEnrollment.objects.select_related('project', 'enrollment').order_by('enrollment__user__first_name')
    
    return render_to_response('genome_annotation/annotation_stats.html', {
                                'class': course_class,
                                'plugin_enrollments': plugin_enrollments,
                                },
                                context_instance=RequestContext(request))


@login_required
def remove_question(request, class_id, project_id, question_id):
    ''' Permite ao instrutor adicionar uma nova pergunta, relacionada a um projeto '''
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    project = Project.objects.get(pk=project_id)
    project.question_set.get(pk=question_id).delete()

    messages.info(request, _('Question removed'))

    return redirect('genome_annotation_manage_questions', 
                            class_id=class_id, project_id=project.id)
                            

@login_required
@class_enrollment_required
@plugin_enrollment_required
def video_tutorials(request, classenrollment_id):
    ''' Redireciona o usuário para validar uma contig (randômica) '''
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = class_enrollment.pluginenrollment_set.all()[0]

    return render_to_response('genome_annotation/video_tutorials.html', {
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                },
                                context_instance=RequestContext(request))    
    
@login_required
@class_enrollment_required
@plugin_enrollment_required
def validate_contig(request, classenrollment_id, pluginenrollment_id, tissue_symbol, contig_id=None, contig_list_filter=None):    
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)
    current_tissue = Tissue.objects.get(symbol=tissue_symbol)
    
    if contig_id:
        contig = get_object_or_404(Contig.objects.filter(tissue=current_tissue), pk=contig_id)
    else:
        contig = Contig.objects.filter(tissue=current_tissue).order_by('-est_qty')[0]
        
    annotation, __ = Annotation.objects.get_or_create(enrollment=plugin_enrollment, contig=contig)
    
    total_analyzed_annotation = plugin_enrollment.annotation_set \
                .filter(Q(status=Annotation.VALIDATED) | Q(status=Annotation.EXCLUDED)).count()
    
    if contig_list_filter is None:
        contig_list = plugin_enrollment.tissue.tissue_set.get(symbol=tissue_symbol).contig_set.all().order_by('-est_qty')
    else:
        contig_list_filter = int(contig_list_filter)
        if contig_list_filter == Annotation.PENDING:
            ''' Se a anotação estiver pendente, talvez ela não esteja ainda 
                tabela de anotações, então retorne todas as contigs excluindo 
                as que estejam anotadas (e não pendentes) '''
            contig_list = plugin_enrollment.tissue.tissue_set.get(symbol=tissue_symbol).contig_set.exclude(id__in=[a.contig_id for a in plugin_enrollment.annotation_set.exclude(status=Annotation.PENDING)]).order_by('-est_qty')
        else:
            ''' A anotação já está na base, listar a partir das já armazenadas '''
            assert contig_list_filter in dict(Annotation.STATUS_CHOICES).keys()
            contig_list = [c.contig for c in plugin_enrollment.annotation_set.filter(contig__tissue=current_tissue, status=contig_list_filter)]
        
    if request.method == 'POST':
        annotation_form = AnnotationForm(request.POST, instance=annotation)
        if annotation_form.is_valid():
            obj = annotation_form.save()
            messages.info(request, _('Annotation saved'))
            
            ''' return redirect('genome_annotation_validate_contig', 
                            classenrollment_id=class_enrollment.id, 
                            pluginenrollment_id=plugin_enrollment.id, 
                            contig_id=contig.id) '''
            return redirect(request.META['HTTP_REFERER'])
    else:
        annotation_form = AnnotationForm(instance=annotation)
    
    return render_to_response('genome_annotation/validate_contig.html', {
                                'course_class': class_enrollment.course_class,
                                'contig': contig,
                                'contig_list': contig_list,
                                'contig_list_filter': contig_list_filter,
                                'annotation_form': annotation_form,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                'tissue_symbol': tissue_symbol,
                                'current_tissue': current_tissue,
                                'total_contig_count': Contig.objects.filter(tissue__kind=plugin_enrollment.tissue).count(),
                                'total_analyzed_annotation': total_analyzed_annotation,
                                'STATUS_CHOICES': Annotation.STATUS_CHOICES,
                                },
                                context_instance=RequestContext(request))

@login_required
def bit_snp(request, contig_id):
    contig = get_object_or_404(Contig, pk=contig_id)
    f = open(os_path.join(settings.MEDIA_ROOT) + '/snps/%s/%s' % (contig.tissue.symbol, contig.name))
    lines = []
    for line in f:
        lines.append(line)
        if len(lines) == 25:
            break
    
    ref = ''
    i = 0
    y = 0
    for l in lines[0]:
        if y > 0:
            y -= 1
        elif i <> 0:
            ref += '.'
        i += 1
        if i % 25 == 0:
            ref += str(i)
            y = len(str(i))
        
    
        
    return render_to_response('genome_annotation/_bit_snp.html', {
                                'ref': ref,
                                'meu': contig.sequence,
                                'consensus': lines[0],
                                'reads': [{'bases': read.split('|')[1], 'name': read.split('|')[0]} for read in lines[1:]],
                                },
                                context_instance=RequestContext(request))



@login_required
def blat(request, contig_id):
    ''' Posta a sequence '''
    contig = get_object_or_404(Contig, pk=contig_id)
    f = open(os_path.join(settings.MEDIA_ROOT) + '/contigs/%s/%s' % (contig.tissue.symbol, contig.name))

    return render_to_response('genome_annotation/_blat.html', {
                                'contig': f.read(),
                                },
                                context_instance=RequestContext(request))

@login_required
def blast(request, mode, contig_id):
    ''' Posta a sequence '''
    contig = get_object_or_404(Contig, pk=contig_id)
    
    return render_to_response('genome_annotation/_blast%s.html' % mode, {
                                'contig': contig,
                                },
                                context_instance=RequestContext(request))


@login_required
def view_file(request, contig_id):
    ''' Posta a sequence '''
    contig = get_object_or_404(Contig, pk=contig_id)
    f = open(os_path.join(settings.MEDIA_ROOT) + '/contigs/%s/%s' % (contig.tissue.symbol, contig.name))

    return HttpResponse(str(f.read()), mimetype='text/plain')
    
    
    
''' submission views '''

@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission(request, classenrollment_id):
    ''' Redireciona o usuário para submissão '''
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = class_enrollment.pluginenrollment_set.all()[0]
    
    return redirect('genome_annotation_submission_title', classenrollment_id=class_enrollment.id, pluginenrollment_id=plugin_enrollment.id)


@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_title(request, classenrollment_id, pluginenrollment_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)
    
    instance, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)

    if instance.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)

    if request.method == 'POST':
        form = SubmissionTitleForm(instance, request.POST)
        
        if form.is_valid():
            form.save()
            messages.info(request, _('Title modified'))
            return redirect('genome_annotation_submission_institutions', classenrollment_id, pluginenrollment_id)
    else:
        form = SubmissionTitleForm(instance, {'title': instance.title})
    
    return render_to_response('genome_annotation/submission/title.html', {
                                'form': form,
                                'submission': instance,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                               },
                               context_instance=RequestContext(request))


@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_institutions(request, classenrollment_id, pluginenrollment_id, institution_id=None, form_class=None):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)
    
    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)
    
    if submission.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
    
    
    if institution_id:
        institution = submission.institution_set.get(pk=institution_id)
    else:
        institution = None
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=institution)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.submission = submission
            obj.save()
            
            messages.info(request, _('Institution added or modified'))
            return redirect('genome_annotation_submission_institutions', classenrollment_id, pluginenrollment_id)
    else:
        form = form_class(instance=institution)
    
    return render_to_response('genome_annotation/submission/institutions.html' , {
                                'form': form,
                                'submission': submission,
                                'institution': institution,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                },
                                context_instance=RequestContext(request))


@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_remove_institution(request, classenrollment_id, pluginenrollment_id, institution_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)
    
    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)
    
    if submission.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
    
    
    institution = submission.institution_set.get(pk=institution_id)
    institution.delete()
    messages.info(request, _('Institution removed'))
    return redirect('genome_annotation_submission_institutions', classenrollment_id, pluginenrollment_id)


@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_authors(request, classenrollment_id, pluginenrollment_id, author_id=None, form_class=None):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)

    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)
    
    if submission.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
    

    if author_id:
        author = submission.author_set.get(pk=author_id)
    else:
        author = None

    if request.method == 'POST':
        form = form_class(submission, request.POST, instance=author)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.submission = submission
            obj.save()

            messages.info(request, _('Author added or modified'))
            return redirect('genome_annotation_submission_authors', classenrollment_id, pluginenrollment_id)
    else:
        form = form_class(submission, instance=author)

    return render_to_response('genome_annotation/submission/authors.html' , {
                                'form': form,
                                'submission': submission,
                                'author': author,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                },
                                context_instance=RequestContext(request))
            

@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_remove_author(request, classenrollment_id, pluginenrollment_id, author_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)
    
    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)
    
    if submission.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
    
    
    author = submission.author_set.get(pk=author_id)
    author.delete()
    messages.info(request, _('Author removed'))
    return redirect('genome_annotation_submission_authors', classenrollment_id, pluginenrollment_id)



@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_resume(request, classenrollment_id, pluginenrollment_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)

    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)
    
    if submission.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
    
    
    if request.method == 'POST':
        submission.text = request.POST.get('text', '')
        submission.save()
        messages.info(request, _('Resume modified'))
        
        return redirect('genome_annotation_submission_resume', classenrollment_id, pluginenrollment_id)
    
    return render_to_response('genome_annotation/submission/resume.html' , {
                                'submission': submission,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                },
                                context_instance=RequestContext(request))


@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_submit(request, classenrollment_id, pluginenrollment_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)

    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)
    
    if submission.date_submitted:
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
    
    if request.POST:
        submission.submit()
        return redirect('genome_annotation_submission_sent', classenrollment_id, pluginenrollment_id)
        
    
    return render_to_response('genome_annotation/submission/submit.html' , {
                                'submission': submission,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                },
                                context_instance=RequestContext(request))
                                

@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_pdf_preview(request, classenrollment_id, pluginenrollment_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)

    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)

    submission.text = submission.text.replace('<br>', '<p>&nbsp;</p>')
    submission.text = submission.text.replace('<br/>', '<p>&nbsp;</p>')

    return render_to_response('genome_annotation/submission/pdf_preview.html' , {
                                'submission': submission,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                'authors': submission.get_ordered_author_institution()[0],
                                'institutions': submission.get_ordered_author_institution()[1],
                                },
                                context_instance=RequestContext(request))
@login_required
def submission_instructor_pdf_download(request, submission_id):
    submission, __ = Submission.objects.get_or_create(pk=submission_id)

    submission.text = submission.text.replace('<br>', '<p>&nbsp;</p>')
    submission.text = submission.text.replace('<br/>', '<p>&nbsp;</p>')

    return render_to_response('genome_annotation/submission/pdf_preview.html' , {
                                'submission': submission,
                                'authors': submission.get_ordered_author_institution()[0],
                                'institutions': submission.get_ordered_author_institution()[1],
                                },
                                context_instance=RequestContext(request))



@login_required
@class_enrollment_required
@plugin_enrollment_required
def submission_sent(request, classenrollment_id, pluginenrollment_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
    plugin_enrollment = get_object_or_404(class_enrollment.pluginenrollment_set, id=pluginenrollment_id)

    submission, __ = Submission.objects.get_or_create(plugin_enrollment=plugin_enrollment)



    return render_to_response('genome_annotation/submission/sent.html' , {
                                'submission': submission,
                                'class_enrollment': class_enrollment,
                                'plugin_enrollment': plugin_enrollment,
                                },
                                context_instance=RequestContext(request))
