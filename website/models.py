from django.db import models

class Cancer(models.Model):
	C_CHOISES = (
		('l', 'lung'),
		('b', 'breast'),
	)
	cancer_name = models.CharField(max_length=1, choices=C_CHOISES)

	def __str__(self):
		return self.cancer_name

class Gene(models.Model):
	gene_name = models.CharField(max_length=50)

	def __str__(self):
		return self.gene_name

class Snp(models.Model):
	snp = models.CharField(max_length=50)
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	cancertype = models.ForeignKey(Cancer, on_delete=models.CASCADE)
	rareall = models.CharField(max_length=2)
	value = models.FloatField(default=1)
	coeff = models.FloatField(default=1)
	link = models.CharField(max_length=100)

	def __str__(self):
		return self.snp
	
