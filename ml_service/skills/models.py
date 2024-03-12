from django.db import models

class Category(models.Model):
    value = models.CharField(max_length=255, unique = True)
    
    def get_label(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"id: {self.id}, value: {self.value}"
    
    
class Skill(models.Model):
    value = models.CharField(max_length=255, unique = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    
    def get_label(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"id: {self.id}, value: {self.value}"
