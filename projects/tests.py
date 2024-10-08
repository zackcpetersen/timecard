import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from accounts.models import User
from projects.models import Project, ProjectImage, ProjectType


class ProjectTests(TestCase):
    def setUp(self):
        # Create User
        self.user1 = User.objects.create(first_name='Tester',
                                         last_name='Testerson',
                                         email='testworkshard@gmail.com',
                                         is_admin=True)
        self.project_type = ProjectType.objects.create(name='Testing Type')
        self.project_name = 'Home Remodel'
        self.project_desc = 'Images of before and after home remodel project'
        self.proj_image_name = 'Before - Outside'
        self.proj_image_desc = 'Before image of the outside of home'
        self.projects_endpoint = '/api/projects/'
        self.proj_images_endpoint = '/api/project-images/'
        self.c = Client()
        self.c.force_login(user=self.user1)

    def test_project_api(self):
        # Create Project
        data = {
            'name': self.project_name,
            'description': self.project_desc,
            'type': self.project_type.pk,
        }
        request = self.c.post(self.projects_endpoint, data=data)
        self.assertEqual(request.json()['name'], data['name'])
        id = request.json()['id']

        # Update Project
        data.update({'name': 'Hotel Remodel'})
        pk_url = '{}{}/'.format(self.projects_endpoint, id)
        request = self.c.patch(pk_url, data=data, content_type='application/json')
        self.assertEqual(request.json()['name'], data['name'])

        # Get Project
        request = self.c.get(pk_url)
        self.assertEqual(request.json()['name'], data['name'])

        # Delete Project
        self.c.delete(pk_url)
        self.assertFalse(Project.objects.filter(pk=id))

    def test_project_image_api(self):
        # Create Project for image
        proj = Project.objects.create(name=self.project_name,
                                      description=self.project_desc,
                                      type=self.project_type)

        filepath = os.path.join(settings.BASE_DIR.parent, 'media/test_media/before_pic_test.jpg')
        with open(filepath, 'rb') as pic:
            uploaded_image = SimpleUploadedFile(pic.name, pic.read())
            data = {
                'name': self.proj_image_name,
                'description': self.proj_image_desc,
                'project': proj.pk,
                'image': uploaded_image
            }
            request = self.c.post(self.proj_images_endpoint, data=data)
            image_pk = request.json()['id']

        data.update({'image': 'http://testserver/media/project-images/before_pic_test'})
        self.assertTrue(data['image'] in request.json()['image'])

        # Update Image Name
        data = {'name': 'Outside Before Image'}
        pk_url = '{}{}/'.format(self.proj_images_endpoint, image_pk)
        request = self.c.patch(pk_url, data=data, content_type='application/json')
        self.assertEqual(request.json()['name'], data['name'])

        # Get Image
        request = self.c.get(pk_url)
        self.assertEqual(request.json()['name'], data['name'])

        # Delete Image
        self.c.delete(pk_url)
        self.assertFalse(ProjectImage.objects.filter(pk=image_pk))

    def test_multiple_proj_images(self):
        # Create Project
        proj = Project.objects.create(name=self.project_name,
                                      description=self.project_desc,
                                      type=self.project_type)

        # Create Images for proj
        filepath = os.path.join(settings.BASE_DIR.parent, 'media/test_media/before_pic_test.jpg')
        with open(filepath, 'rb') as pic:
            uploaded_image = SimpleUploadedFile(pic.name, pic.read())
            ProjectImage.objects.create(name=self.proj_image_name,
                                        description=self.proj_image_desc,
                                        project=proj,
                                        image=uploaded_image)

        filepath = os.path.join(settings.BASE_DIR.parent, 'media/test_media/after_remodel.jpg')
        with open(filepath, 'rb') as pic:
            uploaded_image = SimpleUploadedFile(pic.name, pic.read())
            ProjectImage.objects.create(name='After - Outside',
                                        description='After image outside the home',
                                        project=proj,
                                        image=uploaded_image)

        self.assertEqual(len(proj.project_images.all()), 2)

    def test_single_featured_img(self):
        # Create Project
        proj = Project.objects.create(name=self.project_name,
                                      description=self.project_desc,
                                      type=self.project_type)

        # Create Images for proj
        filepath = os.path.join(settings.BASE_DIR.parent, 'media/test_media/before_pic_test.jpg')
        with open(filepath, 'rb') as pic:
            uploaded_image = SimpleUploadedFile(pic.name, pic.read())
            proj_img_1 = ProjectImage.objects.create(name=self.proj_image_name,
                                                     description=self.proj_image_desc,
                                                     project=proj,
                                                     image=uploaded_image)
        proj_img_1.featured = True
        proj_img_1.save()

        self.assertTrue(proj_img_1.featured)

        filepath = os.path.join(settings.BASE_DIR.parent, 'media/test_media/after_remodel.jpg')
        with open(filepath, 'rb') as pic:
            uploaded_image = SimpleUploadedFile(pic.name, pic.read())
            proj_img_2 = ProjectImage.objects.create(name='After - Outside',
                                                     description='After image outside the home',
                                                     project=proj,
                                                     image=uploaded_image)

        proj_img_2.featured = True
        proj_img_2.save()

        self.assertFalse(ProjectImage.objects.get(pk=proj_img_1.pk).featured)
        self.assertTrue(ProjectImage.objects.get(pk=proj_img_2.pk).featured)
