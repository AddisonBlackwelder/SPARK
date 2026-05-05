from menu import Menu, Action, Toggle, Number, Submenu, Image

intro_NOT = [
    Image("Picture", "images/gates/not.bmp")
]

intro_AND = [
    Image("Picture", "images/gates/and.bmp")
]

intro_NAND = [
    Image("Picture", "images/gates/nand.bmp")
]

intro_OR = [
    Image("Picture", "images/gates/or.bmp")
]

intro_XOR = [
    Image("Picture", "images/gates/xor.bmp")
]

project_1 = [
    
]

project_2 = [
    
]

project_3 = [
    
]

project_4 = [
    
]

project_5 = [
    
]

gate_intros = [
    Submenu("NOT",  intro_NOT),
    Submenu("AND",  intro_AND),
    Submenu("NAND", intro_NAND),
    Submenu("OR",   intro_OR),
    Submenu("XOR",  intro_XOR),
]

projects = [
    Submenu("Project 1", project_1),
    Submenu("Project 2", project_2),
    Submenu("Project 3", project_3),
    Submenu("Project 4", project_4),
    Submenu("Project 5", project_5),
]

settings = [
    Number("Volume", value=5, min_val=0, max_val=10),
    Toggle("WiFi", value=False),
]

def test_send():
    import internet
    internet.send("Button Pressed!")
    return

main_menu = [
    #Action("Run Test", test_send),
    Submenu("Gate Intros",   gate_intros),
    Submenu("Projects", projects),
    Submenu("Settings", settings),
    Image("Teaching Aid", "images/teaching_aid.bmp")
]