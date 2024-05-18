from dataclasses import dataclass

@dataclass
class Hero: 
    name: str
    context: str
    question: str
    answer: str
    where: bool
    when: bool
    who: bool
    what: bool
    how: bool
    why: bool
    how_many: bool
    yes_no: bool
    complete: bool
    partial: bool
    short: bool
    complement_info: bool
    copy: bool
    open_question: bool
