from sqlalchemy import CheckConstraint, Column, ForeignKey, Identity, func, Enum
from sqlalchemy.dialects.oracle import DATE, CHAR, NUMBER, VARCHAR2
from sqlalchemy.orm import relationship
import enum
from validators import Validator

from database import Base

class StatusChoices(enum.Enum):
    PENDING = 1
    SUBMITTED = 2
    SENT = 3

#  Existing Tables
class Education(Base): # type: ignore
    __tablename__ = 'education'
    __table_args__ = {'schema': 'ipl'}
    edcode = Column(CHAR(2), nullable=False, primary_key=True)
    edname = Column(VARCHAR2(20), nullable=False)

class PayMode(Base): # type: ignore
    __tablename__ = 'paymode'
    __table_args__ = {'schema' : 'ipl'}
    pmode = Column(VARCHAR2(2), nullable=False, primary_key=True)
    modename = Column(VARCHAR2(25), nullable=False)


class Occupation(Base): # type: ignore
    __tablename__ = 'occup'
    __table_args__ = {'schema' : 'ipl'}
    occup = Column(CHAR(2), nullable=False, primary_key=True)
    occupname = Column(VARCHAR2(20), nullable=False)
    occupctg = Column(CHAR(1), nullable=True)
    pdab = Column(NUMBER(6,2), nullable=True)
    adb = Column(NUMBER(6,2), nullable=True)
    extra = Column(NUMBER(6,2), nullable=True)

class Plan(Base): # type: ignore
    __tablename__ = 'plan'
    __table_args__ = {'schema' : 'ipl'}
    plan = Column(VARCHAR2(4), nullable=False, primary_key=True)
    planname = Column(VARCHAR2(50), nullable=False)
    policy_type = Column(VARCHAR2(1), nullable=False)
    new_plan = Column(VARCHAR2(4), nullable=True)
    plan_type = Column(VARCHAR2(1), nullable=True)
    bonus = Column(VARCHAR2(1), nullable=True)
    business_type = Column(VARCHAR2(1), nullable=True)
    plan_type_name = Column(VARCHAR2(60), nullable=True)
    min_age = Column(NUMBER(5), nullable=False)
    max_age = Column(NUMBER(5), nullable=False)
    name = Column(VARCHAR2(200), nullable=True)
    prod_code = Column(VARCHAR2(20), nullable=True)
    plan_status = Column(VARCHAR2(1), nullable=True)
    status_date = Column(DATE(timezone=True), nullable=False, server_default=func.sysdate())



# New Tables
class User(Base): # type: ignore
    __tablename__ = "users"
    __table_args__ = {'schema': 'jibon'}
    id = Column(NUMBER(30), primary_key=True, server_default=Identity())
    username = Column(VARCHAR2(30), nullable=False, unique=True)
    full_name = Column(VARCHAR2(30), nullable=False)
    mobile = Column(VARCHAR2(30), nullable=False, unique=True)
    email = Column(VARCHAR2(30), nullable=False, unique=True)
    password = Column(VARCHAR2(65), nullable=False)
    is_active = Column(NUMBER(1), default=True)
    is_admin = Column(NUMBER(1), default=False)
    is_agent = Column(NUMBER(1), default=False)
    is_employee = Column(NUMBER(1), default=False)  
    emp_code = Column(VARCHAR2(10), nullable=True) #TODO: Validation Required for Employee Code
    agent_code = Column(VARCHAR2(12), nullable=True) # TODO: Validation Required for valid agent code

    all_proposals = relationship('Proposal', back_populates='owner')

    created_at = Column(DATE(timezone=True), nullable=False,server_default=func.sysdate())

    def __repr__(self):
        return f"<User id({self.id} name({self.username}))>"



class Proposal(Base): # type: ignore
    __tablename__ = "proposals"
    __table_args__ = {'schema': 'jibon'}
    id = Column(NUMBER(30), primary_key=True, server_default=Identity())
    owner_id = Column(ForeignKey("jibon.users.id"), nullable=False)
    propno = Column(VARCHAR2(30), nullable=False, unique=True)

    owner = relationship('User', back_populates='all_proposals')
    owner_attachments = relationship('ProposerAttachments', back_populates='proposer')
    policy = Column(VARCHAR2(12), nullable=True, default=None)
    name = Column(VARCHAR2(50), nullable=False)
    fhname = Column(VARCHAR2(50), nullable=False)
    mhname = Column(VARCHAR2(50), nullable=False)
    spname = Column(VARCHAR2(50), nullable=True, default=None)
    paddr1 = Column(VARCHAR2(50), nullable=False)
    paddr2 = Column(VARCHAR2(50), nullable=False)
    paddr3 = Column(VARCHAR2(50), nullable=False)
    paddr4 = Column(VARCHAR2(50), nullable=False)
    maddr1 = Column(VARCHAR2(50), nullable=False)
    maddr2 = Column(VARCHAR2(50), nullable=False)
    maddr3 = Column(VARCHAR2(50), nullable=False)
    maddr4 = Column(VARCHAR2(50), nullable=False)
    mobile = Column(VARCHAR2(11), nullable=False)
    email = Column(VARCHAR2(50), nullable=True, default=None)
    telhome = Column(VARCHAR2(50), nullable=True, default=None)
    teloffice = Column(VARCHAR2(50), nullable=True, default=None)
    nid = Column(VARCHAR2(17), nullable=False)
    passport = Column(VARCHAR2(20), nullable=True, default=None)
    passexpdt = Column(DATE(timezone=False), nullable=True, default=None)
    birthid = Column(DATE(timezone=False), nullable=True, default=None)
    birthid = Column(VARCHAR2(20), nullable=True, default=None)
    etin = Column(VARCHAR2(20), nullable=True, default=None)
    drivingid = Column(VARCHAR2(20), nullable=True, default=None)
    drivingexpdt = Column(VARCHAR2(20), nullable=True, default=None)
    dob = Column(DATE(timezone=False), nullable=False)
    age = Column(NUMBER(10), nullable=False)
    sex = Column(VARCHAR2(1), nullable=False)
    maritial_status = Column(VARCHAR2(1), nullable=False)
    # edcode = Column(String(2), nullable=False)
    edcode = Column(CHAR(2), ForeignKey('ipl.education.edcode'))
    # occup = Column(VARCHAR2(2), nullable=False)     # TODO : Validation Required for Occupation
    occup = Column(CHAR(2), ForeignKey('ipl.occup.occup'))
    ur = Column(VARCHAR2(1), nullable=False)
    propdat = Column(DATE(timezone=False), nullable=False)
    comdat = Column(DATE(timezone=False), nullable=False)
    matdate = Column(DATE(timezone=False), nullable=False)
    jobdetails = Column(VARCHAR2(50), nullable=False)
    mon_income = Column(NUMBER(30,2), nullable=False)
    incomesource = Column(VARCHAR2(50), nullable=False)
    incomevalidity = Column(VARCHAR2(50), nullable=False)
    spmonincome = Column(NUMBER(30, 2), nullable=True, default=None)
    sscpf = Column(NUMBER(1), default=True)
    dob_place = Column(VARCHAR2(30), nullable=False)
    polopt = Column(VARCHAR2(1), nullable=False)
    planname = Column(VARCHAR2(50), nullable=False)
    plan_code = Column(VARCHAR2(4), ForeignKey('ipl.plan.plan')) # TODO : Validation required for this field
    # plan = Column(VARCHAR2(4), nullable=False)
    term = Column(VARCHAR2(2), nullable=False)
    sumass = Column(NUMBER(30,2), nullable=False)
    sumatrisk = Column(NUMBER(30,2), nullable=False)
    apu = Column(NUMBER(30,2), nullable=True, default=None)
    adb = Column(NUMBER(30,2), nullable=True, default=None)
    padb = Column(NUMBER(30,2), nullable=True, default=None)
    apc = Column(NUMBER(30,2), nullable=True, default=None)
    hi = Column(NUMBER(1), nullable=False, server_default='0')
    hiplan = Column(NUMBER(4), nullable=True)
    paymode = Column(VARCHAR2(2), ForeignKey('ipl.paymode.pmode'))
    # paymode = Column(VARCHAR2(2), nullable=False)
    lprem = Column(NUMBER(30,2), nullable=True, default=None)
    totprem = Column(NUMBER(30,2), nullable=False)

    exinfo = Column(NUMBER(1), nullable=False, server_default='0')
    comok = Column(NUMBER(1), nullable=False, server_default='1')
    illness = Column(NUMBER(1), nullable=False, server_default='0')
    optacc = Column(NUMBER(1), nullable=False, server_default='0')
    hfit = Column(NUMBER(10), nullable=False)
    hinchs = Column(NUMBER(10), nullable=False)
    weight = Column(NUMBER(3, 2), nullable=False)
    inbrith = Column(NUMBER(10), nullable=False)
    outbrith = Column(NUMBER(10), nullable=False)
    stom = Column(NUMBER(10), nullable=False)
    spmark = Column(VARCHAR2(50), nullable=True, default='None')
    pregn = Column(NUMBER(1), default=None, nullable=True)
    normdel = Column(NUMBER(1), default=None, nullable=True)
    lc_dob = Column(DATE(timezone=False), nullable=True, default=None)
    brescan = Column(NUMBER(1), default=None, nullable=True)
    lc_minst = Column(DATE(timezone=False), nullable=True, default=None)

    inspur = Column(VARCHAR2(40), nullable=False)
    # webproposal_no = Column(VARCHAR2(30), nullable=False, unique=True)

    bankname = Column(VARCHAR2(50), nullable=True, default=None)
    baaccno = Column(VARCHAR2(50), nullable=True, default=None)
    acctype = Column(VARCHAR2(30), nullable=True, default=None)
    baadd = Column(VARCHAR2(50), nullable=True, default=None)
    o_basic = Column(NUMBER(30, 2), nullable=True, default=None)
    o_pdab = Column(NUMBER(30, 2), nullable=True, default=None)
    o_adb = Column(NUMBER(30, 2), nullable=True, default=None)
    o_hi = Column(NUMBER(30,2), nullable=True, default=None)
#     baaccno: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     acctype: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     babran: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     baadd: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     o_basic: Optional[float] = Field(nullable=True, default=None)
#     o_pdab: Optional[float] = Field(nullable=True, default=None)
#     o_adb: Optional[float] = Field(nullable=True, default=None)
#     o_hi: Optional[int] = Field(nullable=True, default=None)

#     numfh: Optional[int] = Field(nullable=True, default=None)
#     agefh: Optional[int] = Field(nullable=True, default=None)
#     prefh: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     agedfh: Optional[int] = Field(nullable=True, default=None)
#     cosfh: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lilfh: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dyfh: Optional[str] = Field(nullable=True, default=None, max_length=20)

#     nummh: Optional[int] = Field(nullable=True, default=None)
#     agemh: Optional[int] = Field(nullable=True, default=None)
#     premh: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     agedmh: Optional[int] = Field(nullable=True, default=None)
#     cosmh: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lilmh: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dymh: Optional[str] = Field(nullable=True, default=None, max_length=20)

#     numbro: Optional[int] = Field(nullable=True, default=None)
#     agebro: Optional[int] = Field(nullable=True, default=None)
#     prebro: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     agedbro: Optional[int] = Field(nullable=True, default=None)
#     cosbro: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lilbro: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dybro: Optional[str] = Field(nullable=True, default=None, max_length=20)

#     numsis: Optional[int] = Field(nullable=True, default=None)
#     agesis: Optional[int] = Field(nullable=True, default=None)
#     presis: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     agedsis: Optional[int] = Field(nullable=True, default=None)
#     cossis: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lilsis: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dysis: Optional[str] = Field(nullable=True, default=None, max_length=20)

#     numsp: Optional[int] = Field(nullable=True, default=None)
#     agesp: Optional[int] = Field(nullable=True, default=None)
#     presp: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     agedsp: Optional[int] = Field(nullable=True, default=None)
#     cossp: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lilsp: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dysp: Optional[str] = Field(nullable=True, default=None, max_length=20)

#     numson: Optional[int] = Field(nullable=True, default=None)
#     ageson: Optional[int] = Field(nullable=True, default=None)
#     preson: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     agedson: Optional[int] = Field(nullable=True, default=None)
#     cosson: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lilson: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dyson: Optional[str] = Field(nullable=True, default=None, max_length=20)

#     numdot: Optional[int] = Field(nullable=True, default=None)
#     agedot: Optional[int] = Field(nullable=True, default=None)
#     predot: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     ageddot: Optional[int] = Field(nullable=True, default=None)
#     cosdot: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     lildot: Optional[str] = Field(nullable=True, default=None, max_length=20)
#     dydot: Optional[str] = Field(nullable=True, default=None, max_length=20)


    status = Column(Enum(StatusChoices,  create_constraint=True), default=StatusChoices.PENDING, nullable=False)

    created_at = Column(DATE(timezone=True), nullable=False, server_default=func.sysdate())

    def __repr__(self):
        return f"<Proposal id({self.id}) user_id({self.user_id}) proposal_no({self.propno})"



class ProposerAttachments(Base): # type: ignore
    __tablename__ = "proposer_attachments"
    __table_args__ = {'schema': 'jibon'}
    
    id = Column(NUMBER(30), primary_key=True, server_default=Identity())
    proposer_id = Column(ForeignKey("jibon.proposals.id", ondelete="CASCADE"), nullable=False)
    proposer_img = Column(VARCHAR2(65), nullable=True, default=None)
    proposer_nid = Column(VARCHAR2(65), nullable=True, default=None)
    proposer_birthid = Column(VARCHAR2(65), nullable=True, default=None)
    proposer_signature = Column(VARCHAR2(65), nullable=True, default=None)
    proposer = relationship("Proposals", back_populates="owner_attachments", passive_deletes=True)

    created_at = Column(DATE(timezone=True), nullable=False, server_default=func.sysdate())

    def __repr__(self):
        return f"<ProposerAttachments id({self.id}) proposer_id({self.proposer_id})"


class Nominee(Base): # type: ignore
    __tablename__ = "nominees"
    __table_args__ = {'schema': 'jibon'}

    id = Column(NUMBER(30), primary_key=True, server_default=Identity())
    proposer_id = Column(ForeignKey("jibon.proposals.id", ondelete="CASCADE"), nullable=False)
    nomname = Column(VARCHAR2(50), nullable=False)
    nomrel = Column(NUMBER(3), nullable=False) # validation required for this field 

    proposal = relationship("Proposal", back_populates="nominees", passive_deletes=True)
    nominee_attachment = relationship("NomineeAttachment", back_populates="nominee", passive_deletes=True)
    nfhname = Column(VARCHAR2(50), nullable=False, default=None)
    nmhname = Column(VARCHAR2(50), nullable=False, default=None)
    nspname= Column(VARCHAR2(50), nullable=True, default=None)
    nid = Column(VARCHAR2(17), nullable=False)
    ndob = Column(DATE(timezone=False), nullable=False)
    nage = Column(NUMBER(3), nullable=False)
    nsex = Column(VARCHAR2(1), nullable=False)
    nmobile = Column(VARCHAR2(11), nullable=False)
    nemail = Column(VARCHAR2(50), nullable=True, default=None)
    noccup = Column(NUMBER(3), nullable=False) # TODO: Validation required for this field
    presentaddr = Column(VARCHAR2(50), nullable=False)
    nompurmaddr = Column(VARCHAR2(50), nullable=False)
    nompar = Column(NUMBER(2, 2), nullable=False)
    parenname = Column(VARCHAR2(30), nullable=True, default=None)
    chnomage = Column(NUMBER(3), nullable=True, default=None)
    chnomrel = Column(NUMBER(3), nullable=True, default=None)

    created_at = Column(DATE(timezone=True), nullable=False, server_default=func.sysdate())

    def __repr__(self):
        return f"<Nominee id({self.id}) proposer_id({self.proposer_id})"


class NomineeAttachment(Base): # type: ignore
    __tablename__ = "nominee_attachments"
    __table_args__ = {'schema': 'jibon'}

    id = Column(NUMBER(30), primary_key=True, server_default=Identity())
    nominee_id = Column(ForeignKey("jibon.nominees.id", ondelete="CASCADE"), nullable=False)
    nominee_img = Column(VARCHAR2(65), nullable=True, default=None)
    nominee_nid = Column(VARCHAR2(65), nullable=True, default=None)
    nominee_birthid = Column(VARCHAR2(65), nullable=True, default=None)
    nominee_signature = Column(VARCHAR2(65), nullable=True, default=None)
    nominee = relationship("Nominee", back_populates="nominee_attachment", passive_deletes=True)

    created_at = Column(DATE(timezone=True), nullable=False, server_default=func.sysdate())

    def __repr__(self):
        return f"<NomineeAttachment id({self.id}) nominee_id({self.nominee_id})>"


# Add Constraints to the tables

CheckConstraint(func.regexp_like(User.email, Validator.EMAIL_STRING_VALIDATOR), name="email_regex")
CheckConstraint(func.regexp_like(User.username, Validator.USERNAME_STRING_VALIDATOR), name="username_regex")
CheckConstraint(func.regexp_like(User.mobile, Validator.MOBILE_NO_STRING_VALIDATOR), name="user_mobile_regex")
CheckConstraint(func.regexp_like(User.full_name, Validator.NAME_STRING_VALIDATOR), name="full_name_regex")
CheckConstraint(func.regexp_like(Proposal.mobile, Validator.MOBILE_NO_STRING_VALIDATOR), name="mobile_regex")
CheckConstraint(func.regexp_like(Proposal.nid, Validator.NID_STRING_VALIDATOR), name="nid_regex")
CheckConstraint(func.regexp_like(Nominee.nmobile, Validator.MOBILE_NO_STRING_VALIDATOR), name="nmobile_regex")
CheckConstraint(func.regexp_like(Nominee.nid, Validator.NID_STRING_VALIDATOR), name="nomnid_regex")
CheckConstraint(func.regexp_like(Nominee.nemail, Validator.EMAIL_STRING_VALIDATOR), name="nemail_regex")
