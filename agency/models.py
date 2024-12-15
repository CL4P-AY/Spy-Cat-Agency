from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Mission(models.Model):
    cat = models.ForeignKey(
        SpyCat,
        related_name="missions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission: {self.name} - Assigned to: {self.cat}"


class Target(models.Model):
    name = models.CharField(max_length=100)
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Target in {self.country} for {self.mission.name}"
