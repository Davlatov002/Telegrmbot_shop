from django.db import models
import uuid
from user.models import User

class Category(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length= 255)
    discrton = models.TextField()
    price = models.FloatField(default=0.00)
    image = models.ImageField(upload_to="image/")
    category_id = models.ForeignKey(Category, related_name="Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    price = models.FloatField(default=0.00)
    user_id = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user_id.first_name



