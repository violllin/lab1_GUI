from PyQt6.QtGui import QAction, QKeySequence

class ActionManager:
    def __init__(self, window, controller):
        style = window.style()
        self.win = window
        self.ctrl = controller

        self.new_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileIcon), "Создать", window)
        self.open_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogOpenButton), "Открыть", window)
        self.save_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogSaveButton), "Сохранить", window)
        self.undo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowBack), "Отменить", window)
        self.redo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowForward), "Повторить", window)
        self.copy_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileLinkIcon), "Копировать", window)
        self.cut_act = QAction(style.standardIcon(style.StandardPixmap.SP_LineEditClearButton), "Вырезать", window)
        self.paste_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileDialogStart), "Вставить", window)
        self.run_act = QAction(style.standardIcon(style.StandardPixmap.SP_MediaPlay), "Пуск", window)
        self.help_act = QAction(style.standardIcon(style.StandardPixmap.SP_TitleBarContextHelpButton), "Справка",
                                window)
        self.about_act = QAction(style.standardIcon(style.StandardPixmap.SP_MessageBoxInformation), "О программе")
        self.zoom_in_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowUp), "Увеличить шрифт", window)
        self.zoom_out_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowDown), "Уменьшить шрифт", window)

        self.menu_new = QAction("Создать", window)
        self.menu_new.setShortcut(QKeySequence.StandardKey.New)
        self.menu_open = QAction("Открыть", window)
        self.menu_open.setShortcut(QKeySequence.StandardKey.Open)
        self.menu_save = QAction("Сохранить", window)
        self.menu_save.setShortcut(QKeySequence.StandardKey.Save)
        self.menu_save_as = QAction("Сохранить как", window)
        self.menu_save_as.setShortcut("Ctrl+Shift+S")
        self.menu_exit = QAction("Выход", window)
        self.menu_exit.setShortcut("Alt+F4")
        self.menu_run_act = QAction("Пуск", window)

        self.menu_undo = QAction("Отменить", window)
        self.menu_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.menu_redo = QAction("Повторить", window)
        self.menu_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.menu_cut = QAction("Вырезать", window)
        self.menu_cut.setShortcut(QKeySequence.StandardKey.Cut)
        self.menu_copy = QAction("Копировать", window)
        self.menu_copy.setShortcut(QKeySequence.StandardKey.Copy)
        self.menu_paste = QAction("Вставить", window)
        self.menu_paste.setShortcut(QKeySequence.StandardKey.Paste)
        self.menu_delete = QAction("Удалить", window)
        self.menu_delete.setShortcut(QKeySequence.StandardKey.Delete)

        self.menu_help = QAction("Вызов справки", window)
        self.menu_help.setShortcut('F1')
        self.menu_about = QAction("О программе", window)

        self._connect_signals()

    def _connect_signals(self):
        self.new_act.triggered.connect(self.ctrl.file_new)
        self.menu_new.triggered.connect(self.ctrl.file_new)
        self.open_act.triggered.connect(self.ctrl.file_open)
        self.menu_open.triggered.connect(self.ctrl.file_open)
        self.save_act.triggered.connect(self.ctrl.file_save)
        self.menu_save.triggered.connect(self.ctrl.file_save)
        self.menu_save_as.triggered.connect(self.ctrl.file_save_as)
        self.menu_exit.triggered.connect(self.win.close)

        self.menu_delete.triggered.connect(
            lambda: self.win.get_current_editor().clear() if self.win.get_current_editor() else None)
        self.undo_act.triggered.connect(
            lambda: self.win.get_current_editor().undo() if self.win.get_current_editor() else None)
        self.menu_undo.triggered.connect(
            lambda: self.win.get_current_editor().undo() if self.win.get_current_editor() else None)
        self.redo_act.triggered.connect(
            lambda: self.win.get_current_editor().redo() if self.win.get_current_editor() else None)
        self.menu_redo.triggered.connect(
            lambda: self.win.get_current_editor().redo() if self.win.get_current_editor() else None)

        self.copy_act.triggered.connect(
            lambda: self.win.get_current_editor().copy() if self.win.get_current_editor() else None)
        self.menu_copy.triggered.connect(
            lambda: self.win.get_current_editor().copy() if self.win.get_current_editor() else None)
        self.cut_act.triggered.connect(
            lambda: self.win.get_current_editor().cut() if self.win.get_current_editor() else None)
        self.menu_cut.triggered.connect(
            lambda: self.win.get_current_editor().cut() if self.win.get_current_editor() else None)
        self.paste_act.triggered.connect(
            lambda: self.win.get_current_editor().paste() if self.win.get_current_editor() else None)
        self.menu_paste.triggered.connect(
            lambda: self.win.get_current_editor().paste() if self.win.get_current_editor() else None)

        self.run_act.triggered.connect(self.ctrl.run_program)
        self.zoom_in_act.triggered.connect(self.ctrl.zoom_in)
        self.zoom_out_act.triggered.connect(self.ctrl.zoom_out)
        self.help_act.triggered.connect(self.ctrl.show_help)
        self.menu_help.triggered.connect(self.ctrl.show_help)
        self.about_act.triggered.connect(self.ctrl.show_about)
        self.menu_about.triggered.connect(self.ctrl.show_about)