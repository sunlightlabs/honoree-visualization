from django.db import models

class Registrant(models.Model):
    original_id = models.CharField(max_length=255, verbose_name="original ID")
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Honoree(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name

class ContributionHonoree(models.Model):
    contribution = models.ForeignKey('Contribution')
    honoree = models.ForeignKey(Honoree)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Contribution(models.Model):
    year = models.IntegerField()
    received = models.DateField()
    type = models.CharField(max_length=255)
    registrant = models.ForeignKey(Registrant)
    lobbyist_name = models.CharField(max_length=255, blank=True)
    contribution_type = models.CharField(max_length=255, choices=(('Honorary Expenses', 'Honorary Expenses'), ('Meeting Expenses', 'Meeting Expenses')))
    original_honoree_description = models.TextField()
    sanitized_honoree_description = models.TextField()
    payee = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_date = models.DateField()
    comments = models.TextField(blank=True)
    honorees = models.ManyToManyField(Honoree, through=ContributionHonoree)
    
    def __str__(self):
        return '%s contribution for %s %s' % (self.registrant.name, self.payee, self.contribution_type.lower())