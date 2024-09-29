import shutil

from django.db import models
import os
from users.models import Seller

# Define path to save images of products
def product_image_path(instance, filename):
    # Assicurati che il prodotto sia stato salvato e abbia un 'pk'
    if not instance.pk:
        instance.save()  # Salva l'istanza per ottenere il pk

    # Genera il percorso per l'immagine
    return os.path.join(f'listings/imgs/{instance.pk}', filename)

class Product(models.Model):

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    description = models.TextField()

    #Images of product, the seller must upload at least one image
    image1 = models.ImageField(upload_to=product_image_path, blank=False, null=False)
    image2 = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    image4 = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    image5 = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    categories = models.ManyToManyField('Category', related_name='products')

    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    def save(self, *args, **kwargs):
        # Before save istance without pk
        if not self.pk:
            saved_images = [self.image1, self.image2, self.image3, self.image4, self.image5]
            self.image1 = None
            self.image2 = None
            self.image3 = None
            self.image4 = None
            self.image5 = None
            super().save(*args, **kwargs)

            #Then save images
            self.image1, self.image2, self.image3, self.image4, self.image5 = saved_images
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Obtain the path of the folder containing the images of the product
        product_folder = os.path.join('listings/imgs', str(self.pk))

        # Verify that the folder exists and if there is, delete it
        if os.path.exists(product_folder) and os.path.isdir(product_folder):
            shutil.rmtree(product_folder)  # Rimuove la cartella e tutto il suo contenuto

        # Delete the product from the database
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    def decrease_quantity(self, n):
        self.quantity -= n
        self.save()

    def increase_quantity(self, n):
        self.quantity += n
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'