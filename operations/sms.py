from sqlalchemy import text
from sqlalchemy.orm import Session
from models import SMSPush, User
from database import engine
from schemas import sms
from schemas.sms import ActionChoices as choose, MessageDB
from schemas.user import UserCreate

def get_sign_up_msg(name: str, password: str):
    return f'Dear {name}, Your account has been created. Please find the details below. USERNAME: {name} PASSWORD: {password}'

def get_forgot_pass_msg(name: str, password: str):
    return f'Dear {name}, Your password reset done. PASSWORD: {password}'

def change_password_msg(name: str):
    return f'Dear {name}, Your password has succesfully changed Thanks for begin with Pragati Life Insurance.'
    

def generate_sms_id() -> str:
    with engine.begin() as connection:
        stmt = text("SELECT 'S'||LPAD(IPL.SMSIDNO.NEXTVAL,11,'0') from DUAL")
        sms_id = connection.execute(stmt).scalar()
        if not sms_id:
            raise Exception("Sequence Error for SMS_ID_NO")
    return sms_id

def get_sms_by_mobile(mobile: str, db: Session):
    return db.query(SMSPush).filter(SMSPush.mobile == mobile).order_by(SMSPush.indate.desc()).all()

def create_sms_row(message_obj: sms.MessageDB, db: Session):
    sms_id: str = generate_sms_id()
    message_obj.idno = sms_id
    obj = SMSPush(**message_obj.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

def get_sms_format(username: str, password: str, mobile:str, action_type=choose.SIGNUP) -> MessageDB:
    if action_type == choose.SIGNUP:
        msg = get_sign_up_msg(username, password)  # type: ignore
        smstp = 5
    elif action_type == choose.FORGOT_PASSWORD:
        msg = get_forgot_pass_msg(username, password) # type: ignore
        smstp = 2
    else:
        smstp = 1
        msg = change_password_msg(username) # type: ignore

    return MessageDB(mobile=mobile, msg=msg, smstp=smstp) # type: ignore