from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import MDListItem
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox

#Класс объектов в списке
class List_Item(MDListItem):
    def __init__(self, mail_number, data_text,**kwargs):
        self.mail_number = mail_number
        self.data_text = data_text
        super().__init__( **kwargs)

#Логотип
class Logo_card(MDBoxLayout):
    pass

#Блок фильтров
class Filter_block(MDCard):
    pass