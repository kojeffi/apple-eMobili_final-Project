from django.db import models

class RecognizedAlphabet(models.Model):
    alphabet = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.0)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return self.alphabet

  