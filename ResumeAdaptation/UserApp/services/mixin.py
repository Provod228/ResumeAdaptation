from django.utils.text import slugify


class SlugMixin:
    @staticmethod
    def generate_unique_slug(model_class, instance, title_field='title'):
        if not getattr(instance, title_field, None):
            base_slug = "untitled"
        else:
            title = getattr(instance, title_field)
            base_slug = slugify(title, allow_unicode=False)

        if not base_slug:
            base_slug = model_class.__name__.lower()

        original_slug = base_slug
        counter = 1
        while model_class.objects.filter(slug=base_slug).exclude(pk=instance.pk).exists():
            base_slug = f"{original_slug}-{counter}"
            counter += 1

        return base_slug