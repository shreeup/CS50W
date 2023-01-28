from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.files import File
import os


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)
  
    #@staticmethod
    # def get_all_categories():
    #     return Category.objects.all()
  
    def __str__(self):
        return self.name



class Listing(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="none")
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    startingbid = models.DecimalField(default=0,decimal_places=2,max_digits=5)
    image_url = models.URLField()
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_by")
    purchaser=models.ForeignKey(User, null=True,blank=True,on_delete=models.CASCADE,related_name="purchased_by")
    watchers=models.ManyToManyField(User, blank=True,related_name="watchers")
    isactive=models.BooleanField(default=False)
    #comments=models.ManyToManyField(Comment,blank=True,related_name="reviews")
    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0]))
                    )
            self.save()


class Comment(models.Model):
    comment=models.CharField(max_length=100)
    commented_on=models.DateTimeField(auto_now_add=True)
    commentator=models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="reviews")

    def __str__(self):
        return self.commentator.username+": "+self.comment+ " - "+self.commented_on.strftime("%d/%m/%Y")

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.PROTECT)
    offer = models.DecimalField(max_digits=8, decimal_places=2)
    done_at = models.DateTimeField(auto_now_add=True)


