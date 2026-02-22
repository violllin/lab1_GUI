from PyQt6.QtGui import QAction
class AppActions:
    def __init__(self, parent, logic):
        style = parent.style()

        self.new_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileIcon), "Создать", parent)
        self.open_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogOpenButton), "Открыть", parent)
        self.save_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogSaveButton), "Сохранить", parent)
        self.undo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowBack), "Отменить", parent)
        self.redo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowForward), "Повторить", parent)
        self.copy_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileLinkIcon), "Копировать", parent)
        self.cut_act = QAction(style.standardIcon(style.StandardPixmap.SP_LineEditClearButton), "Вырезать", parent)
        self.paste_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileDialogStart), "Вставить", parent)
        self.run_act = QAction(style.standardIcon(style.StandardPixmap.SP_MediaPlay), "Пуск", parent)
        self.help_act = QAction(style.standardIcon(style.StandardPixmap.SP_TitleBarContextHelpButton), "Вызов справки", parent)
        self.about_act = QAction(style.standardIcon(style.StandardPixmap.SP_MessageBoxInformation), "О программе", parent)

        self.menu_new = QAction("Создать", parent)
        self.menu_open = QAction("Открыть", parent)
        self.menu_save = QAction("Сохранить", parent)
        self.menu_save_as = QAction("Сохранить как", parent)
        self.menu_exit = QAction("Выход", parent)
        self.menu_undo = QAction("Отменить", parent)
        self.menu_redo = QAction("Повторить", parent)
        self.menu_cut = QAction("Вырезать", parent)
        self.menu_copy = QAction("Копировать", parent)
        self.menu_paste = QAction("Вставить", parent)
        self.menu_delete = QAction("Удалить", parent)
        self.menu_help = QAction("Вызов справки", parent)
        self.menu_about = QAction("О программе", parent)

        self.connect_actions(parent, logic)

    def connect_actions(self, parent, logic):

        for act in [self.new_act, self.menu_new]: act.triggered.connect(logic.file_new)
        for act in [self.open_act, self.menu_open]: act.triggered.connect(logic.file_open)
        for act in [self.save_act, self.menu_save]: act.triggered.connect(logic.file_save)
        self.menu_save_as.triggered.connect(logic.file_save_as)
        self.menu_exit.triggered.connect(parent.close)
        self.menu_delete.triggered.connect(parent.editor.clear)

        for act in [self.undo_act, self.menu_undo]: act.triggered.connect(parent.editor.undo)
        for act in [self.redo_act, self.menu_redo]: act.triggered.connect(parent.editor.redo)
        for act in [self.cut_act, self.menu_cut]: act.triggered.connect(parent.editor.cut)
        for act in [self.copy_act, self.menu_copy]: act.triggered.connect(parent.editor.copy)
        for act in [self.paste_act, self.menu_paste]: act.triggered.connect(parent.editor.paste)

        for act in [self.help_act, self.menu_help]: act.triggered.connect(logic.show_help)
        for act in [self.about_act, self.menu_about]: act.triggered.connect(logic.show_about)