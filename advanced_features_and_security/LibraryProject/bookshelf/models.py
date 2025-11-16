from django.db import models

class Shelf(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Shelf'
        verbose_name_plural = 'Shelves'
        permissions = [
            ("can_view", "Can view shelf"),
            ("can_create", "Can create shelf"),
            ("can_edit", "Can edit shelf"),
            ("can_delete", "Can delete shelf"),
        ]

    def __str__(self):
        return self.name

class Section(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        permissions = [
            ("can_view", "Can view section"),
            ("can_create", "Can create section"),
            ("can_edit", "Can edit section"),
            ("can_delete", "Can delete section"),
        ]

    def __str__(self):
        return f"{self.shelf.name} - {self.name}"
