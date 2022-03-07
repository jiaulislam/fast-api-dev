from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from datetime import datetime
from typing import List
from datetime import date


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        nullable=False, min_length=3, max_length=16, regex="^[a-zA-Z0-9_]*$"
    )
    full_name: str = Field(nullable=False, min_length=3, max_length=50)
    mobile: Optional[str] = Field(
        nullable=True,
        min_length=11,
        max_length=11,
        regex="^017|016|013|018|019|[0-9]{8}$",
    )
    email: Optional[str] = Field(max_length=50, nullable=True)
    password: str = Field(nullable=False, min_length=6, max_length=65)
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    is_agent: bool = Field(default=False, nullable=False)
    is_employee: bool = Field(default=False, nullable=False)
    proposals: List["Proposal"] = Relationship(back_populates="users")
    created_at: Optional[datetime]

    def __repr__(self):
        return f"<User id({self.id} name({self.username}))>"


class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="users.id")
    propno: str = Field(max_length=30, nullable=False)
    policy: str = Field(max_length=30, nullable=True, default=None)
    name: str = Field(nullable=False, max_length=50)
    fhname: str = Field(nullable=False, max_length=50)
    mhname: str = Field(nullable=False, max_length=50)
    spname: Optional[str] = Field(nullable=True, max_length=50, default=None)
    paddr1: str = Field(nullable=False, max_length=50)
    paddr2: str = Field(nullable=False, max_length=50)
    paddr3: str = Field(nullable=False, max_length=50)
    paddr4: str = Field(nullable=False, max_length=50)
    maddr1: str = Field(nullable=False, max_length=50)
    maddr2: str = Field(nullable=False, max_length=50)
    maddr3: str = Field(nullable=False, max_length=50)
    maddr4: str = Field(nullable=False, max_length=50)
    mobile: str = Field(
        nullable=False, max_length=11, regex="^017|016|013|018|019|[0-9]{8}$"
    )
    email: Optional[str] = Field(
        nullable=True,
        max_length=50,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    telhome: Optional[str] = Field(nullable=True, max_length=11)
    teloffice: Optional[str] = Field(nullable=True, max_length=11)
    nid: str = Field(nullable=False, max_length=17)
    passport: Optional[str] = Field(nullable=True, max_length=20)
    passexpdt: Optional[date] = Field(nullable=True, default=None)
    birthid: Optional[str] = Field(nullable=True, max_length=21)
    etin: Optional[str] = Field(nullable=True, default=None, max_length=21)
    drivingid: Optional[str] = Field(nullable=True, default=None, max_length=21)
    drivingexpdt: Optional[date] = Field(nullable=True, default=None)
    dob: date = Field(nullable=False)
    age: int = Field(nullable=False)
    sex: str = Field(nullable=False, max_length=1)
    maritial_status: str = Field(nullable=False, max_length=1)
    edcode: str = Field(nullable=False, max_length=2)
    occup: str = Field(nullable=False, max_length=2)
    ur: str = Field(nullable=False, max_length=1)
    propdat: date = Field(nullable=False, default=date.today())
    datecom: date = Field(nullable=False, default=date.today())
    matdate: date = Field(nullable=False)
    jobdetails: str = Field(nullable=False, max_length=120)
    mon_income: float = Field(nullable=False)
    incomesource: str = Field(nullable=False, max_length=50)
    incomevalidity: str = Field(nullable=False, max_length=50)
    spjobdetails: Optional[str] = Field(nullable=True, max_length=120)
    spmonincome: Optional[float] = Field(nullable=True, default=None)
    sscpf: bool = Field(default=True, nullable=False)
    dobplace: Optional[str] = Field(default=None, nullable=True, max_length=30)
    polopt: str = Field(nullable=False, max_length=1)
    planname: str = Field(nullable=False, max_length=50)
    plan: str = Field(nullable=False, max_length=4)
    term: str = Field(nullable=False, min_length=1, max_length=2)

    sumass: float = Field(nullable=False)
    sumatrisk: float = Field(nullable=False)
    apu: Optional[float] = Field(nullable=True, default=None)
    adb: Optional[float] = Field(nullable=True, default=None)
    padb: Optional[float] = Field(nullable=True, default=None)
    apc: Optional[float] = Field(nullable=True, default=None)
    hi: bool = Field(default=False, nullable=False)
    hiplan: Optional[int] = Field(default=None, nullable=True)
    paymode: Optional[int] = Field(default=None, nullable=True)
    lprem: Optional[float] = Field(default=None, nullable=True)
    totprem: float = Field(nullable=False)

    exinfo: bool = Field(default=False, nullable=False)
    comok: bool = Field(default=True, nullable=False)
    illness: bool = Field(default=False, nullable=False)
    optacc: bool = Field(default=False, nullable=False)
    hfit: int = Field(default=0, nullable=False)
    hinchs: int = Field(default=0, nullable=False)
    weight: float = Field(nullable=False)
    inbrith: float = Field(nullable=False)
    outbrith: float = Field(nullable=False)
    stom: float = Field(nullable=False)
    spmark: Optional[str] = Field(nullable=True, default=None, max_length=50)
    pregn: bool = Field(default=False, nullable=False)
    normdel: Optional[bool] = Field(default=None, nullable=True)
    lc_dob: Optional[date] = Field(nullable=True, default=None)
    brescan: Optional[bool] = Field(nullable=True, default=None)
    lc_minst: Optional[date] = Field(nullable=True, default=None)

    numfh: Optional[int] = Field(nullable=True, default=None)
    agefh: Optional[int] = Field(nullable=True, default=None)
    prefh: Optional[str] = Field(nullable=True, default=None, max_length=20)
    agedfh: Optional[int] = Field(nullable=True, default=None)
    cosfh: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lilfh: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dyfh: Optional[str] = Field(nullable=True, default=None, max_length=20)

    nummh: Optional[int] = Field(nullable=True, default=None)
    agemh: Optional[int] = Field(nullable=True, default=None)
    premh: Optional[str] = Field(nullable=True, default=None, max_length=20)
    agedmh: Optional[int] = Field(nullable=True, default=None)
    cosmh: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lilmh: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dymh: Optional[str] = Field(nullable=True, default=None, max_length=20)

    numbro: Optional[int] = Field(nullable=True, default=None)
    agebro: Optional[int] = Field(nullable=True, default=None)
    prebro: Optional[str] = Field(nullable=True, default=None, max_length=20)
    agedbro: Optional[int] = Field(nullable=True, default=None)
    cosbro: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lilbro: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dybro: Optional[str] = Field(nullable=True, default=None, max_length=20)

    numsis: Optional[int] = Field(nullable=True, default=None)
    agesis: Optional[int] = Field(nullable=True, default=None)
    presis: Optional[str] = Field(nullable=True, default=None, max_length=20)
    agedsis: Optional[int] = Field(nullable=True, default=None)
    cossis: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lilsis: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dysis: Optional[str] = Field(nullable=True, default=None, max_length=20)

    numsp: Optional[int] = Field(nullable=True, default=None)
    agesp: Optional[int] = Field(nullable=True, default=None)
    presp: Optional[str] = Field(nullable=True, default=None, max_length=20)
    agedsp: Optional[int] = Field(nullable=True, default=None)
    cossp: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lilsp: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dysp: Optional[str] = Field(nullable=True, default=None, max_length=20)

    numson: Optional[int] = Field(nullable=True, default=None)
    ageson: Optional[int] = Field(nullable=True, default=None)
    preson: Optional[str] = Field(nullable=True, default=None, max_length=20)
    agedson: Optional[int] = Field(nullable=True, default=None)
    cosson: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lilson: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dyson: Optional[str] = Field(nullable=True, default=None, max_length=20)

    numdot: Optional[int] = Field(nullable=True, default=None)
    agedot: Optional[int] = Field(nullable=True, default=None)
    predot: Optional[str] = Field(nullable=True, default=None, max_length=20)
    ageddot: Optional[int] = Field(nullable=True, default=None)
    cosdot: Optional[str] = Field(nullable=True, default=None, max_length=20)
    lildot: Optional[str] = Field(nullable=True, default=None, max_length=20)
    dydot: Optional[str] = Field(nullable=True, default=None, max_length=20)

    banname: Optional[str] = Field(nullable=True, default=None, max_length=20)
    baaccno: Optional[str] = Field(nullable=True, default=None, max_length=20)
    acctype: Optional[str] = Field(nullable=True, default=None, max_length=20)
    babran: Optional[str] = Field(nullable=True, default=None, max_length=20)
    baadd: Optional[str] = Field(nullable=True, default=None, max_length=20)
    inspur: Optional[str] = Field(nullable=True, default=None, max_length=20)
    webproposal_no: Optional[str] = Field(nullable=True, default=None, max_length=20)
    o_basic: Optional[float] = Field(nullable=True, default=None)
    o_pdab: Optional[float] = Field(nullable=True, default=None)
    o_adb: Optional[float] = Field(nullable=True, default=None)
    o_hi: Optional[int] = Field(nullable=True, default=None)

    users: "Users" = Relationship(back_populates="proposals")
    nominees: List["ProposerNominee"] = Relationship(back_populates="proposal")
    attachments: List["ProposerAttachments"] = Relationship(back_populates="proposal")
    created_at: Optional[datetime]

    def __repr__(self):
        return f"<Proposal id({self.id}) user_id({self.user_id}) proposal_no({self.propno})"


class ProposerNominee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proposal_id: Optional[int] = Field(nullable=False, foreign_key="proposal.id")
    attachment_id: Optional[int] = Field(nullable=False, foreign_key="nomineeattachemnt.id")
    nomname: str = Field(nullable=False, min_length=3, max_length=30)
    nomrel: int = Field(nullable=False, le=1, ge=30)
    nfhname: str = Field(nullable=False, min_length=3, max_length=30)
    nmhname: str = Field(nullable=False, min_length=3, max_length=30)
    nspname: str = Field(nullable=False, min_length=3, max_length=30)
    nid: str = Field(nullable=False, min_length=9, max_length=17)
    ndob: date = Field(nullable=False)
    nage: int = Field(nullable=False, le=150, ge=1)
    nsex: str = Field(nullable=False, min_length=1, max_length=1)
    nmobile: str = Field(
        nullable=False,
        min_length=11,
        max_length=11,
        regex="^017|016|013|018|019|[0-9]{8}$",
    )
    nemail: Optional[str] = Field(
        nullable=True,
        min_length=3,
        max_length=30,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    noccup: str = Field(nullable=False, min_length=3, max_length=30)
    presentaddr: str = Field(nullable=False, min_length=3, max_length=80)
    nompurmaddr: str = Field(nullable=False, min_length=3, max_length=80)
    nompar: float = Field(nullable=False, le=1, ge=100)
    parenname: Optional[str] = Field(nullable=True, min_length=3, max_length=30)
    chnomage: Optional[int] = Field(nullable=True, le=1, ge=100)
    chnomrel: Optional[int] = Field(nullable=True, le=1, ge=30)
    proposal: "Proposal" = Relationship(back_populates="nominees")
    nominee_attachments: List["NomineeAttachment"] = Relationship(back_populates="nominee")



class ProposerAttachments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proposal_id: int = Field(nullable=False, foreign_key="proposal.id")
    proposer_img: Optional[str] = Field(nullable=True, default=None, max_length=65)
    proposer_nid: Optional[str] = Field(nullable=True, default=None, max_length=65)
    proposer_birthid: Optional[str] = Field(nullable=True, default=None, max_length=65)
    proposer_signature: Optional[str] = Field(
        nullable=True, default=None, max_length=65
    )
    proposal: "Proposal" = Relationship(back_populates="attachments")


class NomineeAttachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nominee_id: int = Field(nullable=False, foreign_key="proposer_nominee.id")
    nominee_img: Optional[str] = Field(nullable=True, default=None, max_length=65)
    nominee_nid: Optional[str] = Field(nullable=True, default=None, max_length=65)
    nominee_birthid: Optional[str] = Field(nullable=True, default=None, max_length=65)
    nominee_signature: Optional[str] = Field(nullable=True, default=None, max_length=65)
    nominee: "ProposerNominee" = Relationship(back_populates="nominee_attachments")