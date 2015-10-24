from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
    SelectField, HiddenField, SelectMultipleField, DateField, IntegerField
#from wtforms.fields.html5 import DateField    
from wtforms.validators import Required, Length, Email, Optional
from wtforms import ValidationError, widgets
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User, Room
from datetime import datetime

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email alreay registered')
        
class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
    
class CommentForm(Form):
    body = TextAreaField('', validators=[Required()])
    submit = SubmitField('Submit')
    
class ReservationForm(Form):
    from_date = DateField('From Date', validators=[Required()])
    to_date = DateField('To Date', validators=[Required()])
    submit = SubmitField('Search')
    
    def validate_to_date(self, field):
        #print('>> from_date.data: %s' % ((self.from_date.data >= self.to_date.data)))
        if not self.from_date.data or not self.to_date.data or self.from_date.data >= self.to_date.data:
            raise ValidationError('From date should be smaller than To date')

class BooksForm(Form):
    from_date = DateField('From Date', validators=[Optional()])
    to_date = DateField('To Date', validators=[Optional()])
    name = StringField('Name')
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Search')
    
    def validate_to_date(self, field):
        #print('>> from_date.data: %s' % ((self.from_date.data >= self.to_date.data)))
        if self.to_date.data and self.from_date.data and self.from_date.data >= self.to_date.data:
            raise ValidationError('From date should be greater than To date')

class RoomBookingForm(Form):
    email = StringField('Email *', validators=[Required(), Email()])
    name = StringField('Name *', validators=[Required()])
    mobile = StringField('Mobile')
    phone = StringField('Phone')
    from_date = StringField('From Date')
    to_date = StringField('To Date')
    mobile = StringField('Mobile')
    Phone = StringField('Phone')
    room_id = BooleanField('')
    submit = SubmitField('Submit')
    
    def validate_email(self, field):
        print('>> validate email: %s' % self.email.data)
        if '' == self.email.data:
            raise ValidationError('Email is required')

class RoomForm(Form):
    from_date = DateField('From Date')
    to_date = DateField('To Date')
    submit = SubmitField('Submit')
    
    def validate_to_date(self, field):
        #print('>> from_date.data: %s %s' % ((self.from_date.data >= self.to_date.data), self.to_date.data))
        if self.from_date.data >= self.to_date.data:
            raise ValidationError('From date should be greater than To date')
       
class RoomsForm(Form):
    number = StringField('Room Number', validators=[Required()])       
    name = StringField('Room Name', validators=[Required()]) 
    guests = IntegerField('Guests', validators=[Required()]) 
    active = BooleanField('Active', default=True)     
    submit = SubmitField('Submit')

    def validate_number(self, field):
        #print('>> field.data: %s, self.number: %s' % (field.data, self.number.data))
        if field.data != self.number.data and Room.query.filter_by(number=field.data).first():
            raise ValidationError('Number alreay registered')
        