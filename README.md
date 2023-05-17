# floorwalk

This repository is related to floorwalk project code maintaining purpose.

## For Cloning repository

``` git clone https://github.com/rajparmarr2308/floorwalk.git ```


## Make sure you pull every time before pushing

``` git pull ```

## Add changes 

```
git add .

git commit -m "text for commit"

git push origin main

```
## API Notes

```
GET - to get all categories
http://localhost:8000/api/categories

POST - to add categories
http://localhost:8000/api/categories

GET - to get specific category
http://localhost:8000/api/categories/1

PUT - To update specific category
http://localhost:8000/api/categories/1/


DELETE - to delete specific category
http://localhost:8000/api/categories/1

-------------------------------------------

GET - to get all subcategories
http://localhost:8000/api/subcategories/

POST- to add subcategories
http://localhost:8000/api/subcategories/

GET - to get specific subcategory
http://localhost:8000/api/subcategories/1

PUT - To update specific subcategory
http://localhost:8000/api/subcategories/1/

DELETE - to delete specific subcategory
http://localhost:8000/api/subcategories/1

-------------------------------------------

GET - to get all industries
http://localhost:8000/api/industries/

POST- to add sub industries
http://localhost:8000/api/industries/

GET - to get specific industries
http://localhost:8000/api/industries/1

PUT - To update specific subcategory
http://localhost:8000/api/industries/1/

DELETE - to delete specific industries
http://localhost:8000/api/subcategories/1

-------------------------------------------

GET - to get all interestarea
http://localhost:8000/api/interestarea/

POST- to add sub interestarea
http://localhost:8000/api/interestarea/

GET - to get specific interestarea
http://localhost:8000/api/interestarea/1

PUT - To update specific interestarea
http://localhost:8000/api/interestarea/1/

DELETE - to delete specific interestarea
http://localhost:8000/api/interestarea/1

-------------------------------------------

GET - to get all taxcurd
http://localhost:8000/api/taxcurd/

POST- to add sub taxcurd
http://localhost:8000/api/taxcurd/

GET - to get specific taxcurd
http://localhost:8000/api/taxcurd/1

PUT - To update specific taxcurd
http://localhost:8000/api/taxcurd/1/

DELETE - to delete specific taxcurd
http://localhost:8000/api/taxcurd/1

-------------------------------------------

For Solutions
Add solution  fields currently:-
'name','price','category','sub_category','tax','about','overview','how_it_work','image'

not required fields
image1,image2,iamge3,image4,image5

GET - to get all solutions
http://localhost:8000/api/solutions/

POST- to add sub solutions
http://localhost:8000/api/solutions/

GET - to get specific solutions
http://localhost:8000/api/solutions/1

PUT - To update specific solutions
http://localhost:8000/api/solutions/1/

DELETE - to delete specific solutions
http://localhost:8000/api/solutions/1

-----------------------------------------------------
For register API 

http://localhost:8000/api/register
-------------------------------------------

-------------------------------------------
required fields
-------------------------------------------
email
password
password2
first_name
last_name

-------------------------------------------
not required fields
-------------------------------------------
company
phone_number

-------------------------------------------

For login  API
http://localhost:8000/api/token/

*email and password field required

it will return refresh and access token

-------------------------------------------
For refreshing token (it requires refresh token field to be pass)
http://localhost:8000/api/token/refresh/

it will return access token 

```
