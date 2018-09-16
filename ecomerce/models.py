from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save

from django.utils.text import slugify
# Create your models here.

#################################################
#################################################
# CATEGORY MODEL

class Category(models.Model):
	name = models.CharField(max_length=140)
	description = models.TextField()
	image_url = models.CharField(max_length=250, default = 'null')
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name

	def getName(self):
		return str(self.name)

	def getImage(self):
		return str(self.image_url)

	def getDescription(self):
		return str(self.description)

	def getSlug(self):
		return str(self.slug)
	@property
	def get_place_type(self):
		instance = self
		place_type = ContentType.objects.get_for_model(instance.__class__)
		return place_type

#################################################
#################################################
# ITEM MODEL

class Item(models.Model):
	name = models.CharField(max_length=140)
	item_category = models.CharField(max_length=140)
	item_brand = models.CharField(max_length=140)
	description = models.TextField()
	image_url = models.CharField(max_length=250, default = 'null')
	price = models.IntegerField(default=0,
        validators=[MaxValueValidator(100000), MinValueValidator(0)])
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.item_category + " " + self.item_brand + " " + self.name

	def getName(self):
		return str(self.name)

	def getPrice(self):
		return str(self.price)

	def getImage(self):
		return str(self.image_url)

	def getDescription(self):
		return str(self.description)

	def getCategory(self):
		return str(self.item_category)

	def getBrand(self):
		return str(self.item_brand)

	def getSlug(self):
		return str(self.slug)
	@property
	def get_place_type(self):
		instance = self
		place_type = ContentType.objects.get_for_model(instance.__class__)
		return place_type

#################################################
#################################################
# BRAND MODEL

class Brand(models.Model):
	name = models.CharField(max_length=140)
	description = models.TextField()
	image_url = models.CharField(max_length=250, default = 'null')
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name

	def getName(self):
		return str(self.name)

	def getImage(self):
		return str(self.image_url)

	def getDescription(self):
		return str(self.description)

	def getSlug(self):
		return str(self.slug)
	@property
	def get_place_type(self):
		instance = self
		place_type = ContentType.objects.get_for_model(instance.__class__)
		return place_type


def create_slug_item(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Item.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug_item(instance,new_slug=new_slug)
	return slug

def create_slug_category(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Category.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug_item(instance,new_slug=new_slug)
	return slug

def create_slug_brand(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Brand.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug_item(instance,new_slug=new_slug)
	return slug

def pre_save_post_receiver_item(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug_item(instance)

def pre_save_post_receiver_category(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug_category(instance)

def pre_save_post_receiver_brand(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug_brand(instance)

pre_save.connect(pre_save_post_receiver_item,sender=Item)
pre_save.connect(pre_save_post_receiver_category,sender=Category)
pre_save.connect(pre_save_post_receiver_brand,sender=Brand)