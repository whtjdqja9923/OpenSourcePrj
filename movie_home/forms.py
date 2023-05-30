from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, EmailField, DecimalRangeField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange, email_validator

class signup_form(FlaskForm):
    member_id = StringField('아이디', validators=[DataRequired('아이디를 확인해주세요')], render_kw={"placeholder": "아이디를 입력하세요"})
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 확인해주세요'), EqualTo('password_confirm')], render_kw={"placeholder": "비밀번호를 입력하세요"}) #비밀번호 확인
    password_confirm = PasswordField('password_confirm', validators=[DataRequired()], render_kw={"placeholder": "비밀번호를 한번 더 입력해 주세요"})
    gender = SelectField('성별', choices=[('M', '남성'), ('F', '여성')])
    email = EmailField('이메일', validators=[Email(email_validator, '이메일을 확인해주세요')], render_kw={"placeholder": "이메일을 입력하세요(example@chungbuk.ac.kr)"})
    age = StringField('나이', validators=[DataRequired('나이를 확인해주세요')], render_kw={"placeholder": "나이를 입력하세요"})
    
class signin_form(FlaskForm):
    member_id = StringField('아이디', validators=[DataRequired('아이디를 확인해주세요')], render_kw={"placeholder": "아이디를 입력하세요"})
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 확인해주세요')], render_kw={"placeholder": "비밀번호를 입력하세요"})

class memberupdate_form(FlaskForm):
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 확인해주세요')], render_kw={"placeholder": "비밀번호를 입력하세요"})
    gender = SelectField('성별', choices=[('M', '남성'), ('F', '여성')])
    email = EmailField('이메일', validators=[Email(email_validator, '이메일을 확인해주세요')], render_kw={"placeholder": "이메일을 입력하세요(example@chungbuk.ac.kr)"})
    age = StringField('나이', validators=[DataRequired('나이를 확인해주세요')], render_kw={"placeholder": "나이를 입력하세요"})
