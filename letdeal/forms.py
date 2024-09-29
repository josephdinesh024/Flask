from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms  import StringField,TextAreaField,IntegerField,EmailField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length,ValidationError,Email,NumberRange
from letdeal.models import Product, User, Category
from letdeal import app


class LoginForm(FlaskForm):
    phone_number = IntegerField("Phone Number",validators=[DataRequired(),Length(min=10)])
    otp  = IntegerField("OTP",validators=[DataRequired(),Length(min=6,max=6)])

class ProfileForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Length(min=4,max=25)])
    email = EmailField("Email",validators=[DataRequired(),Email()])
    street = TextAreaField("Street",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired(),Length(min=4,max=100)])
    state =StringField("State",validators=[DataRequired(),Length(min=4,max=100)])
    postal_code = IntegerField("Pincode",validators=[DataRequired()])
    country = StringField("Country",validators=[DataRequired()])
    submit = SubmitField("Save")

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is taken. Please try another email")

class SellerForm(FlaskForm):
    factory_name = StringField("Factory Name",validators=[DataRequired(),Length(min=2,max=50)])
    description = TextAreaField("Description",validators=[DataRequired()],render_kw={"placeholder":"Describe service that you provide"})
    requirement = TextAreaField("Requirement",validators=[DataRequired()],render_kw={"placeholder":"""Any service needed like  
                                Freezer
                                Storage Area
                                ..."""})
    submit = SubmitField("Save")



class ProductForm(FlaskForm):  # seller product form

    @staticmethod
    def choice():
        with app.app_context():
            names = Category.query.all()
            lst = []
            for i in names:
                val = [i.category_id,i.name]
                lst.append((val))

            return lst
        
    category_id = SelectField("Category",choices=choice())
    product_name = StringField("Product Name",validators=[DataRequired(),Length(min=2,max=50)])
    description = TextAreaField("Product Description",validators=[DataRequired()],render_kw={"placeholder":"few words about product & qulaty"})
    price = StringField("Price",validators=[DataRequired(),Length(min=2,max=10)])
    quantity = StringField("Strock Quantity",validators=[DataRequired()]) 
    image = FileField("Product Image",validators=[FileAllowed(['jpg','png','jpeg'])])   
    submit = SubmitField("Add Product")


class BuyForm(FlaskForm):
    product_id = StringField("id",validators=[DataRequired()])
    quantity = IntegerField("quantity",validators=[DataRequired()])
    purchase_price = IntegerField("price",validators=[DataRequired()])
    submit = SubmitField("Place Order")

    def validate_quantity(self,quantity):
        stock = Product.query.filter_by(product_id=self.product_id.data).first()
        if stock.stock_quantity < quantity.data :
            raise ValidationError("Out of Strock")
        
        



