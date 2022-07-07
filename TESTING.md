# Testing of Doodle This
## Code Validation

* HTML code validated with W3C [HTML Validator](https://validator.w3.org/nu/).

* CSS code validated with W3C [CSS Validator](https://jigsaw.w3.org/css-validator/).

* Javascript code validated with [JSHint](https://jshint.com/).

* Python code validated with [PEP8 Online](http://pep8online.com/).

### HTML Validation

All pages validated with no warnings or errors. 

As the navbar renders differet content depending on whether a user is logged out, logged in, or logged in as staff, I tested it in each of the three states.

|             **Page**             |                                 **Screenshot**                                |
|:--------------------------------:|:-----------------------------------------------------------------------------:|
|      **navbar.html (admin)**     | ![](documentation/testing_images/validation/html/admin.jpg)                   |
|   **navbar.html (logged out)**   | ![](documentation/testing_images/validation/html/logged-out.jpg)              |
|    **navbar.html (logged in)**   | ![](documentation/testing_images/validation/html/logged_in.jpg)               |
|           **faq.html**           | ![](documentation/testing_images/validation/html/faq.jpg)                     |
|         **profile.html**         | ![](documentation/testing_images/validation/html/profile.jpg)                 |
|           **cart.html**          | ![](documentation/testing_images/validation/html/cart.jpg)                    |
|         **checkout.html**        | ![](documentation/testing_images/validation/html/checkout.jpg)                |
|     **order_confirmed.html**     | ![](documentation/testing_images/validation/html/order_confirmed.jpg)         |
|      **order_details.html**      | ![](documentation/testing_images/validation/html/order_details.jpg)           |
|    **add_product_image.html**    | ![](documentation/testing_images/validation/html/add_product_image.jpg)       |
|   **add_product_variant.html**   | ![](documentation/testing_images/validation/html/add_product_variant.jpg)     |
|       **add_product.html**       | ![](documentation/testing_images/validation/html/add_product.jpg)             |
|    **edit_product_image.html**   | ![](documentation/testing_images/validation/html/edit_product_image.jpg)      |
|   **edit_product_variant.html**  | ![](documentation/testing_images/validation/html/edit_product_variant.jpg)    |
|       **edit_product.html**      | ![](documentation/testing_images/validation/html/edit_product.jpg)            |
|     **product_details.html**     | ![](documentation/testing_images/validation/html/product_details.jpg)         |
|    **product_management.html**   | ![](documentation/testing_images/validation/html/product_management.jpg)      |
|     **show_all_prints.html**     | ![](documentation/testing_images/validation/html/show_all_prints.jpg)         |
|        **sketchbook.html**       | ![](documentation/testing_images/validation/html/sketchbook.jpg)              |
|      **email_confirm.html**      | ![](documentation/testing_images/validation/html/email_confirm.jpg)           |
|          **email.html**          | ![](documentation/testing_images/validation/html/email.jpg)                   |
|          **login.html**          | ![](documentation/testing_images/validation/html/login.jpg)                   |
|          **logout.html**         | ![](documentation/testing_images/validation/html/logout.jpg)                  |
|     **password_change.html**     | ![](documentation/testing_images/validation/html/password_change.jpg)         |
| **password_reset_from_key.html** | ![](documentation/testing_images/validation/html/password_reset_from_key.jpg) |
|      **password_reset.html**     | ![](documentation/testing_images/validation/html/password_reset.jpg)          |
|       **password_set.html**      | ![](documentation/testing_images/validation/html/password_set.jpg)            |
|          **signup.html**         | ![](documentation/testing_images/validation/html/signup.jpg)                  |
|           **404.html**           | ![](documentation/testing_images/validation/html/404.jpg)                     |
|           **500.html**           | ![](documentation/testing_images/validation/html/500.jpg)                     |

### CSS Validation

All CSS files passed with no errors.

|          File         |                           **Screenshot**                           |
|:---------------------:|:------------------------------------------------------------------:|
| **product-image.css** | ![](documentation/testing_images/validation/css/product-image.jpg) |
|     **style.css**     | ![](documentation/testing_images/validation/css/style.jpg)         |
|      **tour.css**     | ![](documentation/testing_images/validation/css/tour.jpg)          |

The validator returned 21 warnings for style.css. The majority of these were because elements had the same color for background-color and border-color. This is intentional to override Bootstrap's default styles. The remaining few warnings were related to vendor pseudo-elements. These are also Bootstrap styles that are being overwritten.

The validator returned 28 warnings for tour.css. All warnings were related to the css variables used and shouldn't be a concern.

### Javascript Validation

All javascript files validated with no errors. Because I made significant changes to the Atrament library's atrament.js and pointer.js files in [my fork](https://github.com/lmjh/atrament.js/) of the library, I also validated those files.

|       File       |                               **Screenshot**                              |                                                       **Notes**                                                       |
|:----------------:|:-------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------:|
| productImage.js  | ![](documentation/testing_images/validation/javascript/productImage.jpg)  |                                                                                                                       |
| logout.js        | ![](documentation/testing_images/validation/javascript/logout.jpg)        | One undefined variable: localforage                                                                                   |
| cart.js          | ![](documentation/testing_images/validation/javascript/cart.jpg)          | One undefined variable: localforage                                                                                   |
| notifications.js | ![](documentation/testing_images/validation/javascript/notifications.jpg) | One undefined variable: bootstrap                                                                                     |
| checkout.js      | ![](documentation/testing_images/validation/javascript/orders.jpg)        | Three undefined variables: Stripe, localforage, displayToast                                                          |
| prints.js        | ![](documentation/testing_images/validation/javascript/prints.jpg)        | Two undefined variables: localforage, displayToast                                                                    |
| sketchbook.js    | ![](documentation/testing_images/validation/javascript/sketchbook.jpg)    | Eight undefined variables - Atrament, Coloris, bootstrap, localforage, displayToast, introJs, tourMobile, tourDesktop |
| tour.js          | ![](documentation/testing_images/validation/javascript/tour.jpg)          | Two unused variables: tourMobile, tourDesktop                                                                         |
| atrament.js      | ![](documentation/testing_images/validation/javascript/atrament.png)      |                                                                                                                       |
| pointer.js       | ![](documentation/testing_images/validation/javascript/pointer.png)       |                                                                                                                       |

In various combinations, the validator returned 'undefined variable' warnings about the following objects:

* Atrament - This comes from the Atrament library used to provide the drawing canvas. It is loaded in the base template.
* Stripe - This comes from the Strip javascript files which provide the payment system. It is loaded in the base template. 
* Coloris - This comes from the Coloris library which is used to provide the colour mixer. It is loaded in the sketchbook page template.
* bootstrap -  This comes from Bootstrap 5 and is loaded in the base template.
* localforage - This come from the localforage library which is used to manage local storage of files and variables. It is loaded in the base template.
* displayToast -  This is a function I wrote to display notifications. It is defined in notifications.js and loaded in the base template.
* introJs - This come from the library used to implement the homepage tour. It is loaded in the base template.

The validator returned two 'unused variable' warnings about the tourMobile and tourDesktop objects in the tour.js file. These objects define the homepage tours. They are imported to the sketchbook.js file and used there.

### Python Validation

|                       File                       |                                 **Screenshot**                                 |   **Notes**  |
|:------------------------------------------------:|:------------------------------------------------------------------------------:|:------------:|
|               **accounts/forms.py**              | ![](documentation/testing_images/validation/python/accounts_forms.jpg)         |              |
|              **accounts/models.py**              | ![](documentation/testing_images/validation/python/accounts_models.jpg)        |              |
|               **accounts/urls.py**               | ![](documentation/testing_images/validation/python/accounts_urls.jpg)          |              |
|               **accounts/views.py**              | ![](documentation/testing_images/validation/python/accounts_views.jpg)         |              |
|         **accounts/tests/test_forms.py**         | ![](documentation/testing_images/validation/python/accounts_test_forms.jpg)    |              |
|         **accounts/tests/test_models.py**        | ![](documentation/testing_images/validation/python/accounts_test_models.jpg)   |              |
|         **accounts/tests/test_views.py**         | ![](documentation/testing_images/validation/python/accounts_test_views.jpg)    |              |
|               **cart/contexts.py**               | ![](documentation/testing_images/validation/python/cart_contexts.jpg)          |              |
|                 **cart/urls.py**                 | ![](documentation/testing_images/validation/python/cart_urls.jpg)              |              |
|                 **cart/views.py**                | ![](documentation/testing_images/validation/python/cart_views.jpg)             | W503 warning |
|          **cart/tests/test_contexts.py**         | ![](documentation/testing_images/validation/python/cart_test_contexts.jpg)     |              |
|           **cart/tests/test_views.py**           | ![](documentation/testing_images/validation/python/cart_test_views.jpg)        |              |
|            **doodle_this/settings.py**           | ![](documentation/testing_images/validation/python/main_settings.jpg)          | E501 warning |
|              **doodle_this/urls.py**             | ![](documentation/testing_images/validation/python/main_urls.jpg)              |              |
|              **doodle_this/views.py**            | ![](documentation/testing_images/validation/python/main_views.jpg)             |              |
|           **notifications/contexts.py**          | ![](documentation/testing_images/validation/python/notifications_contexts.jpg) |              |
|              **orders/__init__.py**              | ![](documentation/testing_images/validation/python/orders_init.jpg)            |              |
|                **orders/admin.py**               | ![](documentation/testing_images/validation/python/orders_admin.jpg)           |              |
|                **orders/apps.py**                | ![](documentation/testing_images/validation/python/orders_apps.jpg)            |              |
|                **orders/forms.py**               | ![](documentation/testing_images/validation/python/orders_forms.jpg)           |              |
|               **orders/models.py**               | ![](documentation/testing_images/validation/python/orders_models.jpg)          |              |
|               **orders/signals.py**              | ![](documentation/testing_images/validation/python/orders_signals.jpg)         |              |
|                **orders/urls.py**                | ![](documentation/testing_images/validation/python/orders_urls.jpg)            |              |
|                **orders/views.py**               | ![](documentation/testing_images/validation/python/orders_views.jpg)           |              |
|           **orders/webhook_handler.py**          | ![](documentation/testing_images/validation/python/orders_webhook_handler.jpg) |              |
|              **orders/webhooks.py**              | ![](documentation/testing_images/validation/python/orders_webhooks.jpg)        |              |
|          **orders/tests/test_views.py**          | ![](documentation/testing_images/validation/python/orders_test_views.jpg)      |              |
|                **prints/admin.py**               | ![](documentation/testing_images/validation/python/prints_admin.jpg)           |              |
|                **prints/forms.py**               | ![](documentation/testing_images/validation/python/prints_forms.jpg)           |              |
|               **prints/models.py**               | ![](documentation/testing_images/validation/python/prints_models.jpg)          |              |
|                **prints/urls.py**                | ![](documentation/testing_images/validation/python/prints_urls.jpg)            |              |
|                **prints/views.py**               | ![](documentation/testing_images/validation/python/prints_views.jpg)           |              |
|               **prints/widgets.py**              | ![](documentation/testing_images/validation/python/prints_widgets.jpg)         |              |
| **prints/template_tags/custom_template_tags.py** | ![](documentation/testing_images/validation/python/prints_template_tags.jpg)   |              |
|          **prints/tests/test_forms.py**          | ![](documentation/testing_images/validation/python/prints_test_forms.jpg)      |              |
|          **prints/tests/test_models.py**         | ![](documentation/testing_images/validation/python/prints_test_models.jpg)     |              |
|          **prints/tests/test_views.py**          | ![](documentation/testing_images/validation/python/prints_test_views.jpg)      | W503 warning |
|               **prompts/admin.py**               | ![](documentation/testing_images/validation/python/prompts_admin.jpg)          |              |
|               **prompts/models.py**              | ![](documentation/testing_images/validation/python/prompts_models.jpg)         |              |
|              **prompts/prompts.py**              | ![](documentation/testing_images/validation/python/prompts_prompts.jpg)        |              |
|                **prompts/urls.py**               | ![](documentation/testing_images/validation/python/prompts_urls.jpg)           |              |
|               **prompts/views.py**               | ![](documentation/testing_images/validation/python/prompts_views.jpg)          |              |
|         **prompts/tests/test_models.py**         | ![](documentation/testing_images/validation/python/prompts_test_models.jpg)    |              |
|         **prompts/tests/test_prompts.py**        | ![](documentation/testing_images/validation/python/prompts_test_prompts.jpg)   |              |
|          **prompts/tests/test_views.py**         | ![](documentation/testing_images/validation/python/prompts_test_views.jpg)     |              |
|              **sketchbook/urls.py**              | ![](documentation/testing_images/validation/python/sketchbook_urls.jpg)        |              |
|              **sketchbook/views.py**             | ![](documentation/testing_images/validation/python/sketchbook_views.jpg)       |              |
|        **sketchbook/tests/test_views.py**        | ![](documentation/testing_images/validation/python/sketchbook_test_views.jpg)  |              |
|              **custom_storages.py**              | ![](documentation/testing_images/validation/python/custom_storages.jpg)        |              |

The PEP8online.com validator returned four style errors for "line break before the binary operator" in the Cart app views.py file and the Prints app test_views.py file. I'm not sure why the validation tool flags this as an error, because the PEP 8 specifications [for this style rule](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator) state that line breaks either before or after a binary operator are permissible, but line breaks before are suggested for new code as it improves readability. I have therefore left the code in both files as it was, with the line breaks before the binary operators.

Long line warnings were returned for the password validators in settings.py. This is standard Django generated code and can't be changed to fix the errors.

***

## User Stories Testing

#### 1. New User Stories

**1.1. As a new user I want to be able to quickly understand the purpose of the site so that I can decide if it provides value to me**

* Users are welcomed to the homepage with a welcome modal which describes the purposes of the site.
* Putting the sketchbook on the homepage also allows users to immediately see from the controls and layout that this is a drawing application.  

![](documentation/testing_images/user_stories/user-story-1-1-1.jpg)

**1.2. As a new user I want to be able to quickly understand how to use the application so that I can start using it to create art**

* The welcome modal has a link to start a tour of the site's features which users can use to quickly get an overview of all controls.
![](documentation/testing_images/user_stories/user-story-1-2-1.jpg)
* The tool icons are designed so that their purpose should be fairly clear to anyone familiar with drawing software, so users who don't want to take the tour should be able to use most features quickly anyway.  
![](documentation/testing_images/user_stories/user-story-1-2-2.jpg)

**1.3. As a new user I want to be able to know where to look for help so that I can find answers to my questions**

* A large help button is situated in the sketchbook's left/top control panel, which launches the intro tour.  
![](documentation/testing_images/user_stories/user-story-1-3-1.jpg)
* An FAQ is linked in the main navigation bar, which provides more information about the site.  
![](documentation/testing_images/user_stories/user-story-1-3-2.jpg)

**1.4. As a new user I want to be able to easily sign up for an account so that I can store my details and save my artwork**

* Registration links are situated in the sketchbook's control panel for users who aren't signed in, and also in the main site nav.  
![](documentation/testing_images/user_stories/user-story-1-4-1.jpg)
![](documentation/testing_images/user_stories/user-story-1-4-2.jpg)
* Users can complete a simple form to register an account.  
![](documentation/testing_images/user_stories/user-story-1-4-3.jpg)

#### 2. Registered User Stories

**2.1. As a registered user I want to be able to easily log in to or out of my account so that I can access the data I've stored**

* Links to the sign in page are situated in the sketchbook control panel and in the main site nav.  
![](documentation/testing_images/user_stories/user-story-2-1-1.jpg)  
![](documentation/testing_images/user_stories/user-story-2-1-2.jpg)  
* Users can complete a simple form to sign in. 
![](documentation/testing_images/user_stories/user-story-2-1-3.jpg)  

**2.2. As a registered user I want to be able to save my drawings so that I can access them later**

* The Save / Load button opens a save/load modal.  
![](documentation/testing_images/user_stories/user-story-2-2-1.jpg)  
* Users can save their drawings by selecting a save slot, clicking 'Save' and then confirming.  
![](documentation/testing_images/user_stories/user-story-2-2-2.jpg)  
![](documentation/testing_images/user_stories/user-story-2-2-3.jpg)  

**2.3. As a registered user I want to be able to edit my saved drawings so that I can make changes to them after they're saved**

* Users can load a drawing back into their sketchbook by selecting the saved drawing and then clicking 'Load'.  
![](documentation/testing_images/user_stories/user-story-2-3-1.jpg)  
* Once a drawing is loaded on the sketchbook, users can make any changes they like.  
![](documentation/testing_images/user_stories/user-story-2-3-2.jpg)  

**2.4. As a registered user I want to be able to delete my saved drawings so that I can get rid of old drawings and make space for new ones**

* Users can delete their saved drawings by clicking the Delete button in the Gallery section of the Account page.  
![](documentation/testing_images/user_stories/user-story-2-4-1.jpg)  
* A confirmation modal is opened to avoid accidental deletions. Once users confirm the deletion, the saved drawing is removed.  
![](documentation/testing_images/user_stories/user-story-2-4-2.jpg)  
![](documentation/testing_images/user_stories/user-story-2-4-3.jpg)  

**2.5. As a registered user I want to be able to save my shipping details so that I can checkout more quickly in future**

* Users can fill out and submit the shipping details form on the Account page to save their details.  
![](documentation/testing_images/user_stories/user-story-2-5-1.jpg)  
* Alternatively, ticking the 'Save my details' box on the checkout page will save the delivery information entered on that page in the user's account.  
![](documentation/testing_images/user_stories/user-story-2-5-2.jpg)  

#### 3. Drawing App User Stories

**3.1. As a drawing app user I want to be able to use a selection of basic drawing tools so that I can create drawings**

* Four basic drawing tools are provided for users.
* While more advanced drawing software might have many more tools, these four tools cover all of the basic requirements for creating drawings.  
![](documentation/testing_images/user_stories/user-story-3-1-1.jpg)  
* The pencil tool allows drawing lines of varying thickness (in combination with the stroke width slider).
* The fill tool allows filling large areas with colours.
* The eraser tool allows removing colours from parts of the canvas.
* The colour picker tool allows quickly selecting colours from the canvas.  


**3.2. As a drawing app user I want to be able to select from a number of preset colours so that I can quickly create art with a balanced palette**

* A range of preset colour options are provided.
* I took time to carefully select the palette, choosing colours that I thought would would work well together and cover a wide array of needs.
* There are six primary colours, six lighter pastel shades, four skin tone colours, two greys, white and black.  
![](documentation/testing_images/user_stories/user-story-3-2-1.jpg)  


**3.3. As a drawing app user I want to be able to use custom colours so that I can draw with any colour I want**

* A colour mixer is availabe which allows users can select any colour they wish.  
![](documentation/testing_images/user_stories/user-story-3-3-1.jpg)  
* Custom colours can be quickly retrieved from the canvas using the colour picker tool.  
![](documentation/testing_images/user_stories/user-story-3-3-2.jpg)  


**3.4. As a drawing app user I want to be able to generate random drawing prompts so that I can quickly get ideas about what to draw**

* Random drawing prompts are generated by functions from lists and displayed on the sketchbook page.
* Users can simply click the "New Prompt" button to generate a new prompt without leaving the page.   
![](documentation/testing_images/user_stories/user-story-3-4-1.jpg)  

  
#### 4. Shopper User Stories

**4.1. As a shopper I want to be able to purchase products printed with my drawing so that I can own or gift a physical copy of my drawing**

* Doodle This features an ecommerce shop that allows users to buy products printed with their drawings.
* A 'Buy a Print' link to the shop is prominently positioned in the nav bar and styled to stand out from the others.  
![](documentation/testing_images/user_stories/user-story-4-1-1.jpg)  
* On mobile screens, the button is usually hidden to save space, but the shopping cart logo is always visible, hinting that a shop is available, and the link is styled to stand out in the drop-down mobile nav.  
![](documentation/testing_images/user_stories/user-story-4-1-2.jpg)  

**4.2. As a shopper I want to be able to view the products available to purchase so that I can decide if there are any I'd like to buy**

* Clicking the 'Buy a Print' button takes users to a shop page where all of the available product types are listed.  
![](documentation/testing_images/user_stories/user-story-4-2-1.jpg)  


**4.3. As a shopper I want to be able to view product details so that I can find out more about the product and any variants available**

* When users click any of the product on the main shop page, they're taken to a details page for that product.  
![](documentation/testing_images/user_stories/user-story-4-3-1.jpg)  
* Users can select the product variant (i.e. the colour or size) they're interested in by selecting from a drop-down menu.  
![](documentation/testing_images/user_stories/user-story-4-3-2.jpg)  
* Selecting different variants of the product can update the product description text and the price, if the variants have differing descriptions and/or prices.  
![](documentation/testing_images/user_stories/user-story-4-3-3.jpg)  
![](documentation/testing_images/user_stories/user-story-4-3-4.jpg)  

**4.4. As a shopper I want to be able to view a preview of my drawing on a product so that I can get an idea of how my artwork would look when printed**

* The product page use javascript to overlay the user's drawings onto the product images, to provide a preview of how the print might look.  
![](documentation/testing_images/user_stories/user-story-4-4-1.jpg)  
* If users select a different drawing with the Select Doodle dropdown, the preview is automatically updated with the selected drawing.  
![](documentation/testing_images/user_stories/user-story-4-4-2.jpg)  
* Each product image is stored with its own set of overlay dimensions, so the print preview is scaled and positioned appropriately for the product image.  
![](documentation/testing_images/user_stories/user-story-4-4-3.jpg)  

**4.5. As a shopper I want to be able to easily manage my shopping cart so that I can select the products I want and see the costs**

* The shopping cart icon is always visible in the nav bar. A small coloured tag is positioned over it to show the current number of items in the cart.  
![](documentation/testing_images/user_stories/user-story-4-5-1.jpg)  
* Clicking the cart icon takes users to the cart page, where they can manage their cart items.  
![](documentation/testing_images/user_stories/user-story-4-5-2.jpg)  
* Users can update the quantity of a cart item or remove it from the cart.  
![](documentation/testing_images/user_stories/user-story-4-5-3.jpg)  
* If a user sets a new quantity and clicks 'Update', the cart price totals will also be updated.  
![](documentation/testing_images/user_stories/user-story-4-5-4.jpg)  
* Clicking the 'Remove' link removes the item from the cart.
![](documentation/testing_images/user_stories/user-story-4-5-5.jpg)  


**4.6. As a shopper I want to be able to easily checkout and pay for my order so that I can purchase the products I want**

* Clicking the 'Checkout Now' button on the shopping cart page takes users to a checkout form, where they can see a summary of their order and enter their delivery/payment details.  
![](documentation/testing_images/user_stories/user-story-4-6-1.jpg)  
* Users can simply complete the form and press 'Submit Order' to place an order.  
![](documentation/testing_images/user_stories/user-story-4-6-2.jpg)  
* Users are redirected to an order confirmation page to confirm their order has been placed.  
![](documentation/testing_images/user_stories/user-story-4-6-3.jpg)  
* Users also receive an email to confirm that their order has been placed.  
![](documentation/testing_images/user_stories/user-story-4-6-4.jpg)  
* The system uses webhooks as a reundancy system to create orders if there are any issues with the client side order process after a payment has been made.  
![](documentation/testing_images/user_stories/user-story-4-6-5.jpg)  

#### 5. Admin User Stories

**5.1. As a site administrator I want to be able to add new products and product variants so that I can sell new products in the store.**

* Users who are signed in and have the 'is_staff' BooleanField of their account set to true get access to a Product Management page.  
![](documentation/testing_images/user_stories/user-story-5-1-1.jpg)  
* The Product Management page shows details of all the Products, ProductVariants and ProductImages in the database.  
![](documentation/testing_images/user_stories/user-story-5-1-2.jpg)  
![](documentation/testing_images/user_stories/user-story-5-1-3.jpg)  
![](documentation/testing_images/user_stories/user-story-5-1-4.jpg)  
* Staff users can add a Product, ProductVariant, or ProductImage by clicking the 'Add' button beneath the relevant table and filling out a form.  
![](documentation/testing_images/user_stories/user-story-5-1-5.jpg)  
![](documentation/testing_images/user_stories/user-story-5-1-6.jpg)  

**5.2. As a site administrator I want to be able to update the products and product variants in the store so that I can change their details, prices and images.**

* Links are placed in the Product and ProductVariant tables to update pages for each product and variant.  
![](documentation/testing_images/user_stories/user-story-5-2-1.jpg)  
![](documentation/testing_images/user_stories/user-story-5-2-2.jpg)  
* Users can click the link to see a form populated with the item's current values.  
![](documentation/testing_images/user_stories/user-story-5-2-3.jpg)  
* Changing the values and the form updates the item in the database.  
![](documentation/testing_images/user_stories/user-story-5-2-4.jpg)  
![](documentation/testing_images/user_stories/user-story-5-2-5.jpg)  

**5.3. As a site administrator I want to be able to delete products and variants from the store so that I can remove products that are no longer sold.**

* Links are placed in the Product and ProductVariant tables to delete each product and variant.  
![](documentation/testing_images/user_stories/user-story-5-3-1.jpg)  
![](documentation/testing_images/user_stories/user-story-5-3-2.jpg)  
* Clicking the links opens a confirmation modal, to avoid accidental deletions.  
![](documentation/testing_images/user_stories/user-story-5-3-3.jpg)  
* When a user confirms the deletion, the relevant item is deleted from the database.  
![](documentation/testing_images/user_stories/user-story-5-3-4.jpg)  
* Some items are restricted to preserve database integrity (e.g. a user cannot delete a product if it currently has variants assigned to it). In these cases, messages are shown to inform users of which items are blocking the deletion, so they can reassign or delete those items to remove the restriction.  
![](documentation/testing_images/user_stories/user-story-5-3-5.jpg)  

**5.4 As a site administrator I want to be able to add, update and remove product images so that I can make sure products have up to date and accurate images.**

* Full CRUD functionality for ProductImage objects is provided in the Product Images section of the Product Management page.  
![](documentation/testing_images/user_stories/user-story-5-4-1.jpg)    
* Users can add new product images by clicking the 'Add Product Image' button and filling out the form.  
![](documentation/testing_images/user_stories/user-story-5-4-2.jpg)    
* Users can edit existing product images by clicking the 'Edit' link next to the image and filling out the form.  
![](documentation/testing_images/user_stories/user-story-5-4-3.jpg)    
* Users can delete product images by clicking the 'Delete' link next to the image and the confirming in the modal that's displayed.  
![](documentation/testing_images/user_stories/user-story-5-4-4.jpg)    
![](documentation/testing_images/user_stories/user-story-5-4-5.jpg)    

**5.5 As a site administrator I want to see a preview of how a user's drawings will be positioned over the product images so that I can select appropriate overlay dimensions.**

* On the Add Product Image and Edit Product Image pages, users can add an image file by clicking 'Browse' and then selecting an image.  
![](documentation/testing_images/user_stories/user-story-5-5-1.jpg)  
* An image preview is loaded onto the page from the selected file.
* An orange semi-transparent overlay is positioned over the preview image. This shows where a user's drawings will be positioned on top of the product image on the product pages.  
![](documentation/testing_images/user_stories/user-story-5-5-2.jpg)  
* When an admin changes the overlay settings on the Add / Edit Product Image pages, the overlay position is automatically updated to show where the drawing would be positioned with the given settings.  
![](documentation/testing_images/user_stories/user-story-5-5-3.jpg)  
![](documentation/testing_images/user_stories/user-story-5-5-4.jpg)  
* The overlay is positioned by setting its 'width', 'top' and 'left' attributes with javascript, so any units valid for these properties can be entered (though % makes the most sense in this context).  
![](documentation/testing_images/user_stories/user-story-5-5-5.jpg)  

**5.6 As a site administrator I want to receive clear feedback when I can't delete an item so that I can understand which objects are causing the restriction.**

* When a user tries to delete a Product that currently has Product Variants assigned to it, or a Product Image that is currently assigned to either a Product Variant or a Product, the deletion will be restricted to preserve database integrity.
* A toast message will be displayed which will list all of the Product and/or Product Variants that are preventing the deletion.  
![](documentation/testing_images/user_stories/user-story-5-6-1.jpg)  
![](documentation/testing_images/user_stories/user-story-5-6-2.jpg)  

***

## Automated Testing

Auotmated testing of app models, forms and views was performed with Django unittests. 94 tests were written, with a total coverage of 90%. The screenshots below show the coverage report summary and a full list of unit tests.  

![](documentation/testing_images/automated_testing/unittest-coverage.jpg)  
![](documentation/testing_images/automated_testing/unittest-list.jpg)  

***

## Responsiveness Testing

All the main pages of the site were tested for responsiveness using the Firefox browser Responsive Design Mode and screen widths of 350px, 810px and 1280px and screenshots are collected below. I tested all of the allauth account related pages, though for the sake of brevity I've only included screenshots of the tests of the most used pages (login, logout and register), as the pages all have very similar layouts.

|           Page           |                                     **Mobile (350px)**                                    |                                     **Tablet (810px)**                                    |                                     **Desktop (1280px)**                                    |
|:------------------------:|:-----------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|
| **Sketchbook**           | ![](documentation/testing_images/responsiveness_testing/350/350-sketchbook.png)           | ![](documentation/testing_images/responsiveness_testing/810/810-sketchbook.png)           | ![](documentation/testing_images/responsiveness_testing/1280/1280-sketchbook.png)           |
| **Logout**               | ![](documentation/testing_images/responsiveness_testing/350/350-logout.png)               | ![](documentation/testing_images/responsiveness_testing/810/810-logout.png)               | ![](documentation/testing_images/responsiveness_testing/1280/1280-logout.png)               |
| **Login**                | ![](documentation/testing_images/responsiveness_testing/350/350-login.png)                | ![](documentation/testing_images/responsiveness_testing/810/810-login.png)                | ![](documentation/testing_images/responsiveness_testing/1280/1280-login.png)                |
| **Signup**               | ![](documentation/testing_images/responsiveness_testing/350/350-register.png)               | ![](documentation/testing_images/responsiveness_testing/810/810-register.png)               | ![](documentation/testing_images/responsiveness_testing/1280/1280-register.png)               |
| **Account**              | ![](documentation/testing_images/responsiveness_testing/350/350-account.png)              | ![](documentation/testing_images/responsiveness_testing/810/810-account.png)              | ![](documentation/testing_images/responsiveness_testing/1280/1280-account.png)              |
| **Show All Prints**      | ![](documentation/testing_images/responsiveness_testing/350/350-show-all-prints.png)      | ![](documentation/testing_images/responsiveness_testing/810/810-show-all-prints.png)      | ![](documentation/testing_images/responsiveness_testing/1280/1280-show-all-prints.png)      |
| **Product Details**      | ![](documentation/testing_images/responsiveness_testing/350/350-product-details.png)      | ![](documentation/testing_images/responsiveness_testing/810/810-product-details.png)      | ![](documentation/testing_images/responsiveness_testing/1280/1280-product-details.png)      |
| **Cart**                 | ![](documentation/testing_images/responsiveness_testing/350/350-cart.png)                 | ![](documentation/testing_images/responsiveness_testing/810/810-cart.png)                 | ![](documentation/testing_images/responsiveness_testing/1280/1280-cart.png)                 |
| **Checkout**             | ![](documentation/testing_images/responsiveness_testing/350/350-checkout.png)             | ![](documentation/testing_images/responsiveness_testing/810/810-checkout.png)             | ![](documentation/testing_images/responsiveness_testing/1280/1280-checkout.png)             |
| **Order Confirmed**      | ![](documentation/testing_images/responsiveness_testing/350/350-order-confirmed.png)      | ![](documentation/testing_images/responsiveness_testing/810/810-order-confirmed.png)      | ![](documentation/testing_images/responsiveness_testing/1280/1280-order-confirmed.png)      |
| **Order Details**        | ![](documentation/testing_images/responsiveness_testing/350/350-order-details.png)        | ![](documentation/testing_images/responsiveness_testing/810/810-order-details.png)        | ![](documentation/testing_images/responsiveness_testing/1280/1280-order-details.png)        |
| **Faq**                  | ![](documentation/testing_images/responsiveness_testing/350/350-faq.png)                  | ![](documentation/testing_images/responsiveness_testing/810/810-faq.png)                  | ![](documentation/testing_images/responsiveness_testing/1280/1280-faq.png)                  |
| **Product Management**   | ![](documentation/testing_images/responsiveness_testing/350/350-product-management.png)   | ![](documentation/testing_images/responsiveness_testing/810/810-product-management.png)   | ![](documentation/testing_images/responsiveness_testing/1280/1280-product-management.png)   |
| **Add Product**          | ![](documentation/testing_images/responsiveness_testing/350/350-add-product.png)          | ![](documentation/testing_images/responsiveness_testing/810/810-add-product.png)          | ![](documentation/testing_images/responsiveness_testing/1280/1280-add-product.png)          |
| **Edit Product**         | ![](documentation/testing_images/responsiveness_testing/350/350-edit-product.png)         | ![](documentation/testing_images/responsiveness_testing/810/810-edit-product.png)         | ![](documentation/testing_images/responsiveness_testing/1280/1280-edit-product.png)         |
| **Add Product Variant**  | ![](documentation/testing_images/responsiveness_testing/350/350-add-product-variant.png)  | ![](documentation/testing_images/responsiveness_testing/810/810-add-product-variant.png)  | ![](documentation/testing_images/responsiveness_testing/1280/1280-add-product-variant.png)  |
| **Edit Product Variant** | ![](documentation/testing_images/responsiveness_testing/350/350-edit-product-variant.png) | ![](documentation/testing_images/responsiveness_testing/810/810-edit-product-variant.png) | ![](documentation/testing_images/responsiveness_testing/1280/1280-edit-product-variant.png) |
| **Add Product Image**    | ![](documentation/testing_images/responsiveness_testing/350/350-add-product-image.png)    | ![](documentation/testing_images/responsiveness_testing/810/810-add-product-image.png)    | ![](documentation/testing_images/responsiveness_testing/1280/1280-add-product-image.png)    |
| **Edit Product Image**   | ![](documentation/testing_images/responsiveness_testing/350/350-edit-product-image.png)   | ![](documentation/testing_images/responsiveness_testing/810/810-edit-product-image.png)   | ![](documentation/testing_images/responsiveness_testing/1280/1280-edit-product-image.png)   |

***

## Compatibility Testing

I tested the site for compatibility with Google Chrome, Mozilla Firefox and Microsoft Edge. I wasn't able to test Safari as I didn't have access to any Apple devices to test with.

![](documentation/testing_images/compatibility_testing/chrome-compatibility-testing.jpg)
![](documentation/testing_images/compatibility_testing/firefox-compatibility-testing.jpg)
![](documentation/testing_images/compatibility_testing/edge-compatibility-testing.jpg)

I created a list of tests to check all of the site's functionality was working and all pages were displaying correctly. I ran through every test on all three browsers. 

|           Page           |                      **Test**                     |     **Chrome**     |     **Firefox**    |      **Edge**      |               **Notes**              |
|:------------------------:|:-------------------------------------------------:|:------------------:|:------------------:|:------------------:|:------------------------------------:|
|      **Sketchbook**      | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | All drawing tools functioning                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | All preset colours functioning                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Coloris Color mixer functioning                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | All tool and canvas settings functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | All tool and canvas settings being stored         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Prompt generation functioning                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Intro tour functioning                            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Save and load system functioning                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | Canvas drift bug in Chrome and Edge. |
|      **Sketchbook**      | Undo functioning                                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Autosave functioning                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Welcome popup functioning                         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Sketchbook**      | Welcome popup hidden on request                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Signup**        | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Signup**        | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Signup**        | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Signup**        | Able to register account                          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Login**        | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Login**        | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Login**        | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Login**        | Able to log in                                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Logout**        | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Logout**        | Able to log out                                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Logout**        | Able to clear sketchbook on logout                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Nav Bar**       | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Nav Bar**       | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Nav Bar**       | Correct links showing for user                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Nav Bar**       | Correct links showing for staff                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | Able to update details                            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | Able to view saved drawings                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | Able to delete saved drawings                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|        **Account**       | Order history displaying correctly                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Show All Prints**   | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Show All Prints**   | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Show All Prints**   | All products displayed                            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Product Details**   | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Product Details**   | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Product Details**   | Preview overlay rendering correctly               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Product Details**   | Price, description and overlay updating correctly | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Product Details**   | Able to add to cart                               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Cart**         | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Cart**         | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Cart**         | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Cart**         | Cart icon updating correctly                      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Cart**         | Able to update quantities                         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|         **Cart**         | Able to remove items                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | Saved details prepopulating form                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | Able to save details                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | Stripe elements rendering correctly               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|       **Checkout**       | Able to place orders                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Order Confirmed**   | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|    **Order Confirmed**   | Confimration email sent and received              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|     **Order Details**    | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|          **FAQ**         | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | Chrome and Edge card outline bug.    |
|          **FAQ**         | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Product Management**  | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Product Management**  | All links functioning                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Product Management**  | Able to delete products                           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Product Management**  | Able to delete product variants                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Product Management**  | Able to delete product images                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Add Product**     | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Add Product**     | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|      **Add Product**     | Able to add products                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|     **Edit Product**     | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|     **Edit Product**     | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|     **Edit Product**     | Fields prepopulating with data correctly          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|     **Edit Product**     | Able to edit products                             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Add Product Variant** | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Add Product Variant** | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Add Product Variant** | Able to add product variants                      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
| **Edit Product Variant** | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
| **Edit Product Variant** | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
| **Edit Product Variant** | Fields prepopulating with data correctly          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
| **Edit Product Variant** | Able to edit product variants                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|   **Add Product Image**  | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|   **Add Product Image**  | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|   **Add Product Image**  | Image overlay preview functioning correctly       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|   **Add Product Image**  | Able to add product images                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Edit Product Image**  | Responsive layout rendering correctly             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Edit Product Image**  | All form/validation elements functioning          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Edit Product Image**  | Image overlay preview functioning correctly       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |
|  **Edit Product Image**  | Able to edit product images                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                      |

Two issues were discovered during compatibility testing.

Firstly, I discovered an issue in Chrome and Edge where the user's drawings were drifting across the canvas when saved and reloaded repeatedly. 

![](documentation/testing_images/compatibility_testing/chrome-canvas-drift.png)

This bug has been fixed and more detail on this can be found in the 'Canvas Drift Bug' section of the [Bugs](BUGS.md) document.

Secondly, I discovered an issue in Chrome and Edge where the cards in the FAQ section had partial white outlines. This was caused by the card's white background being partially visible around the edge of a dark overlay that was on top of it. 

![](documentation/testing_images/compatibility_testing/edge-faq-bug.jpg)

This was simply resolved by removing the overlay and changing the white background to dark grey with CSS.

![](documentation/testing_images/compatibility_testing/edge-faq-bug-fixed.jpg)

***

## Bugs Fixed

Please see [BUGS.md](BUGS.md) for full details of bugs fixed.

***

## Outstanding Issues

