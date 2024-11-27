import json
from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.db.models import Q
from xhtml2pdf import pisa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Parish, Inspection, Question, GeneralComment, InspectionQuestion
from .forms import ParishForm, InspectionForm
from django.utils import timezone
from django.core.paginator import Paginator


class HomeView(ListView):
    model = Parish
    template_name = 'inspections/home.html'
    context_object_name = 'parishes'
    paginate_by = 10

    def get_queryset(self):
        return Parish.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_paginated'] = self.paginate_by < self.get_queryset().count()
        context['count_parishes'] = self.get_queryset().count()
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'inspections/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user after successful registration
        return redirect(self.success_url)


class ParishCreateView(LoginRequiredMixin, CreateView):
    model = Parish
    form_class = ParishForm
    template_name = 'inspections/create_parish.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        parish = form.save(commit=False)
        parish.save()
        return redirect(self.success_url)


class ParishDetailView(DetailView):
    model = Parish
    template_name = 'inspections/parish_detail.html'
    context_object_name = 'parish'
    pk_url_kwarg = 'parish_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parish = self.get_object()
        # Fetch all inspections ordered by the most recent update
        context['inspections'] = self.object.inspections.all().order_by('-updated_at')
        context['num_inspections'] = self.object.inspections.count()
        context['is_creator'] = self.request.user.is_authenticated and parish.created_by == self.request.user
        return context


class InspectionCreateView(LoginRequiredMixin, CreateView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'inspections/create_inspection.html'

    def form_valid(self, form):
        parish = Parish.objects.get(id=self.kwargs['parish_id'])
        inspection = form.save(commit=False)
        inspection.parish = parish
        inspection.save()

        # Save responses to questions
        for field_name, field_value in form.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = int(field_name.split('_')[1])
                question_instance = Question.objects.get(id=question_id)

                InspectionQuestion.objects.create(
                    inspection=inspection,
                    question=question_instance,
                    answer=field_value
                )

        comment_text = form.cleaned_data.get('comment_text', '')
        if comment_text:
            GeneralComment.objects.create(inspection=inspection, comment_text=comment_text)

        return redirect('parish_detail', parish_id=parish.id)


class InspectionDetailView(DetailView):
    model = Inspection
    template_name = 'inspections/inspection_detail.html'
    pk_url_kwarg = 'inspection_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inspection = self.get_object()

        # Fetch all questions related to this inspection
        inspection_questions = inspection.inspection_questions.all()  # Make sure to have the related name correctly set

        # Set up pagination
        paginator = Paginator(inspection_questions, 7)  # Show 7 questions per page
        page_number = self.request.GET.get('page')  # Get the page number from the URL
        questions_page = paginator.get_page(page_number)  # Get the relevant page of questions

        # Add paginated questions and comments to the context
        context['inspection_questions'] = questions_page  # Use the paginated questions
        context['comment'] = GeneralComment.objects.filter(inspection=inspection).first()

        # def get_context_data(self, **kwargs):
        #     context = super().get_context_data(**kwargs)
        # Fetch all questions and their related answers for this inspection
        #     inspection_questions = self.object.inspection_questions.all()
        #     context['inspection_questions'] = inspection_questions
        #     context['comment'] = GeneralComment.objects.filter(inspection=self.object).first()
        return context


class InspectionEditView(LoginRequiredMixin, UpdateView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'inspections/edit_inspection.html'
    pk_url_kwarg = 'inspection_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        inspection = self.object

        # Total questions and answered questions logic
        inspection_questions = InspectionQuestion.objects.filter(
            inspection=inspection,
            question__deleted=False  # Exclude deleted questions
        )

        paginator = Paginator(inspection_questions, 7)  # Show 7 questions per page
        page_number = self.request.GET.get('page')  # Get the page number from the URL
        questions_page = paginator.get_page(page_number)  # Get the relevant page of questions

        context['inspection_questions'] = questions_page

        # General comment field
        general_comment = GeneralComment.objects.filter(inspection=inspection).first()
        context['general_comment'] = general_comment.comment_text if general_comment else ""

        # For progress tracking
        total_questions = inspection_questions.count()
        answered_questions = inspection_questions.filter(answer__in=['yes', 'no', 'other']).count()

        context['total_questions'] = total_questions
        context['answered_questions'] = answered_questions

        return context

    def form_valid(self, form):
        inspection = form.save(commit=False)
        inspection.updated_at = timezone.now()
        inspection.save()

        # Update existing questions
        for field_name, field_value in form.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = int(field_name.split('_')[1])
                try:
                    inspection_question = InspectionQuestion.objects.get(
                        inspection=inspection,
                        question_id=question_id
                    )
                    inspection_question.answer = field_value
                    inspection_question.save()
                except InspectionQuestion.DoesNotExist:
                    # If the `InspectionQuestion` does not exist, skip or log an error
                    continue

        # Handle new questions
        new_questions = self.request.POST.getlist('new_questions[]')
        for question_text in new_questions:
            if question_text.strip():  # Ensure non-empty input
                question = Question.objects.create(
                    question_text=question_text.strip(),
                    is_default=False  # Ensure this is specific to this inspection
                )
                InspectionQuestion.objects.create(
                    inspection=inspection,
                    question=question,
                    answer=None  # No initial answer
                )

        # Handle removed questions
        removed_question_ids = self.request.POST.get('removed_questions', '[]')
        removed_question_ids = json.loads(removed_question_ids)  # Parse JSON string
        for question_id in removed_question_ids:
            try:
                inspection_question = InspectionQuestion.objects.get(
                    inspection=inspection,
                    question_id=question_id
                )
                inspection_question.delete()
            except InspectionQuestion.DoesNotExist:
                continue  # Skip if already deleted

        # Handle the general comment
        comment_text = form.cleaned_data.get('comment_text', '').strip()
        general_comment = GeneralComment.objects.filter(inspection=inspection).first()
        if comment_text:
            if general_comment:
                general_comment.comment_text = comment_text
                general_comment.save()
            else:
                GeneralComment.objects.create(inspection=inspection, comment_text=comment_text)
        elif general_comment:
            general_comment.delete()

        return redirect('parish_detail', parish_id=inspection.parish.id)


class InspectionDeleteView(DeleteView):
    model = Inspection
    template_name = 'inspections/delete_inspection.html'
    pk_url_kwarg = 'inspection_id'

    def get_object(self, queryset=None):
        parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])
        inspection = get_object_or_404(Inspection, id=self.kwargs['inspection_id'], parish=parish)

        # Check if the user is the creator of the parish
        if parish.created_by != self.request.user:
            raise HttpResponseForbidden("You are not allowed to delete inspections from this parish.")

        return inspection

    def get_success_url(self):
        parish_id = self.kwargs['parish_id']
        return reverse_lazy('parish_detail', kwargs={'parish_id': parish_id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class ParishDeleteView(DeleteView):
    model = Parish
    template_name = 'inspections/delete_parish.html'
    pk_url_kwarg = 'parish_id'

    def get_object(self, queryset=None):
        parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])
        if parish.created_by != self.request.user:
            raise HttpResponseForbidden("You are not allowed to delete this parish.")
        return parish

    def get_success_url(self):
        return reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class ParishEditView(LoginRequiredMixin, UpdateView):
    model = Parish
    form_class = ParishForm
    template_name = 'inspections/edit_parish.html'
    pk_url_kwarg = 'parish_id'

    def get_object(self, queryset=None):
        parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])
        # Check if the current user is the creator of the parish
        if parish.created_by != self.request.user:
            raise HttpResponseForbidden("You are not allowed to edit this parish.")
        return parish

    def form_valid(self, form):
        parish = form.save(commit=False)
        parish.save()
        return redirect('parish_detail', parish_id=parish.id)


class ExportInspectionPDFView(DetailView):
    model = Inspection
    template_name = 'inspections/inspection_pdf_template.html'
    context_object_name = 'inspection'
    pk_url_kwarg = 'inspection_id'

    def get(self, request, *args, **kwargs):
        # Explicitly call get_object to set self.object
        inspection = self.get_object()  # This loads the inspection object
        parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])

        # Context data for PDF rendering
        context = {
            'parish': parish,
            'inspection': inspection,
            'responses': inspection.inspection_questions.all()  # Assuming responses are related to inspection questions
        }

        # Render the inspection details to a template (HTML)
        html = render_to_string(self.template_name, context)

        # Prepare the PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="inspection_{inspection.id}.pdf"'

        # Convert HTML to PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Check if PDF generation was successful
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        # Return the generated PDF
        return response


class ParishSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            parishes = Parish.objects.filter(Q(name__icontains=query)).values('id', 'name')
        else:
            parishes = Parish.objects.values('id', 'name')

        return JsonResponse(list(parishes), safe=False)


def reports_view(request):
    """
    Renders the reports page that loads the datatable with inspection reports.
    This view does not need the 'draw' and other DataTables parameters.
    """
    # Render the reports page without requiring the DataTables parameters
    return render(request, 'inspections/reports.html')


class InspectionReportsAjaxDatatableView(AjaxDatatableView):
    model = Inspection
    title = "Inspection Reports"
    initial_order = [["date", "desc"]]

    column_defs = [
        {
            "name": "parish_name",
            "title": "Parish Name",
            "foreign_field": "parish__name",
            "orderable": True,
            "searchable": True,
        },
        {
            "name": "owner",
            "title": "Inspection Owner",
            "foreign_field": "parish__created_by",
            "orderable": True,
            "searchable": False,
        },
        {
            "name": "date",
            "title": "Date",
            "orderable": True,
            "searchable": False,
            "sort_field": "updated_at",
        },
        {
            "name": "name",
            "title": "Report Name",
            "orderable": False,
            "searchable": False,
            "sort_field": "id",
        },
        {
            "name": "download",
            "title": "Download",
            "orderable": False,
            "searchable": False,
            "defaultContent": "",
        },
    ]

    def get_initial_queryset(self, request=None):
        """
        Define the initial queryset that powers the datatable.
        """
        queryset = Inspection.objects.select_related("parish", "parish__created_by")
        queryset = queryset.order_by('updated_at')

        # Handle sorting based on request parameters
        if request and 'order' in request.GET:
            order_column = request.GET.get('order[0][column]')
            order_dir = request.GET.get('order[0][dir]')
            order_by_field = self.column_defs[int(order_column)]['sort_field'] if order_column else None

            if order_by_field:
                # Apply sorting to the queryset based on column and direction
                order_by = f"-{order_by_field}" if order_dir == 'desc' else order_by_field
                queryset = queryset.order_by(order_by)

        # Handle search functionality
        search_value = request.GET.get('search[value]', None)
        if search_value:
            queryset = queryset.filter(parish__name__icontains=search_value)  # Search by Report Name

        return queryset

    def customize_row(self, row, obj):
        """
        Customize how each row is rendered.
        """
        row["parish_name"] = obj.parish.name
        row["owner"] = obj.parish.created_by.username if obj.parish.created_by else "N/A"
        row["date"] = obj.updated_at.strftime("%Y-%m-%d") if obj.updated_at else "N/A"
        row["name"] = str(obj)
        row["download"] = format_html('<a href="{}export_pdf/" class="btn btn-primary"><i class="fa fa-download"></i> Download</a>',
    reverse('inspection_detail', kwargs={'parish_id': obj.parish.id, 'inspection_id': obj.id}))
        return row

    def get_data(self, request):
        """
        Handle DataTable's ajax request.
        """
        # Fetch parameters from the request
        draw = request.GET.get('draw', None)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        # search_value = request.GET.get('search[value]', '')

        # Get the base queryset
        queryset = self.get_initial_queryset(request)

        # Apply pagination
        total_count = queryset.count()
        queryset = queryset[start:start + length]

        # Prepare the data for the response
        data = [self.customize_row({}, obj) for obj in queryset]

        # Return the response in the required format
        response_data = {
            "draw": int(draw) if draw else 1,
            "recordsTotal": Inspection.objects.count(),
            "recordsFiltered": total_count,
            "data": data,
        }

        return JsonResponse(response_data)

