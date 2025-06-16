from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from photoapp.forms import CustomUserCreationForm, CustomPasswordChangeForm, ProfileUpdateForm, PhotoUploadForm
from django.contrib.auth import update_session_auth_hash
from photoapp.models import CustomUser, Photo
import cloudinary.uploader
from django.conf import settings

def home_view(request):
    photos = Photo.objects.all().order_by('-created_at')
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = photos.filter(tags__icontains=tag_filter)
    return render(request, 'accounts/home.html', {'photos': photos})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    form = CustomPasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, 'accounts/dashboard.html', {'form': form})

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                uploaded_file = request.FILES['profile_picture']
                # Simple image validation
                if not uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    messages.error(request, 'Please upload a valid image file (jpg, jpeg, png, gif).')
                    return render(request, 'accounts/profile_update.html', {'form': form})
                try:
                    result = cloudinary.uploader.upload(
                        uploaded_file,
                        folder='profiles',
                        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
                        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME']
                    )
                    user.profile_picture = result['public_id']
                except Exception as e:
                    messages.error(request, f"Cloudinary upload failed: {str(e)}")
                    return render(request, 'accounts/profile_update.html', {'form': form})
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})

@login_required
def photo_upload_view(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            uploaded_file = request.FILES['image']
            # Simple image validation
            if not uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                messages.error(request, 'Please upload a valid image file (jpg, jpeg, png, gif).')
                return render(request, 'accounts/photo_upload.html', {'form': form})
            try:
                result = cloudinary.uploader.upload(
                    uploaded_file,
                    folder='photos',
                    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
                    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME']
                )
                photo.image = result['public_id']
                photo.save()
                messages.success(request, 'Photo uploaded successfully!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Cloudinary upload failed: {str(e)}")
                return render(request, 'accounts/photo_upload.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PhotoUploadForm()
    return render(request, 'accounts/photo_upload.html', {'form': form})

def photo_detail_view(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'accounts/photo_detail.html', {'photo': photo})

@login_required
def photo_like_view(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
        messages.success(request, 'Photo unliked.')
    else:
        photo.likes.add(request.user)
        messages.success(request, 'Photo liked!')
    return redirect('photo_detail', pk=pk)