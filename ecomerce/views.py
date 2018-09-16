from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from ecomerce.models import Item, Brand, Category
# Create your views here.

##########################################################
############            INDEX               ##############
##########################################################
def index(request):
	categories = Category.objects.all().order_by("name")
	brands = Brand.objects.all()
	items = Item.objects.all()
	category_1_items = []
	category_2_items = []
	category_3_items = []

	cartItems = []
	
	for item in items:
		if item.item_category == "Category 3":
			category_3_items.append(item)
		
		elif item.item_category == "Category 2":
			category_2_items.append(item)
		
		elif item.item_category == "Category 1":
			category_1_items.append(item)
		
	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""
	
	return render(request, 'ecomerce/home.html', {
		'categories':categories,
		'brands':brands,
		'items':items,
		'category_1_items':category_1_items[:4],
		'category_2_items':category_2_items[:4],
		'category_3_items':category_3_items[:4],
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
	})

##########################################################
############             CART               ##############
##########################################################
def cart(request):
	categories = Category.objects.all().order_by("name")
	brands = Brand.objects.all()
	items = Item.objects.all()

	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
		lst = cartItems.split()
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""
	
	itemsToBuy = getItemsFromCart(lst,items)
	return render(request, 'ecomerce/cart.html', {
		'categories':categories,
		'brands':brands,
		'items':items,
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
		'itemsToBuy':itemsToBuy,
	})

##########################################################
##############       CHOOSE PACKAGE         ##############
##########################################################
def choosePackage(request):
	items = Item.objects.all()
	brands = Brand.objects.all()
	categories = Category.objects.all()
	cartItems = request.COOKIES['cartItems']
	lst = cartItems.split()
	itemsToBuy = getItemsFromCart(lst,items)

	brands_that_offer_package = []
	brands_that_offer_package_total_price = {}
	j = 0
	for brand in brands:
		brandpackage = []
		for i in range(0,len(itemsToBuy)):
			item_instance = Item.objects.filter(item_category=str(itemsToBuy[i].item_category),item_brand=str(brand))[:1].get()
			item_id = str(item_instance.id)
			brandpackage.append(item_id)
		
		if len(brandpackage) == len(itemsToBuy):
			brands_that_offer_package.append(brand)
			price , totalItems = getPriceAndTotalItems(brandpackage,items)
			brands_that_offer_package_total_price[str(j)] = price
			print(brands_that_offer_package_total_price)
			j += 1


	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""

	return render(request, 'ecomerce/choose-package.html',
		{
		'categories':categories,
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
		'brands_that_offer_package':brands_that_offer_package,
		'brands_that_offer_package_total_price':brands_that_offer_package_total_price,
		})

##########################################################
##############       CHOOSE PACKAGE         ##############
##########################################################
def finalThanks(request):
	categories = Category.objects.all().order_by("name")

	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""

	return render(request, 'ecomerce/final-thanks.html',
		{
		'categories':categories,
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
		})

##########################################################
##############      BRAND PACKAGE INFO      ##############
##########################################################
def brandPackageInfo(request, slug):
	items = Item.objects.all()
	brand = get_object_or_404(Brand,slug=slug)
	categories = Category.objects.all()
	cartItems = request.COOKIES['cartItems']
	lst = cartItems.split()
	itemsToBuy = getItemsFromCart(lst,items)

	brandpackage = []
	for i in range(0,len(itemsToBuy)):
		item_instance = Item.objects.filter(item_category=str(itemsToBuy[i].item_category),item_brand=str(brand))[:1].get()
		brandpackage.append(item_instance)
	
	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""

	return render(request, 'ecomerce/brand-package-info.html',
		{
		'categories':categories,
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
		'brandpackage':brandpackage,
		'brand':brand,
		})

##########################################################
############          ADD TO CART           ##############
##########################################################
def addToCart(request):
	item_instance = Item.objects.get(id=request.GET.get('id'))
	items = Item.objects.all()
	response = HttpResponse("Error")
	if request.is_ajax():
		cartItems = ""
		if 'cartItems' in request.COOKIES:
			cartItems = request.COOKIES['cartItems']
		cartItems = cartItems + " " + str(item_instance.id)
		response = HttpResponse("Added")
		response.set_cookie("cartItems", cartItems)
		lst = cartItems.split()
		
		price , totalItems = getPriceAndTotalItems(lst,items)
		totalPrice = str(price)
		response.set_cookie("totalPrice", totalPrice)
		response.set_cookie("totalItems", totalItems)	
		return response
	return response

##########################################################
############        REMOVE ITEM             ##############
##########################################################
def removeItem(request):
	item = Item.objects.get(id=request.GET.get('id'))
	items = Item.objects.all()
	response = HttpResponse("Error")
	if request.is_ajax():
		cartItems = ""
		if 'cartItems' in request.COOKIES:
			cartItems = request.COOKIES['cartItems']
		cartItems_list = cartItems.split()
		
		for mID in cartItems_list:
			if mID == (str(item.id)):
				cartItems_list.remove(str(item.id))
				break
		
		cartItems = ""
		for mID in cartItems_list:
			cartItems = cartItems + " " + str(mID)
		response = HttpResponse("Removed")
		response.set_cookie("cartItems", cartItems)
		totalPrice , totalItems = getPriceAndTotalItems(cartItems_list,items)	
		response.set_cookie("totalPrice", totalPrice)
		response.set_cookie("totalItems", totalItems)
		return response
	return response

##########################################################
##############    GEN CATEGORY PAGE         ##############
##########################################################
def genCategoryPage(request, slug):
	categories = Category.objects.all()
	category_instance = get_object_or_404(categories, slug=slug)
	tempItems = Item.objects.all()
	items = []
	for tempItem in tempItems:
		if tempItem.item_category == category_instance.name:
			items.append(tempItem)
	brands = Brand.objects.all()
	
	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""

	return render(request, 'ecomerce/category-page.html',
		{
		'items':items, 
		'brands':brands, 
		'category':category_instance, 
		'categories':categories,
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
		})

##########################################################
##############       GEN ITEM PAGE          ##############
##########################################################
def genItemPage(request, slug):
	categories = Category.objects.all()
	items = Item.objects.all()
	item_instance = get_object_or_404(items, slug=slug)
	
	if 'cartItems' in request.COOKIES:
		cartItems = request.COOKIES['cartItems']
	else:
		cartItems = []
	
	if 'totalPrice' in request.COOKIES:
		totalPrice = request.COOKIES['totalPrice']
	else:
		totalPrice = ""
	
	if 'totalItems' in request.COOKIES:
		totalItems = request.COOKIES['totalItems']
	else:
		totalItems = ""

	return render(request, 'ecomerce/item-page.html',
		{
		'item_instance':item_instance, 
		'categories':categories,
		'cartItems':cartItems,
		'totalPrice':totalPrice,
		'totalItems':totalItems,
		})

##########################################################
##############       HELPER FUNCTIONS       ##############
##########################################################
#--->
#--->
#--->
def getPriceAndTotalItems(lst, items):
	price = 0
	totalItems = len(lst)
	for iID in lst:
		for item in items:
			if iID == str(item.id):
				price += item.price
	return price,totalItems

#--->
#--->
#--->

def getItemsFromCart(lst,items):
	itemsToBuy = []
	for iID in lst:
		for item in items:
			if iID == str(item.id):
				itemsToBuy.append(item)
	return itemsToBuy
