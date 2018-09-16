from django.conf.urls import url, include
from djurl import url, register_pattern
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'home'),
	url(r'^cart$', views.cart, name = 'cart'),
	url(r'^thank-for-shapping$', views.finalThanks, name = 'final-thank-you'),
	url(r'^choose-package/$', views.choosePackage, name = 'choose-package'),
	url(r'^brand-package-info/:slug$', views.brandPackageInfo, name = 'brand-package-info'),
	url(r'^remove-item$', views.removeItem, name = 'remove-item-from-cart'),
	url(r'^add-to-cart$', views.addToCart, name = 'add-item-to-cart'),
	url(r'^:slug/$', views.genCategoryPage, name = 'categoryPage'),
	url(r'^Item/:slug/$', views.genItemPage, name = 'itemPage'),
]