from django.db import models

class Category(models.Model):
    value = models.CharField(max_length=255, unique = True)
    
    def get_label(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"id: {self.id}, value: {self.value}"
    
    
class Skill(models.Model):
    value = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    class Meta:
        unique_together = ('value', 'category')
    
    def get_label(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"id: {self.id}, value: {self.value}"
    

class Job(models.Model):
    value = models.CharField(max_length=255, unique = True)

    def get_label(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"id: {self.id}, value: {self.value}"
    
class JobGuide(models.Model):
    value = models.CharField(max_length=1000)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job")
    skills = models.CharField(blank=True, max_length=1000)

    def set_skills(self, skill_list):
        self.skills = ','.join(skill_list)

    def get_skills(self):
        return self.skills.split(',') if self.skills else []
    
    skill_list = property(get_skills, set_skills)