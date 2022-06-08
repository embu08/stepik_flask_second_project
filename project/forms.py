from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class CardForm(FlaskForm):
    card = SelectField('Выберите карту',
                       choices=[('6', '6'),
                                ('7', '7'),
                                ('8', '8'),
                                ('9', '9'),
                                ('10', '10'),
                                ('Валет', 'Валет'),
                                ('Дама', "Дама"),
                                ("Король", "Король"),
                                ("Туз", "Туз")
                                ]
                       )
    submit = SubmitField('Показать')


class RequirementsForm(FlaskForm):
    first = PasswordField('Первая строка: ', validators=[DataRequired(), Length(min=2, max=30, message='от 2 до 30')])
    equal = PasswordField('Вторая строка: ', validators=[DataRequired(), EqualTo('first', message='не совпадают(')])
    submit = SubmitField('Сравнить')

