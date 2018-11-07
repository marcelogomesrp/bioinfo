# coding: utf-8
from django.conf.urls.defaults import *
from forms import AddInstitutionForm, EditInstitutionForm, AddAuthorForm, EditAuthorForm
import views

urlpatterns = patterns('',
    # submission views
    url(r'^submission/(?P<classenrollment_id>\d+)/r/$', views.submission, 
        name='genome_annotation_submission'),
    
    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/title/$', views.submission_title, 
        name='genome_annotation_submission_title'),
        
    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/institutions/$', views.submission_institutions, {
        'form_class': AddInstitutionForm,
    }, name='genome_annotation_submission_institutions'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/institutions/(?P<institution_id>\d+)/$', views.submission_institutions, {
        'form_class': EditInstitutionForm,
    }, name='genome_annotation_submission_institutions'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/institutions/(?P<institution_id>\d+)/rm/$', views.submission_remove_institution,
        name='genome_annotation_submission_remove_institution'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/author/$', views.submission_authors, {
        'form_class': AddAuthorForm,
    }, name='genome_annotation_submission_authors'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/author/(?P<author_id>\d+)/$', views.submission_authors, {
        'form_class': EditAuthorForm,
    }, name='genome_annotation_submission_authors'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/author/(?P<author_id>\d+)/rm/$', views.submission_remove_author,
        name='genome_annotation_submission_remove_author'),
        
    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/resume/$', views.submission_resume,
        name='genome_annotation_submission_resume'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/submit/$', views.submission_submit,
        name='genome_annotation_submission_submit'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/preview/$', views.submission_pdf_preview,
        name='genome_annotation_submission_pdf_preview'),

    url(r'^submission/(?P<submission_id>\d+)/pdf-d/$', views.submission_instructor_pdf_download,
            name='submission_instructor_pdf_download'),

    url(r'^submission/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/sent/$', views.submission_sent,
        name='genome_annotation_submission_sent'),

    # other views

    url(r'^projects/(?P<class_id>\d+)/manage/$', 
        views.manage_projects, name='genome_annotation_manage_projects'),
        
    url(r'^questions/(?P<class_id>\d+)/(?P<project_id>\d+)/manage/$', 
        views.manage_questions, name='genome_annotation_manage_questions'),
        
    url(r'^questions/(?P<class_id>\d+)/(?P<project_id>\d+)/add/$', 
        views.add_question, name='genome_annotation_add_question'),

    url(r'^questions/(?P<class_id>\d+)/(?P<project_id>\d+)/(?P<question_id>\d+)/modify/$', 
        views.modify_question, name='genome_annotation_modify_question'),
        
    url(r'^questions/(?P<class_id>\d+)/(?P<project_id>\d+)/(?P<question_id>\d+)/remove/$', 
        views.remove_question, name='genome_annotation_remove_question'),
        
    url(r'^questions/(?P<classenrollment_id>\d+)/$', views.questions, 
        name='genome_annotation_questions'),
        
    url(r'^c(?P<class_id>\d+)/stats/$', 
        views.annotation_stats, name='genome_annotation_annotation_stats'),
        
    url(r'^enrollment/(?P<classenrollment_id>\d+)/$', 
        views.plugin_enrollment, name='genome_annotation_plugin_enrollment'),
        
    url(r'^tutorials/(?P<classenrollment_id>\d+)/$', 
        views.video_tutorials, name='genome_annotation_video_tutorials'),
        
    url(r'^validate/(?P<classenrollment_id>\d+)/$', 
        views.contig_validation, name='genome_annotation_validation'),
        
    url(r'^validate/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/(?P<tissue_symbol>\w{2})/$', 
        views.validate_contig, name='genome_annotation_validate_contig'),
        
    url(r'^validate/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/(?P<tissue_symbol>\w{2})/(?P<contig_id>\d+)/$', 
        views.validate_contig, name='genome_annotation_validate_contig'),
        
    url(r'^validate/(?P<classenrollment_id>\d+)/(?P<pluginenrollment_id>\d+)/(?P<tissue_symbol>\w{2})/(?P<contig_id>\d+)/(?P<contig_list_filter>\d+)/$', 
        views.validate_contig, name='genome_annotation_validate_contig'),
        
    url(r'^_blast(?P<mode>[n|x])/(?P<contig_id>\d+)/$', views.blast, 
        name='genome_annotation_blast'),
            
    url(r'^_blat/(?P<contig_id>\d+)/$', views.blat, 
        name='genome_annotation_blat'),
        
    url(r'^bit/(?P<contig_id>\d+)/snp/$', views.bit_snp, 
        name='genome_annotation_bit_snp'),

    url(r'^view-file/(?P<contig_id>\d+)/$', views.view_file, 
        name='genome_annotation_view_file'),
)