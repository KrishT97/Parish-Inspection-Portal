from django.shortcuts import render, redirect, get_object_or_404
from .models import Parish, Inspection, Question, GeneralComment
from django.contrib.auth.decorators import login_required
from .forms import ParishForm, InspectionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.utils import timezone


def home(request):
    parishes_list = Parish.objects.all()
    paginator = Paginator(parishes_list, 10)  # Show 10 parishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inspections/home.html',
                  {'parishes': page_obj, 'page_obj': page_obj, 'is_paginated': page_obj.has_other_pages()})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'inspections/register.html', {'form': form})


@login_required
def create_parish(request):
    if request.method == "POST":
        form = ParishForm(request.POST)
        if form.is_valid():
            parish = form.save(commit=False)
            parish.created_by = request.user
            parish.save()
            return redirect('home')
    else:
        form = ParishForm()
    return render(request, 'inspections/create_parish.html', {'form': form})


def parish_detail(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)

    # Retrieve inspections sorted by the updated_at field in descending order
    inspections = parish.inspections.all().order_by('-updated_at')

    # Check if the user is the creator of the parish
    is_creator = request.user.is_authenticated and parish.created_by == request.user

    context = {
        'parish': parish,
        'inspections': inspections,
        'is_creator': is_creator,
    }
    return render(request, 'inspections/parish_detail.html', context)


@login_required
def create_inspection(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    if request.method == "POST":
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.parish = parish
            inspection.created_by = request.user
            inspection.save()
            comment_text = form.cleaned_data.get('comment_text', '')
            if comment_text:
                GeneralComment.objects.create(inspection=inspection, comment_text=comment_text)

            return redirect('parish_detail', parish_id=parish.id)
    else:
        form = InspectionForm()
    return render(request, 'inspections/create_inspection.html', {'form': form, 'parish': parish})


def inspection_detail(request, parish_id, inspection_id):
    inspection = get_object_or_404(Inspection, id=inspection_id, parish_id=parish_id)
    questions = Question.objects.filter(inspection=inspection)
    comment = GeneralComment.objects.filter(inspection=inspection).first()  # Get the first comment or None

    context = {
        'inspection': inspection,
        'questions': questions,
        'comment': comment,
    }
    return render(request, 'inspections/inspection_detail.html', context)


def edit_inspection(request, parish_id, inspection_id):
    parish = get_object_or_404(Parish, id=parish_id)
    inspection = get_object_or_404(Inspection, id=inspection_id, parish=parish)

    # Only allow the parish owner to edit their own parish's inspections
    if parish.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to edit this inspection.")

    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            # Update the updated_at field to the current time
            inspection.updated_at = timezone.now()

            # Save the inspection and update its timestamp
            form.save()

            # Handle general comment separately
            comment_text = form.cleaned_data.get('comment_text', '').strip()

            # Check if a GeneralComment exists for this inspection
            general_comment = GeneralComment.objects.filter(inspection=inspection).first()

            if comment_text:  # If there is a comment text provided
                if general_comment:  # Update existing comment
                    general_comment.comment_text = comment_text
                    general_comment.save()
                else:  # Create a new GeneralComment
                    GeneralComment.objects.create(inspection=inspection, comment_text=comment_text)
            else:
                # If no comment_text and a comment exists, delete it
                if general_comment:
                    general_comment.delete()

            return redirect('parish_detail', parish_id=parish.id)
    else:
        form = InspectionForm(instance=inspection)

    return render(request, 'inspections/edit_inspection.html', {'form': form, 'parish': parish, 'inspection': inspection})


def delete_inspection(request, parish_id, inspection_id):
    parish = get_object_or_404(Parish, id=parish_id)
    inspection = get_object_or_404(Inspection, id=inspection_id, parish=parish)

    # Check if the user is the creator of the parish
    if parish.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete inspections from this parish.")

    inspection.delete()
    return redirect('parish_detail', parish_id=parish.id)
