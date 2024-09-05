from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SelectField, FloatField, SelectMultipleField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from wtforms.widgets import ListWidget, CheckboxInput


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    latitude = HiddenField('Latitude')  
    longitude = HiddenField('Longitude')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ScreeningForm(FlaskForm):
    province = StringField('Province', validators=[DataRequired()])
    is_farmer = StringField('Are you a farmer?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DemographicForm(FlaskForm):
    registered_name = StringField('Registered/Legal Name', validators=[DataRequired()])
    
    province = SelectField('In which province is the farm/forest/fisheries operation situated?',
                           choices=[('wc', 'Western Cape'), ('ec', 'Eastern Cape'), ('nc', 'Northern Cape'), 
                                    ('gp', 'Gauteng'), ('kzn', 'KwaZulu-Natal'), ('fs', 'Free State'),
                                    ('lp', 'Limpopo'), ('mp', 'Mpumalanga'), ('nw', 'North West')],
                           validators=[DataRequired()])
    
    district = SelectField('District/Metropolitan Municipality', 
                           choices=[
                               ('cape_town', 'City of Cape Town'),
                               ('cape_winelands', 'Cape Winelands District Municipality'),
                               ('central_karoo', 'Central Karoo District Municipality'),
                               ('eden', 'Garden Route District Municipality'),
                               ('overberg', 'Overberg District Municipality'),
                               ('west_coast', 'West Coast District Municipality')],
                           validators=[DataRequired()])
    
    municipality = SelectField('Local Municipality',
                               choices=[
                                   # Local municipalities in the Cape Winelands District
                                   ('breede_valley', 'Breede Valley Local Municipality'),
                                   ('drakenstein', 'Drakenstein Local Municipality'),
                                   ('langeberg', 'Langeberg Local Municipality'),
                                   ('stellenbosch', 'Stellenbosch Local Municipality'),
                                   ('witzenberg', 'Witzenberg Local Municipality'),
                                   
                                   # Local municipalities in the Central Karoo District
                                   ('beaufort_west', 'Beaufort West Local Municipality'),
                                   ('laingsburg', 'Laingsburg Local Municipality'),
                                   ('prince_albert', 'Prince Albert Local Municipality'),
                                   
                                   # Local municipalities in the Garden Route District
                                   ('bitou', 'Bitou Local Municipality'),
                                   ('george', 'George Local Municipality'),
                                   ('knysna', 'Knysna Local Municipality'),
                                   ('mossel_bay', 'Mossel Bay Local Municipality'),
                                   ('oudtshoorn', 'Oudtshoorn Local Municipality'),
                                   
                                   # Local municipalities in the Overberg District
                                   ('cape_agulhas', 'Cape Agulhas Local Municipality'),
                                   ('overstrand', 'Overstrand Local Municipality'),
                                   ('swellendam', 'Swellendam Local Municipality'),
                                   ('theewaterskloof', 'Theewaterskloof Local Municipality'),
                                   
                                   # Local municipalities in the West Coast District
                                   ('bergrivier', 'Bergrivier Local Municipality'),
                                   ('cederberg', 'Cederberg Local Municipality'),
                                   ('matzikama', 'Matzikama Local Municipality'),
                                   ('saldanha_bay', 'Saldanha Bay Local Municipality'),
                                   ('swartland', 'Swartland Local Municipality')
                               ],
                               validators=[DataRequired()])
    
    agricultural_activity = SelectMultipleField(
        'Agricultural activity(ies) of this farm/forest/fisheries operation',
        choices=[
            ('farming', 'Farming: growing of crops and raising of animals'),
            ('services', 'Rendering of farming, fisheries and services'),
            ('wild_farming', 'Farming in wild animals (game)'),
            ('hunting', 'Hunting and trapping'),
            ('organic_fertiliser', 'Production of manure (organic fertiliser)'),
            ('forestry', 'Forestry, logging and related services'),
            ('fishing', 'Ocean and sea (coastal) fishing'),
            ('fish_farming', 'Fish farming (including hatcheries)'),
            ('processing', 'Processing of agricultural produce'),
            ('other', 'Other (specify):') 
        ],
        validators=[Optional()],
        option_widget=CheckboxInput(), 
        widget=ListWidget(prefix_label=False)
    )
    
    other_agricultural_activity = StringField('If Other, please specify:', validators=[Optional()])
    
    farm_activity = SelectMultipleField('In the growing of crops and raising of animals, which activity(ies) is this farm involved in?',
                                        choices=[('field_crops', 'Field crops: grain/cereals and other crops'),
                                                 ('vegetables', 'Vegetables and herbs'),
                                                 ('flowers', 'Flowers (nursery/ornamental plants)'),
                                                 ('fruits', 'Fruits'),
                                                 ('tree_nuts', 'Tree nuts'),
                                                 ('spices', 'Teas and spice crops'),
                                                 ('honey', 'Bee farming (honey and wax production)'),
                                                 ('animal_farming', 'Farming/raising of animals (excluding wild animals) and poultry production'),
                                                 ('seed', 'Production of seed')],
                                        validators=[Optional()],
                                        option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    
    submit = SubmitField('Next')

class SurveyForm(FlaskForm):
    crops_own = FloatField('Own (Area in hectares) - Crops', validators=[Optional()])
    crops_govt = FloatField('Lease/rent from government (Area in hectares) - Crops', validators=[Optional()])
    crops_traditional = FloatField('Lease/rent from traditional administration (Area in hectares) - Crops', validators=[Optional()])
    crops_other = FloatField('Lease/rent from other (Area in hectares) - Crops', validators=[Optional()])
    
    pastures_own = FloatField('Own (Area in hectares) - Pastures', validators=[Optional()])
    pastures_govt = FloatField('Lease/rent from government (Area in hectares) - Pastures', validators=[Optional()])
    pastures_traditional = FloatField('Lease/rent from traditional administration (Area in hectares) - Pastures', validators=[Optional()])
    pastures_other = FloatField('Lease/rent from other (Area in hectares) - Pastures', validators=[Optional()])
    
    greenhouses_own = FloatField('Own (Area in hectares) - Greenhouses', validators=[Optional()])
    greenhouses_govt = FloatField('Lease/rent from government (Area in hectares) - Greenhouses', validators=[Optional()])
    greenhouses_traditional = FloatField('Lease/rent from traditional administration (Area in hectares) - Greenhouses', validators=[Optional()])
    greenhouses_other = FloatField('Lease/rent from other (Area in hectares) - Greenhouses', validators=[Optional()])
    
    natural_forest_own = FloatField('Own (Area in hectares) - Natural forest', validators=[Optional()])
    natural_forest_govt = FloatField('Lease/rent from government (Area in hectares) - Natural forest', validators=[Optional()])
    natural_forest_traditional = FloatField('Lease/rent from traditional administration (Area in hectares) - Natural forest', validators=[Optional()])
    natural_forest_other = FloatField('Lease/rent from other (Area in hectares) - Natural forest', validators=[Optional()])
    
    woodland_own = FloatField('Own (Area in hectares) - Woodland', validators=[Optional()])
    woodland_govt = FloatField('Lease/rent from government (Area in hectares) - Woodland', validators=[Optional()])
    woodland_traditional = FloatField('Lease/rent from traditional administration (Area in hectares) - Woodland', validators=[Optional()])
    woodland_other = FloatField('Lease/rent from other (Area in hectares) - Woodland', validators=[Optional()])
    
    forest_plantations_own = FloatField('Own (Area in hectares) - Forest plantations', validators=[Optional()])
    forest_plantations_govt = FloatField('Lease/rent from government (Area in hectares) - Forest plantations', validators=[Optional()])
    forest_plantations_traditional = FloatField('Lease/rent from traditional administration (Area in hectares) - Forest plantations', validators=[Optional()])
    forest_plantations_other = FloatField('Lease/rent from other (Area in hectares) - Forest plantations', validators=[Optional()])
    
   
    submit = SubmitField('Submit')


class FieldHorticulturalCropsForm(FlaskForm):
    farming_practice = SelectMultipleField(
        'What type of farming practice does this operation use for crop production?',
        choices=[('Irrigation', 'Irrigation'),
                 ('Dry land/rain-fed', 'Dry land/rain-fed'),
                 ('Both irrigation and dry land/rain-fed', 'Both irrigation and dry land/rain-fed')],
        widget=CheckboxInput() 
    )
    
    water_supply = SelectMultipleField(
        'What source(s) of water supply for crop production is/are used by this operation?',
        choices=[('Municipal water supply', 'Municipal water supply'),
                 ('Groundwater/boreholes', 'Groundwater/boreholes'),
                 ('Both surface water and groundwater', 'Both surface water and groundwater'),
                 ('River', 'River'),
                 ('Dam', 'Dam'),
                 ('Water boards/schemes', 'Water boards/schemes'),
                 ('Treated wastewater', 'Treated wastewater'),
                 ('Rainwater harvesting', 'Rainwater harvesting')],
        widget=CheckboxInput() 
    )
    
    irrigation_system = SelectMultipleField(
        'Which type(s) of irrigation system(s) is/are used by this operation?',
        choices=[('Sprinklers', 'Sprinklers'),
                 ('Micro-irrigation', 'Micro-irrigation'),
                 ('Drip irrigation', 'Drip irrigation'),
                 ('Pivots', 'Pivots'),
                 ('Canals', 'Canals'),
                 ('Flood irrigation', 'Flood irrigation'),
                 ('Draglines, quick-coupling lines', 'Draglines, quick-coupling lines'),
                 ('Other', 'Other')],
        widget=CheckboxInput() 
    )
    
    submit = SubmitField('Submit')






















