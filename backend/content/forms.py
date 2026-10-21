from django import forms
from django.core.exceptions import ValidationError
from .models import Topic, TopicPublication, ContentBlock, LearningResource, Question
from .validators import validate_image, validate_pdf_upload


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

    class Media:
        css = {'all': ('admin/css/prepal_wysiwyg.css',)}
        js = ('admin/js/prepal_wysiwyg.js',)

    def clean(self):
        data = super().clean()
        parent = data.get('parent')
        seen = {self.instance.pk} if self.instance.pk else set()
        for _ in range(32):
            if not parent:
                break
            if parent.pk in seen:
                raise ValidationError('Topic hierarchy cannot contain a cycle.')
            seen.add(parent.pk)
            parent = parent.parent
        else:
            raise ValidationError('Topic hierarchy is too deep.')
        pub = TopicPublication.objects.filter(topic_id=self.instance.pk).first()
        if pub and (data.get('slug') != pub.snapshot['slug'] or getattr(data.get('parent'), 'pk', None) != pub.snapshot['parent_id']):
            raise ValidationError('Published slugs and parents are stable. Request a reviewed move.')
        return data


class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12, 'cols': 85, 'class': 'prepal-wysiwyg-textarea'})
        }

    class Media:
        css = {'all': ('admin/css/prepal_wysiwyg.css',)}
        js = ('admin/js/prepal_wysiwyg.js',)

    def clean(self):
        data = super().clean()
        file = data.get('file')
        if file and data.get('block_type') == 'image':
            validate_image(file)
        if file and data.get('block_type') == 'pdf' and 'file' in self.changed_data:
            raise ValidationError('Use Learning resources for new PDFs, then review and publish them.')
        return data


class ResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ['topic', 'title', 'file', 'source_reference', 'rights_note']

    def clean_file(self):
        file = self.cleaned_data['file']
        if 'file' in self.changed_data:
            validate_pdf_upload(file)
        return file

    def clean(self):
        data = super().clean()
        if self.instance.pk and self.instance.status in ('processing', 'ready', 'approved', 'withdrawn', 'needs_ocr') and self.changed_data:
            raise ValidationError('Processed candidates are immutable. Upload a new resource to replace this one.')
        return data


class TopicResourceInlineForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ['title', 'file', 'source_reference', 'rights_note']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and 'file' in self.changed_data:
            validate_pdf_upload(file)
        return file

    def clean(self):
        data = super().clean()
        if self.instance.pk and self.instance.status in ('processing', 'ready', 'approved', 'withdrawn', 'needs_ocr') and self.changed_data:
            raise ValidationError('Processed candidates are immutable. Upload a new resource to replace this one.')
        return data


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        data = super().clean()
        primary = data.get('primary_topic')
        related = data.get('related_topics')
        if primary and related is not None and primary in related:
            raise ValidationError('The primary subtopic must not also be a related subtopic.')
        # Existing ancestor-level legacy locations remain editable. New or moved
        # associations must use leaf subtopics, rather than broad subject nodes.
        for topic in ([primary] if primary and (not self.instance.pk or 'primary_topic' in self.changed_data) else []) + list(related or []):
            if topic.children.exists():
                raise ValidationError('Choose a syllabus leaf subtopic for question associations.')
        return data
