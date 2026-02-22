from PyQt6.QtGui import QAction

class AppActions:
    def __init__(self, parent):
        self.parent = parent
        style = parent.style()

        self.new_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileIcon), "Создать", parent)
        self.open_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogOpenButton), "Открыть", parent)
        self.save_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogSaveButton), "Сохранить", parent)
        self.save_as_act = QAction("Сохранить как", parent)
        self.exit_act = QAction("Выход", parent)

        self.undo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowBack), "Отменить", parent)
        self.redo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowForward), "Повторить", parent)
        self.cut_act = QAction(style.standardIcon(style.StandardPixmap.SP_LineEditClearButton), "Вырезать", parent)
        self.copy_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileLinkIcon), "Копировать", parent)
        self.paste_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileDialogStart), "Вставить", parent)

        self.run_act = QAction(style.standardIcon(style.StandardPixmap.SP_MediaPlay), "Пуск", parent)

        self.help_act = QAction(style.standardIcon(style.StandardPixmap.SP_TitleBarContextHelpButton), "Вызов справки", parent)
        self.about_act = QAction(style.standardIcon(style.StandardPixmap.SP_MessageBoxInformation), "О программе", parent)